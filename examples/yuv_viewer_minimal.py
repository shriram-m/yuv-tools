#!/usr/bin/env python3
"""
Minimal YUV420 Frame Viewer using only PIL/Pillow
This script requires only the Pillow library for image handling.

Install with: pip install Pillow
"""

import struct
import argparse
import os
import sys

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL/Pillow not available. Only raw analysis will be performed.")

# Video dimensions (from playback_config.h)
VIDEO_WIDTH = 736
VIDEO_HEIGHT = 442

# Calculate frame size
Y_SIZE = VIDEO_WIDTH * VIDEO_HEIGHT
UV_SIZE = (VIDEO_WIDTH // 2) * (VIDEO_HEIGHT // 2)
FRAME_SIZE = Y_SIZE + 2 * UV_SIZE

def clamp(value, min_val=0, max_val=255):
    """Clamp value to valid range"""
    return max(min_val, min(max_val, int(value)))

def yuv420_to_rgb_manual(y_plane, u_plane, v_plane):
    """
    Convert YUV420 planar format to RGB using manual conversion
    Returns list of RGB tuples
    """
    rgb_pixels = []
    
    # Process each pixel
    for row in range(VIDEO_HEIGHT):
        for col in range(VIDEO_WIDTH):
            # Get Y value
            y_idx = row * VIDEO_WIDTH + col
            y = y_plane[y_idx] if y_idx < len(y_plane) else 0
            
            # Get U and V values (subsampled)
            uv_row = row // 2
            uv_col = col // 2
            uv_idx = uv_row * (VIDEO_WIDTH // 2) + uv_col
            
            u = u_plane[uv_idx] if uv_idx < len(u_plane) else 128
            v = v_plane[uv_idx] if uv_idx < len(v_plane) else 128
            
            # Convert YUV to RGB (ITU-R BT.601)
            c = y - 16
            d = u - 128
            e = v - 128
            
            r = clamp((298 * c + 409 * e + 128) >> 8)
            g = clamp((298 * c - 100 * d - 208 * e + 128) >> 8)
            b = clamp((298 * c + 516 * d + 128) >> 8)
            
            rgb_pixels.append((r, g, b))
    
    return rgb_pixels

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

def analyze_frame_data(y, u, v, frame_number):
    """
    Analyze frame data without external dependencies
    """
    print(f"\nFrame {frame_number} Analysis:")
    print(f"Frame size: {FRAME_SIZE} bytes")
    print(f"Y plane: {len(y)} bytes - Min: {min(y)}, Max: {max(y)}, Avg: {sum(y)/len(y):.2f}")
    print(f"U plane: {len(u)} bytes - Min: {min(u)}, Max: {max(u)}, Avg: {sum(u)/len(u):.2f}")
    print(f"V plane: {len(v)} bytes - Min: {min(v)}, Max: {max(v)}, Avg: {sum(v)/len(v):.2f}")
    
    # Check for potential issues
    y_range = max(y) - min(y)
    u_range = max(u) - min(u)
    v_range = max(v) - min(v)
    
    print(f"Value ranges - Y: {y_range}, U: {u_range}, V: {v_range}")
    
    if y_range < 10:
        print("WARNING: Very low Y (luminance) range - image may appear flat")
    if u_range < 5 and v_range < 5:
        print("WARNING: Very low UV (chroma) range - image may appear grayscale")
    
    # Sample some pixel values
    print(f"Sample Y values (first 10): {y[:10]}")
    print(f"Sample U values (first 10): {u[:10]}")
    print(f"Sample V values (first 10): {v[:10]}")

def save_frame_as_ppm(y, u, v, frame_number, output_dir="frames"):
    """
    Save frame as PPM (Portable Pixmap) format - can be opened by most image viewers
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"frame_{frame_number:06d}.ppm")
    
    # Convert to RGB
    rgb_pixels = yuv420_to_rgb_manual(y, u, v)
    
    # Write PPM file
    with open(filename, 'wb') as f:
        # PPM header
        header = f"P6\n{VIDEO_WIDTH} {VIDEO_HEIGHT}\n255\n"
        f.write(header.encode('ascii'))
        
        # Write pixel data
        for r, g, b in rgb_pixels:
            f.write(bytes([r, g, b]))
    
    print(f"Saved frame {frame_number} as {filename}")

def save_frame_as_pil(y, u, v, frame_number, output_dir="frames"):
    """
    Save frame using PIL/Pillow
    """
    if not PIL_AVAILABLE:
        print("PIL not available, using PPM format instead")
        save_frame_as_ppm(y, u, v, frame_number, output_dir)
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert to RGB
    rgb_pixels = yuv420_to_rgb_manual(y, u, v)
    
    # Create PIL image
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT))
    img.putdata(rgb_pixels)
    
    # Save as PNG
    filename = os.path.join(output_dir, f"frame_{frame_number:06d}.png")
    img.save(filename)
    print(f"Saved frame {frame_number} as {filename}")

def save_raw_planes(y, u, v, frame_number, output_dir="raw_planes"):
    """
    Save individual Y, U, V planes as raw binary files for debugging
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Save Y plane
    with open(os.path.join(output_dir, f"frame_{frame_number:06d}_Y.raw"), 'wb') as f:
        f.write(bytes(y))
    
    # Save U plane
    with open(os.path.join(output_dir, f"frame_{frame_number:06d}_U.raw"), 'wb') as f:
        f.write(bytes(u))
    
    # Save V plane
    with open(os.path.join(output_dir, f"frame_{frame_number:06d}_V.raw"), 'wb') as f:
        f.write(bytes(v))
    
    print(f"Saved raw planes for frame {frame_number}")

def check_frame_corruption(y, u, v, frame_number):
    """
    Check for signs of frame corruption
    """
    issues = []
    
    # Check for all-zero data
    if all(val == 0 for val in y):
        issues.append("Y plane is all zeros")
    if all(val == 0 for val in u):
        issues.append("U plane is all zeros")
    if all(val == 0 for val in v):
        issues.append("V plane is all zeros")
    
    # Check for stuck values
    if len(set(y)) < 5:
        issues.append(f"Y plane has very few unique values ({len(set(y))})")
    if len(set(u)) < 3:
        issues.append(f"U plane has very few unique values ({len(set(u))})")
    if len(set(v)) < 3:
        issues.append(f"V plane has very few unique values ({len(set(v))})")
    
    # Check for unrealistic values
    y_outliers = sum(1 for val in y if val < 16 or val > 235)
    if y_outliers > len(y) * 0.1:
        issues.append(f"High number of Y values outside normal range: {y_outliers}/{len(y)}")
    
    if issues:
        print(f"Frame {frame_number} potential issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"Frame {frame_number} appears healthy")

def hexdump_sample(data, label, num_bytes=32):
    """
    Print hex dump of first few bytes for debugging
    """
    print(f"\n{label} (first {min(num_bytes, len(data))} bytes):")
    hex_str = " ".join(f"{b:02x}" for b in data[:num_bytes])
    print(f"  {hex_str}")

def main():
    parser = argparse.ArgumentParser(description='Minimal YUV420 Frame Viewer')
    parser.add_argument('yuv_file', help='Path to the YUV file')
    parser.add_argument('--frame', '-f', type=int, default=0, help='Frame number to analyze')
    parser.add_argument('--analyze', '-a', action='store_true', help='Analyze frame data')
    parser.add_argument('--save', '-s', action='store_true', help='Save frame as image')
    parser.add_argument('--save-raw', action='store_true', help='Save raw Y/U/V planes')
    parser.add_argument('--check-corruption', '-c', action='store_true', help='Check for corruption')
    parser.add_argument('--hexdump', action='store_true', help='Show hex dump of frame data')
    parser.add_argument('--range', '-r', nargs=2, type=int, metavar=('START', 'END'), 
                       help='Process a range of frames')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.yuv_file):
        print(f"Error: File '{args.yuv_file}' not found!")
        sys.exit(1)
    
    # Get file info
    frame_count = get_frame_count(args.yuv_file)
    file_size_mb = os.path.getsize(args.yuv_file) / (1024 * 1024)
    
    print(f"YUV File: {args.yuv_file}")
    print(f"Video Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT}")
    print(f"Frame Size: {FRAME_SIZE} bytes")
    print(f"Total Frames: {frame_count}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"PIL/Pillow Available: {PIL_AVAILABLE}")
    
    with open(args.yuv_file, 'rb') as f:
        frames_to_process = []
        
        if args.range:
            start, end = args.range
            frames_to_process = list(range(start, min(end + 1, frame_count)))
        else:
            frames_to_process = [args.frame]
        
        for frame_num in frames_to_process:
            if frame_num >= frame_count:
                print(f"Warning: Frame {frame_num} is beyond available frames (0-{frame_count-1})")
                continue
            
            print(f"\n{'='*50}")
            print(f"Processing Frame {frame_num}")
            print(f"{'='*50}")
            
            y, u, v = read_yuv_frame(f, frame_num)
            
            if y is None:
                print(f"Error reading frame {frame_num}")
                continue
            
            if args.analyze:
                analyze_frame_data(y, u, v, frame_num)
            
            if args.check_corruption:
                check_frame_corruption(y, u, v, frame_num)
            
            if args.hexdump:
                hexdump_sample(y, "Y plane", 32)
                hexdump_sample(u, "U plane", 16)
                hexdump_sample(v, "V plane", 16)
            
            if args.save:
                save_frame_as_pil(y, u, v, frame_num)
            
            if args.save_raw:
                save_raw_planes(y, u, v, frame_num)

if __name__ == "__main__":
    main()
