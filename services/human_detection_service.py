"""
Human Detection Service

Handles detection and counting of humans in images using YOLOv8
"""

import logging
from io import BytesIO
from typing import Optional

from PIL import Image
from ultralytics import YOLO

from models.responses import HumanCountResponse

logger = logging.getLogger(__name__)


class HumanDetectionService:
    """Service for detecting and counting humans in images"""
    
    def __init__(self) -> None:
        """Initialize the human detection service with YOLO model"""
        self.model: Optional[YOLO] = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load YOLOv8 model for human detection"""
        try:
            logger.info("Loading YOLOv8 model for human detection...")
            # YOLOv8n is lightweight and fast
            # Will download ~6MB model on first run
            self.model = YOLO('yolov8n.pt')
            logger.info("✅ YOLOv8 model loaded successfully")
                
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            self.model = None
            raise
    
    def is_ready(self) -> bool:
        """Check if service is ready to detect humans"""
        return self.model is not None
    
    async def count_humans(self, image_bytes: bytes) -> HumanCountResponse:
        """
        Count humans in an image
        
        Args:
            image_bytes: Raw image file bytes
        
        Returns:
            HumanCountResponse with count of detected humans
        
        Raises:
            Exception: If image processing fails
        """
        # Open image from bytes
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Detect humans
        human_count = await self._detect_humans(image)
        
        return HumanCountResponse(humansCount=human_count)
    
    async def _detect_humans(self, image: Image.Image) -> int:
        """
        Detect and count humans in image using YOLO
        
        Args:
            image: PIL Image object
        
        Returns:
            Count of humans detected (0 if none)
        """
        try:
            # Run inference
            # verbose=False to reduce console output
            results = self.model(image, verbose=False)
            
            # Count persons (class 0 in COCO dataset)
            # YOLO returns class IDs, 0 = person
            human_count = 0
            
            for result in results:
                # Get detected classes
                if result.boxes is not None:
                    classes = result.boxes.cls.cpu().numpy()
                    # Count class 0 (person)
                    human_count += int((classes == 0).sum())
            
            logger.info(f"Detected {human_count} human(s) in image")
            return human_count
            
        except Exception as e:
            logger.error(f"Error detecting humans: {e}")
            # Return 0 on error rather than failing
            return 0
