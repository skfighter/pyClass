# PyClass API# FastAPI Image Analysis Server# pyClass



A powerful, production-ready FastAPI server that provides AI-powered image analysis and OCR (Optical Character Recognition) capabilities.This is for python invasion.



## ✨ FeaturesA powerful FastAPI-based REST API that provides AI-powered image analysis and OCR (Optical Character Recognition) capabilities.



- 🖼️ **AI Image Description** - Automatically describes image content using the BLIP AI model

- 📝 **OCR Text Extraction** - Extracts text from images using Tesseract OCR

- 🎨 **Black & White Conversion** - Convert images to black and white (grayscale)

- 🚀 **Fast & Modern** - Built with FastAPI for high performance and async support

- 🔄 **Auto-reload** - Development server with hot reload

- 📚 **Interactive API Docs** - Automatic OpenAPI/Swagger documentationA basic Python API server built with FastAPI.

- 🐳 **Easy Setup** - Automated setup script for first-time installation

- 🏗️ **Industrial Code Quality** - Proper separation of concerns, logging, validation, and error handling- 🖼️ **AI Image Description** - Automatically describes what's in an image using the BLIP AI model

- ⚙️ **Configuration Management** - Environment-based configuration with Pydantic

- 🛡️ **Input Validation** - File size limits and type checking- 📝 **OCR Text Extraction** - Extracts text from images using Tesseract OCR### Features

- 📊 **Structured Logging** - Comprehensive logging for debugging and monitoring

- 🚀 **Fast & Modern** - Built with FastAPI for high performance

## 🛠️ Tech Stack

- 🔄 **Auto-reload** - Development server with hot reload- Simple REST API endpoints

- **FastAPI** - Modern, high-performance Python web framework

- **BLIP** - Salesforce's AI model for image captioning- 📚 **Interactive API Docs** - Automatic OpenAPI/Swagger documentation- Health check endpoint

- **Tesseract OCR** - Industry-standard OCR engine

- **PyTorch** - Deep learning framework- 🐳 **Easy Setup** - Simple automated setup script- API information endpoint

- **Transformers** - Hugging Face models library

- **Pillow** - Image processing library- Auto-generated interactive API documentation (Swagger UI)

- **Pydantic** - Data validation and settings management

## Tech Stack

## 📁 Project Structure

### Installation

```

pyClass/- **FastAPI** - Modern Python web framework

├── main.py                 # FastAPI application entry point

├── config.py              # Configuration management with Pydantic- **BLIP** - Salesforce's AI model for image captioning1. Install dependencies:

├── models/

│   ├── __init__.py- **Tesseract OCR** - Industry-standard OCR engine```bash

│   └── responses.py       # Pydantic response models

├── services/- **PyTorch** - Deep learning frameworkpip install -r requirements.txt

│   ├── __init__.py

│   └── image_service.py   # Image analysis and OCR service- **Transformers** - Hugging Face models library```

├── requirements.txt       # Python dependencies

├── setup.sh              # Automated setup script- **Pillow** - Image processing

├── run.sh                # Server startup script

├── .env.example          # Environment variables template### Running the Server

└── README.md             # This file

```## Prerequisites



## 📋 PrerequisitesStart the development server:



- Python 3.8 or higher- Python 3.8 or higher```bash

- pip (Python package manager)

- Tesseract OCR (installed at system level)- pip (Python package manager)uvicorn main:app --reload



## 🚀 Quick Start- Tesseract OCR (automatically installed by setup script on Linux/Mac)```



### Option 1: Automated Setup (Recommended)



```bash## Quick StartThe server will start on `http://127.0.0.1:8000`

# 1. Clone the repository

git clone <your-repo-url>

cd pyClass

### 1. Clone the repository### API Endpoints

# 2. Run the setup script

chmod +x setup.sh```bash

./setup.sh

git clone <your-repo-url>- `GET /` - Welcome message

# 3. Start the server

chmod +x run.shcd pyClass- `GET /health` - Health check

./run.sh

``````- `GET /api/info` - API information



The setup script will:

- ✅ Check Python installation

- ✅ Install Tesseract OCR (if needed)### 2. Run setup script### API Documentation

- ✅ Create a virtual environment

- ✅ Install all Python dependencies```bash

- ✅ Download AI models (~1GB on first run)

chmod +x setup.shOnce the server is running, you can access:

### Option 2: Manual Setup

./setup.sh- Swagger UI: `http://127.0.0.1:8000/docs`

```bash

# 1. Create virtual environment```- ReDoc: `http://127.0.0.1:8000/redoc`

python3 -m venv .venv

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

This will:

# 2. Install Tesseract OCR- Check Python installation

# Ubuntu/Debian:- Install Tesseract OCR (if needed)

sudo apt-get install tesseract-ocr- Create a virtual environment

- Install all Python dependencies

# macOS:- Download AI models (~1GB on first run)

brew install tesseract

### 3. Start the server

# Windows:```bash

# Download from https://github.com/tesseract-ocr/tesseractchmod +x run.sh

./run.sh

# 3. Install Python dependencies```

pip install -r requirements.txt

The server will start at `http://localhost:8000`

# 4. Run the server

uvicorn main:app --reload --host 0.0.0.0 --port 8000## API Endpoints

```

### GET `/`

The server will start at `http://localhost:8000`Welcome endpoint



## ⚙️ Configuration**Response:**

```json

Create a `.env` file in the project root (copy from `.env.example`):{

  "message": "Welcome to PyClass API",

```bash  "status": "running"

# Server Configuration}

HOST=0.0.0.0```

PORT=8000

RELOAD=true### GET `/health`

Health check endpoint

# AI Model Configuration

MODEL_NAME=Salesforce/blip-image-captioning-base**Response:**

MAX_CAPTION_LENGTH=50```json

{

# File Upload Limits  "status": "healthy"

MAX_FILE_SIZE_MB=10}

ALLOWED_EXTENSIONS=.jpg,.jpeg,.png,.webp,.gif,.bmp```



# Logging### GET `/api/info`

LOG_LEVEL=INFOAPI information



# API Metadata**Response:**

API_TITLE=PyClass API```json

API_VERSION=1.0.0{

API_DESCRIPTION=AI-powered image analysis and OCR API  "name": "PyClass API",

```  "version": "1.0.0",

  "description": "A basic Python API server using FastAPI"

## 📡 API Endpoints}

```

### `GET /`

Welcome endpoint### POST `/seeImageAiInfo`

Analyze an image with AI and extract text

**Response:**

```json**Request:**

{- Method: POST

  "message": "Welcome to PyClass API",- Content-Type: multipart/form-data

  "status": "running",- Body: file (image file - JPG, PNG, WEBP, etc.)

  "version": "1.0.0"

}**Response:**

``````json

{

### `GET /health`  "success": true,

Health check endpoint  "filename": "example.jpg",

  "description": "a cat sitting on a wooden table",

**Response:**  "extracted_text": "Hello World! Some text from the image",

```json  "has_text": true,

{  "image_info": {

  "status": "healthy",    "width": 1024,

  "models_loaded": true    "height": 768,

}    "format": "JPEG",

```    "mode": "RGB",

    "size_bytes": 245760

### `GET /api/info`  }

API information}

```

**Response:**

```json## Usage Examples

{

  "name": "PyClass API",### Using cURL

  "version": "1.0.0",```bash

  "description": "AI-powered image analysis and OCR API",curl -X POST "http://localhost:8000/seeImageAiInfo" \

  "endpoints": {  -H "accept: application/json" \

    "GET /": "Welcome message",  -H "Content-Type: multipart/form-data" \

    "GET /health": "Health check",  -F "file=@/path/to/your/image.jpg"

    "GET /api/info": "API information",```

    "POST /seeImageAiInfo": "Image analysis with AI and OCR"

  }### Using Python requests

}```python

```import requests



### `POST /seeImageAiInfo`url = "http://localhost:8000/seeImageAiInfo"

Analyze an image with AI and extract textfiles = {"file": open("image.jpg", "rb")}

response = requests.post(url, files=files)

**Request:**print(response.json())

- Method: POST```

- Content-Type: multipart/form-data

- Body: file (image file - JPG, PNG, WEBP, GIF, BMP)### Using the Interactive Docs

- Max file size: 10MB (configurable)1. Navigate to `http://localhost:8000/docs`

2. Click on the `/seeImageAiInfo` endpoint

**Response:**3. Click "Try it out"

```json4. Upload an image file

{5. Click "Execute"

  "success": true,6. See the results!

  "description": "a cat sitting on a wooden table",

  "extracted_text": "Hello World\nSome text from the image",## Development

  "has_text": true,

  "filename": "example.jpg"### Manual Setup (without setup.sh)

}

```1. Create virtual environment:

```bash

## 💻 Usage Examplespython3 -m venv .venv

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

### Using cURL```

```bash

curl -X POST "http://localhost:8000/seeImageAiInfo" \2. Install Tesseract OCR:

  -H "accept: application/json" \- **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`

  -H "Content-Type: multipart/form-data" \- **macOS:** `brew install tesseract`

  -F "file=@/path/to/your/image.jpg"- **Windows:** Download from [GitHub releases](https://github.com/tesseract-ocr/tesseract)

```

3. Install dependencies:

### Using Python requests```bash

```pythonpip install -r requirements.txt

import requests```



url = "http://localhost:8000/seeImageAiInfo"4. Run the server:

files = {"file": open("image.jpg", "rb")}```bash

response = requests.post(url, files=files)uvicorn main:app --reload --host 0.0.0.0 --port 8000

print(response.json())```

```

### Project Structure

### Using the Interactive Docs```

1. Navigate to `http://localhost:8000/docs`pyClass/

2. Click on the `/seeImageAiInfo` endpoint├── main.py              # FastAPI application

3. Click "Try it out"├── requirements.txt     # Python dependencies

4. Upload an image file├── setup.sh            # Automated setup script

5. Click "Execute"├── run.sh              # Server run script

6. See the results!├── README.md           # This file

└── .venv/              # Virtual environment (created by setup)

**Alternative:** ReDoc documentation at `http://localhost:8000/redoc````



## 🏗️ Architecture## Configuration



### Service Layer Pattern### Changing the Port

The application follows a clean architecture with separation of concerns:Edit `run.sh` and change the port number:

```bash

- **`main.py`** - API layer, handles HTTP requests/responsesuvicorn main:app --reload --host 0.0.0.0 --port 8080

- **`services/image_service.py`** - Business logic for image analysis```

- **`models/responses.py`** - Pydantic models for type-safe responses

- **`config.py`** - Centralized configuration management### GPU Support

To use GPU for faster AI processing, ensure you have CUDA installed and modify the model loading in `main.py`.

### Lifespan Management

Uses FastAPI's lifespan context manager for proper startup/shutdown:## Troubleshooting

- Loads AI models once at startup

- Graceful shutdown handling### "Tesseract not found" error

- Resource cleanupMake sure Tesseract OCR is installed:

```bash

### Error Handlingtesseract --version

- Comprehensive error handling at all levels```

- Proper HTTP status codes (400, 500, 503)If not installed, run the setup script again or install manually.

- Detailed error messages for debugging

- Structured logging with context### "AI model not available" error

The server is still loading AI models. Wait a few seconds and try again.

## 🔍 Development

### Port already in use

### Running TestsChange the port in `run.sh` or kill the existing process:

```bash```bash

# Activate virtual environmentlsof -ti:8000 | xargs kill -9

source .venv/bin/activate```



# Run with pytest (add tests in tests/ directory)## Performance Notes

pytest

```- **First startup:** Downloads ~1GB of AI models (one-time)

- **Subsequent startups:** Models are cached locally

### Changing Configuration- **Image processing:** 1-3 seconds per image depending on size

Edit `.env` file or use environment variables:- **OCR processing:** Additional 0.5-2 seconds for text extraction

```bash

export PORT=8080## License

export LOG_LEVEL=DEBUG

./run.sh[Your License Here]

```

## Contributing

### GPU Support

To use GPU for faster AI processing:Contributions are welcome! Please feel free to submit a Pull Request.

1. Install CUDA-enabled PyTorch

2. The code automatically detects and uses GPU if available## Support



## 🐛 TroubleshootingFor issues and questions, please open an issue on GitHub.


### "Tesseract not found" error
```bash
# Check if Tesseract is installed
tesseract --version

# If not installed, run setup script or install manually
sudo apt-get install tesseract-ocr  # Ubuntu/Debian
brew install tesseract              # macOS
```

### "AI model not available" error
The server is still loading AI models. Wait 10-15 seconds after startup and try again.

### Port already in use
```bash
# Kill existing process
pkill -f uvicorn

# Or change port in .env file
PORT=8080
```

### Import errors
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## 📊 Performance Notes

- **First startup:** Downloads ~1GB of AI models (one-time)
- **Subsequent startups:** Models are cached locally (~10 seconds)
- **Image processing:** 1-3 seconds per image depending on size
- **OCR processing:** Additional 0.5-2 seconds for text extraction
- **CPU mode:** Default, works on all systems
- **GPU mode:** 5-10x faster if CUDA is available

## 🔒 Security Considerations

- File type validation prevents non-image uploads
- File size limits prevent DoS attacks
- CORS middleware enabled (configure for production)
- No sensitive data logged
- Environment variables for configuration

## 📝 License

[Your License Here]

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ using FastAPI and AI**
