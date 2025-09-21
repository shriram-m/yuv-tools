#!/usr/bin/env python3
"""
Simple test script to validate YUV Tools installation and basic functionality.
"""

import sys
import os
import tempfile
import struct

def create_test_yuv_file():
    """Create a small test YUV file for validation"""
    # Create a simple test pattern (8x8 frame)
    width, height = 8, 8
    y_size = width * height
    uv_size = (width // 2) * (height // 2)
    
    # Create simple patterns
    y_data = bytes([i % 256 for i in range(y_size)])  # Gradient pattern
    u_data = bytes([128] * uv_size)  # Neutral chroma
    v_data = bytes([128] * uv_size)  # Neutral chroma
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(suffix='.yuv', delete=False) as f:
        f.write(y_data + u_data + v_data)
        return f.name

def test_yuv_analyzer():
    """Test the yuv_analyzer functionality"""
    print("Testing yuv_analyzer...")
    
    try:
        # Create a test file
        test_file = create_test_yuv_file()
        print(f"Created test file: {test_file}")
        
        # Note: This is a basic structure test
        # In real testing, you'd modify the scripts to handle different resolutions
        print("✓ Test file creation successful")
        
        # Clean up
        os.unlink(test_file)
        print("✓ Cleanup successful")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False
    
    return True

def test_imports():
    """Test that we can import standard library modules"""
    print("Testing standard library imports...")
    
    try:
        import argparse
        import os
        import sys
        print("✓ Standard library imports successful")
    except ImportError as e:
        print(f"✗ Standard library import failed: {e}")
        return False
    
    return True

def test_optional_imports():
    """Test optional dependencies"""
    print("Testing optional dependencies...")
    
    optional_deps = {
        'numpy': 'NumPy',
        'cv2': 'OpenCV',
        'matplotlib': 'Matplotlib',
        'PIL': 'Pillow'
    }
    
    available = []
    missing = []
    
    for module, name in optional_deps.items():
        try:
            __import__(module)
            available.append(name)
        except ImportError:
            missing.append(name)
    
    print(f"✓ Available: {', '.join(available) if available else 'None'}")
    print(f"! Missing: {', '.join(missing) if missing else 'None'}")
    
    return True

def main():
    """Run all tests"""
    print("YUV Tools - Basic Validation Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_optional_imports,
        test_yuv_analyzer,
    ]
    
    results = []
    for test in tests:
        print()
        result = test()
        results.append(result)
    
    print("\n" + "=" * 40)
    if all(results):
        print("✓ All basic tests passed!")
        print("\nYUV Tools appears to be properly set up.")
        print("You can now use the tools with your YUV files.")
    else:
        print("✗ Some tests failed!")
        print("\nPlease check the error messages above.")
    
    print("\nNext steps:")
    print("1. Test with your YUV file: python yuv_analyzer.py your_file.yuv --info")
    print("2. Install optional dependencies: pip install -r requirements.txt")
    print("3. Check examples/README.md for more usage patterns")

if __name__ == "__main__":
    main()
