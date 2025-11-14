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

from fastapi import FastAPI, File, UploadFile, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from config import settings
from services.image_service import ImageAnalysisService
from services.human_detection_service import HumanDetectionService
from services.audio_service import AudioTranscriptionService
from models.responses import ImageAnalysisResponse, HealthResponse, InfoResponse, HumanCountResponse, AudioTranscriptionResponse, BlackAndWhiteResponse, BackgroundRemovalResponse
from utils.file_validation import validate_file_type, validate_file_size

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instance
image_service: ImageAnalysisService = None
human_detection_service: HumanDetectionService = None
audio_service: AudioTranscriptionService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - handles startup and shutdown"""
    # Startup
    global image_service, human_detection_service, audio_service
    logger.info("Starting PyClass API...")
    logger.info("Loading AI models...")
    
    try:
        image_service = ImageAnalysisService()
        logger.info("✅ AI models loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load AI models: {e}")
        image_service = None
    
    try:
        human_detection_service = HumanDetectionService()
        logger.info("✅ Human detection model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load human detection model: {e}")
        human_detection_service = None
    
    try:
        audio_service = AudioTranscriptionService(model_size="base")
        logger.info("✅ Audio transcription model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load audio transcription model: {e}")
        audio_service = None
    
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

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse, tags=["General"])
async def root(request: Request):
    """
    Root endpoint - Serves the interactive web frontend
    
    Returns:
        HTML page with interactive demo of all API features
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "version": settings.api_version
        }
    )


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
            "POST /seeImageAiInfo": "Image analysis with AI and OCR",
            "POST /checkHumansCount": "Count humans in image",
            "POST /transcribeAudio": "Transcribe audio to text",
            "POST /convertToBlackAndWhite": "Convert image to black and white",
            "POST /removeBackground": "Remove background from image"
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
    allowed_exts = [f".{ext}" for ext in settings.allowed_extensions]
    validate_file_type(file, allowed_exts, "image")
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Validate file size
        file_size_mb, _ = validate_file_size(contents, settings.max_file_size_mb, file.filename)
        
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


@app.post("/checkHumansCount", response_model=HumanCountResponse, tags=["Image Analysis"])
async def check_humans_count(file: UploadFile = File(...)) -> HumanCountResponse:
    """
    Count humans in an uploaded image using AI object detection
    
    This endpoint:
    1. Validates the uploaded image
    2. Detects all humans in the image using YOLOv8
    3. Returns the count of detected humans
    
    Args:
        file: Uploaded image file (JPG, PNG, WEBP, GIF, BMP)
    
    Returns:
        HumanCountResponse with count of humans (0 if none detected)
    
    Raises:
        HTTPException: 
            - 503 if detection model is not available
            - 400 if file type is invalid or file is too large
            - 500 if processing fails
    """
    # Check if service is ready
    if human_detection_service is None or not human_detection_service.is_ready():
        logger.error("Human detection requested but service not ready")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Human detection model not available. Server is still loading, please try again in a moment."
        )
    
    # Validate file type
    allowed_exts = [f".{ext}" for ext in settings.allowed_extensions]
    validate_file_type(file, allowed_exts, "image")
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Validate file size
        file_size_mb, _ = validate_file_size(contents, settings.max_file_size_mb, file.filename)
        
        logger.info(f"Detecting humans in image: {file.filename} ({file_size_mb:.2f}MB)")
        
        # Count humans
        result = await human_detection_service.count_humans(contents)
        
        logger.info(f"Successfully processed: {file.filename} - Found {result.humansCount} human(s)")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error detecting humans in {file.filename}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )
    finally:
        await file.close()


@app.post("/transcribeAudio", response_model=AudioTranscriptionResponse, tags=["Audio Analysis"])
async def transcribe_audio(file: UploadFile = File(...)) -> AudioTranscriptionResponse:
    """
    Transcribe uploaded audio file to text using AI
    
    This endpoint:
    1. Validates the uploaded audio file
    2. Extracts audio metadata (duration, sample rate, etc.)
    3. Transcribes speech to text using OpenAI Whisper
    4. Detects the language of the audio
    5. Returns transcription and audio information
    
    Args:
        file: Uploaded audio file (MP3, WAV, M4A, FLAC, OGG, etc.)
    
    Returns:
        AudioTranscriptionResponse with transcription, language, and metadata
    
    Raises:
        HTTPException: 
            - 503 if transcription model is not available
            - 400 if file type is invalid or file is too large
            - 500 if processing fails
    """
    # Check if service is ready
    if audio_service is None or not audio_service.is_ready():
        logger.error("Audio transcription requested but service not ready")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Audio transcription model not available. Server is still loading, please try again in a moment."
        )
    
    # Validate file type
    allowed_exts = [f".{ext}" for ext in settings.allowed_audio_extensions]
    validate_file_type(file, allowed_exts, "audio")
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Validate file size (audio files use larger limit)
        file_size_mb, _ = validate_file_size(contents, settings.max_audio_size_mb, file.filename)
        
        logger.info(f"Transcribing audio: {file.filename} ({file_size_mb:.2f}MB)")
        
        # Transcribe audio
        result = await audio_service.transcribe_audio(contents, file.filename)
        
        logger.info(f"Successfully transcribed: {file.filename} - Language: {result.language}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error transcribing audio {file.filename}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing audio: {str(e)}"
        )
    finally:
        await file.close()


@app.post("/removeBackground", response_model=BackgroundRemovalResponse, tags=["Image Processing"])
async def remove_background(file: UploadFile = File(...)) -> BackgroundRemovalResponse:
    """
    Remove background from uploaded image
    
    This endpoint:
    1. Validates the uploaded image
    2. Uses AI to detect and remove the background
    3. Returns the image with transparent background as base64 encoded PNG
    4. Includes image metadata (dimensions, size)
    
    Args:
        file: Uploaded image file (JPG, PNG, WEBP, GIF, BMP)
    
    Returns:
        BackgroundRemovalResponse with base64 encoded transparent PNG and metadata
    
    Raises:
        HTTPException: 
            - 503 if image service is not available
            - 400 if file type is invalid or file is too large
            - 500 if processing fails
    """
    # Check if service is ready
    if image_service is None or not image_service.is_ready():
        logger.error("Background removal requested but service not ready")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Image service not available. Server is still loading, please try again in a moment."
        )
    
    # Validate file type
    allowed_exts = [f".{ext}" for ext in settings.allowed_extensions]
    validate_file_type(file, allowed_exts, "image")
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Validate file size
        file_size_mb, _ = validate_file_size(contents, settings.max_file_size_mb, file.filename)
        
        logger.info(f"Removing background from: {file.filename} ({file_size_mb:.2f}MB)")
        
        # Remove background
        result = await image_service.remove_background(contents, file.filename)
        
        logger.info(f"Successfully removed background: {file.filename}")
        
        return BackgroundRemovalResponse(
            success=True,
            filename=file.filename,
            no_bg_image_base64=result["no_bg_image_base64"],
            image_info=result["image_info"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing background from {file.filename}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )
    finally:
        await file.close()


@app.post("/convertToBlackAndWhite", response_model=BlackAndWhiteResponse, tags=["Image Processing"])
async def convert_to_black_and_white(file: UploadFile = File(...)) -> BlackAndWhiteResponse:
    """
    Convert uploaded image to black and white (grayscale)
    
    This endpoint:
    1. Validates the uploaded image
    2. Converts the image to grayscale (black and white)
    3. Returns the converted image as base64 encoded data URL for easy display
    4. Includes image metadata (dimensions, format, size)
    
    Args:
        file: Uploaded image file (JPG, PNG, WEBP, GIF, BMP)
    
    Returns:
        BlackAndWhiteResponse with base64 encoded B&W image and metadata
    
    Raises:
        HTTPException: 
            - 503 if image service is not available
            - 400 if file type is invalid or file is too large
            - 500 if processing fails
    """
    # Check if service is ready
    if image_service is None or not image_service.is_ready():
        logger.error("Image conversion requested but service not ready")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Image service not available. Server is still loading, please try again in a moment."
        )
    
    # Validate file type
    allowed_exts = [f".{ext}" for ext in settings.allowed_extensions]
    validate_file_type(file, allowed_exts, "image")
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Validate file size
        file_size_mb, _ = validate_file_size(contents, settings.max_file_size_mb, file.filename)
        
        logger.info(f"Converting to black and white: {file.filename} ({file_size_mb:.2f}MB)")
        
        # Convert to black and white
        result = await image_service.convert_to_black_and_white(contents, file.filename)
        
        logger.info(f"Successfully converted: {file.filename}")
        
        return BlackAndWhiteResponse(
            success=True,
            filename=file.filename,
            bw_image_base64=result["bw_image_base64"],
            image_info=result["image_info"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error converting image {file.filename}: {e}", exc_info=True)
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
