"""
Human Detection Service

Handles detection and counting of humans in images using YOLOv8
"""

import logging
import base64
from io import BytesIO
from typing import Optional

import cv2
import numpy as np
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
        """Load YOLOv8 model for human detection with GPU acceleration"""
        try:
            logger.info("Loading YOLOv8 model for human detection...")
            # YOLOv8n is lightweight and fast
            # Will download ~6MB model on first run
            self.model = YOLO('yolov8n.pt')
            
            # Check for GPU availability
            import torch
            if torch.cuda.is_available():
                device = 'cuda:0'
                gpu_name = torch.cuda.get_device_name(0)
                logger.info(f"🚀 GPU detected: {gpu_name}")
                logger.info(f"🔥 Moving model to GPU for blazing fast inference!")
                self.model.to(device)
                logger.info("✅ YOLOv8 model loaded on GPU successfully")
            else:
                logger.info("⚠️ GPU not available, using CPU")
                logger.info("✅ YOLOv8 model loaded on CPU successfully")
                
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
    
    async def detect_faces(self, image_bytes: bytes, filename: str) -> dict:
        """
        Detect human faces in image and mark them with red circles
        
        Args:
            image_bytes: Raw image file bytes
            filename: Original filename for logging
        
        Returns:
            Dictionary with base64 encoded image with marked faces and metadata
        
        Raises:
            Exception: If face detection fails
        """
        try:
            # Load the image
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert PIL Image to OpenCV format (numpy array)
            img_array = np.array(image)
            img_cv2 = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            width, height = image.size
            logger.info(f"Detecting faces in {filename} - {width}x{height}")
            
            # Load OpenCV's pre-trained Haar Cascade for face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            # Parameters: scaleFactor, minNeighbors, minSize
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            face_count = len(faces)
            logger.info(f"Detected {face_count} face(s) in {filename}")
            
            # Draw red circles around detected faces
            for (x, y, w, h) in faces:
                # Calculate center and radius
                center_x = x + w // 2
                center_y = y + h // 2
                radius = max(w, h) // 2 + 10  # Add padding
                
                # Draw red circle (BGR format: Red = (0, 0, 255))
                cv2.circle(img_cv2, (center_x, center_y), radius, (0, 0, 255), 3)
                
                # Optional: Draw a small dot at the center
                cv2.circle(img_cv2, (center_x, center_y), 3, (0, 0, 255), -1)
            
            # Convert back to RGB for PIL
            img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
            result_image = Image.fromarray(img_rgb)
            
            # Save to bytes buffer
            output_buffer = BytesIO()
            # Use original format if available, otherwise PNG
            save_format = image.format if image.format else 'PNG'
            result_image.save(output_buffer, format=save_format)
            output_buffer.seek(0)
            
            # Convert to base64
            result_bytes = output_buffer.getvalue()
            result_base64 = base64.b64encode(result_bytes).decode('utf-8')
            
            # Create data URL
            mime_type = f"image/{save_format.lower()}"
            data_url = f"data:{mime_type};base64,{result_base64}"
            
            logger.info(f"Marked {face_count} face(s) with red circles in {filename}")
            
            return {
                "marked_image_base64": data_url,
                "faces_detected": face_count,
                "image_info": {
                    "width": width,
                    "height": height,
                    "format": save_format,
                    "size_bytes": len(result_bytes)
                }
            }
            
        except Exception as e:
            logger.error(f"Error detecting faces in image: {e}")
            raise
    
    async def detect_all_objects(self, image_bytes: bytes) -> dict:
        """
        Detect all objects in image using YOLOv8
        
        Args:
            image_bytes: Raw image file bytes
        
        Returns:
            Dictionary with detected objects and their properties
        """
        try:
            # Open image from bytes
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Run inference with confidence threshold
            results = self.model(image, verbose=False, conf=0.25)
            
            detected_objects = []
            
            for result in results:
                if result.boxes is not None:
                    boxes = result.boxes
                    
                    # Get class names, confidences, and coordinates
                    for i in range(len(boxes)):
                        class_id = int(boxes.cls[i].cpu().numpy())
                        confidence = float(boxes.conf[i].cpu().numpy())
                        class_name = result.names[class_id]
                        
                        detected_objects.append({
                            'name': class_name,
                            'confidence': round(confidence * 100, 2),
                            'class_id': class_id
                        })
            
            logger.info(f"Detected {len(detected_objects)} object(s)")
            
            return {
                'success': True,
                'objects': detected_objects,
                'total_objects': len(detected_objects)
            }
            
        except Exception as e:
            logger.error(f"Error detecting objects: {e}", exc_info=True)
            return {
                'success': False,
                'objects': [],
                'total_objects': 0,
                'error': str(e)
            }
