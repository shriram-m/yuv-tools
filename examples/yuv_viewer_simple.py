#!/usr/bin/env python3
"""
Simple YUV420 Frame Viewer using matplotlib
Alternative viewer that doesn't require OpenCV installation.
"""

import numpy as np
import matplotlib.pyplot as plt
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

def yuv420_to_rgb_simple(y_plane, u_plane, v_plane):
    """
    Convert YUV420 planar format to RGB using simple upsampling
    """
    # Reshape planes
    y = y_plane.reshape(VIDEO_HEIGHT, VIDEO_WIDTH).astype(np.float32)
    u = u_plane.reshape(VIDEO_HEIGHT // 2, VIDEO_WIDTH // 2).astype(np.float32)
    v = v_plane.reshape(VIDEO_HEIGHT // 2, VIDEO_WIDTH // 2).astype(np.float32)
    
    # Simple nearest neighbor upsampling for U and V
    u_upsampled = np.repeat(np.repeat(u, 2, axis=0), 2, axis=1)
    v_upsampled = np.repeat(np.repeat(v, 2, axis=0), 2, axis=1)
    
    # Ensure dimensions match
    u_upsampled = u_upsampled[:VIDEO_HEIGHT, :VIDEO_WIDTH]
    v_upsampled = v_upsampled[:VIDEO_HEIGHT, :VIDEO_WIDTH]
    
    # YUV to RGB conversion (ITU-R BT.601)
    r = y + 1.402 * (v_upsampled - 128)
    g = y - 0.344136 * (u_upsampled - 128) - 0.714136 * (v_upsampled - 128)
    b = y + 1.772 * (u_upsampled - 128)
    
    # Clip values to [0, 255]
    rgb_image = np.stack([
        np.clip(r, 0, 255),
        np.clip(g, 0, 255),
        np.clip(b, 0, 255)
    ], axis=2).astype(np.uint8)
    
    return rgb_image

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
    
    # Convert to numpy array
    frame_array = np.frombuffer(frame_data, dtype=np.uint8)
    
    # Split into Y, U, V planes
    y_plane = frame_array[:Y_SIZE]
    u_plane = frame_array[Y_SIZE:Y_SIZE + UV_SIZE]
    v_plane = frame_array[Y_SIZE + UV_SIZE:Y_SIZE + 2 * UV_SIZE]
    
    return y_plane, u_plane, v_plane

def get_frame_count(filename):
    """
    Calculate the number of frames in the YUV file
    """
    file_size = os.path.getsize(filename)
    return file_size // FRAME_SIZE

def analyze_frame_planes(y, u, v, frame_number):
    """
    Analyze individual Y, U, V planes for debugging
    """
    print(f"\nFrame {frame_number} Analysis:")
    print(f"Y plane - Min: {np.min(y)}, Max: {np.max(y)}, Mean: {np.mean(y):.2f}")
    print(f"U plane - Min: {np.min(u)}, Max: {np.max(u)}, Mean: {np.mean(u):.2f}")
    print(f"V plane - Min: {np.min(v)}, Max: {np.max(v)}, Mean: {np.mean(v):.2f}")

def display_frame_components(y, u, v, frame_number):
    """
    Display Y, U, V planes separately and the combined RGB image
    """
    # Create RGB image
    rgb_image = yuv420_to_rgb_simple(y, u, v)
    
    # Create subplot layout
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Frame {frame_number} - YUV Components and RGB Result', fontsize=14)
    
    # Y plane (luminance)
    y_reshaped = y.reshape(VIDEO_HEIGHT, VIDEO_WIDTH)
    axes[0, 0].imshow(y_reshaped, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title('Y Plane (Luminance)')
    axes[0, 0].axis('off')
    
    # U plane (chroma)
    u_reshaped = u.reshape(VIDEO_HEIGHT // 2, VIDEO_WIDTH // 2)
    axes[0, 1].imshow(u_reshaped, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title('U Plane (Chroma)')
    axes[0, 1].axis('off')
    
    # V plane (chroma)
    v_reshaped = v.reshape(VIDEO_HEIGHT // 2, VIDEO_WIDTH // 2)
    axes[1, 0].imshow(v_reshaped, cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title('V Plane (Chroma)')
    axes[1, 0].axis('off')
    
    # RGB result
    axes[1, 1].imshow(rgb_image)
    axes[1, 1].set_title('RGB Result')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.show()

def save_frame_analysis(y, u, v, frame_number, output_dir="frame_analysis"):
    """
    Save frame analysis as images
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Save individual planes
    y_reshaped = y.reshape(VIDEO_HEIGHT, VIDEO_WIDTH)
    plt.figure(figsize=(8, 6))
    plt.imshow(y_reshaped, cmap='gray', vmin=0, vmax=255)
    plt.title(f'Frame {frame_number} - Y Plane')
    plt.colorbar()
    plt.savefig(os.path.join(output_dir, f'frame_{frame_number:06d}_Y.png'))
    plt.close()
    
    # Save RGB result
    rgb_image = yuv420_to_rgb_simple(y, u, v)
    plt.figure(figsize=(8, 6))
    plt.imshow(rgb_image)
    plt.title(f'Frame {frame_number} - RGB')
    plt.axis('off')
    plt.savefig(os.path.join(output_dir, f'frame_{frame_number:06d}_RGB.png'))
    plt.close()
    
    print(f"Saved analysis for frame {frame_number}")

def main():
    parser = argparse.ArgumentParser(description='Simple YUV420 Frame Viewer')
    parser.add_argument('yuv_file', help='Path to the YUV file')
    parser.add_argument('--frame', '-f', type=int, default=0, help='Frame number to display')
    parser.add_argument('--components', '-c', action='store_true', help='Show Y, U, V components separately')
    parser.add_argument('--analyze', '-a', action='store_true', help='Print frame analysis')
    parser.add_argument('--save', '-s', action='store_true', help='Save frame analysis')
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
            
            y, u, v = read_yuv_frame(f, frame_num)
            
            if y is None:
                print(f"Error reading frame {frame_num}")
                continue
            
            if args.analyze:
                analyze_frame_planes(y, u, v, frame_num)
            
            if args.save:
                save_frame_analysis(y, u, v, frame_num)
            
            if args.components:
                display_frame_components(y, u, v, frame_num)
            else:
                # Simple RGB display
                rgb_image = yuv420_to_rgb_simple(y, u, v)
                
                plt.figure(figsize=(10, 8))
                plt.imshow(rgb_image)
                plt.title(f'Frame {frame_num} - RGB (Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT})')
                plt.axis('off')
                
                if len(frames_to_process) == 1:
                    plt.show()
                else:
                    plt.savefig(f'frame_{frame_num:06d}.png', bbox_inches='tight', dpi=150)
                    plt.close()
                    print(f"Saved frame_{frame_num:06d}.png")

if __name__ == "__main__":
    main()
