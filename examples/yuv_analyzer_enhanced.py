#!/usr/bin/env python3
"""
Enhanced YUV Frame Analyzer with Better Visualization
This script provides detailed analysis and creates visual representations
of YUV data to help debug video decoder issues.
"""

import argparse
import os
import sys

# Video dimensions (from playback_config.h)
VIDEO_WIDTH = 736
VIDEO_HEIGHT = 442

# Calculate frame size
Y_SIZE = VIDEO_WIDTH * VIDEO_HEIGHT
UV_SIZE = (VIDEO_WIDTH // 2) * (VIDEO_HEIGHT // 2)
FRAME_SIZE = Y_SIZE + 2 * UV_SIZE

def read_yuv_frame(file_handle, frame_number):
    """Read a specific YUV420 frame from the file"""
    file_handle.seek(frame_number * FRAME_SIZE)
    frame_data = file_handle.read(FRAME_SIZE)
    
    if len(frame_data) != FRAME_SIZE:
        return None, None, None
    
    y_plane = list(frame_data[:Y_SIZE])
    u_plane = list(frame_data[Y_SIZE:Y_SIZE + UV_SIZE])
    v_plane = list(frame_data[Y_SIZE + UV_SIZE:Y_SIZE + 2 * UV_SIZE])
    
    return y_plane, u_plane, v_plane

def get_frame_count(filename):
    """Calculate the number of frames in the YUV file"""
    file_size = os.path.getsize(filename)
    return file_size // FRAME_SIZE

def create_detailed_ascii_art(y, frame_number, rows=32, cols=64):
    """Create a detailed ASCII art representation of the Y plane"""
    print(f"\nDETAILED ASCII VISUALIZATION - Frame {frame_number}")
    print(f"Showing {rows}x{cols} downsampled view of {VIDEO_WIDTH}x{VIDEO_HEIGHT} frame")
    print("=" * 80)
    
    step_x = VIDEO_WIDTH // cols
    step_y = VIDEO_HEIGHT // rows
    
    # Create ASCII art
    for row in range(rows):
        line = ""
        for col in range(cols):
            src_x = col * step_x
            src_y = row * step_y
            src_idx = src_y * VIDEO_WIDTH + src_x
            
            if src_idx < len(y):
                val = y[src_idx]
                # More detailed ASCII mapping
                if val == 0:
                    char = ' '  # Pure black
                elif val < 8:
                    char = '.'
                elif val < 16:
                    char = ':'
                elif val < 24:
                    char = ';'
                elif val < 32:
                    char = '!'
                elif val < 40:
                    char = '?'
                elif val < 48:
                    char = '+'
                elif val < 56:
                    char = '='
                elif val < 64:
                    char = '*'
                elif val < 80:
                    char = '#'
                elif val < 100:
                    char = '%'
                elif val < 128:
                    char = '@'
                elif val < 160:
                    char = '&'
                elif val < 192:
                    char = '$'
                else:
                    char = 'W'  # Very bright
            else:
                char = '?'
            line += char
        print(line)
    
    print("\nBrightness Legend:")
    print("  [space] = 0 (black)")
    print("  . : ; ! ? = 1-48 (very dark)")
    print("  + = * = 49-64 (dark)")
    print("  # % @ = 65-128 (medium)")
    print("  & $ W = 129+ (bright)")

def analyze_y_plane_distribution(y, frame_number):
    """Detailed analysis of Y plane distribution"""
    print(f"\nDETAILED Y PLANE ANALYSIS - Frame {frame_number}")
    print("=" * 60)
    
    # Create histogram
    bins = [0] * 16  # 16 bins of 16 values each
    for val in y:
        bin_idx = min(val // 16, 15)
        bins[bin_idx] += 1
    
    total_pixels = len(y)
    print("Luminance Distribution (16 bins of 16 values each):")
    
    for i, count in enumerate(bins):
        start_val = i * 16
        end_val = (i + 1) * 16 - 1
        percentage = (count / total_pixels) * 100
        bar_length = int(percentage / 2)  # Scale for display
        bar = '#' * bar_length
        print(f"  {start_val:3d}-{end_val:3d}: {count:6d} ({percentage:5.1f}%) {bar}")
    
    # Check for unusual patterns
    zero_pixels = bins[0]
    if zero_pixels > total_pixels * 0.1:
        print(f"\nWARNING: {zero_pixels} pixels are pure black ({100*zero_pixels/total_pixels:.1f}%)")
    
    # Check for clustering
    max_bin = max(bins)
    max_bin_idx = bins.index(max_bin)
    if max_bin > total_pixels * 0.8:
        print(f"WARNING: {100*max_bin/total_pixels:.1f}% of pixels are in range {max_bin_idx*16}-{(max_bin_idx+1)*16-1}")

def check_frame_validity(y, u, v, frame_number):
    """Check if frame data looks valid or corrupted"""
    print(f"\nFRAME VALIDITY CHECK - Frame {frame_number}")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # Check Y plane
    y_range = max(y) - min(y)
    y_unique = len(set(y))
    y_zeros = sum(1 for val in y if val == 0)
    
    if y_range < 30:
        issues.append(f"Very low Y range ({y_range}) - image will appear flat")
    if y_unique < 50:
        warnings.append(f"Low Y diversity ({y_unique} unique values)")
    if y_zeros > len(y) * 0.1:
        warnings.append(f"Many zero Y values ({y_zeros}/{len(y)})")
    
    # Check U plane
    u_unique = len(set(u))
    u_avg = sum(u) / len(u)
    if u_unique < 10:
        warnings.append(f"Very low U diversity ({u_unique} unique values)")
    
    # Check V plane
    v_unique = len(set(v))
    v_avg = sum(v) / len(v)
    if v_unique < 10:
        warnings.append(f"Very low V diversity ({v_unique} unique values)")
    
    # Check for potential padding or stride issues
    # Look for repeated patterns at line endings
    line_end_pattern = []
    for row in range(min(10, VIDEO_HEIGHT)):  # Check first 10 rows
        line_start_idx = row * VIDEO_WIDTH
        line_end_idx = line_start_idx + VIDEO_WIDTH - 1
        if line_end_idx < len(y):
            line_end_pattern.append(y[line_end_idx])
    
    if len(set(line_end_pattern)) == 1 and len(line_end_pattern) > 5:
        issues.append("Suspicious pattern at line endings - possible stride issue")
    
    # Report findings
    if issues:
        print("CRITICAL ISSUES:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    
    if warnings:
        print("WARNINGS:")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    
    if not issues and not warnings:
        print("Frame appears to have valid data structure ✓")
    
    return len(issues) == 0

def save_analysis_report(y, u, v, frame_number, filename=None):
    """Save detailed analysis to a text file"""
    if filename is None:
        filename = f"frame_{frame_number:06d}_analysis.txt"
    
    with open(filename, 'w') as f:
        f.write(f"DETAILED FRAME ANALYSIS REPORT\n")
        f.write(f"Frame Number: {frame_number}\n")
        f.write(f"Video Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT}\n")
        f.write(f"Frame Size: {FRAME_SIZE} bytes\n")
        f.write("=" * 60 + "\n\n")
        
        # Y plane statistics
        f.write("Y PLANE (LUMINANCE) ANALYSIS:\n")
        f.write(f"  Size: {len(y)} bytes\n")
        f.write(f"  Min: {min(y)}, Max: {max(y)}, Average: {sum(y)/len(y):.2f}\n")
        f.write(f"  Unique values: {len(set(y))}/256\n")
        f.write(f"  Standard deviation: {calculate_std(y):.2f}\n")
        
        # Create histogram for file
        bins = [0] * 16
        for val in y:
            bin_idx = min(val // 16, 15)
            bins[bin_idx] += 1
        
        f.write("\n  Histogram (16 bins):\n")
        for i, count in enumerate(bins):
            start_val = i * 16
            end_val = (i + 1) * 16 - 1
            percentage = (count / len(y)) * 100
            f.write(f"    {start_val:3d}-{end_val:3d}: {count:6d} ({percentage:5.1f}%)\n")
        
        # U and V plane statistics
        f.write(f"\nU PLANE (CHROMA BLUE) ANALYSIS:\n")
        f.write(f"  Size: {len(u)} bytes\n")
        f.write(f"  Min: {min(u)}, Max: {max(u)}, Average: {sum(u)/len(u):.2f}\n")
        f.write(f"  Unique values: {len(set(u))}/256\n")
        
        f.write(f"\nV PLANE (CHROMA RED) ANALYSIS:\n")
        f.write(f"  Size: {len(v)} bytes\n")
        f.write(f"  Min: {min(v)}, Max: {max(v)}, Average: {sum(v)/len(v):.2f}\n")
        f.write(f"  Unique values: {len(set(v))}/256\n")
        
        # Sample data for debugging
        f.write(f"\nSAMPLE DATA (first 32 bytes of each plane):\n")
        f.write(f"Y: {' '.join(f'{val:02x}' for val in y[:32])}\n")
        f.write(f"U: {' '.join(f'{val:02x}' for val in u[:16])}\n")
        f.write(f"V: {' '.join(f'{val:02x}' for val in v[:16])}\n")
    
    print(f"Detailed analysis saved to: {filename}")

def calculate_std(data):
    """Calculate standard deviation"""
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return variance ** 0.5

def main():
    parser = argparse.ArgumentParser(description='Enhanced YUV420 Frame Analyzer')
    parser.add_argument('yuv_file', help='Path to the YUV file')
    parser.add_argument('--frame', '-f', type=int, default=0, help='Frame number to analyze')
    parser.add_argument('--ascii', action='store_true', help='Show detailed ASCII art')
    parser.add_argument('--histogram', action='store_true', help='Show luminance histogram')
    parser.add_argument('--validate', action='store_true', help='Validate frame data')
    parser.add_argument('--save-report', action='store_true', help='Save detailed analysis report')
    parser.add_argument('--compare', '-c', nargs=2, type=int, metavar=('FRAME1', 'FRAME2'),
                       help='Compare two frames')
    parser.add_argument('--info', '-i', action='store_true', help='Show file info only')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.yuv_file):
        print(f"Error: File '{args.yuv_file}' not found!")
        sys.exit(1)
    
    # Get file info
    frame_count = get_frame_count(args.yuv_file)
    file_size_mb = os.path.getsize(args.yuv_file) / (1024 * 1024)
    
    print(f"ENHANCED YUV FILE ANALYSIS")
    print(f"File: {args.yuv_file}")
    print(f"Video Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT}")
    print(f"Frame Size: {FRAME_SIZE} bytes")
    print(f"Total Frames: {frame_count}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Estimated Duration: {frame_count/18.2:.1f} seconds (at 18.2 fps)")
    
    if args.info:
        return
    
    with open(args.yuv_file, 'rb') as f:
        if args.compare:
            frame1, frame2 = args.compare
            if frame1 >= frame_count or frame2 >= frame_count:
                print(f"Error: Frame numbers must be < {frame_count}")
                sys.exit(1)
            
            print(f"\nCOMPARING FRAMES {frame1} and {frame2}")
            y1, u1, v1 = read_yuv_frame(f, frame1)
            y2, u2, v2 = read_yuv_frame(f, frame2)
            
            if y1 and y2:
                y_diffs = [abs(a - b) for a, b in zip(y1, y2)]
                print(f"Y plane differences: avg={sum(y_diffs)/len(y_diffs):.2f}, max={max(y_diffs)}")
            return
        
        # Single frame analysis
        if args.frame >= frame_count:
            print(f"Error: Frame {args.frame} is beyond available frames (0-{frame_count-1})")
            sys.exit(1)
        
        y, u, v = read_yuv_frame(f, args.frame)
        
        if y is None:
            print(f"Error reading frame {args.frame}")
            sys.exit(1)
        
        if args.ascii:
            create_detailed_ascii_art(y, args.frame)
        
        if args.histogram:
            analyze_y_plane_distribution(y, args.frame)
        
        if args.validate:
            check_frame_validity(y, u, v, args.frame)
        
        if args.save_report:
            save_analysis_report(y, u, v, args.frame)

if __name__ == "__main__":
    main()
