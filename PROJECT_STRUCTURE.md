# GeoMask Project Structure

## Overview

GeoMask is a full-stack web application that protects user privacy by replacing identifiable background views in photos with AI-generated decoy scenes.

## Directory Structure

```
GeoMask/
├── 📁 app/                          # Backend Python application
│   ├── __init__.py                  # Package initialization
│   ├── main.py                      # FastAPI application entry point
│   ├── config.py                    # Configuration settings
│   ├── 📁 models/                   # Data models
│   │   ├── __init__.py
│   │   └── schemas.py               # Pydantic schemas
│   ├── 📁 services/                 # Business logic services
│   │   ├── __init__.py
│   │   ├── image_processor.py       # Image processing service
│   │   └── ai_generator.py          # AI image generation service
│   └── 📁 utils/                    # Utility functions
│       ├── __init__.py
│       ├── logger.py                # Logging configuration
│       └── file_utils.py            # File handling utilities
│
├── 📁 frontend/                     # React frontend application
│   ├── package.json                 # Node.js dependencies
│   ├── 📁 public/                   # Static assets
│   │   ├── index.html               # Main HTML file
│   │   └── manifest.json            # Web app manifest
│   └── 📁 src/                      # React source code
│       ├── index.js                 # React entry point
│       ├── index.css                # Global styles
│       ├── App.js                   # Main App component
│       ├── 📁 components/           # Reusable components
│       │   ├── Header.js            # Navigation header
│       │   └── Footer.js            # Footer component
│       └── 📁 pages/                # Page components
│           ├── Home.js              # Landing page
│           ├── Upload.js            # Image upload page
│           └── About.js             # About page
│
├── 📁 docs/                         # Documentation
│   ├── API.md                       # API documentation
│   └── DEPLOYMENT.md                # Deployment guide
│
├── 📁 tests/                        # Test suite
│   ├── __init__.py
│   └── test_main.py                 # API endpoint tests
│
├── 📁 scripts/                      # Utility scripts
│   └── start.sh                     # Development startup script
│
├── 📁 assets/                       # Project assets (images, logos)
│   └── README.md                    # Assets documentation
│
├── 📄 .gitignore                    # Git ignore rules
├── 📄 requirements.txt              # Python dependencies
├── 📄 Dockerfile                    # Docker container configuration
├── 📄 docker-compose.yml            # Multi-container setup
├── 📄 env.example                   # Environment variables template
├── 📄 Makefile                      # Development commands
├── 📄 pytest.ini                    # Test configuration
├── 📄 LICENSE                       # MIT License
└── 📄 README.md                     # Project documentation
```

## Key Components

### Backend (Python/FastAPI)

#### Core Application (`app/main.py`)
- FastAPI application setup
- API endpoints for image processing
- CORS middleware configuration
- Health check endpoints

#### Configuration (`app/config.py`)
- Environment-based settings
- API key management
- File size limits
- AI provider configuration

#### Data Models (`app/models/schemas.py`)
- Pydantic schemas for request/response validation
- ProcessRequest, ProcessResponse models
- Error handling schemas

#### Services

**Image Processor (`app/services/image_processor.py`)**
- Window/background detection
- Image blending and replacement
- OpenCV-based image processing
- Quality enhancement

**AI Generator (`app/services/ai_generator.py`)**
- OpenAI DALL-E integration
- Scene template management
- Fallback image generation
- Multiple AI provider support

#### Utilities

**Logger (`app/utils/logger.py`)**
- Structured logging configuration
- File and console output
- Error tracking

**File Utils (`app/utils/file_utils.py`)**
- File upload validation
- Safe filename generation
- Temporary file cleanup

### Frontend (React)

#### Core Components

**App (`frontend/src/App.js`)**
- Main application component
- Routing configuration
- Global state management

**Header (`frontend/src/components/Header.js`)**
- Navigation menu
- Responsive design
- Mobile menu support

**Footer (`frontend/src/components/Footer.js`)**
- Project information
- Social links
- Copyright notice

#### Pages

**Home (`frontend/src/pages/Home.js`)**
- Landing page with features
- Hero section
- How it works explanation

**Upload (`frontend/src/pages/Upload.js`)**
- Drag-and-drop file upload
- Scene selection interface
- Processing status display
- Download functionality

**About (`frontend/src/pages/About.js`)**
- Project information
- Technology stack
- Team details

## Configuration Files

### Environment (`env.example`)
- API keys configuration
- Development/production settings
- File size limits
- AI provider selection

### Docker (`Dockerfile`, `docker-compose.yml`)
- Container configuration
- Multi-service setup
- Volume mounting
- Health checks

### Development (`Makefile`, `scripts/start.sh`)
- Development commands
- Automated setup
- Testing and linting
- Deployment helpers

## Data Flow

1. **Upload**: User uploads image via React frontend
2. **Validation**: Backend validates file type, size, and format
3. **Processing**: Image processor detects windows/backgrounds
4. **AI Generation**: AI service creates replacement background
5. **Blending**: Original image is blended with new background
6. **Output**: Processed image is saved and download link provided

## Security Features

- File type validation
- Size limits enforcement
- Secure file handling
- Temporary file cleanup
- Rate limiting
- CORS configuration

## Testing

- Unit tests for API endpoints
- Integration tests for image processing
- Frontend component testing
- End-to-end workflow testing

## Deployment

### Development
```bash
./scripts/start.sh
```

### Production
```bash
docker-compose up -d
```

### Manual Setup
```bash
make install
make run-backend  # Terminal 1
make run-frontend # Terminal 2
```

## File Organization Principles

1. **Separation of Concerns**: Backend and frontend are completely separate
2. **Modular Design**: Services are independent and testable
3. **Configuration Management**: Environment-based settings
4. **Documentation**: Comprehensive docs for all components
5. **Testing**: Tests alongside implementation
6. **Security**: Input validation and secure file handling
7. **Scalability**: Docker-ready for easy deployment 