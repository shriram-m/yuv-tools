# YUV Tools

A comprehensive collection of Python tools for analyzing and viewing YUV420 video data. These tools are designed to help with video decoder debugging, frame analysis, and visual inspection of raw YUV data.

## Features

- **Zero-dependency analyzer** - Basic analysis using only standard Python
- **Flexible viewing options** - Multiple viewers with different dependency requirements
- **Comprehensive analysis** - Detailed frame statistics and health checks
- **Multiple output formats** - Save frames as images or analyze in terminal
- **Batch processing** - Process multiple frames at once

## Tools Overview

### Main Tools

1. **`yuv_analyzer.py`** ⭐ *Recommended*
   - **Dependencies**: None (standard Python only)
   - **Purpose**: Frame analysis, comparison, text visualization
   - **Best for**: Quick analysis when libraries are problematic

2. **`yuv_viewer.py`**
   - **Dependencies**: `numpy`, `opencv-python`, `matplotlib`
   - **Purpose**: Interactive viewing, video playback, advanced analysis
   - **Best for**: Full-featured analysis and viewing

3. **`yuv_batch_viewer.py`** ⭐ *Very Useful*
   - **Dependencies**: None (standard Python only)
   - **Purpose**: Batch export frames as PPM images
   - **Best for**: Converting many frames to viewable images

### Alternative Tools (in [examples/](examples/))

4. **`yuv_viewer_minimal.py`**
   - **Dependencies**: `Pillow` (optional)
   - **Purpose**: Image saving, corruption detection, basic viewing
   - **Best for**: When you want to save actual images with minimal setup

5. **`yuv_viewer_simple.py`**
   - **Dependencies**: `numpy`, `matplotlib`
   - **Purpose**: Simple viewing without OpenCV
   - **Best for**: When OpenCV is not available

## Installation

### Option 1: Clone and use directly
```bash
git clone https://github.com/shriram-m/yuv-tools.git
cd yuv-tools
```

### Option 2: Install as package
```bash
git clone https://github.com/shriram-m/yuv-tools.git
cd yuv-tools
pip install -e .
```

### Option 3: Install dependencies manually
```bash
# For full functionality
pip install -r requirements.txt

# Minimal dependencies (for yuv_viewer_simple.py)
pip install numpy matplotlib

# For yuv_viewer_minimal.py only
pip install Pillow
```

## Quick Start

### 1. Zero-dependency analysis (Recommended first step)
```bash
python yuv_analyzer.py your_file.yuv --analyze --frame 0
```

### 2. View a specific frame
```bash
python yuv_viewer.py your_file.yuv --frame 5
```

### 3. Play all frames as video
```bash
python yuv_viewer.py your_file.yuv --play
```

### 4. Batch export frames as images
```bash
python yuv_batch_viewer.py your_file.yuv --range 0 10
```

## Usage Examples

### Basic Frame Analysis
```bash
# Analyze first frame (no dependencies required)
python yuv_analyzer.py decoded_frames.yuv --analyze --frame 0

# Compare two frames
python yuv_analyzer.py decoded_frames.yuv --compare 0 5

# Get file information
python yuv_analyzer.py decoded_frames.yuv --info
```

### Advanced Viewing
```bash
# View specific frame with full OpenCV viewer
python yuv_viewer.py decoded_frames.yuv --frame 10

# Play all frames as video
python yuv_viewer.py decoded_frames.yuv --play

# Save frame as image
python yuv_viewer.py decoded_frames.yuv --frame 5 --save frame_5.png
```

### Batch Processing
```bash
# Export a single frame
python yuv_batch_viewer.py decoded_frames.yuv --frame 5

# Export specific frame range (frames 0 to 19)
python yuv_batch_viewer.py decoded_frames.yuv --range 0 19

# Export frames 100 to 149
python yuv_batch_viewer.py decoded_frames.yuv --range 100 149

# Sample every 10th frame throughout the video
python yuv_batch_viewer.py decoded_frames.yuv --sample 10

# Export to custom directory
python yuv_batch_viewer.py decoded_frames.yuv --range 0 9 --output my_frames
```

## Configuration

The tools are currently configured for:
- **Resolution**: 736×442 pixels
- **Format**: YUV420 planar
- **Layout**: Y plane + U plane + V plane

To modify for different resolutions, edit the constants at the top of each script:
```python
VIDEO_WIDTH = 736
VIDEO_HEIGHT = 442
```

## YUV420 Format Details

The tools expect YUV420 planar format with the following layout:
- **Y plane**: 736×442 bytes (luminance)
- **U plane**: 368×221 bytes (chroma blue)
- **V plane**: 368×221 bytes (chroma red)
- **Total frame size**: 325,954 bytes per frame

## Troubleshooting

### Library Installation Issues
If you have trouble installing OpenCV or other dependencies:
1. Use `yuv_analyzer.py` (no dependencies)
2. Try `yuv_viewer_minimal.py` (only needs Pillow)
3. Use `yuv_batch_viewer.py` for image export (no dependencies)

### Common Issues
- **File not found**: Check file path and ensure YUV file exists
- **Incorrect frame count**: Verify file size matches expected format
- **Garbled output**: Check if video resolution matches configured values
- **Installation errors**: Use virtual environment or try minimal tools first

### Getting Help
```bash
# Get help for any tool
python yuv_analyzer.py --help
python yuv_viewer.py --help
python examples/yuv_viewer_minimal.py --help
```

## File Format Support

Currently supports:
- ✅ YUV420 planar format
- ✅ Raw binary YUV files
- ✅ Multiple frames in single file

Currently unsupported formats:
- 🔄 YUV422 format
- 🔄 YUV444 format
- 🔄 Packed YUV formats

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## Examples

Check the [examples/](examples/) directory for:
- Sample usage scripts
- Alternative implementations
- Specialized tools for specific use cases

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/shriram-m/yuv-tools/issues) page
2. Create a new issue with detailed information
3. Include your command, expected behavior, and actual behavior

---
