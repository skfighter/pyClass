#!/usr/bin/env python3
"""
Test script for black and white conversion endpoint
"""

import requests
import json

def test_bw_conversion():
    """Test the /convertToBlackAndWhite endpoint"""
    url = "http://localhost:8000/convertToBlackAndWhite"
    
    # Test with an existing image
    with open("test_image.png", "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Black and White Conversion Test PASSED")
        print(f"   Success: {result['success']}")
        print(f"   Filename: {result['filename']}")
        print(f"   Image Dimensions: {result['image_info']['width']}x{result['image_info']['height']}")
        print(f"   Output Size: {result['image_info']['size_bytes']} bytes")
        print(f"   Format: {result['image_info']['format']}")
        print(f"   Mode: {result['image_info']['mode']}")
        print(f"   Base64 Data Preview: {result['bw_image_base64'][:60]}...")
        
        # Save the result to a file for verification
        with open("bw_test_result.json", "w") as f:
            json.dump(result, f, indent=2)
        print("\n📄 Full result saved to: bw_test_result.json")
        
    else:
        print(f"❌ Test FAILED - Status: {response.status_code}")
        print(f"   Error: {response.text}")

if __name__ == "__main__":
    test_bw_conversion()
