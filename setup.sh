#!/bin/bash

# FastAPI Image Analysis Server - Setup Script
# This script will set up and run the project on your computer

set -e  # Exit on error

echo "=========================================="
echo "FastAPI Image Analysis Server - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check if Tesseract OCR is installed
echo "Checking Tesseract OCR..."
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Tesseract OCR is not installed."
    echo "Installing Tesseract OCR..."
    
    # Detect OS and install Tesseract
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            echo "Detected Debian/Ubuntu system"
            sudo apt-get update
            sudo apt-get install -y tesseract-ocr
        elif command -v yum &> /dev/null; then
            echo "Detected RedHat/CentOS system"
            sudo yum install -y tesseract
        else
            echo "❌ Could not detect package manager. Please install Tesseract OCR manually."
            echo "Visit: https://github.com/tesseract-ocr/tesseract"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Detected macOS"
        if command -v brew &> /dev/null; then
            brew install tesseract
        else
            echo "❌ Homebrew not found. Please install Homebrew first or install Tesseract manually."
            echo "Visit: https://brew.sh/"
            exit 1
        fi
    else
        echo "❌ Unsupported OS. Please install Tesseract OCR manually."
        echo "Visit: https://github.com/tesseract-ocr/tesseract"
        exit 1
    fi
else
    echo "✅ Tesseract OCR is already installed"
fi
echo ""

# Create virtual environment
echo "Creating Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
echo "This may take a few minutes (downloading AI models)..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Check if models need to be downloaded
echo "Checking AI models..."
echo "Note: First run will download ~1GB of AI models"
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the server, run:"
echo "  ./run.sh"
echo ""
echo "Or manually with:"
echo "  source .venv/bin/activate"
echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "The API will be available at:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo "  - Health: http://localhost:8000/health"
echo ""
