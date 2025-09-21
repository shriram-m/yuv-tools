#!/usr/bin/env python3
"""
Simple Batch Frame Viewer for YUV Files
Creates PPM images that can be opened with any image viewer
"""

import argparse
import os
import sys

# Video dimensions
VIDEO_WIDTH = 736
VIDEO_HEIGHT = 442
Y_SIZE = VIDEO_WIDTH * VIDEO_HEIGHT
UV_SIZE = (VIDEO_WIDTH // 2) * (VIDEO_HEIGHT // 2)
FRAME_SIZE = Y_SIZE + 2 * UV_SIZE

def read_yuv_frame(file_handle, frame_number):
    """Read a YUV420 frame from file"""
    file_handle.seek(frame_number * FRAME_SIZE)
    frame_data = file_handle.read(FRAME_SIZE)
    
    if len(frame_data) != FRAME_SIZE:
        return None, None, None
    
    y_plane = list(frame_data[:Y_SIZE])
    u_plane = list(frame_data[Y_SIZE:Y_SIZE + UV_SIZE])
    v_plane = list(frame_data[Y_SIZE + UV_SIZE:Y_SIZE + 2 * UV_SIZE])
    
    return y_plane, u_plane, v_plane

def yuv_to_rgb(y, u, v):
    """Convert YUV to RGB using ITU-R BT.601 standard"""
    # ITU-R BT.601 conversion
    c = y - 16
    d = u - 128
    e = v - 128
    
    r = max(0, min(255, int((298 * c + 409 * e + 128) >> 8)))
    g = max(0, min(255, int((298 * c - 100 * d - 208 * e + 128) >> 8)))
    b = max(0, min(255, int((298 * c + 516 * d + 128) >> 8)))
    
    return r, g, b

def save_frame_as_ppm(y, u, v, frame_number, output_dir="yuv_frames"):
    """Save frame as PPM (can be opened by most image viewers)"""
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"frame_{frame_number:06d}.ppm")
    
    with open(filename, 'wb') as f:
        # PPM header
        header = f"P6\n{VIDEO_WIDTH} {VIDEO_HEIGHT}\n255\n"
        f.write(header.encode('ascii'))
        
        # Convert and write pixel data
        for row in range(VIDEO_HEIGHT):
            for col in range(VIDEO_WIDTH):
                # Get Y value
                y_idx = row * VIDEO_WIDTH + col
                y_val = y[y_idx] if y_idx < len(y) else 0
                
                # Get U and V values (subsampled)
                uv_row = row // 2
                uv_col = col // 2
                uv_idx = uv_row * (VIDEO_WIDTH // 2) + uv_col
                
                u_val = u[uv_idx] if uv_idx < len(u) else 128
                v_val = v[uv_idx] if uv_idx < len(v) else 128
                
                # Convert to RGB
                r, g, b = yuv_to_rgb(y_val, u_val, v_val)
                f.write(bytes([r, g, b]))
    
    print(f"Saved: {filename}")
    return filename

def create_frame_summary(y, u, v, frame_number):
    """Create a text summary of the frame"""
    y_min, y_max, y_avg = min(y), max(y), sum(y)/len(y)
    u_min, u_max, u_avg = min(u), max(u), sum(u)/len(u)
    v_min, v_max, v_avg = min(v), max(v), sum(v)/len(v)
    
    return f"Frame {frame_number}: Y({y_min}-{y_max}, avg={y_avg:.1f}) U({u_min}-{u_max}, avg={u_avg:.1f}) V({v_min}-{v_max}, avg={v_avg:.1f})"

def main():
    parser = argparse.ArgumentParser(description='Batch YUV Frame Viewer')
    parser.add_argument('yuv_file', help='Path to YUV file')
    parser.add_argument('--frame', '-f', type=int, help='Single frame to convert')
    parser.add_argument('--range', '-r', nargs=2, type=int, metavar=('START', 'END'), 
                       help='Range of frames to convert')
    parser.add_argument('--sample', '-s', type=int, default=10, 
                       help='Sample every N frames (default: 10)')
    parser.add_argument('--output', '-o', default='yuv_frames', 
                       help='Output directory (default: yuv_frames)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.yuv_file):
        print(f"Error: File not found: {args.yuv_file}")
        sys.exit(1)
    
    # Get file info
    file_size = os.path.getsize(args.yuv_file)
    frame_count = file_size // FRAME_SIZE
    
    print(f"YUV File: {args.yuv_file}")
    print(f"Total frames: {frame_count}")
    print(f"Output directory: {args.output}")
    
    with open(args.yuv_file, 'rb') as f:
        frames_to_process = []
        
        if args.frame is not None:
            # Single frame
            frames_to_process = [args.frame]
        elif args.range:
            # Range of frames
            start, end = args.range
            frames_to_process = list(range(start, min(end + 1, frame_count)))
        else:
            # Sample frames throughout the video
            frames_to_process = list(range(0, frame_count, args.sample))
            print(f"Sampling every {args.sample} frames...")
        
        print(f"Processing {len(frames_to_process)} frames...")
        
        summaries = []
        saved_files = []
        
        for i, frame_num in enumerate(frames_to_process):
            if frame_num >= frame_count:
                print(f"Warning: Frame {frame_num} beyond file ({frame_count} frames)")
                continue
            
            y, u, v = read_yuv_frame(f, frame_num)
            if y is None:
                print(f"Error reading frame {frame_num}")
                continue
            
            # Save frame
            filename = save_frame_as_ppm(y, u, v, frame_num, args.output)
            saved_files.append(filename)
            
            # Create summary
            summary = create_frame_summary(y, u, v, frame_num)
            summaries.append(summary)
            print(f"  {summary}")
            
            # Progress indicator
            if len(frames_to_process) > 10 and (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{len(frames_to_process)} frames")
        
        # Save summary file
        summary_file = os.path.join(args.output, "frame_summary.txt")
        with open(summary_file, 'w') as sf:
            sf.write(f"YUV Frame Analysis Summary\n")
            sf.write(f"Source: {args.yuv_file}\n")
            sf.write(f"Total frames: {frame_count}\n")
            sf.write(f"Processed frames: {len(saved_files)}\n")
            sf.write("=" * 60 + "\n\n")
            
            for summary in summaries:
                sf.write(summary + "\n")
        
        print(f"\nComplete! Saved {len(saved_files)} frames to {args.output}/")
        print(f"Frame summary saved to: {summary_file}")
        print(f"\nTo view frames:")
        print(f"  - Open .ppm files with any image viewer")
        print(f"  - Windows: Paint, IrfanView, GIMP")
        print(f"  - Mac: Preview, GIMP")
        print(f"  - Linux: Eye of GNOME, GIMP, ImageMagick")

if __name__ == "__main__":
    main()
