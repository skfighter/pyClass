"""
Image Analysis Service

Handles AI-powered image description and OCR text extraction
"""

import logging
import base64
from io import BytesIO
from typing import Optional

import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import pytesseract
from rembg import remove

from config import settings
from models.responses import ImageAnalysisResponse

logger = logging.getLogger(__name__)


class ImageAnalysisService:
    """Service for analyzing images with AI and OCR"""
    
    def __init__(self) -> None:
        """Initialize the image analysis service with AI models"""
        self.processor: Optional[BlipProcessor] = None
        self.model: Optional[BlipForConditionalGeneration] = None
        self._load_models()
    
    def _load_models(self) -> None:
        """Load BLIP AI model and processor"""
        try:
            logger.info(f"Loading BLIP model: {settings.model_name}")
            self.processor = BlipProcessor.from_pretrained(settings.model_name)
            self.model = BlipForConditionalGeneration.from_pretrained(settings.model_name)
            
            # Move model to GPU if available
            if torch.cuda.is_available():
                self.model = self.model.to("cuda")
                logger.info("✅ Model loaded on GPU")
            else:
                logger.info("✅ Model loaded on CPU")
                
        except Exception as e:
            logger.error(f"Failed to load AI model: {e}")
            self.processor = None
            self.model = None
            raise
    
    def is_ready(self) -> bool:
        """Check if service is ready to process images"""
        return self.processor is not None and self.model is not None
    
    async def analyze_image(self, image_bytes: bytes, filename: str) -> ImageAnalysisResponse:
        """
        Analyze image with AI description and OCR text extraction
        
        Args:
            image_bytes: Raw image file bytes
            filename: Original filename for logging
        
        Returns:
            ImageAnalysisResponse with description and extracted text
        
        Raises:
            Exception: If image processing fails
        """
        # Open image from bytes
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to RGB if necessary (for PNG with alpha, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Generate AI description
        description = await self._generate_description(image)
        
        # Extract text using OCR
        extracted_text = await self._extract_text(image)
        
        return ImageAnalysisResponse(
            success=True,
            description=description,
            extracted_text=extracted_text,
            has_text=bool(extracted_text.strip()),
            filename=filename
        )
    
    async def _generate_description(self, image: Image.Image) -> str:
        """
        Generate AI description of image content
        
        Args:
            image: PIL Image object
        
        Returns:
            AI-generated description or error message
        """
        try:
            # Process image for model
            inputs = self.processor(image, return_tensors="pt")
            
            # Move to same device as model
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            
            # Generate caption
            out = self.model.generate(
                **inputs,
                max_length=settings.max_caption_length
            )
            
            # Decode output
            description = self.processor.decode(out[0], skip_special_tokens=True)
            logger.debug(f"Generated description: {description}")
            
            return description
            
        except Exception as e:
            logger.error(f"Error generating image description: {e}")
            return f"Error: Unable to generate description - {str(e)}"
    
    async def _extract_text(self, image: Image.Image) -> str:
        """
        Extract text from image using Tesseract OCR
        
        Args:
            image: PIL Image object
        
        Returns:
            Extracted text or empty string/error message
        """
        try:
            # Extract text using pytesseract
            text = pytesseract.image_to_string(image)
            
            # Clean up extracted text
            text = text.strip()
            
            if text:
                logger.debug(f"Extracted text ({len(text)} chars)")
            else:
                logger.debug("No text found in image")
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return f"Error: OCR failed - {str(e)}"
    
    async def convert_to_black_and_white(self, image_bytes: bytes, filename: str) -> dict:
        """
        Convert image to black and white (grayscale)
        
        Args:
            image_bytes: Raw image file bytes
            filename: Original filename for logging
        
        Returns:
            Dictionary with base64 encoded black and white image and metadata
        
        Raises:
            Exception: If image processing fails
        """
        import base64
        
        try:
            # Open image from bytes
            image = Image.open(BytesIO(image_bytes))
            
            # Store original info
            original_format = image.format
            width, height = image.size
            
            # Convert to grayscale (black and white)
            bw_image = image.convert('L')
            
            # Save to bytes buffer
            output_buffer = BytesIO()
            # Use JPEG for efficient encoding, PNG for lossless
            save_format = 'JPEG' if original_format in ['JPEG', 'JPG'] else 'PNG'
            bw_image.save(output_buffer, format=save_format, quality=95)
            output_buffer.seek(0)
            
            # Convert to base64
            bw_bytes = output_buffer.getvalue()
            bw_base64 = base64.b64encode(bw_bytes).decode('utf-8')
            
            # Create data URL for easy display in browser
            mime_type = f"image/{save_format.lower()}"
            data_url = f"data:{mime_type};base64,{bw_base64}"
            
            logger.info(f"Converted {filename} to black and white - {width}x{height}")
            
            return {
                "bw_image_base64": data_url,
                "image_info": {
                    "width": width,
                    "height": height,
                    "format": save_format,
                    "mode": "L",  # L = grayscale
                    "size_bytes": len(bw_bytes)
                }
            }
            
        except Exception as e:
            logger.error(f"Error converting image to black and white: {e}")
            raise
    
    async def remove_background(self, image_bytes: bytes, filename: str) -> dict:
        """
        Remove background from image
        
        Args:
            image_bytes: Raw image file bytes
            filename: Original filename for logging
        
        Returns:
            Dictionary with base64 encoded image (transparent background) and metadata
        
        Raises:
            Exception: If background removal fails
        """
        try:
            # Open image from bytes
            image = Image.open(BytesIO(image_bytes))
            
            # Store original info
            width, height = image.size
            
            logger.info(f"Removing background from {filename} - {width}x{height}")
            
            # Remove background using rembg
            output_bytes = remove(image_bytes)
            
            # Open the result as PIL Image
            output_image = Image.open(BytesIO(output_bytes))
            
            # Save to bytes buffer as PNG (to preserve transparency)
            output_buffer = BytesIO()
            output_image.save(output_buffer, format='PNG')
            output_buffer.seek(0)
            
            # Convert to base64
            no_bg_bytes = output_buffer.getvalue()
            no_bg_base64 = base64.b64encode(no_bg_bytes).decode('utf-8')
            
            # Create data URL for easy display in browser
            data_url = f"data:image/png;base64,{no_bg_base64}"
            
            logger.info(f"Background removed from {filename} - Output size: {len(no_bg_bytes)} bytes")
            
            return {
                "no_bg_image_base64": data_url,
                "image_info": {
                    "width": width,
                    "height": height,
                    "format": "PNG",
                    "mode": "RGBA",  # RGBA = with alpha channel (transparency)
                    "size_bytes": len(no_bg_bytes)
                }
            }
            
        except Exception as e:
            logger.error(f"Error removing background from image: {e}")
            raise
