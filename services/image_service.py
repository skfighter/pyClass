"""
Image Analysis Service

Handles AI-powered image description and OCR text extraction
"""

import logging
from io import BytesIO
from typing import Optional

import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import pytesseract

from config import settings
from models.responses import ImageAnalysisResponse

logger = logging.getLogger(__name__)


class ImageAnalysisService:
    """Service for analyzing images with AI and OCR"""
    
    def __init__(self):
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
