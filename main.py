"""
PyClass API - FastAPI Server
AI-powered image analysis and OCR API

This module provides endpoints for:
- Image description using BLIP AI model
- Text extraction using Tesseract OCR
- Health checks and API information
"""

import logging
from typing import Dict
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from services.image_service import ImageAnalysisService
from models.responses import ImageAnalysisResponse, HealthResponse, InfoResponse

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instance
image_service: ImageAnalysisService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - handles startup and shutdown"""
    # Startup
    global image_service
    logger.info("Starting PyClass API...")
    logger.info("Loading AI models...")
    
    try:
        image_service = ImageAnalysisService()
        logger.info("✅ AI models loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load AI models: {e}")
        image_service = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down PyClass API...")


# Initialize FastAPI application
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=Dict[str, str], tags=["General"])
async def root() -> Dict[str, str]:
    """
    Root endpoint - Welcome message
    
    Returns:
        Dict with welcome message and status
    """
    return {
        "message": f"Welcome to {settings.api_title}",
        "status": "running",
        "version": settings.api_version
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint
    
    Returns:
        Health status with model availability
    """
    return HealthResponse(
        status="healthy",
        models_loaded=image_service is not None and image_service.is_ready()
    )


@app.get("/api/info", response_model=InfoResponse, tags=["General"])
async def api_info() -> InfoResponse:
    """
    API information endpoint
    
    Returns:
        API metadata and configuration
    """
    return InfoResponse(
        name=settings.api_title,
        version=settings.api_version,
        description=settings.api_description,
        endpoints={
            "GET /": "Welcome message",
            "GET /health": "Health check",
            "GET /api/info": "API information",
            "POST /seeImageAiInfo": "Image analysis with AI and OCR"
        }
    )


@app.post("/seeImageAiInfo", response_model=ImageAnalysisResponse, tags=["Image Analysis"])
async def analyze_image(file: UploadFile = File(...)) -> ImageAnalysisResponse:
    """
    Analyze uploaded image with AI and extract text using OCR
    
    This endpoint:
    1. Validates the uploaded image
    2. Generates an AI description of the image content
    3. Extracts any text found in the image using OCR
    4. Returns comprehensive analysis results
    
    Args:
        file: Uploaded image file (JPG, PNG, WEBP, GIF, BMP)
    
    Returns:
        ImageAnalysisResponse with description, extracted text, and metadata
    
    Raises:
        HTTPException: 
            - 503 if AI model is not available
            - 400 if file type is invalid or file is too large
            - 500 if processing fails
    """
    # Check if service is ready
    if image_service is None or not image_service.is_ready():
        logger.error("Image analysis requested but service not ready")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI model not available. Server is still loading, please try again in a moment."
        )
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        logger.warning(f"Invalid file type uploaded: {file.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Please upload an image file. Allowed: {', '.join(settings.allowed_extensions)}"
        )
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Check file size
        file_size_mb = len(contents) / (1024 * 1024)
        if file_size_mb > settings.max_file_size_mb:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
            )
        
        logger.info(f"Processing image: {file.filename} ({file_size_mb:.2f}MB)")
        
        # Analyze image
        result = await image_service.analyze_image(contents, file.filename)
        
        logger.info(f"Successfully processed: {file.filename}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image {file.filename}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )
    finally:
        await file.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
