# Development Guide

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- Code editor (VS Code recommended)

### First Time Setup
```bash
# Clone repository
git clone <your-repo-url>
cd pyClass

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source .venv/bin/activate
```

### Starting Development Server
```bash
# Option 1: Using run script
./run.sh

# Option 2: Direct uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Project Structure

```
pyClass/
├── main.py                 # FastAPI app & routes
├── config.py              # Settings & configuration
├── models/
│   ├── __init__.py
│   └── responses.py       # Pydantic response models
├── services/
│   ├── __init__.py
│   └── image_service.py   # Business logic
├── requirements.txt       # Dependencies
├── .env.example          # Config template
├── .env                  # Your local config (git-ignored)
└── tests/                # Tests (to be added)
```

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key settings:
- `HOST` - Server bind address
- `PORT` - Server port
- `LOG_LEVEL` - DEBUG, INFO, WARNING, ERROR
- `MAX_FILE_SIZE_MB` - Upload size limit
- `MODEL_NAME` - AI model to use

## Making Changes

### Adding a New Endpoint

1. **Add route in `main.py`:**
```python
@app.get("/my-endpoint", tags=["Custom"])
async def my_endpoint() -> MyResponse:
    """Endpoint description"""
    return MyResponse(data="example")
```

2. **Create response model in `models/responses.py`:**
```python
class MyResponse(BaseModel):
    data: str
    
    class Config:
        json_schema_extra = {"example": {"data": "example"}}
```

3. **Test at:** `http://localhost:8000/docs`

### Adding Service Logic

1. **Create method in `services/image_service.py`:**
```python
async def new_feature(self, input_data):
    """New feature logic"""
    try:
        # Implementation
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

2. **Call from endpoint:**
```python
result = await image_service.new_feature(data)
```

### Adding Configuration

1. **Add to `config.py`:**
```python
class Settings(BaseSettings):
    new_setting: str = "default_value"
```

2. **Add to `.env.example`:**
```
NEW_SETTING=default_value
```

3. **Use in code:**
```python
from config import settings
value = settings.new_setting
```

## Code Style

### Python Standards
- Follow PEP 8
- Use type hints everywhere
- Write docstrings for functions/classes
- Keep functions small and focused

### Example Function
```python
async def process_data(
    input_data: str,
    options: Optional[Dict[str, Any]] = None
) -> ProcessedData:
    """
    Process input data with optional configuration.
    
    Args:
        input_data: Raw data to process
        options: Processing options
    
    Returns:
        ProcessedData object with results
    
    Raises:
        ValueError: If input_data is invalid
    """
    logger.info(f"Processing data: {len(input_data)} bytes")
    
    try:
        # Processing logic
        result = do_processing(input_data, options)
        return ProcessedData(result=result)
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise
```

## Logging

### Log Levels
```python
logger.debug("Detailed debug info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)
```

### Best Practices
- Use INFO for important events
- Use DEBUG for detailed tracing
- Use ERROR for exceptions
- Include context in messages
- Don't log sensitive data

## Error Handling

### HTTP Status Codes
```python
# 400 - Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input"
)

# 404 - Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)

# 500 - Internal Server Error
raise HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Processing failed"
)

# 503 - Service Unavailable
raise HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Service temporarily unavailable"
)
```

### Exception Handling Pattern
```python
try:
    # Main logic
    result = await service.process(data)
    return result
except HTTPException:
    # Re-raise HTTP exceptions
    raise
except ValueError as e:
    # Handle specific exceptions
    logger.error(f"Validation error: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    # Catch-all for unexpected errors
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal error")
```

## Testing

### Running Tests (when added)
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_api.py::test_health_check
```

### Writing Tests
```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
```

## Debugging

### VS Code Debug Configuration
Add to `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--reload",
                "--host", "0.0.0.0",
                "--port", "8000"
            ],
            "jinja": true
        }
    ]
}
```

### Debug Tips
1. Set breakpoints in VS Code
2. Use `logger.debug()` for tracing
3. Check logs in terminal
4. Use `/docs` to test endpoints
5. Monitor with `/health` endpoint

## Common Tasks

### Update Dependencies
```bash
# Update requirements.txt
pip freeze > requirements.txt

# Install updated deps
pip install -r requirements.txt
```

### Add New Dependency
```bash
# Install package
pip install new-package

# Add to requirements.txt
pip freeze | grep new-package >> requirements.txt
```

### Check Code Quality
```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy .

# Sort imports
isort .
```

### Database Migrations (if adding database)
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Deployment

### Production Checklist
- [ ] Set `RELOAD=false` in .env
- [ ] Set `LOG_LEVEL=INFO` or `WARNING`
- [ ] Configure CORS properly
- [ ] Set up HTTPS/TLS
- [ ] Use production WSGI server (e.g., Gunicorn)
- [ ] Set up monitoring
- [ ] Configure backup strategy
- [ ] Document deployment process

### Docker Deployment (to be added)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Server Won't Start
```bash
# Check if port is in use
lsof -i :8000

# Kill process
pkill -f uvicorn

# Check Python version
python --version

# Verify virtual environment
which python
```

### Import Errors
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
echo $PYTHONPATH
```

### Model Loading Fails
```bash
# Check disk space
df -h

# Check internet connection (first time)
ping huggingface.co

# Clear cache and retry
rm -rf ~/.cache/huggingface
```

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Uvicorn Docs](https://www.uvicorn.org/)

### Tools
- [Swagger UI](http://localhost:8000/docs) - Interactive API docs
- [ReDoc](http://localhost:8000/redoc) - Alternative API docs
- [Postman](https://www.postman.com/) - API testing

### Community
- FastAPI Discord
- Stack Overflow
- GitHub Issues

## Git Workflow

### Feature Development
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
# ... edit files ...

# Commit
git add .
git commit -m "Add new feature"

# Push
git push origin feature/my-feature

# Create pull request on GitHub
```

### Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat: Add image batch processing endpoint

- Add new endpoint for processing multiple images
- Update documentation
- Add response model

Closes #123
```

## Performance Tips

1. **Use async/await** for I/O operations
2. **Cache model results** if appropriate
3. **Limit concurrent requests** with semaphores
4. **Use GPU** if available
5. **Monitor memory** usage
6. **Profile** slow endpoints
7. **Optimize** image loading

## Security Best Practices

1. **Validate all inputs**
2. **Sanitize file uploads**
3. **Use HTTPS in production**
4. **Keep dependencies updated**
5. **Don't log secrets**
6. **Use environment variables**
7. **Implement rate limiting**
8. **Add authentication** for production

## Getting Help

1. Check this guide
2. Read the code comments
3. Check logs
4. Search GitHub issues
5. Ask in team chat
6. Create GitHub issue

---

Happy coding! 🚀
