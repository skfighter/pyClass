"""
Audio Transcription Service

Handles audio transcription using OpenAI Whisper and audio analysis
"""

import logging
import tempfile
import os
from typing import Optional, Dict, Any

import whisper
import librosa
import numpy as np

from models.responses import AudioTranscriptionResponse

logger = logging.getLogger(__name__)


class AudioTranscriptionService:
    """Service for transcribing audio files and extracting metadata"""
    
    # Supported model sizes
    SUPPORTED_MODELS = ["tiny", "base", "small", "medium", "large"]
    
    def __init__(self, model_size: str = "base") -> None:
        """
        Initialize the audio transcription service with Whisper model
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
                       'base' is a good balance of speed and accuracy
                       
        Raises:
            ValueError: If model_size is not supported
        """
        if model_size not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Unsupported model size: {model_size}. "
                f"Supported models: {', '.join(self.SUPPORTED_MODELS)}"
            )
        
        self.model: Optional[whisper.Whisper] = None
        self.model_size = model_size
        self._load_model()
    
    def _load_model(self) -> None:
        """Load Whisper model for transcription"""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            # Download model on first run (~140MB for base model)
            self.model = whisper.load_model(self.model_size)
            logger.info(f"✅ Whisper {self.model_size} model loaded successfully")
                
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            self.model = None
            raise
    
    def is_ready(self) -> bool:
        """Check if service is ready to transcribe audio"""
        return self.model is not None
    
    async def transcribe_audio(self, audio_bytes: bytes, filename: str) -> AudioTranscriptionResponse:
        """
        Transcribe audio file and extract metadata
        
        Args:
            audio_bytes: Raw audio file bytes
            filename: Original filename for logging
        
        Returns:
            AudioTranscriptionResponse with transcription and metadata
        
        Raises:
            Exception: If audio processing fails
        """
        # Create temporary file for audio processing
        # Whisper needs a file path, not just bytes
        temp_file = None
        try:
            # Create temp file with appropriate extension
            file_ext = os.path.splitext(filename)[1] or '.wav'
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)
            temp_file.write(audio_bytes)
            temp_file.close()
            
            logger.info(f"Processing audio: {filename}")
            
            # Get audio metadata using librosa
            audio_info = await self._get_audio_info(temp_file.name)
            
            # Transcribe audio using Whisper
            result = self.model.transcribe(temp_file.name)
            
            transcription = result["text"].strip()
            language = result.get("language", "unknown")
            
            logger.info(f"Transcription complete: {filename} - Language: {language}")
            
            return AudioTranscriptionResponse(
                success=True,
                transcription=transcription,
                language=language,
                duration_seconds=audio_info["duration"],
                audio_info=audio_info,
                filename=filename
            )
            
        except Exception as e:
            logger.error(f"Error transcribing audio {filename}: {e}", exc_info=True)
            raise
            
        finally:
            # Clean up temp file
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                except Exception as e:
                    logger.warning(f"Failed to delete temp file: {e}")
    
    async def _get_audio_info(self, file_path: str) -> Dict[str, Any]:
        """
        Extract audio file metadata
        
        Args:
            file_path: Path to audio file
        
        Returns:
            Dictionary with audio information including:
                - sample_rate: Audio sample rate in Hz
                - duration: Duration in seconds
                - channels: Number of audio channels
                - format: File format extension
                - file_size_bytes: File size in bytes
                - file_size_mb: File size in megabytes
        """
        try:
            # Load audio file with librosa
            y: np.ndarray
            sr: int
            y, sr = librosa.load(file_path, sr=None)
            
            # Calculate duration
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Determine format from file extension
            file_format = os.path.splitext(file_path)[1].lstrip('.')
            
            return {
                "sample_rate": int(sr),
                "duration": round(duration, 2),
                "channels": 1 if len(y.shape) == 1 else y.shape[0],
                "format": file_format,
                "file_size_bytes": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error(f"Error extracting audio info: {e}", exc_info=True)
            # Return minimal info on error
            return {
                "sample_rate": 0,
                "duration": 0,
                "channels": 0,
                "format": "unknown",
                "file_size_bytes": 0,
                "file_size_mb": 0
            }
