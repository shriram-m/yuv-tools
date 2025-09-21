# Examples

This directory contains alternative implementations and specialized tools for working with YUV files.

## Alternative Viewers

### `yuv_viewer_minimal.py`
- **Dependencies**: `Pillow` (optional)
- **Features**: Image saving, corruption detection, raw plane export
- **Usage**: 
  ```bash
  python yuv_viewer_minimal.py your_file.yuv --frame 5
  python yuv_viewer_minimal.py your_file.yuv --save-frame 5 --output frame_5.png
  ```

### `yuv_viewer_simple.py`
- **Dependencies**: `numpy`, `matplotlib`
- **Features**: Simple viewing without OpenCV dependency
- **Usage**:
  ```bash
  python yuv_viewer_simple.py your_file.yuv --frame 10
  python yuv_viewer_simple.py your_file.yuv --play
  ```

### `yuv_analyzer_enhanced.py`
- **Dependencies**: None (standard Python only)
- **Features**: Enhanced ASCII visualization and detailed analysis
- **Usage**:
  ```bash
  python yuv_analyzer_enhanced.py your_file.yuv --frame 0 --ascii
  python yuv_analyzer_enhanced.py your_file.yuv --frame 0 --detailed
  ```

## Use Cases

### When to use minimal tools:
- Library installation issues
- Resource-constrained environments
- Quick analysis without dependencies
- Batch processing for automation

### When to use enhanced tools:
- Detailed debugging requirements
- Visual inspection needs
- Educational purposes
- Development and testing

## Example Workflows

### Quick Analysis Workflow
```bash
# 1. Check file info
python ../yuv_analyzer.py your_file.yuv --info

# 2. Analyze first frame
python ../yuv_analyzer.py your_file.yuv --analyze --frame 0

# 3. Export first 10 frames as images (batch viewer is now in main directory)
python ../yuv_batch_viewer.py your_file.yuv --range 0 9
```

### Detailed Debugging Workflow
```bash
# 1. Enhanced analysis with ASCII art
python yuv_analyzer_enhanced.py your_file.yuv --frame 0 --ascii

# 2. Compare frames for differences
python ../yuv_analyzer.py your_file.yuv --compare 0 5

# 3. Save problematic frame as image
python yuv_viewer_minimal.py your_file.yuv --save-frame 5 --output debug_frame.png
```

### Cross-platform Workflow
```bash
# 1. Use zero-dependency analyzer first
python ../yuv_analyzer.py your_file.yuv --analyze --frame 0

# 2. Try minimal viewer if Pillow is available
python yuv_viewer_minimal.py your_file.yuv --frame 0

# 3. Fallback to batch export if needed (batch viewer is now in main directory)
python ../yuv_batch_viewer.py your_file.yuv --range 0 4
```
