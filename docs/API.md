# GeoMask API Documentation

## Overview

The GeoMask API provides endpoints for processing images to replace identifiable background views with AI-generated decoy scenes.

## Base URL

- Development: `http://localhost:8000`

## Authentication

Currently, the API does not require authentication. However, rate limiting is applied to prevent abuse.

## Endpoints

### Health Check

**GET** `/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "geomask"
}
```

### Root

**GET** `/`

Get basic information about the service.

**Response:**
```json
{
  "message": "Welcome to GeoMask! 🗺️🕵️‍♂️",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### Get Available Scenes

**GET** `/api/scenes`

Get list of available scene types for background replacement.

**Response:**
```json
{
  "scenes": [
    {
      "id": "random",
      "name": "Random Location",
      "description": "Random city or landscape"
    },
    {
      "id": "city",
      "name": "Cityscape",
      "description": "Urban city view"
    },
    {
      "id": "mountain",
      "name": "Mountain Village",
      "description": "Swiss mountain village"
    },
    {
      "id": "beach",
      "name": "Beach",
      "description": "Tropical beach scene"
    },
    {
      "id": "forest",
      "name": "Forest",
      "description": "Dense forest view"
    },
    {
      "id": "desert",
      "name": "Desert",
      "description": "Desert landscape"
    },
    {
      "id": "custom",
      "name": "Custom",
      "description": "Custom scene description"
    }
  ]
}
```

### Process Image

**POST** `/api/process`

Upload and process an image to replace background with decoy scene.

**Form Data:**
- `file` (required): Image file (JPEG, PNG, GIF, BMP, TIFF, WebP)
- `scene_type` (optional): Scene type (default: "random")
- `custom_prompt` (optional): Custom scene description (required if scene_type is "custom")

**File Requirements:**
- Maximum size: 10MB
- Supported formats: JPEG, PNG, GIF, BMP, TIFF, WebP
- Must be a valid image file

**Response:**
```json
{
  "success": true,
  "original_file": "photo.jpg",
  "processed_file": "photo_geomasked_1234567890.jpg",
  "download_url": "/api/download/photo_geomasked_1234567890.jpg",
  "processing_time": 15.2
}
```

**Error Response:**
```json
{
  "detail": "File must be an image"
}
```

### Download Processed Image

**GET** `/api/download/{filename}`

Download a processed image.

**Parameters:**
- `filename` (required): Name of the processed file

**Response:**
- File download (image/jpeg)

**Error Response:**
```json
{
  "detail": "File not found"
}
```

### Cleanup Files

**DELETE** `/api/cleanup`

Clean up temporary files.

**Response:**
```json
{
  "message": "Cleanup completed successfully"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input data |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

## Rate Limiting

- **Rate Limit:** 10 requests per minute per IP
- **Headers:** Rate limit information is included in response headers

## File Processing

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

### Processing Steps
1. **Upload Validation:** Check file type, size, and format
2. **Window Detection:** Automatically detect windows/backgrounds in the image
3. **AI Generation:** Generate replacement background using AI
4. **Background Replacement:** Blend the new background with the original image
5. **Output:** Save processed image and provide download link

### Scene Types

#### Random
AI chooses a random scene from various options (city, mountain, beach, forest, desert).

#### City
Urban cityscape with modern architecture and skyscrapers.

#### Mountain
Swiss mountain village with alpine scenery and snow-capped peaks.

#### Beach
Tropical beach scene with palm trees and turquoise water.

#### Forest
Dense forest view with green trees and natural lighting.

#### Desert
Desert landscape with sand dunes and clear blue sky.

#### Custom
User-provided description of the desired scene.

## Examples

### cURL Example

```bash
# Process an image with random scene
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@photo.jpg" \
  -F "scene_type=random"

# Process an image with custom scene
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@photo.jpg" \
  -F "scene_type=custom" \
  -F "custom_prompt=A cozy coffee shop in Paris with Eiffel Tower view"
```

### Python Example

```python
import requests

# Process image
with open('photo.jpg', 'rb') as f:
    files = {'file': f}
    data = {
        'scene_type': 'mountain',
        'custom_prompt': ''
    }
    response = requests.post('http://localhost:8000/api/process', 
                           files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print(f"Processed file: {result['processed_file']}")
    print(f"Download URL: {result['download_url']}")
else:
    print(f"Error: {response.json()['detail']}")
```

### JavaScript Example

```javascript
// Process image
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('scene_type', 'beach');

fetch('/api/process', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('Download URL:', data.download_url);
    window.open(data.download_url, '_blank');
  }
})
.catch(error => console.error('Error:', error));
```

## Configuration

The API behavior can be configured using environment variables:

- `OPENAI_API_KEY`: OpenAI API key for AI image generation
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 10MB)
- `AI_PROVIDER`: AI provider to use (openai, stability, local, fallback)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

## Support

For API support and questions:
- GitHub Issues: https://github.com/makalin/GeoMask/issues
