"""
Image Analysis Service

Handles AI-powered image description and OCR text extraction
"""

import logging
import base64
from io import BytesIO
from typing import Optional, List, Tuple
from collections import Counter

import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import pytesseract
from rembg import remove
import numpy as np
from sklearn.cluster import KMeans

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
        """Load BLIP AI model and processor with GPU acceleration"""
        try:
            logger.info(f"Loading BLIP model: {settings.model_name}")
            self.processor = BlipProcessor.from_pretrained(settings.model_name)
            self.model = BlipForConditionalGeneration.from_pretrained(settings.model_name)
            
            # Move model to GPU if available for faster inference
            if torch.cuda.is_available():
                device = "cuda"
                gpu_name = torch.cuda.get_device_name(0)
                logger.info(f"🚀 GPU detected: {gpu_name}")
                logger.info(f"🔥 Moving BLIP model to GPU for blazing fast inference!")
                self.model = self.model.to(device)
                logger.info("✅ BLIP model loaded on GPU successfully")
            else:
                logger.info("⚠️ GPU not available, using CPU")
                logger.info("✅ BLIP model loaded on CPU successfully")
                
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
    
    async def extract_colors(self, image_bytes: bytes, filename: str, num_colors: int = 10) -> dict:
        """
        Extract dominant colors from an image using K-means clustering
        
        Args:
            image_bytes: Raw image file bytes
            filename: Original filename for logging
            num_colors: Number of dominant colors to extract (default: 10)
        
        Returns:
            Dictionary with list of colors (RGB, HEX, percentage) and metadata
        
        Raises:
            Exception: If color extraction fails
        """
        try:
            # Open image from bytes
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Store original info
            width, height = image.size
            total_pixels = width * height
            
            logger.info(f"Extracting colors from {filename} - {width}x{height}")
            
            # Resize image for faster processing (optional, for very large images)
            max_dimension = 400
            if max(width, height) > max_dimension:
                ratio = max_dimension / max(width, height)
                new_size = (int(width * ratio), int(height * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
                logger.info(f"Resized to {new_size[0]}x{new_size[1]} for processing")
            
            # Convert image to numpy array
            img_array = np.array(image)
            
            # Reshape to list of RGB pixels
            pixels = img_array.reshape(-1, 3)
            
            # Use K-means clustering to find dominant colors
            kmeans = KMeans(n_clusters=min(num_colors, len(pixels)), random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Get the colors (cluster centers)
            colors = kmeans.cluster_centers_.astype(int)
            
            # Get labels and count occurrences
            labels = kmeans.labels_
            label_counts = Counter(labels)
            
            # Calculate percentages and create color data
            color_data = []
            for i, color in enumerate(colors):
                count = label_counts[i]
                percentage = (count / len(pixels)) * 100
                
                # RGB values
                r, g, b = int(color[0]), int(color[1]), int(color[2])
                
                # Convert to HEX
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                
                # Get color name (approximate)
                color_name = self._get_color_name(r, g, b)
                
                color_data.append({
                    "rgb": [r, g, b],
                    "hex": hex_color,
                    "percentage": round(percentage, 2),
                    "color_name": color_name
                })
            
            # Sort by percentage (most dominant first)
            color_data.sort(key=lambda x: x['percentage'], reverse=True)
            
            logger.info(f"Extracted {len(color_data)} colors from {filename}")
            
            return {
                "colors": color_data,
                "total_colors_found": len(color_data),
                "image_info": {
                    "width": width,
                    "height": height,
                    "total_pixels": total_pixels,
                    "format": image.format or "Unknown"
                }
            }
            
        except Exception as e:
            logger.error(f"Error extracting colors from image: {e}")
            raise
    
    def _get_color_name(self, r: int, g: int, b: int) -> str:
        """
        Get approximate color name from RGB values
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        
        Returns:
            Color name as string
        """
        # Simple color name mapping based on RGB dominance
        # This is a simplified version - you could use a library like webcolors for more accuracy
        
        # Calculate luminance
        luminance = (0.299 * r + 0.587 * g + 0.114 * b)
        
        # Check for grayscale
        if abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
            if luminance < 50:
                return "Black"
            elif luminance < 100:
                return "Dark Gray"
            elif luminance < 180:
                return "Gray"
            elif luminance < 230:
                return "Light Gray"
            else:
                return "White"
        
        # Determine dominant color
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        
        # Check for brown (low saturation orange/red)
        if r > g > b and g > 100 and r - g < 100:
            return "Brown"
        
        # Primary and secondary colors
        if r == max_val and g == max_val:
            return "Yellow"
        elif r == max_val and b == max_val:
            return "Magenta"
        elif g == max_val and b == max_val:
            return "Cyan"
        elif r == max_val:
            if r > 200 and g < 100 and b < 100:
                return "Red"
            elif g > 100:
                return "Orange"
            else:
                return "Red"
        elif g == max_val:
            return "Green"
        elif b == max_val:
            if r < 100 and g < 100:
                return "Blue"
            else:
                return "Purple"
        
        return "Mixed"
