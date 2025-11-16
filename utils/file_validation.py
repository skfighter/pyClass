"""
File validation utilities

Provides validation functions for file uploads
"""

import logging
from typing import List, Tuple
from fastapi import UploadFile, HTTPException, status

logger = logging.getLogger(__name__)


def validate_file_type(
    file: UploadFile,
    allowed_types: List[str],
    type_category: str = "file"
) -> None:
    """
    Validate uploaded file type
    
    Args:
        file: Uploaded file object
        allowed_types: List of allowed file extensions (e.g., ['.jpg', '.png'])
        type_category: Category name for error message (e.g., 'image', 'audio')
    
    Raises:
        HTTPException: If file type is not allowed
    """
    if not file.content_type:
        logger.warning(f"File uploaded without content type: {file.filename}")
        # Try to validate by extension
        if not any(file.filename.lower().endswith(ext) for ext in allowed_types):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed {type_category} formats: {', '.join(allowed_types)}"
            )
        return
    
    # Check content type prefix
    expected_prefix = _get_content_type_prefix(type_category)
    if expected_prefix and not file.content_type.startswith(expected_prefix):
        # Also check by extension as fallback
        if not any(file.filename.lower().endswith(ext) for ext in allowed_types):
            logger.warning(f"Invalid file type uploaded: {file.content_type}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Please upload a {type_category} file. Allowed formats: {', '.join(allowed_types)}"
            )


def validate_file_size(
    file_bytes: bytes,
    max_size_mb: float,
    filename: str = "file"
) -> Tuple[float, int]:
    """
    Validate uploaded file size
    
    Args:
        file_bytes: File content as bytes
        max_size_mb: Maximum allowed file size in megabytes
        filename: Filename for logging
    
    Returns:
        Tuple of (file_size_mb, file_size_bytes)
    
    Raises:
        HTTPException: If file size exceeds limit
    """
    file_size_bytes = len(file_bytes)
    file_size_mb = file_size_bytes / (1024 * 1024)
    
    if file_size_mb > max_size_mb:
        logger.warning(
            f"File too large: {filename} ({file_size_mb:.2f}MB) "
            f"exceeds limit of {max_size_mb}MB"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {max_size_mb}MB (uploaded: {file_size_mb:.2f}MB)"
        )
    
    return file_size_mb, file_size_bytes


def _get_content_type_prefix(type_category: str) -> str:
    """Get expected content type prefix for file category"""
    prefixes = {
        "image": "image/",
        "audio": "audio/",
        "video": "video/",
        "text": "text/",
    }
    return prefixes.get(type_category.lower(), "")


def get_file_extension(filename: str) -> str:
    """
    Extract file extension from filename
    
    Args:
        filename: Name of the file
    
    Returns:
        File extension including the dot (e.g., '.jpg')
    """
    import os
    return os.path.splitext(filename)[1].lower()
