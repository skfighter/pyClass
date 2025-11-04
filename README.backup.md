# FastAPI Image Analysis Server# pyClass

This is for python invasion.

A powerful FastAPI-based REST API that provides AI-powered image analysis and OCR (Optical Character Recognition) capabilities.

## FastAPI Server

## Features

A basic Python API server built with FastAPI.

- 🖼️ **AI Image Description** - Automatically describes what's in an image using the BLIP AI model

- 📝 **OCR Text Extraction** - Extracts text from images using Tesseract OCR### Features

- 🚀 **Fast & Modern** - Built with FastAPI for high performance

- 🔄 **Auto-reload** - Development server with hot reload- Simple REST API endpoints

- 📚 **Interactive API Docs** - Automatic OpenAPI/Swagger documentation- Health check endpoint

- 🐳 **Easy Setup** - Simple automated setup script- API information endpoint

- Auto-generated interactive API documentation (Swagger UI)

## Tech Stack

### Installation

- **FastAPI** - Modern Python web framework

- **BLIP** - Salesforce's AI model for image captioning1. Install dependencies:

- **Tesseract OCR** - Industry-standard OCR engine```bash

- **PyTorch** - Deep learning frameworkpip install -r requirements.txt

- **Transformers** - Hugging Face models library```

- **Pillow** - Image processing

### Running the Server

## Prerequisites

Start the development server:

- Python 3.8 or higher```bash

- pip (Python package manager)uvicorn main:app --reload

- Tesseract OCR (automatically installed by setup script on Linux/Mac)```



## Quick StartThe server will start on `http://127.0.0.1:8000`



### 1. Clone the repository### API Endpoints

```bash

git clone <your-repo-url>- `GET /` - Welcome message

cd pyClass- `GET /health` - Health check

```- `GET /api/info` - API information



### 2. Run setup script### API Documentation

```bash

chmod +x setup.shOnce the server is running, you can access:

./setup.sh- Swagger UI: `http://127.0.0.1:8000/docs`

```- ReDoc: `http://127.0.0.1:8000/redoc`


This will:
- Check Python installation
- Install Tesseract OCR (if needed)
- Create a virtual environment
- Install all Python dependencies
- Download AI models (~1GB on first run)

### 3. Start the server
```bash
chmod +x run.sh
./run.sh
```

The server will start at `http://localhost:8000`

## API Endpoints

### GET `/`
Welcome endpoint

**Response:**
```json
{
  "message": "Welcome to PyClass API",
  "status": "running"
}
```

### GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy"
}
```

### GET `/api/info`
API information

**Response:**
```json
{
  "name": "PyClass API",
  "version": "1.0.0",
  "description": "A basic Python API server using FastAPI"
}
```

### POST `/seeImageAiInfo`
Analyze an image with AI and extract text

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (image file - JPG, PNG, WEBP, etc.)

**Response:**
```json
{
  "success": true,
  "filename": "example.jpg",
  "description": "a cat sitting on a wooden table",
  "extracted_text": "Hello World! Some text from the image",
  "has_text": true,
  "image_info": {
    "width": 1024,
    "height": 768,
    "format": "JPEG",
    "mode": "RGB",
    "size_bytes": 245760
  }
}
```

## Usage Examples

### Using cURL
```bash
curl -X POST "http://localhost:8000/seeImageAiInfo" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.jpg"
```

### Using Python requests
```python
import requests

url = "http://localhost:8000/seeImageAiInfo"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Using the Interactive Docs
1. Navigate to `http://localhost:8000/docs`
2. Click on the `/seeImageAiInfo` endpoint
3. Click "Try it out"
4. Upload an image file
5. Click "Execute"
6. See the results!

## Development

### Manual Setup (without setup.sh)

1. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install Tesseract OCR:
- **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
- **macOS:** `brew install tesseract`
- **Windows:** Download from [GitHub releases](https://github.com/tesseract-ocr/tesseract)

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Project Structure
```
pyClass/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── setup.sh            # Automated setup script
├── run.sh              # Server run script
├── README.md           # This file
└── .venv/              # Virtual environment (created by setup)
```

## Configuration

### Changing the Port
Edit `run.sh` and change the port number:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### GPU Support
To use GPU for faster AI processing, ensure you have CUDA installed and modify the model loading in `main.py`.

## Troubleshooting

### "Tesseract not found" error
Make sure Tesseract OCR is installed:
```bash
tesseract --version
```
If not installed, run the setup script again or install manually.

### "AI model not available" error
The server is still loading AI models. Wait a few seconds and try again.

### Port already in use
Change the port in `run.sh` or kill the existing process:
```bash
lsof -ti:8000 | xargs kill -9
```

## Performance Notes

- **First startup:** Downloads ~1GB of AI models (one-time)
- **Subsequent startups:** Models are cached locally
- **Image processing:** 1-3 seconds per image depending on size
- **OCR processing:** Additional 0.5-2 seconds for text extraction

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
