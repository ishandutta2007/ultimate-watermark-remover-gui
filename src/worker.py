import sys
import cv2
import numpy as np
import os
import subprocess


def is_video_file(path):
    video_extensions = (".mp4", ".avi", ".mov", ".mkv")
    return path.lower().endswith(video_extensions)


def is_image_file(path):
    image_extensions = (".png", ".jpg", ".jpeg", ".bmp")
    return path.lower().endswith(image_extensions)


def remove_watermark_from_image_using_template(image_path, mask_path, inpaint_radius=3):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image from {image_path}")
        return

    mask_with_alpha = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    if mask_with_alpha is None:
        print(f"Error: Could not load mask from {mask_path}")
        return

    if mask_with_alpha.shape[2] == 4:  # Check for alpha channel
        # Use the alpha channel as the mask
        _, mask = cv2.threshold(mask_with_alpha[:, :, 3], 1, 255, cv2.THRESH_BINARY)
    else:
        # Fallback to grayscale if no alpha channel
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # Using Telea's method (cv2.INPAINT_TELEA) for potentially better speed
    result = cv2.inpaint(img, mask, inpaint_radius, cv2.INPAINT_TELEA)

    return result


def main():
    """
    A worker function that removes a watermark from an image or video using a provided mask.
    """
    print("Worker process started.")

    if len(sys.argv) < 5:
        print(
            "Error: Missing arguments. Expected: watermark_template_path, watermark_mask_applied_path, media_to_be_edited_path, steps"
        )
        sys.exit(1)

    watermark_template_path = sys.argv[1]  # This will be the watermark template input
    watermark_mask_applied_path = sys.argv[
        2
    ]  # This will be ignored as per user's request
    media_to_be_edited_path = sys.argv[3]  # This will be the image or video input
    steps = int(sys.argv[4])  # Currently not used for image/video processing

    print(f"Watermark template path: {watermark_template_path}")
    print(
        f"Watermark mask (image to be applied) path (ignored): {watermark_mask_applied_path}"
    )
    print(f"Media to be edited path: {media_to_be_edited_path}")
    print(f"Processing steps: {steps}")

    try:
        if media_to_be_edited_path and os.path.exists(media_to_be_edited_path):
            if is_video_file(media_to_be_edited_path):
                print(
                    f"DEBUG: Entering video processing block for {media_to_be_edited_path}"
                )
                cap = cv2.VideoCapture(media_to_be_edited_path)
                if not cap.isOpened():
                    print(
                        f"Error: Could not open video file at {media_to_be_edited_path}"
                    )
                    sys.exit(1)

                frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)  # Use float for FPS
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                print(f"DEBUG: Video total frames: {total_frames}")

                # Create subfolders for frames
                video_basename = os.path.splitext(
                    os.path.basename(media_to_be_edited_path)
                )[0]
                output_frames_dir = os.path.join(
                    os.path.dirname(media_to_be_edited_path), f"{video_basename}_frames"
                )
                original_frames_dir = os.path.join(output_frames_dir, "original_frames")
                unmasked_frames_dir = os.path.join(output_frames_dir, "unmasked_frames")

                os.makedirs(original_frames_dir, exist_ok=True)
                os.makedirs(unmasked_frames_dir, exist_ok=True)
                print(f"DEBUG: Original frames will be saved to: {original_frames_dir}")
                print(f"DEBUG: Unmasked frames will be saved to: {unmasked_frames_dir}")

                output_video_path = media_to_be_edited_path.replace(".", "_unmasked.")
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                out = cv2.VideoWriter(
                    output_video_path, fourcc, fps, (frame_width, frame_height)
                )

                unmasked_frames = 0
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Save original frame
                    original_frame_path = os.path.join(
                        original_frames_dir, f"frame_{unmasked_frames:05d}.jpg"
                    )
                    cv2.imwrite(original_frame_path, frame)

                    unmasked_frame = remove_watermark_from_image_using_template(
                        original_frame_path, watermark_template_path
                    )  # , threshold=tolerance/100.0)
                    if unmasked_frame is not None:
                        out.write(unmasked_frame)
                        # Save unmasked frame
                        unmasked_frame_path = os.path.join(
                            unmasked_frames_dir, f"frame_{unmasked_frames:05d}.jpg"
                        )
                        cv2.imwrite(unmasked_frame_path, unmasked_frame)

                    unmasked_frames += 1
                    if total_frames > 0:
                        progress = int((unmasked_frames / total_frames) * 100)
                        print(f"PROGRESS:{progress}")
                        sys.stdout.flush()

                cap.release()
                out.release()

                # --- Audio Merging Logic ---
                temp_video_path = output_video_path  # The one without audio
                final_video_path_with_audio = temp_video_path.replace(
                    "_unmasked.", "_unmasked_with_audio."
                )
                audio_path = os.path.join(output_frames_dir, "extracted_audio.aac")

                try:
                    # 1. Extract audio from original video
                    extract_command = [
                        "ffmpeg",
                        "-y",
                        "-i",
                        media_to_be_edited_path,
                        "-vn",
                        "-acodec",
                        "copy",
                        audio_path,
                    ]
                    print("DEBUG: Extracting audio...")
                    subprocess.run(extract_command, check=True, capture_output=True)

                    # 2. Combine unmasked video with extracted audio
                    combine_command = [
                        "ffmpeg",
                        "-y",
                        "-i",
                        temp_video_path,
                        "-i",
                        audio_path,
                        "-c:v",
                        "copy",
                        "-c:a",
                        "aac",
                        "-strict",
                        "experimental",
                        final_video_path_with_audio,
                    ]
                    print("DEBUG: Combining video and audio...")
                    subprocess.run(combine_command, check=True, capture_output=True)

                    # 3. Success: cleanup and rename
                    os.remove(temp_video_path)
                    os.remove(audio_path)
                    os.rename(final_video_path_with_audio, output_video_path)
                    print("DEBUG: Audio merged successfully.")

                except (subprocess.CalledProcessError, FileNotFoundError) as e:
                    # ffmpeg might not be installed, or the video might not have audio.
                    # In that case, we will just use the video without audio.
                    print(
                        f"DEBUG: Could not merge audio. Using video without audio. Reason: {e}"
                    )
                    if os.path.exists(final_video_path_with_audio):
                        os.remove(final_video_path_with_audio)
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                    # The output_video_path is already the silent one, so we are good.

                print(f"Unmasked video saved to: {output_video_path}")
                print("PROGRESS:100")
                sys.stdout.flush()

            elif is_image_file(media_to_be_edited_path):
                print(
                    f"DEBUG: Entering image processing block for {media_to_be_edited_path}"
                )
                img = cv2.imread(media_to_be_edited_path)
                if img is None:
                    print(
                        f"Error: Could not open or find the image at {media_to_be_edited_path}"
                    )
                    sys.exit(1)

                unmasked_img = remove_watermark_from_image_using_template(
                    img, watermark_template_path
                )  # , threshold=tolerance/100.0)
                if unmasked_img is not None:
                    output_path = media_to_be_edited_path.replace(".", "_unmasked.")
                    cv2.imwrite(output_path, unmasked_img)
                    print(f"Unmasked image saved to: {output_path}")
                print("PROGRESS:100")
                sys.stdout.flush()
            else:
                print(
                    "Error: Provided path is neither a valid image nor a valid video file."
                )
                sys.exit(1)
        else:
            print(
                "Error: No valid media path provided for processing or path does not exist."
            )
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        sys.exit(1)

    print("Worker process finished successfully.")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
