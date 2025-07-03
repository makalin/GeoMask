"""
Image processing service for GeoMask
"""

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import os
import time
from pathlib import Path
from typing import Tuple, Optional, List
import logging

from app.config import settings
from app.services.ai_generator import AIGenerator
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageProcessor:
    """Handles image processing and background replacement"""
    
    def __init__(self):
        self.ai_generator = AIGenerator()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.window_detector = self._load_window_detector()
    
    def _load_window_detector(self):
        """Load window detection model (placeholder for now)"""
        # In a real implementation, you'd load a trained model
        # For now, we'll use basic edge detection
        return None
    
    async def process_image(
        self, 
        image_path: str, 
        scene_type: str = "random", 
        custom_prompt: str = ""
    ) -> str:
        """
        Process image to replace background with AI-generated scene
        
        Args:
            image_path: Path to input image
            scene_type: Type of scene to generate
            custom_prompt: Custom scene description
            
        Returns:
            Path to processed image
        """
        start_time = time.time()
        
        try:
            logger.info(f"Processing image: {image_path}")
            
            # Load image
            original_image = cv2.imread(image_path)
            if original_image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Detect windows/backgrounds
            window_regions = self._detect_windows(original_image)
            
            if not window_regions:
                logger.warning("No windows detected, processing entire image")
                window_regions = [(0, 0, original_image.shape[1], original_image.shape[0])]
            
            # Generate replacement background
            background_image = await self._generate_background(
                original_image, scene_type, custom_prompt
            )
            
            # Replace backgrounds
            processed_image = self._replace_backgrounds(
                original_image, background_image, window_regions
            )
            
            # Save processed image
            output_path = self._save_processed_image(processed_image, image_path)
            
            processing_time = time.time() - start_time
            logger.info(f"Image processing completed in {processing_time:.2f}s")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise
    
    def _detect_windows(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect windows in the image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of window regions (x, y, width, height)
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            window_regions = []
            
            for contour in contours:
                # Filter by area
                area = cv2.contourArea(contour)
                if area < 1000:  # Minimum area threshold
                    continue
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter by aspect ratio (windows are usually rectangular)
                aspect_ratio = w / h
                if 0.5 < aspect_ratio < 3.0:
                    window_regions.append((x, y, w, h))
            
            # Merge overlapping regions
            window_regions = self._merge_overlapping_regions(window_regions)
            
            logger.info(f"Detected {len(window_regions)} window regions")
            return window_regions
            
        except Exception as e:
            logger.error(f"Error detecting windows: {e}")
            return []
    
    def _merge_overlapping_regions(self, regions: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
        """Merge overlapping window regions"""
        if not regions:
            return []
        
        # Sort by area (largest first)
        regions = sorted(regions, key=lambda r: r[2] * r[3], reverse=True)
        
        merged = []
        for region in regions:
            x1, y1, w1, h1 = region
            
            # Check if this region overlaps with any existing merged region
            should_merge = False
            for i, (x2, y2, w2, h2) in enumerate(merged):
                # Check overlap
                if (x1 < x2 + w2 and x1 + w1 > x2 and 
                    y1 < y2 + h2 and y1 + h1 > y2):
                    # Merge regions
                    new_x = min(x1, x2)
                    new_y = min(y1, y2)
                    new_w = max(x1 + w1, x2 + w2) - new_x
                    new_h = max(y1 + h1, y2 + h2) - new_y
                    merged[i] = (new_x, new_y, new_w, new_h)
                    should_merge = True
                    break
            
            if not should_merge:
                merged.append(region)
        
        return merged
    
    async def _generate_background(
        self, 
        original_image: np.ndarray, 
        scene_type: str, 
        custom_prompt: str
    ) -> np.ndarray:
        """
        Generate background image using AI
        
        Args:
            original_image: Original image for reference
            scene_type: Type of scene to generate
            custom_prompt: Custom scene description
            
        Returns:
            Generated background image
        """
        try:
            # Get dimensions from original image
            height, width = original_image.shape[:2]
            
            # Generate AI image
            background_path = await self.ai_generator.generate_image(
                scene_type=scene_type,
                custom_prompt=custom_prompt,
                width=width,
                height=height
            )
            
            # Load generated image
            background_image = cv2.imread(background_path)
            if background_image is None:
                raise ValueError(f"Could not load generated background: {background_path}")
            
            # Resize to match original dimensions
            background_image = cv2.resize(background_image, (width, height))
            
            return background_image
            
        except Exception as e:
            logger.error(f"Error generating background: {e}")
            # Fallback to a simple gradient
            return self._create_fallback_background(original_image.shape[:2])
    
    def _create_fallback_background(self, shape: Tuple[int, int]) -> np.ndarray:
        """Create a fallback background if AI generation fails"""
        height, width = shape
        
        # Create a simple gradient background
        background = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create gradient from top to bottom
        for y in range(height):
            ratio = y / height
            color = (
                int(100 + 155 * ratio),  # Blue
                int(150 + 105 * ratio),  # Green
                int(200 + 55 * ratio)    # Red
            )
            background[y, :] = color
        
        return background
    
    def _replace_backgrounds(
        self, 
        original_image: np.ndarray, 
        background_image: np.ndarray, 
        window_regions: List[Tuple[int, int, int, int]]
    ) -> np.ndarray:
        """
        Replace backgrounds in detected window regions
        
        Args:
            original_image: Original image
            background_image: Generated background image
            window_regions: List of window regions to replace
            
        Returns:
            Processed image with replaced backgrounds
        """
        try:
            # Create a copy of the original image
            processed_image = original_image.copy()
            
            for x, y, w, h in window_regions:
                # Extract window region
                window_region = original_image[y:y+h, x:x+w]
                
                # Extract corresponding background region
                bg_region = background_image[y:y+h, x:x+w]
                
                # Create mask for smooth blending
                mask = self._create_blend_mask(window_region)
                
                # Blend the regions
                blended_region = self._blend_regions(window_region, bg_region, mask)
                
                # Replace the region in processed image
                processed_image[y:y+h, x:x+w] = blended_region
            
            return processed_image
            
        except Exception as e:
            logger.error(f"Error replacing backgrounds: {e}")
            return original_image
    
    def _create_blend_mask(self, region: np.ndarray) -> np.ndarray:
        """Create a mask for smooth blending"""
        height, width = region.shape[:2]
        
        # Create a gradient mask
        mask = np.zeros((height, width), dtype=np.float32)
        
        # Create radial gradient from center
        center_y, center_x = height // 2, width // 2
        max_distance = np.sqrt(center_x**2 + center_y**2)
        
        for y in range(height):
            for x in range(width):
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                mask[y, x] = 1.0 - (distance / max_distance)
        
        # Apply Gaussian blur for smoother edges
        mask = cv2.GaussianBlur(mask, (15, 15), 0)
        
        return mask
    
    def _blend_regions(
        self, 
        original_region: np.ndarray, 
        background_region: np.ndarray, 
        mask: np.ndarray
    ) -> np.ndarray:
        """Blend original and background regions using mask"""
        # Normalize mask to 0-1 range
        mask = np.clip(mask, 0, 1)
        
        # Expand mask to 3 channels
        mask_3d = np.stack([mask] * 3, axis=2)
        
        # Blend regions
        blended = (original_region * mask_3d + 
                  background_region * (1 - mask_3d)).astype(np.uint8)
        
        return blended
    
    def _save_processed_image(self, image: np.ndarray, original_path: str) -> str:
        """Save processed image to output directory"""
        try:
            # Generate output filename
            original_name = Path(original_path).stem
            timestamp = int(time.time())
            output_filename = f"{original_name}_geomasked_{timestamp}.jpg"
            output_path = Path(settings.PROCESSED_DIR) / output_filename
            
            # Save image with high quality
            cv2.imwrite(str(output_path), image, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            logger.info(f"Processed image saved: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error saving processed image: {e}")
            raise
    
    def enhance_image(self, image_path: str) -> str:
        """Enhance image quality"""
        try:
            # Load image with PIL for enhancement
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Enhance sharpness
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.2)
                
                # Enhance contrast
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.1)
                
                # Save enhanced image
                enhanced_path = image_path.replace('.jpg', '_enhanced.jpg')
                img.save(enhanced_path, 'JPEG', quality=95)
                
                return enhanced_path
                
        except Exception as e:
            logger.error(f"Error enhancing image: {e}")
            return image_path 