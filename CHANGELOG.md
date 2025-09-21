# Changelog

All notable changes to the YUV Tools project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-21

### Added
- Initial release of YUV Tools collection
- `yuv_analyzer.py` - Zero-dependency YUV frame analyzer
- `yuv_viewer.py` - Full-featured YUV viewer with OpenCV support
- `yuv_batch_viewer.py` - Batch frame export tool (now promoted to main tool)
- `yuv_viewer_minimal.py` - Minimal viewer with Pillow support
- `yuv_viewer_simple.py` - Simple viewer with matplotlib support
- `yuv_analyzer_enhanced.py` - Enhanced analyzer with ASCII visualization
- Comprehensive documentation and examples
- Package structure for pip installation
- Cross-platform support (Windows, Linux, macOS)

### Features
- **Multiple dependency options**: From zero dependencies to full-featured
- **Frame analysis**: Statistical analysis, health checks, corruption detection
- **Visual inspection**: ASCII art, image export, interactive viewing
- **Batch processing**: Export multiple frames at once
- **Format support**: YUV420 planar format (736×442 resolution)
- **Flexible workflows**: Support for different use cases and environments

### Documentation
- Complete README with usage examples
- Individual tool documentation
- Installation instructions for different scenarios
- Troubleshooting guide
- Example workflows for common tasks

### Technical Details
- Python 3.7+ support
- Configurable video dimensions
- Multiple output formats (PPM, PNG, analysis text)
- Memory-efficient frame processing
- Cross-platform file handling

## [Unreleased]

### Planned Features
- Support for YUV422 and YUV444 formats
- Additional video resolutions
- Performance optimizations
- GUI interface
- Video comparison tools
- Automated testing suite

---

## Release Notes

### Version 1.0.0
This is the initial stable release of YUV Tools. The collection provides a comprehensive set of utilities for working with YUV420 video files, particularly useful for:

- Video decoder debugging
- Frame-by-frame analysis
- Visual inspection of decoded video data
- Batch processing of video frames
- Educational purposes and research

The tools are designed with flexibility in mind, offering options from zero-dependency command-line analysis to full-featured interactive viewing, making them suitable for various environments and use cases.
