"""
Pydantic schemas for GeoMask API
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ProcessRequest(BaseModel):
    """Request model for image processing"""
    scene_type: str = Field(default="random", description="Type of scene to generate")
    custom_prompt: Optional[str] = Field(default="", description="Custom scene description")
    preserve_quality: bool = Field(default=True, description="Preserve original image quality")
    blend_mode: str = Field(default="seamless", description="Blending mode for background replacement")


class ProcessResponse(BaseModel):
    """Response model for image processing"""
    success: bool = Field(description="Whether processing was successful")
    original_file: str = Field(description="Original filename")
    processed_file: str = Field(description="Processed filename")
    download_url: str = Field(description="URL to download processed image")
    processing_time: Optional[float] = Field(default=None, description="Processing time in seconds")
    message: Optional[str] = Field(default=None, description="Additional message")


class SceneInfo(BaseModel):
    """Scene information model"""
    id: str = Field(description="Scene identifier")
    name: str = Field(description="Scene display name")
    description: str = Field(description="Scene description")
    preview_url: Optional[str] = Field(default=None, description="Preview image URL")


class ScenesResponse(BaseModel):
    """Response model for available scenes"""
    scenes: List[SceneInfo] = Field(description="List of available scenes")


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(description="Service status")
    service: str = Field(description="Service name")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")
    version: str = Field(default="1.0.0", description="Service version")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(default=None, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")


class FileInfo(BaseModel):
    """File information model"""
    filename: str = Field(description="File name")
    size: int = Field(description="File size in bytes")
    content_type: str = Field(description="File MIME type")
    upload_time: datetime = Field(description="Upload timestamp")


class ProcessingStatus(BaseModel):
    """Processing status model"""
    job_id: str = Field(description="Processing job ID")
    status: str = Field(description="Processing status")
    progress: float = Field(default=0.0, description="Processing progress (0-100)")
    estimated_time: Optional[float] = Field(default=None, description="Estimated completion time")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Job creation time") 