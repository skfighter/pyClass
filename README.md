# pyClass
This is for python invasion.

## FastAPI Server

A basic Python API server built with FastAPI.

### Features

- Simple REST API endpoints
- Health check endpoint
- API information endpoint
- Auto-generated interactive API documentation (Swagger UI)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server

Start the development server:
```bash
uvicorn main:app --reload
```

The server will start on `http://127.0.0.1:8000`

### API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/info` - API information

### API Documentation

Once the server is running, you can access:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
