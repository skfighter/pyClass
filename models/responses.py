"""
API Response Models

Pydantic models for type-safe API responses
"""

from typing import Dict, Any
from pydantic import BaseModel, Field


class ImageAnalysisResponse(BaseModel):
    """Response model for image analysis endpoint"""
    
    success: bool = Field(
        ...,
        description="Whether the analysis was successful"
    )
    description: str = Field(
        ...,
        description="AI-generated description of the image content"
    )
    extracted_text: str = Field(
        ...,
        description="Text extracted from the image using OCR"
    )
    has_text: bool = Field(
        ...,
        description="Whether text was found in the image"
    )
    filename: str = Field(
        ...,
        description="Original filename of the uploaded image"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "description": "a person sitting at a desk with a laptop",
                "extracted_text": "Hello World\nWelcome to PyClass API",
                "has_text": True,
                "filename": "example.jpg"
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    
    status: str = Field(
        ...,
        description="Overall health status of the API"
    )
    models_loaded: bool = Field(
        ...,
        description="Whether AI models are loaded and ready"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "models_loaded": True
            }
        }


class InfoResponse(BaseModel):
    """Response model for API information endpoint"""
    
    name: str = Field(
        ...,
        description="API name"
    )
    version: str = Field(
        ...,
        description="API version"
    )
    description: str = Field(
        ...,
        description="API description"
    )
    endpoints: Dict[str, str] = Field(
        ...,
        description="Available endpoints and their descriptions"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "PyClass API",
                "version": "1.0.0",
                "description": "AI-powered image analysis and OCR API",
                "endpoints": {
                    "GET /": "Welcome message",
                    "GET /health": "Health check",
                    "GET /api/info": "API information",
                    "POST /seeImageAiInfo": "Image analysis with AI and OCR"
                }
            }
        }


class HumanCountResponse(BaseModel):
    """Response model for human count endpoint"""
    
    humansCount: int = Field(
        ...,
        description="Number of humans detected in the image",
        ge=0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "humansCount": 3
            }
        }


class AudioTranscriptionResponse(BaseModel):
    """Response model for audio transcription endpoint"""
    
    success: bool = Field(
        ...,
        description="Whether the transcription was successful"
    )
    transcription: str = Field(
        ...,
        description="Transcribed text from the audio file"
    )
    language: str = Field(
        ...,
        description="Detected language of the audio"
    )
    duration_seconds: float = Field(
        ...,
        description="Duration of the audio file in seconds"
    )
    audio_info: Dict[str, Any] = Field(
        ...,
        description="Additional audio file information"
    )
    filename: str = Field(
        ...,
        description="Original filename of the uploaded audio"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "transcription": "Hello, this is a sample audio transcription.",
                "language": "en",
                "duration_seconds": 5.2,
                "audio_info": {
                    "sample_rate": 16000,
                    "channels": 1,
                    "format": "mp3"
                },
                "filename": "sample.mp3"
            }
        }


class BlackAndWhiteResponse(BaseModel):
    """Response model for black and white conversion endpoint"""
    
    success: bool = Field(
        ...,
        description="Whether the conversion was successful"
    )
    filename: str = Field(
        ...,
        description="Original filename of the uploaded image"
    )
    bw_image_base64: str = Field(
        ...,
        description="Base64 encoded black and white image (data URL format)"
    )
    image_info: Dict[str, Any] = Field(
        ...,
        description="Image metadata (width, height, format, etc.)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "filename": "photo.jpg",
                "bw_image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
                "image_info": {
                    "width": 800,
                    "height": 600,
                    "format": "JPEG",
                    "mode": "L",
                    "size_bytes": 45678
                }
            }
        }


class FaceDetectionResponse(BaseModel):
    """Response model for face detection endpoint"""
    
    success: bool = Field(
        ...,
        description="Whether the face detection was successful"
    )
    filename: str = Field(
        ...,
        description="Original filename of the uploaded image"
    )
    marked_image_base64: str = Field(
        ...,
        description="Base64 encoded image with detected faces marked with red circles"
    )
    faces_detected: int = Field(
        ...,
        description="Number of faces detected in the image"
    )
    image_info: Dict[str, Any] = Field(
        ...,
        description="Image metadata (width, height, format, etc.)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "filename": "group_photo.jpg",
                "marked_image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
                "faces_detected": 3,
                "image_info": {
                    "width": 1920,
                    "height": 1080,
                    "format": "JPEG",
                    "size_bytes": 245678
                }
            }
        }


class ColorExtractionResponse(BaseModel):
    """Response model for color extraction endpoint"""
    
    success: bool = Field(
        ...,
        description="Whether the color extraction was successful"
    )
    filename: str = Field(
        ...,
        description="Original filename of the uploaded image"
    )
    colors: list = Field(
        ...,
        description="List of dominant colors with RGB, HEX, percentage, and name"
    )
    total_colors_found: int = Field(
        ...,
        description="Total number of dominant colors extracted"
    )
    image_info: Dict[str, Any] = Field(
        ...,
        description="Image metadata (width, height, total pixels, etc.)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "filename": "sunset.jpg",
                "colors": [
                    {
                        "rgb": [255, 128, 64],
                        "hex": "#ff8040",
                        "percentage": 35.5,
                        "color_name": "Orange"
                    },
                    {
                        "rgb": [64, 128, 192],
                        "hex": "#4080c0",
                        "percentage": 28.3,
                        "color_name": "Blue"
                    }
                ],
                "total_colors_found": 10,
                "image_info": {
                    "width": 1920,
                    "height": 1080,
                    "total_pixels": 2073600,
                    "format": "JPEG"
                }
            }
        }


class BackgroundRemovalResponse(BaseModel):
    """Response model for background removal endpoint"""
    
    success: bool = Field(
        ...,
        description="Whether the background removal was successful"
    )
    filename: str = Field(
        ...,
        description="Original filename of the uploaded image"
    )
    no_bg_image_base64: str = Field(
        ...,
        description="Base64 encoded image with background removed (data URL format with transparent background)"
    )
    image_info: Dict[str, Any] = Field(
        ...,
        description="Image metadata (width, height, format, etc.)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "filename": "person.jpg",
                "no_bg_image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUh...",
                "image_info": {
                    "width": 800,
                    "height": 600,
                    "format": "PNG",
                    "mode": "RGBA",
                    "size_bytes": 125678
                }
            }
        }
