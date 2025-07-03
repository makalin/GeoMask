"""
Configuration settings for GeoMask
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Environment
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    STABILITY_API_KEY: Optional[str] = Field(default=None, env="STABILITY_API_KEY")
    
    # File Settings
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    ALLOWED_EXTENSIONS: list = Field(default=[".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"])
    UPLOAD_DIR: str = Field(default="uploads", env="UPLOAD_DIR")
    PROCESSED_DIR: str = Field(default="processed", env="PROCESSED_DIR")
    TEMP_DIR: str = Field(default="temp", env="TEMP_DIR")
    OUTPUT_DIR: str = Field(default="output", env="OUTPUT_DIR")
    
    # AI Settings
    AI_PROVIDER: str = Field(default="openai", env="AI_PROVIDER")  # openai, stability, local
    IMAGE_SIZE: str = Field(default="1024x1024", env="IMAGE_SIZE")
    QUALITY: str = Field(default="standard", env="QUALITY")  # standard, hd
    STYLE: str = Field(default="natural", env="STYLE")  # natural, vivid
    
    # Processing Settings
    DETECTION_CONFIDENCE: float = Field(default=0.7, env="DETECTION_CONFIDENCE")
    BLEND_MODE: str = Field(default="seamless", env="BLEND_MODE")  # seamless, overlay
    PRESERVE_ASPECT_RATIO: bool = Field(default=True, env="PRESERVE_ASPECT_RATIO")
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=10, env="RATE_LIMIT_PER_MINUTE")
    
    # CORS
    ALLOWED_ORIGINS: list = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="ALLOWED_ORIGINS"
    )
    
    # Database (if needed later)
    DATABASE_URL: Optional[str] = Field(default=None, env="DATABASE_URL")
    
    # Redis (if needed later)
    REDIS_URL: Optional[str] = Field(default=None, env="REDIS_URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories"""
        for directory in [self.UPLOAD_DIR, self.PROCESSED_DIR, self.TEMP_DIR, self.OUTPUT_DIR]:
            Path(directory).mkdir(exist_ok=True)
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT.lower() == "production"
    
    def get_ai_prompt(self, scene_type: str, custom_prompt: str = "") -> str:
        """Generate AI prompt based on scene type"""
        prompts = {
            "random": "A beautiful random location with a window view, photorealistic, high quality",
            "city": "A modern cityscape view through a window, urban architecture, photorealistic",
            "mountain": "A Swiss mountain village view through a window, alpine scenery, photorealistic",
            "beach": "A tropical beach view through a window, ocean and palm trees, photorealistic",
            "forest": "A dense forest view through a window, green trees and nature, photorealistic",
            "desert": "A desert landscape view through a window, sand dunes and sky, photorealistic"
        }
        
        if custom_prompt:
            return f"A view through a window showing: {custom_prompt}, photorealistic, high quality"
        
        return prompts.get(scene_type, prompts["random"])


# Create settings instance
settings = Settings() 