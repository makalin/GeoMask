"""
File utility functions for GeoMask
"""

import os
import shutil
import time
import uuid
from pathlib import Path
from typing import Optional, List
import magic
from fastapi import UploadFile

from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def save_upload_file(file: UploadFile) -> str:
    """
    Save uploaded file to uploads directory
    
    Args:
        file: Uploaded file
        
    Returns:
        Path to saved file
    """
    try:
        # Validate file
        await validate_file(file)
        
        # Generate unique filename
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        extension = Path(file.filename).suffix.lower()
        filename = f"upload_{timestamp}_{unique_id}{extension}"
        
        # Save file
        file_path = Path(settings.UPLOAD_DIR) / filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File saved: {file_path}")
        return str(file_path)
        
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise


async def validate_file(file: UploadFile) -> bool:
    """
    Validate uploaded file
    
    Args:
        file: Uploaded file
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If file is invalid
    """
    # Check file size
    if file.size > settings.MAX_FILE_SIZE:
        raise ValueError(f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes")
    
    # Check file extension
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise ValueError(f"File extension {file_extension} not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}")
    
    # Check MIME type
    if not file.content_type.startswith("image/"):
        raise ValueError("File must be an image")
    
    # Read first few bytes to check magic number
    content = await file.read(1024)
    await file.seek(0)  # Reset file pointer
    
    mime_type = magic.from_buffer(content, mime=True)
    if not mime_type.startswith("image/"):
        raise ValueError(f"Invalid image format: {mime_type}")
    
    return True


def get_file_info(file_path: str) -> dict:
    """
    Get file information
    
    Args:
        file_path: Path to file
        
    Returns:
        Dictionary with file information
    """
    try:
        path = Path(file_path)
        stat = path.stat()
        
        return {
            "filename": path.name,
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "extension": path.suffix.lower(),
            "exists": path.exists()
        }
    except Exception as e:
        logger.error(f"Error getting file info: {e}")
        return {}


def cleanup_temp_files(directory: str = None, max_age_hours: int = 24):
    """
    Clean up temporary files older than specified age
    
    Args:
        directory: Directory to clean (defaults to temp directory)
        max_age_hours: Maximum age in hours before deletion
    """
    try:
        if directory is None:
            directory = settings.TEMP_DIR
        
        temp_dir = Path(directory)
        if not temp_dir.exists():
            return
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        cleaned_count = 0
        
        for file_path in temp_dir.iterdir():
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                
                if file_age > max_age_seconds:
                    try:
                        file_path.unlink()
                        cleaned_count += 1
                        logger.debug(f"Cleaned up old file: {file_path}")
                    except Exception as e:
                        logger.warning(f"Could not delete file {file_path}: {e}")
        
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old files from {directory}")
            
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")


def ensure_directory_exists(directory: str) -> bool:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory: Directory path
        
    Returns:
        True if directory exists or was created
    """
    try:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")
        return False


def get_safe_filename(filename: str) -> str:
    """
    Convert filename to safe version
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    safe_filename = filename
    
    for char in unsafe_chars:
        safe_filename = safe_filename.replace(char, '_')
    
    # Limit length
    if len(safe_filename) > 255:
        name, ext = os.path.splitext(safe_filename)
        safe_filename = name[:255-len(ext)] + ext
    
    return safe_filename


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    try:
        size_bytes = Path(file_path).stat().st_size
        return size_bytes / (1024 * 1024)
    except Exception as e:
        logger.error(f"Error getting file size: {e}")
        return 0.0


def is_image_file(file_path: str) -> bool:
    """
    Check if file is an image
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file is an image
    """
    try:
        # Check extension
        extension = Path(file_path).suffix.lower()
        if extension not in settings.ALLOWED_EXTENSIONS:
            return False
        
        # Check magic number
        with open(file_path, 'rb') as f:
            content = f.read(1024)
            mime_type = magic.from_buffer(content, mime=True)
            return mime_type.startswith("image/")
            
    except Exception as e:
        logger.error(f"Error checking if file is image: {e}")
        return False


def list_files_in_directory(directory: str, pattern: str = "*") -> List[str]:
    """
    List files in directory matching pattern
    
    Args:
        directory: Directory path
        pattern: File pattern (e.g., "*.jpg")
        
    Returns:
        List of file paths
    """
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return []
        
        files = list(dir_path.glob(pattern))
        return [str(f) for f in files if f.is_file()]
        
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return []


def move_file(source: str, destination: str) -> bool:
    """
    Move file from source to destination
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        True if successful
    """
    try:
        # Ensure destination directory exists
        dest_dir = Path(destination).parent
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Move file
        shutil.move(source, destination)
        logger.info(f"Moved file from {source} to {destination}")
        return True
        
    except Exception as e:
        logger.error(f"Error moving file: {e}")
        return False


def copy_file(source: str, destination: str) -> bool:
    """
    Copy file from source to destination
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        True if successful
    """
    try:
        # Ensure destination directory exists
        dest_dir = Path(destination).parent
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(source, destination)
        logger.info(f"Copied file from {source} to {destination}")
        return True
        
    except Exception as e:
        logger.error(f"Error copying file: {e}")
        return False 