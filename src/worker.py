import time
import sys
import cv2
import numpy as np
import os

def remove_watermark_from_frame(frame, mask_path):
    """
    Removes a watermark from a single frame using a provided mask.
    """
    if frame is None:
        return None

    # Load the watermark mask
    mask_img = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask_img is None:
        print(f"Error: Could not open or find the watermark mask at {mask_path}")
        return frame # Return original frame if mask not found

    # Resize mask to match frame dimensions
    mask = cv2.resize(mask_img, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_AREA)

    # Ensure mask is binary (0 or 255)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # Use inpainting to remove the watermark
    dst = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
    return dst

import time
import sys
import cv2
import numpy as np
import os

def is_image_file(path):
    image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
    return path.lower().endswith(image_extensions)

def is_video_file(path):
    video_extensions = (".mp4", ".avi", ".mov", ".mkv")
    return path.lower().endswith(video_extensions)

def remove_watermark_from_frame(frame, mask_path):
    """
    Removes a watermark from a single frame using a provided mask.
    """
    if frame is None:
        return None

    # Load the watermark mask
    mask_img = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask_img is None:
        print(f"Error: Could not open or find the watermark mask at {mask_path}")
        return frame # Return original frame if mask not found

    # Resize mask to match frame dimensions
    mask = cv2.resize(mask_img, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_AREA)

    # Ensure mask is binary (0 or 255)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # Use inpainting to remove the watermark
    dst = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
    return dst

def main():
    """
    A worker function that removes a watermark from an image or video using a provided mask.
    """
    print("Worker process started.")

    if len(sys.argv) < 7:
        print("Error: Missing arguments. Expected: watermark_mask_deleted_path, watermark_mask_applied_path, video_to_be_edited_path, steps, color, tolerance")
        sys.exit(1)

    watermark_mask_deleted_path = sys.argv[1] # This will be the image input
    watermark_mask_applied_path = sys.argv[2]
    video_to_be_edited_path = sys.argv[3] # This will be the video input
    steps = int(sys.argv[4]) # Currently not used for image/video processing
    hex_color = sys.argv[5] # Currently not used for mask based removal
    tolerance = int(sys.argv[6]) # Currently not used for mask based removal

    print(f"Watermark mask (image to be cleaned) path: {watermark_mask_deleted_path}")
    print(f"Watermark mask (mask image) path: {watermark_mask_applied_path}")
    print(f"Video to be edited path: {video_to_be_edited_path}")
    print(f"Processing steps: {steps}")
    print(f"Color received: {hex_color}")
    print(f"Tolerance received: {tolerance}")

    color = (255, 255, 255)  # Default to white
    hex_color = hex_color.lstrip('#')
    try:
        color = tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))
    except ValueError:
        print("Invalid color format. Using default color (white).")


    try:
        if video_to_be_edited_path and os.path.exists(video_to_be_edited_path) and is_video_file(video_to_be_edited_path):
            print(f"DEBUG: Entering video processing block for {video_to_be_edited_path}")
            cap = cv2.VideoCapture(video_to_be_edited_path)
            if not cap.isOpened():
                print(f"Error: Could not open video file at {video_to_be_edited_path}")
                sys.exit(1)

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS) # Use float for FPS
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"DEBUG: Video total frames: {total_frames}")
            
            # Create subfolders for frames
            video_basename = os.path.splitext(os.path.basename(video_to_be_edited_path))[0]
            output_frames_dir = os.path.join(os.path.dirname(video_to_be_edited_path), f"{video_basename}_frames")
            original_frames_dir = os.path.join(output_frames_dir, "original_frames")
            processed_frames_dir = os.path.join(output_frames_dir, "processed_frames")

            os.makedirs(original_frames_dir, exist_ok=True)
            os.makedirs(processed_frames_dir, exist_ok=True)
            print(f"DEBUG: Original frames will be saved to: {original_frames_dir}")
            print(f"DEBUG: Processed frames will be saved to: {processed_frames_dir}")


            output_video_path = video_to_be_edited_path.replace(".", "_processed.")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

            processed_frames = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Save original frame
                original_frame_path = os.path.join(original_frames_dir, f"frame_{processed_frames:05d}.jpg")
                cv2.imwrite(original_frame_path, frame)

                processed_frame = remove_watermark_from_frame(frame, watermark_mask_applied_path)
                if processed_frame is not None:
                    out.write(processed_frame)
                    # Save processed frame
                    processed_frame_path = os.path.join(processed_frames_dir, f"frame_{processed_frames:05d}.jpg")
                    cv2.imwrite(processed_frame_path, processed_frame)
                
                processed_frames += 1
                if total_frames > 0: 
                    progress = int((processed_frames / total_frames) * 100)
                    print(f"PROGRESS:{progress}")
                    sys.stdout.flush()
                
            cap.release()
            out.release()
            print(f"Processed video saved to: {output_video_path}")
            print("PROGRESS:100")
            sys.stdout.flush()
        
        elif watermark_mask_deleted_path and os.path.exists(watermark_mask_deleted_path) and is_image_file(watermark_mask_deleted_path):
            print(f"DEBUG: Entering image processing block for {watermark_mask_deleted_path}")
            img = cv2.imread(watermark_mask_deleted_path)
            if img is None:
                print(f"Error: Could not open or find the image at {watermark_mask_deleted_path}")
                sys.exit(1)
            
            processed_img = remove_watermark_from_frame(img, watermark_mask_applied_path)
            if processed_img is not None:
                output_path = watermark_mask_deleted_path.replace(".", "_processed.")
                cv2.imwrite(output_path, processed_img)
                print(f"Processed image saved to: {output_path}")
            print("PROGRESS:100")
            sys.stdout.flush()

        else:
            print("Error: No valid image or video path provided for processing.")
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        sys.exit(1)

    print("Worker process finished successfully.")
    sys.stdout.flush()

if __name__ == "__main__":
    main()

