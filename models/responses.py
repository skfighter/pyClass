"""
API Response Models

Pydantic models for type-safe API responses
"""

from typing import Dict
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
