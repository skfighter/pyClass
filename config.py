"""
Configuration module for PyClass API
Handles environment variables and application settings
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True  # Auto-reload on code changes (dev mode)
    
    # AI Model Configuration
    model_name: str = "Salesforce/blip-image-captioning-base"
    max_caption_length: int = 50
    num_beams: int = 5
    
    # File Upload Limits
    max_file_size_mb: int = 10
    max_audio_size_mb: int = 25
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "webp", "gif", "bmp"]
    allowed_audio_extensions: List[str] = ["mp3", "wav", "m4a", "flac", "ogg", "aac", "wma"]
    
    # Logging
    log_level: str = "INFO"
    
    # API Metadata
    api_title: str = "PyClass API"
    api_description: str = "AI-powered image analysis and OCR API"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
