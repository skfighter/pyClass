"""
Basic FastAPI Server
A simple API server demonstrating FastAPI capabilities
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Optional
import io
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import pytesseract
import numpy as np

app = FastAPI(
    title="PyClass API",
    description="A basic Python API server using FastAPI",
    version="1.0.0"
)

# Initialize the AI model for image captioning
# Using BLIP (Bootstrapping Language-Image Pre-training) model
processor = None
model = None

def load_model():
    """Load the BLIP model for image captioning"""
    global processor, model
    try:
        print("Loading AI model...")
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        print("✅ AI model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading AI model: {e}")
        processor = None
        model = None

# Load model on startup (you can also do this lazily on first request)
load_model()


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint that returns a welcome message
    """
    return {
        "message": "Welcome to PyClass API",
        "status": "running"
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint
    """
    return {
        "status": "healthy"
    }


@app.get("/api/info")
async def api_info() -> Dict[str, str]:
    """
    API information endpoint
    """
    return {
        "name": "PyClass API",
        "version": "1.0.0",
        "description": "A basic Python API server using FastAPI"
    }


@app.post("/seeImageAiInfo")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze uploaded image and return information about what's in the image.
    Also extracts any text found in the image using OCR.
    
    Args:
        file: Uploaded image file (supports common formats: JPG, PNG, WEBP, etc.)
    
    Returns:
        JSON response with:
        - description: AI-generated description of the image
        - extracted_text: Any text found in the image (if present)
        - image_info: Technical details about the image
    """
    # Check if model is loaded
    if processor is None or model is None:
        raise HTTPException(
            status_code=503, 
            detail="AI model not available. Server is still loading, please try again in a moment."
        )
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload an image file (JPG, PNG, etc.)."
        )
    
    try:
        # Read the uploaded image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 1. Generate AI description of the image
        description = ""
        try:
            inputs = processor(image, return_tensors="pt")
            with torch.no_grad():
                out = model.generate(**inputs, max_length=50, num_beams=5)
            description = processor.decode(out[0], skip_special_tokens=True)
        except Exception as desc_error:
            print(f"Description error: {desc_error}")
            description = "Unable to generate description"
        
        # 2. Extract text from image using OCR
        extracted_text = ""
        try:
            # Use pytesseract for OCR
            extracted_text = pytesseract.image_to_string(image).strip()
        except Exception as ocr_error:
            print(f"OCR error: {ocr_error}")
            # OCR is optional, continue even if it fails
        
        # Get basic image info
        width, height = image.size
        format_info = image.format or "Unknown"
        
        # Build response
        response_data = {
            "success": True,
            "filename": file.filename,
            "description": description,
            "extracted_text": extracted_text if extracted_text else "",
            "has_text": len(extracted_text) > 0,
            "image_info": {
                "width": width,
                "height": height,
                "format": format_info,
                "mode": image.mode,
                "size_bytes": len(contents)
            }
        }
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        print(f"Error processing image: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing image: {str(e)}"
        )
    finally:
        # Clean up
        await file.close()
