#!/usr/bin/env python3
"""
Example Usage Script for YUV Tools
This script demonstrates common usage patterns and workflows.
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and print its output"""
    print(f"\n{'='*60}")
    print(f"EXAMPLE: {description}")
    print(f"COMMAND: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print("OUTPUT:")
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print("ERROR:")
            print(result.stderr)
    except Exception as e:
        print(f"Failed to run command: {e}")

def main():
    # Check if YUV file is provided
    if len(sys.argv) < 2:
        print("Usage: python usage_examples.py <yuv_file>")
        print("\nThis script demonstrates various YUV tool usage patterns.")
        sys.exit(1)
    
    yuv_file = sys.argv[1]
    
    if not os.path.exists(yuv_file):
        print(f"Error: YUV file '{yuv_file}' not found!")
        sys.exit(1)
    
    print("YUV Tools - Usage Examples")
    print(f"Working with file: {yuv_file}")
    
    # Example 1: Get file information
    run_command(
        f"python ../yuv_analyzer.py \"{yuv_file}\" --info",
        "Get basic file information"
    )
    
    # Example 2: Analyze first frame
    run_command(
        f"python ../yuv_analyzer.py \"{yuv_file}\" --analyze --frame 0",
        "Analyze the first frame"
    )
    
    # Example 3: Compare two frames
    run_command(
        f"python ../yuv_analyzer.py \"{yuv_file}\" --compare 0 1",
        "Compare first two frames"
    )
    
    # Example 4: Enhanced analysis with ASCII
    run_command(
        f"python yuv_analyzer_enhanced.py \"{yuv_file}\" --frame 0 --ascii",
        "Enhanced analysis with ASCII visualization"
    )
    
    # Example 5: Export first 3 frames as PPM images
    run_command(
        f"python ../yuv_batch_viewer.py \"{yuv_file}\" --range 0 2",
        "Export first 3 frames as PPM images"
    )
    
    print(f"\n{'='*60}")
    print("EXAMPLES COMPLETED")
    print("Check the 'yuv_frames' directory for exported images.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
