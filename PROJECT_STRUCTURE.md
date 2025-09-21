# YUV Tools - Project Structure

### Main Tools (Root Directory)

- **`yuv_analyzer.py`** - Zero dependencies, basic analysis
- **`yuv_viewer.py`** - Full features, requires OpenCV
- **`yuv_batch_viewer.py`** - Zero dependencies, batch export

### Alternative Tools (Examples Directory)

- **`yuv_viewer_minimal.py`** - Lightweight, optional Pillow
- **`yuv_viewer_simple.py`** - No OpenCV, uses matplotlib
- **`yuv_analyzer_enhanced.py`** - Zero dependencies, detailed output

```
yuv-tools/
├── README.md                     # Main documentation and usage guide
├── LICENSE                       # MIT License
├── .gitignore                   # Git ignore patterns
├── CHANGELOG.md                 # Version history and changes
├── CONTRIBUTING.md              # Contribution guidelines
├── requirements.txt             # Python dependencies
├── setup.py                     # Package installation script
├── test_installation.py         # Basic validation test
│
├── yuv_analyzer.py              # ⭐ Main zero-dependency analyzer
├── yuv_viewer.py                # Full-featured viewer with OpenCV
├── yuv_batch_viewer.py          # ⭐ Batch frame export (zero dependencies)
│
└── examples/                    # Alternative tools and examples
    ├── README.md                # Examples documentation
    ├── usage_examples.py        # Demo script showing common workflows
    ├── yuv_viewer_minimal.py    # Minimal viewer (Pillow only)
    ├── yuv_viewer_simple.py     # Simple viewer (matplotlib only)
    └── yuv_analyzer_enhanced.py # Enhanced analyzer with ASCII art
```

## Tool Overview

### Main Tools (Root Directory)
- **`yuv_analyzer.py`** - Zero dependencies, basic analysis
- **`yuv_viewer.py`** - Full features, requires OpenCV

### Alternative Tools (Examples Directory)
- **`yuv_viewer_minimal.py`** - Lightweight, optional Pillow
- **`yuv_viewer_simple.py`** - No OpenCV, uses matplotlib
- **`yuv_batch_viewer.py`** - No dependencies, batch export
- **`yuv_analyzer_enhanced.py`** - No dependencies, detailed output

### Supporting Files
- **`test_installation.py`** - Validates setup
- **`usage_examples.py`** - Demonstrates workflows
- **Documentation** - Complete guides for all tools

## Key Features

✅ **Multiple dependency options** - From zero to full-featured
✅ **Comprehensive documentation** - README, examples, changelog
✅ **Package structure** - Installable via pip
✅ **Cross-platform** - Works on Windows, Linux, macOS
✅ **Flexible workflows** - Different tools for different needs
✅ **Professional structure** - Follows Python packaging standards

## Repository Ready for GitHub

This structure is ready to be uploaded to GitHub and provides:
- Clear organization and documentation
- Multiple installation options
- Examples for different use cases
- Professional project structure
- MIT license for open source use
