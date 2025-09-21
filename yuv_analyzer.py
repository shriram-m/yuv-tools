#!/usr/bin/env python3
"""
Zero-dependency YUV420 Frame Analyzer
This script requires NO external libraries - only standard Python.
It provides basic analysis and can save frames in PPM format.
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
    """
    Read a specific YUV420 frame from the file
    """
    # Seek to the start of the desired frame
    file_handle.seek(frame_number * FRAME_SIZE)
    
    # Read the frame data
    frame_data = file_handle.read(FRAME_SIZE)
    
    if len(frame_data) != FRAME_SIZE:
        return None, None, None
    
    # Split into Y, U, V planes
    y_plane = list(frame_data[:Y_SIZE])
    u_plane = list(frame_data[Y_SIZE:Y_SIZE + UV_SIZE])
    v_plane = list(frame_data[Y_SIZE + UV_SIZE:Y_SIZE + 2 * UV_SIZE])
    
    return y_plane, u_plane, v_plane

def get_frame_count(filename):
    """
    Calculate the number of frames in the YUV file
    """
    file_size = os.path.getsize(filename)
    return file_size // FRAME_SIZE

def analyze_frame_basic(y, u, v, frame_number):
    """
    Basic frame analysis without external dependencies
    """
    print(f"\n{'='*60}")
    print(f"FRAME {frame_number} ANALYSIS")
    print(f"{'='*60}")
    
    print(f"Frame size: {FRAME_SIZE} bytes")
    print(f"Expected layout:")
    print(f"  Y plane: 0 to {Y_SIZE-1} ({Y_SIZE} bytes)")
    print(f"  U plane: {Y_SIZE} to {Y_SIZE + UV_SIZE - 1} ({UV_SIZE} bytes)")
    print(f"  V plane: {Y_SIZE + UV_SIZE} to {FRAME_SIZE - 1} ({UV_SIZE} bytes)")
    
    # Y plane analysis
    y_min, y_max = min(y), max(y)
    y_avg = sum(y) / len(y)
    y_unique = len(set(y))
    
    print(f"\nY PLANE (Luminance) - {VIDEO_WIDTH}x{VIDEO_HEIGHT}:")
    print(f"  Min: {y_min}, Max: {y_max}, Average: {y_avg:.2f}")
    print(f"  Unique values: {y_unique}/256")
    print(f"  Value distribution:")
    print(f"    0-63 (dark): {sum(1 for v in y if 0 <= v < 64)} pixels")
    print(f"    64-127 (mid-dark): {sum(1 for v in y if 64 <= v < 128)} pixels")
    print(f"    128-191 (mid-bright): {sum(1 for v in y if 128 <= v < 192)} pixels")
    print(f"    192-255 (bright): {sum(1 for v in y if 192 <= v <= 255)} pixels")
    
    # U plane analysis
    u_min, u_max = min(u), max(u)
    u_avg = sum(u) / len(u)
    u_unique = len(set(u))
    
    print(f"\nU PLANE (Chroma Blue) - {VIDEO_WIDTH//2}x{VIDEO_HEIGHT//2}:")
    print(f"  Min: {u_min}, Max: {u_max}, Average: {u_avg:.2f}")
    print(f"  Unique values: {u_unique}/256")
    print(f"  Deviation from neutral (128): {abs(u_avg - 128):.2f}")
    
    # V plane analysis
    v_min, v_max = min(v), max(v)
    v_avg = sum(v) / len(v)
    v_unique = len(set(v))
    
    print(f"\nV PLANE (Chroma Red) - {VIDEO_WIDTH//2}x{VIDEO_HEIGHT//2}:")
    print(f"  Min: {v_min}, Max: {v_max}, Average: {v_avg:.2f}")
    print(f"  Unique values: {v_unique}/256")
    print(f"  Deviation from neutral (128): {abs(v_avg - 128):.2f}")
    
    # Health check
    print(f"\nHEALTH CHECK:")
    issues = []
    
    if y_max - y_min < 20:
        issues.append("Low luminance contrast (might appear flat)")
    if y_unique < 50:
        issues.append("Very few unique luminance values")
    if u_unique < 10:
        issues.append("Very few unique U (blue chroma) values")
    if v_unique < 10:
        issues.append("Very few unique V (red chroma) values")
    if all(val == y[0] for val in y):
        issues.append("Y plane has constant value (solid color)")
    if all(val == u[0] for val in u):
        issues.append("U plane has constant value")
    if all(val == v[0] for val in v):
        issues.append("V plane has constant value")
    
    if issues:
        print(f"  POTENTIAL ISSUES DETECTED:")
        for i, issue in enumerate(issues, 1):
            print(f"    {i}. {issue}")
    else:
        print(f"  Frame appears healthy ✓")

def compare_frames(file_handle, frame1, frame2):
    """
    Compare two frames to detect significant differences (potential tearing)
    """
    print(f"\n{'='*60}")
    print(f"COMPARING FRAMES {frame1} and {frame2}")
    print(f"{'='*60}")
    
    y1, u1, v1 = read_yuv_frame(file_handle, frame1)
    y2, u2, v2 = read_yuv_frame(file_handle, frame2)
    
    if y1 is None or y2 is None:
        print("Error reading frames for comparison")
        return
    
    # Calculate differences
    y_diffs = [abs(a - b) for a, b in zip(y1, y2)]
    u_diffs = [abs(a - b) for a, b in zip(u1, u2)]
    v_diffs = [abs(a - b) for a, b in zip(v1, v2)]
    
    y_avg_diff = sum(y_diffs) / len(y_diffs)
    u_avg_diff = sum(u_diffs) / len(u_diffs)
    v_avg_diff = sum(v_diffs) / len(v_diffs)
    
    y_max_diff = max(y_diffs)
    u_max_diff = max(u_diffs)
    v_max_diff = max(v_diffs)
    
    print(f"DIFFERENCE ANALYSIS:")
    print(f"  Y plane - Avg diff: {y_avg_diff:.2f}, Max diff: {y_max_diff}")
    print(f"  U plane - Avg diff: {u_avg_diff:.2f}, Max diff: {u_max_diff}")
    print(f"  V plane - Avg diff: {v_avg_diff:.2f}, Max diff: {v_max_diff}")
    
    # Count significant differences
    y_big_diffs = sum(1 for d in y_diffs if d > 50)
    total_pixels = len(y_diffs)
    
    print(f"  Pixels with >50 luminance difference: {y_big_diffs}/{total_pixels} ({100*y_big_diffs/total_pixels:.1f}%)")
    
    if y_avg_diff > 30:
        print("  WARNING: High average difference - frames very different")
    elif y_avg_diff < 2:
        print("  NOTE: Very low difference - frames might be nearly identical")
    else:
        print("  Normal frame-to-frame difference")

def save_text_visualization(y, u, v, frame_number):
    """
    Save a text-based visualization of the frame
    """
    filename = f"frame_{frame_number:06d}_visual.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Frame {frame_number} Text Visualization\n")
        f.write(f"Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT}\n")
        f.write("=" * 60 + "\n\n")
        
        # Create ASCII representation of Y plane (downsampled)
        f.write("Y PLANE (Luminance) - ASCII Art (16x16 downsampled):\n")
        step_x = VIDEO_WIDTH // 16
        step_y = VIDEO_HEIGHT // 16
        
        for row in range(16):
            line = ""
            for col in range(16):
                # Sample pixel from downsampled position
                src_x = col * step_x
                src_y = row * step_y
                src_idx = src_y * VIDEO_WIDTH + src_x
                
                if src_idx < len(y):
                    val = y[src_idx]
                    if val < 32:
                        char = ' '
                    elif val < 64:
                        char = '.'
                    elif val < 96:
                        char = ':'
                    elif val < 128:
                        char = '-'
                    elif val < 160:
                        char = '='
                    elif val < 192:
                        char = '+'
                    elif val < 224:
                        char = '*'
                    else:
                        char = '#'
                else:
                    char = '?'
                line += char * 2  # Make it wider
            f.write(line + "\n")
        
        f.write(f"\nLegend: [space]=black, .=dark, :=dim, -=med, +=bright, *=brighter, #=white\n")
        
        # Statistics
        f.write(f"\nSTATISTICS:\n")
        f.write(f"Y: min={min(y)}, max={max(y)}, avg={sum(y)/len(y):.1f}\n")
        f.write(f"U: min={min(u)}, max={max(u)}, avg={sum(u)/len(u):.1f}\n")
        f.write(f"V: min={min(v)}, max={max(v)}, avg={sum(v)/len(v):.1f}\n")
    
    print(f"Saved text visualization: {filename}")

def hexdump_frame_start(y, u, v):
    """
    Show hex dump of the beginning of each plane
    """
    print(f"\nHEX DUMP (first 32 bytes of each plane):")
    
    print(f"Y plane: {' '.join(f'{b:02x}' for b in y[:32])}")
    print(f"U plane: {' '.join(f'{b:02x}' for b in u[:16])}")
    print(f"V plane: {' '.join(f'{b:02x}' for b in v[:16])}")

def main():
    parser = argparse.ArgumentParser(description='Zero-dependency YUV420 Frame Analyzer')
    parser.add_argument('yuv_file', help='Path to the YUV file')
    parser.add_argument('--frame', '-f', type=int, default=0, help='Frame number to analyze')
    parser.add_argument('--analyze', '-a', action='store_true', help='Full frame analysis')
    parser.add_argument('--compare', '-c', nargs=2, type=int, metavar=('FRAME1', 'FRAME2'),
                       help='Compare two frames')
    parser.add_argument('--hexdump', action='store_true', help='Show hex dump')
    parser.add_argument('--text-viz', action='store_true', help='Save text visualization')
    parser.add_argument('--info', '-i', action='store_true', help='Show file info only')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.yuv_file):
        print(f"Error: File '{args.yuv_file}' not found!")
        sys.exit(1)
    
    # Get file info
    frame_count = get_frame_count(args.yuv_file)
    file_size_mb = os.path.getsize(args.yuv_file) / (1024 * 1024)
    
    print(f"YUV FILE INFORMATION")
    print(f"File: {args.yuv_file}")
    print(f"Video Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT}")
    print(f"Frame Size: {FRAME_SIZE} bytes")
    print(f"Total Frames: {frame_count}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Estimated Duration: {frame_count/24:.1f} seconds (at 24 fps)")
    
    if args.info:
        return
    
    with open(args.yuv_file, 'rb') as f:
        if args.compare:
            frame1, frame2 = args.compare
            if frame1 >= frame_count or frame2 >= frame_count:
                print(f"Error: Frame numbers must be < {frame_count}")
                sys.exit(1)
            compare_frames(f, frame1, frame2)
            return
        
        # Single frame analysis
        if args.frame >= frame_count:
            print(f"Error: Frame {args.frame} is beyond available frames (0-{frame_count-1})")
            sys.exit(1)
        
        y, u, v = read_yuv_frame(f, args.frame)
        
        if y is None:
            print(f"Error reading frame {args.frame}")
            sys.exit(1)
        
        if args.analyze:
            analyze_frame_basic(y, u, v, args.frame)
        
        if args.hexdump:
            hexdump_frame_start(y, u, v)
        
        if args.text_viz:
            save_text_visualization(y, u, v, args.frame)

if __name__ == "__main__":
    main()
