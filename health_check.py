#!/usr/bin/env python3
"""
Health check script for PyClass API
Tests basic functionality and dependencies
"""

import sys
import importlib
from typing import List, Tuple


def check_imports() -> List[Tuple[str, bool, str]]:
    """Check if all required packages can be imported"""
    required_packages = [
        ("fastapi", "FastAPI framework"),
        ("uvicorn", "ASGI server"),
        ("torch", "PyTorch for AI models"),
        ("transformers", "Hugging Face transformers"),
        ("PIL", "Pillow for image processing"),
        ("pytesseract", "Tesseract OCR"),
        ("ultralytics", "YOLOv8 for object detection"),
        ("whisper", "OpenAI Whisper for audio transcription"),
        ("librosa", "Audio processing library"),
        ("pydantic", "Data validation"),
        ("jinja2", "Template engine"),
    ]
    
    results = []
    for package, description in required_packages:
        try:
            importlib.import_module(package)
            results.append((package, True, description))
        except ImportError as e:
            results.append((package, False, f"{description} - ERROR: {e}"))
    
    return results


def check_services() -> List[Tuple[str, bool, str]]:
    """Check if services can be imported and initialized"""
    services = []
    
    try:
        from services.image_service import ImageAnalysisService
        services.append(("ImageAnalysisService", True, "Image analysis and OCR"))
    except Exception as e:
        services.append(("ImageAnalysisService", False, f"ERROR: {e}"))
    
    try:
        from services.human_detection_service import HumanDetectionService
        services.append(("HumanDetectionService", True, "Human detection with YOLO"))
    except Exception as e:
        services.append(("HumanDetectionService", False, f"ERROR: {e}"))
    
    try:
        from services.audio_service import AudioTranscriptionService
        services.append(("AudioTranscriptionService", True, "Audio transcription with Whisper"))
    except Exception as e:
        services.append(("AudioTranscriptionService", False, f"ERROR: {e}"))
    
    return services


def check_config() -> bool:
    """Check if configuration loads correctly"""
    try:
        from config import settings
        required_attrs = ['host', 'port', 'api_title', 'api_version']
        for attr in required_attrs:
            if not hasattr(settings, attr):
                print(f"❌ Missing config attribute: {attr}")
                return False
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False


def main():
    """Run all health checks"""
    print("=" * 60)
    print("PyClass API Health Check")
    print("=" * 60)
    
    # Check imports
    print("\n📦 Checking package imports...")
    import_results = check_imports()
    import_success = all(success for _, success, _ in import_results)
    
    for package, success, description in import_results:
        status = "✅" if success else "❌"
        print(f"{status} {package:20s} - {description}")
    
    # Check configuration
    print("\n⚙️  Checking configuration...")
    config_success = check_config()
    status = "✅" if config_success else "❌"
    print(f"{status} Configuration loaded")
    
    # Check services
    print("\n🔧 Checking services...")
    service_results = check_services()
    service_success = all(success for _, success, _ in service_results)
    
    for service, success, description in service_results:
        status = "✅" if success else "❌"
        print(f"{status} {service:30s} - {description}")
    
    # Check main application
    print("\n🚀 Checking main application...")
    try:
        from main import app
        print("✅ Main application loads successfully")
        main_success = True
    except Exception as e:
        print(f"❌ Main application error: {e}")
        main_success = False
    
    # Summary
    print("\n" + "=" * 60)
    all_success = import_success and config_success and service_success and main_success
    
    if all_success:
        print("✅ All health checks passed!")
        print("\nYou can start the server with:")
        print("  ./run.sh")
        print("  or")
        print("  uvicorn main:app --reload")
        return 0
    else:
        print("❌ Some health checks failed. Please fix the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
