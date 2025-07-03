"""
Main FastAPI application for GeoMask
"""

import os
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

from app.config import settings
from app.services.image_processor import ImageProcessor
from app.services.ai_generator import AIGenerator
from app.models.schemas import ProcessRequest, ProcessResponse
from app.utils.file_utils import save_upload_file, cleanup_temp_files
from app.utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="GeoMask",
    description="Protect your privacy from AI-powered GeoGuessr tools",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
for directory in ["uploads", "processed", "output", "temp", "logs"]:
    Path(directory).mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
image_processor = ImageProcessor()
ai_generator = AIGenerator()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting GeoMask application...")
    try:
        await ai_generator.initialize()
        logger.info("AI Generator initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI Generator: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down GeoMask application...")
    cleanup_temp_files()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to GeoMask! 🗺️🕵️‍♂️",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "geomask"}

@app.post("/api/process", response_model=ProcessResponse)
async def process_image(
    file: UploadFile = File(...),
    scene_type: str = Form("random"),
    custom_prompt: str = Form("")
):
    """
    Process an uploaded image to replace background with decoy scene
    """
    try:
        # Validate file
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        if file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"File size must be less than {settings.MAX_FILE_SIZE} bytes"
            )
        
        # Save uploaded file
        file_path = await save_upload_file(file)
        logger.info(f"File uploaded: {file_path}")
        
        # Process image
        processed_path = await image_processor.process_image(
            file_path, 
            scene_type, 
            custom_prompt
        )
        
        # Generate response
        return ProcessResponse(
            success=True,
            original_file=file.filename,
            processed_file=os.path.basename(processed_path),
            download_url=f"/api/download/{os.path.basename(processed_path)}"
        )
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{filename}")
async def download_processed_image(filename: str):
    """Download processed image"""
    file_path = Path("processed") / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="image/jpeg"
    )

@app.get("/api/scenes")
async def get_available_scenes():
    """Get available scene types for background replacement"""
    return {
        "scenes": [
            {"id": "random", "name": "Random Location", "description": "Random city or landscape"},
            {"id": "city", "name": "Cityscape", "description": "Urban city view"},
            {"id": "mountain", "name": "Mountain Village", "description": "Swiss mountain village"},
            {"id": "beach", "name": "Beach", "description": "Tropical beach scene"},
            {"id": "forest", "name": "Forest", "description": "Dense forest view"},
            {"id": "desert", "name": "Desert", "description": "Desert landscape"},
            {"id": "custom", "name": "Custom", "description": "Custom scene description"}
        ]
    }

@app.delete("/api/cleanup")
async def cleanup_files():
    """Clean up temporary files"""
    try:
        cleanup_temp_files()
        return {"message": "Cleanup completed successfully"}
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        raise HTTPException(status_code=500, detail="Cleanup failed")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False
    ) 