"""
Tests for main application functionality
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "GeoMask" in data["message"]


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "geomask"


def test_get_scenes():
    """Test scenes endpoint"""
    response = client.get("/api/scenes")
    assert response.status_code == 200
    data = response.json()
    assert "scenes" in data
    assert len(data["scenes"]) > 0
    
    # Check if expected scenes are present
    scene_ids = [scene["id"] for scene in data["scenes"]]
    assert "random" in scene_ids
    assert "city" in scene_ids
    assert "mountain" in scene_ids


def test_upload_without_file():
    """Test upload endpoint without file"""
    response = client.post("/api/process")
    assert response.status_code == 422  # Validation error


def test_download_nonexistent_file():
    """Test download of non-existent file"""
    response = client.get("/api/download/nonexistent.jpg")
    assert response.status_code == 404


def test_cleanup_endpoint():
    """Test cleanup endpoint"""
    response = client.delete("/api/cleanup")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data 