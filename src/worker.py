import time
import sys

def main():
    """
    A simple worker function that simulates a multi-step process.
    It prints its progress to stdout and flushes the buffer to ensure
    the parent process receives the messages in real-time.
    """
    print("Worker process started.")
    sys.stdout.flush()

    for i in range(5):
        print(f"Processing step {i + 1}/5...")
        sys.stdout.flush()
        time.sleep(1)

    print("Worker process finished successfully.")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
