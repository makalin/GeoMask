#!/bin/bash

# GeoMask Startup Script
# This script helps you start the GeoMask application

set -e

echo "🚀 Starting GeoMask..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed (for frontend)
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js is not installed. Frontend will not be available."
    echo "   Install Node.js to run the frontend: https://nodejs.org/"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads processed output temp logs

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp env.example .env
    echo "📝 Please edit .env file with your API keys and settings."
    echo "   Required: OPENAI_API_KEY"
fi

# Start backend
echo "🔧 Starting backend server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend if Node.js is available
if command -v node &> /dev/null; then
    echo "🎨 Starting frontend..."
    cd frontend
    
    # Install frontend dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "📥 Installing frontend dependencies..."
        npm install
    fi
    
    # Start frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    echo "✅ Frontend is running on http://localhost:3000"
else
    echo "⚠️  Frontend not started (Node.js not available)"
fi

echo ""
echo "🎉 GeoMask is running!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping GeoMask..."
    kill $BACKEND_PID 2>/dev/null || true
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo "✅ GeoMask stopped"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Wait for background processes
wait 