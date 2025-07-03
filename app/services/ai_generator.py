"""
AI image generation service for GeoMask
"""

import os
import time
import asyncio
from pathlib import Path
from typing import Optional, Tuple
import logging
import random

import openai
from PIL import Image
import numpy as np

from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class AIGenerator:
    """Handles AI image generation for background replacement"""
    
    def __init__(self):
        self.client = None
        self.initialized = False
        self.provider = settings.AI_PROVIDER.lower()
        
        # Scene templates for different types
        self.scene_templates = {
            "random": [
                "A beautiful cityscape view through a window, modern architecture, photorealistic",
                "A serene mountain landscape through a window, alpine scenery, photorealistic",
                "A peaceful beach view through a window, ocean waves, photorealistic",
                "A lush forest view through a window, green trees, photorealistic",
                "A desert sunset view through a window, golden sand dunes, photorealistic"
            ],
            "city": [
                "A modern cityscape view through a window, skyscrapers, urban architecture, photorealistic",
                "A bustling city street view through a window, people walking, photorealistic",
                "A city skyline at sunset through a window, golden hour lighting, photorealistic"
            ],
            "mountain": [
                "A Swiss mountain village view through a window, alpine scenery, snow-capped peaks, photorealistic",
                "A cozy mountain cabin view through a window, pine trees, photorealistic",
                "A mountain lake view through a window, crystal clear water, photorealistic"
            ],
            "beach": [
                "A tropical beach view through a window, palm trees, turquoise water, photorealistic",
                "A sunset beach view through a window, golden sand, ocean waves, photorealistic",
                "A coastal cliff view through a window, dramatic ocean scenery, photorealistic"
            ],
            "forest": [
                "A dense forest view through a window, green trees, natural lighting, photorealistic",
                "A misty forest view through a window, fog, mysterious atmosphere, photorealistic",
                "A forest clearing view through a window, sunlight filtering through trees, photorealistic"
            ],
            "desert": [
                "A desert landscape view through a window, sand dunes, clear blue sky, photorealistic",
                "A desert sunset view through a window, golden hour, dramatic lighting, photorealistic",
                "A desert oasis view through a window, palm trees, water, photorealistic"
            ]
        }
    
    async def initialize(self):
        """Initialize the AI generator"""
        try:
            if self.provider == "openai":
                await self._initialize_openai()
            elif self.provider == "stability":
                await self._initialize_stability()
            elif self.provider == "local":
                await self._initialize_local()
            else:
                logger.warning(f"Unknown AI provider: {self.provider}, using fallback")
                await self._initialize_fallback()
            
            self.initialized = True
            logger.info(f"AI Generator initialized with provider: {self.provider}")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI Generator: {e}")
            await self._initialize_fallback()
    
    async def _initialize_openai(self):
        """Initialize OpenAI client"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        logger.info("OpenAI client initialized")
    
    async def _initialize_stability(self):
        """Initialize Stability AI client"""
        if not settings.STABILITY_API_KEY:
            raise ValueError("Stability API key not configured")
        
        # Placeholder for Stability AI integration
        logger.info("Stability AI client initialized")
    
    async def _initialize_local(self):
        """Initialize local AI model"""
        # Placeholder for local model integration (e.g., Stable Diffusion)
        logger.info("Local AI model initialized")
    
    async def _initialize_fallback(self):
        """Initialize fallback generator"""
        logger.info("Using fallback image generator")
        self.provider = "fallback"
    
    async def generate_image(
        self,
        scene_type: str = "random",
        custom_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        quality: str = "standard"
    ) -> str:
        """
        Generate an image using AI
        
        Args:
            scene_type: Type of scene to generate
            custom_prompt: Custom scene description
            width: Image width
            height: Image height
            quality: Image quality (standard, hd)
            
        Returns:
            Path to generated image
        """
        try:
            if not self.initialized:
                await self.initialize()
            
            # Generate prompt
            prompt = self._generate_prompt(scene_type, custom_prompt)
            
            # Generate image based on provider
            if self.provider == "openai":
                image_path = await self._generate_openai_image(prompt, width, height, quality)
            elif self.provider == "stability":
                image_path = await self._generate_stability_image(prompt, width, height, quality)
            elif self.provider == "local":
                image_path = await self._generate_local_image(prompt, width, height, quality)
            else:
                image_path = await self._generate_fallback_image(prompt, width, height, quality)
            
            logger.info(f"Generated image: {image_path}")
            return image_path
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            # Return fallback image
            return await self._generate_fallback_image("", width, height, quality)
    
    def _generate_prompt(self, scene_type: str, custom_prompt: str) -> str:
        """Generate AI prompt based on scene type and custom prompt"""
        if custom_prompt:
            return f"A view through a window showing: {custom_prompt}, photorealistic, high quality, 8k resolution"
        
        templates = self.scene_templates.get(scene_type, self.scene_templates["random"])
        base_prompt = random.choice(templates)
        
        # Add quality enhancements
        quality_enhancements = [
            "high quality",
            "8k resolution",
            "professional photography",
            "natural lighting",
            "detailed"
        ]
        
        enhancements = random.sample(quality_enhancements, 2)
        return f"{base_prompt}, {', '.join(enhancements)}"
    
    async def _generate_openai_image(
        self, 
        prompt: str, 
        width: int, 
        height: int, 
        quality: str
    ) -> str:
        """Generate image using OpenAI DALL-E"""
        try:
            # Ensure dimensions are valid for DALL-E
            if width > 1024 or height > 1024:
                width = min(width, 1024)
                height = min(height, 1024)
            
            # Map quality to DALL-E quality
            dall_e_quality = "hd" if quality == "hd" else "standard"
            
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=f"{width}x{height}",
                quality=dall_e_quality,
                n=1
            )
            
            # Download and save image
            image_url = response.data[0].url
            image_path = await self._download_and_save_image(image_url, "openai")
            
            return image_path
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise
    
    async def _generate_stability_image(
        self, 
        prompt: str, 
        width: int, 
        height: int, 
        quality: str
    ) -> str:
        """Generate image using Stability AI"""
        # Placeholder for Stability AI integration
        logger.info("Stability AI generation not implemented yet")
        return await self._generate_fallback_image(prompt, width, height, quality)
    
    async def _generate_local_image(
        self, 
        prompt: str, 
        width: int, 
        height: int, 
        quality: str
    ) -> str:
        """Generate image using local model"""
        # Placeholder for local model integration
        logger.info("Local model generation not implemented yet")
        return await self._generate_fallback_image(prompt, width, height, quality)
    
    async def _generate_fallback_image(
        self, 
        prompt: str, 
        width: int, 
        height: int, 
        quality: str
    ) -> str:
        """Generate fallback image when AI services are unavailable"""
        try:
            # Create a simple gradient image
            image = self._create_gradient_image(width, height)
            
            # Save image
            timestamp = int(time.time())
            filename = f"fallback_{timestamp}.jpg"
            image_path = Path(settings.TEMP_DIR) / filename
            
            image.save(image_path, "JPEG", quality=95)
            
            logger.info(f"Generated fallback image: {image_path}")
            return str(image_path)
            
        except Exception as e:
            logger.error(f"Error generating fallback image: {e}")
            raise
    
    def _create_gradient_image(self, width: int, height: int) -> Image.Image:
        """Create a gradient image as fallback"""
        # Create gradient from top to bottom
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        for y in range(height):
            ratio = y / height
            # Create a pleasant gradient
            r = int(100 + 155 * ratio)
            g = int(150 + 105 * ratio)
            b = int(200 + 55 * ratio)
            
            for x in range(width):
                pixels[x, y] = (r, g, b)
        
        return image
    
    async def _download_and_save_image(self, image_url: str, provider: str) -> str:
        """Download and save image from URL"""
        try:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)
                response.raise_for_status()
                
                # Save image
                timestamp = int(time.time())
                filename = f"{provider}_{timestamp}.jpg"
                image_path = Path(settings.TEMP_DIR) / filename
                
                with open(image_path, "wb") as f:
                    f.write(response.content)
                
                return str(image_path)
                
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            raise
    
    def get_available_scenes(self) -> dict:
        """Get available scene types"""
        return {
            scene_type: {
                "name": scene_type.title(),
                "description": f"Generate {scene_type} scene",
                "templates": len(templates)
            }
            for scene_type, templates in self.scene_templates.items()
        }
    
    async def cleanup_temp_files(self):
        """Clean up temporary generated files"""
        try:
            temp_dir = Path(settings.TEMP_DIR)
            for file in temp_dir.glob("*.jpg"):
                if file.name.startswith(("openai_", "stability_", "local_", "fallback_")):
                    file.unlink()
                    logger.debug(f"Cleaned up temp file: {file}")
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}") 