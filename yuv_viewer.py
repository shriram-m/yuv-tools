#!/usr/bin/env python3
"""
YUV420 Frame Viewer for H.264 Decoded Video
This script reads the YUV420 planar format output from the H.264 decoder
and displays the frames for visual inspection.

Video Format: YUV420 Planar
Resolution: 736x442 pixels
Layout: Y plane (736×442) + U plane (368×221) + V plane (368×221)
"""

import numpy as np
import cv2
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

def yuv420_to_rgb(y_plane, u_plane, v_plane):
    """
    Convert YUV420 planar format to RGB
    """
    # Reshape planes
    y = y_plane.reshape(VIDEO_HEIGHT, VIDEO_WIDTH)
    u = u_plane.reshape(VIDEO_HEIGHT // 2, VIDEO_WIDTH // 2)
    v = v_plane.reshape(VIDEO_HEIGHT // 2, VIDEO_WIDTH // 2)
    
    # Upsample U and V planes to match Y plane size
    u_upsampled = cv2.resize(u, (VIDEO_WIDTH, VIDEO_HEIGHT), interpolation=cv2.INTER_LINEAR)
    v_upsampled = cv2.resize(v, (VIDEO_WIDTH, VIDEO_HEIGHT), interpolation=cv2.INTER_LINEAR)
    
    # Stack YUV channels
    yuv_image = np.stack([y, u_upsampled, v_upsampled], axis=2).astype(np.uint8)
    
    # Convert YUV to RGB using OpenCV
    rgb_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2RGB)
    
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

def save_frame_as_image(rgb_frame, frame_number, output_dir="frames"):
    """
    Save an RGB frame as a PNG image
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"frame_{frame_number:06d}.png")
    # Convert RGB to BGR for OpenCV
    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, bgr_frame)
    print(f"Saved frame {frame_number} as {filename}")

def analyze_frame_differences(yuv_file, start_frame=0, num_frames=10):
    """
    Analyze differences between consecutive frames to detect tearing or artifacts
    """
    print(f"\nAnalyzing frame differences (frames {start_frame} to {start_frame + num_frames - 1})...")
    
    with open(yuv_file, 'rb') as f:
        prev_frame = None
        
        for i in range(num_frames):
            frame_num = start_frame + i
            y, u, v = read_yuv_frame(f, frame_num)
            
            if y is None:
                print(f"Could not read frame {frame_num}")
                break
                
            current_frame = yuv420_to_rgb(y, u, v)
            
            if prev_frame is not None:
                # Calculate frame difference
                diff = cv2.absdiff(current_frame, prev_frame)
                diff_mean = np.mean(diff)
                diff_max = np.max(diff)
                
                print(f"Frame {frame_num}: Mean diff = {diff_mean:.2f}, Max diff = {diff_max}")
                
                # Save difference image for analysis
                if i < 5:  # Save first few difference images
                    save_frame_as_image(diff, f"{frame_num}_diff", "frame_diffs")
            
            prev_frame = current_frame.copy()

def main():
    parser = argparse.ArgumentParser(description='YUV420 Frame Viewer for H.264 Decoded Video')
    parser.add_argument('yuv_file', help='Path to the YUV file')
    parser.add_argument('--frame', '-f', type=int, default=0, help='Frame number to display (default: 0)')
    parser.add_argument('--play', '-p', action='store_true', help='Play all frames in sequence')
    parser.add_argument('--save', '-s', action='store_true', help='Save frames as PNG images')
    parser.add_argument('--analyze', '-a', action='store_true', help='Analyze frame differences')
    parser.add_argument('--start', type=int, default=0, help='Start frame for analysis/saving')
    parser.add_argument('--count', type=int, default=10, help='Number of frames to process')
    
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
    
    if args.analyze:
        analyze_frame_differences(args.yuv_file, args.start, args.count)
        return
    
    with open(args.yuv_file, 'rb') as f:
        if args.play:
            # Play all frames
            print("Playing frames... Press 'q' to quit, 'p' to pause/resume, 's' to save current frame")
            frame_num = args.start
            paused = False
            
            while frame_num < min(frame_count, args.start + args.count):
                if not paused:
                    y, u, v = read_yuv_frame(f, frame_num)
                    
                    if y is None:
                        print(f"End of file reached at frame {frame_num}")
                        break
                    
                    rgb_frame = yuv420_to_rgb(y, u, v)
                    
                    # Display frame info
                    display_frame = rgb_frame.copy()
                    cv2.putText(display_frame, f"Frame: {frame_num}/{frame_count-1}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    
                    # Convert RGB to BGR for OpenCV display
                    bgr_frame = cv2.cvtColor(display_frame, cv2.COLOR_RGB2BGR)
                    cv2.imshow('YUV Frame Viewer', bgr_frame)
                    
                    if args.save:
                        save_frame_as_image(rgb_frame, frame_num)
                    
                    frame_num += 1
                
                key = cv2.waitKey(100) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('p'):
                    paused = not paused
                    print("Paused" if paused else "Resumed")
                elif key == ord('s') and not paused:
                    save_frame_as_image(rgb_frame, frame_num - 1)
        
        else:
            # Display single frame
            if args.frame >= frame_count:
                print(f"Error: Frame {args.frame} is beyond the available frames (0-{frame_count-1})")
                sys.exit(1)
            
            y, u, v = read_yuv_frame(f, args.frame)
            
            if y is None:
                print(f"Error reading frame {args.frame}")
                sys.exit(1)
            
            rgb_frame = yuv420_to_rgb(y, u, v)
            
            if args.save:
                save_frame_as_image(rgb_frame, args.frame)
            
            # Display the frame
            print(f"Displaying frame {args.frame}. Press any key to close.")
            
            # Add frame info to display
            display_frame = rgb_frame.copy()
            cv2.putText(display_frame, f"Frame: {args.frame}/{frame_count-1}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Convert RGB to BGR for OpenCV display
            bgr_frame = cv2.cvtColor(display_frame, cv2.COLOR_RGB2BGR)
            cv2.imshow('YUV Frame Viewer', bgr_frame)
            cv2.waitKey(0)
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
