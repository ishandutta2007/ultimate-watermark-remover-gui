import time
import sys
import cv2
import numpy as np

def main():
    """
    A worker function that removes a watermark from an image.
    """
    print("Worker process started.")
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"File path received: {file_path}")
    else:
        print("No file path received.")
        sys.exit(1)

    color = (255, 255, 255)  # Default to white
    if len(sys.argv) > 3:
        hex_color = sys.argv[3]
        print(f"Color received: {hex_color}")
        hex_color = hex_color.lstrip('#')
        try:
            color = tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))
        except ValueError:
            print("Invalid color format. Using default color (white).")

    tolerance = 10
    if len(sys.argv) > 4:
        try:
            tolerance = int(sys.argv[4])
            print(f"Tolerance received: {tolerance}")
        except ValueError:
            print("Invalid tolerance value. Using default value (10).")


    try:
        # Load the image
        img = cv2.imread(file_path)
        if img is None:
            print(f"Error: Could not open or find the image at {file_path}")
            sys.exit(1)

        # Create a mask of the watermark
        lower = np.array([max(0, c - tolerance) for c in color], dtype=np.uint8)
        upper = np.array([min(255, c + tolerance) for c in color], dtype=np.uint8)
        mask = cv2.inRange(img, lower, upper)

        # Use inpainting to remove the watermark
        dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

        # Save the processed image
        output_path = file_path.replace(".", "_processed.")
        cv2.imwrite(output_path, dst)
        print(f"Processed image saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred during image processing: {e}")
        sys.exit(1)

    print("Worker process finished successfully.")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
