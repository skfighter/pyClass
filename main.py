"""
Basic FastAPI Server
A simple API server demonstrating FastAPI capabilities
"""

from fastapi import FastAPI
from typing import Dict

app = FastAPI(
    title="PyClass API",
    description="A basic Python API server using FastAPI",
    version="1.0.0"
)


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint that returns a welcome message
    """
    return {
        "message": "Welcome to PyClass API",
        "status": "running"
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint
    """
    return {
        "status": "healthy"
    }


@app.get("/api/info")
async def api_info() -> Dict[str, str]:
    """
    API information endpoint
    """
    return {
        "name": "PyClass API",
        "version": "1.0.0",
        "description": "A basic Python API server using FastAPI"
    }
