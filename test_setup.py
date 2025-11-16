"""Test script to verify installation"""
import sys

def test_imports():
    """Test if all required packages can be imported"""
    results = {}
    
    packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('PIL', 'Pillow'),
        ('torch', 'PyTorch'),
        ('transformers', 'Transformers'),
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
    ]
    
    print("Testing package imports...\n")
    
    for package, name in packages:
        try:
            __import__(package)
            results[name] = '✅ OK'
            print(f"✅ {name:15} - Installed")
        except ImportError as e:
            results[name] = f'❌ FAILED: {e}'
            print(f"❌ {name:15} - NOT installed")
    
    print(f"\n{'='*50}")
    print(f"Results: {sum(1 for v in results.values() if '✅' in v)}/{len(packages)} packages OK")
    print(f"{'='*50}\n")
    
    return all('✅' in v for v in results.values())

if __name__ == '__main__':
    success = test_imports()
    sys.exit(0 if success else 1)
