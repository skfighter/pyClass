#!/bin/bash

# FastAPI Image Analysis Server - Run Script
# Starts the FastAPI server

set -e  # Exit on error

echo "=========================================="
echo "FastAPI Image Analysis Server"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup first: ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "❌ Dependencies not installed!"
    echo "Please run setup first: ./setup.sh"
    exit 1
fi

echo "✅ Environment ready"
echo ""
echo "Starting FastAPI server..."
echo "----------------------------------------"
echo "Server will be available at:"
echo "  - API: http://localhost:8000"
echo "  - Interactive Docs: http://localhost:8000/docs"
echo "  - Alternative Docs: http://localhost:8000/redoc"
echo "  - Health Check: http://localhost:8000/health"
echo ""
echo "API Endpoints:"
echo "  GET  /                  - Welcome message"
echo "  GET  /health            - Health check"
echo "  GET  /api/info          - API information"
echo "  POST /seeImageAiInfo    - Image analysis with AI + OCR"
echo ""
echo "Note: First startup may take a moment (loading AI models)"
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------"
echo ""

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
