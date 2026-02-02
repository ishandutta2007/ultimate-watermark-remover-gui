import time
import sys

def main():
    """
    A simple worker function that simulates a multi-step process.
    It prints its progress to stdout and flushes the buffer to ensure
    the parent process receives the messages in real-time.
    """
    print("Worker process started.")
    steps = 5
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"File path received: {file_path}")
    else:
        print("No file path received.")
    
    if len(sys.argv) > 2:
        try:
            steps = int(sys.argv[2])
            print(f"Number of steps: {steps}")
        except ValueError:
            print("Invalid number of steps. Using default value (5).")

    sys.stdout.flush()

    for i in range(steps):
        print(f"Processing step {i + 1}/{steps}...")
        sys.stdout.flush()
        time.sleep(1)

    print("Worker process finished successfully.")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
