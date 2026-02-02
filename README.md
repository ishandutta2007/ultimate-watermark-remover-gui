# Ultimate Watermark Remover GUI - Free & Open-Source Image and Video Watermark Removal Tool

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Goals & Technology Stack](#goals--technology-stack)
- [Installation Guide](#installation-guide)
  - [Prerequisites](#prerequisites)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Install Python Dependencies](#step-2-install-python-dependencies)
  - [Step 3: FFmpeg Installation (Crucial for Video)](#step-3-ffmpeg-installation-crucial-for-video)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Project Overview
Tired of unwanted watermarks diminishing the quality of your cherished photos and videos? The **Ultimate Watermark Remover GUI** is a powerful, user-friendly, and completely free open-source desktop application designed to seamlessly remove watermarks from both images and videos. Built with Python and PySide6, this tool offers a robust solution for content creators, photographers, and anyone needing to clean up their media files. Whether it's a logo, text, or any intrusive overlay, our advanced processing engine, powered by OpenCV and FFmpeg, helps you achieve clean, watermark-free results.

## Key Features
*   **Intelligent Watermark Removal**: Utilizes advanced image processing techniques (OpenCV inpainting) to effectively remove watermarks based on a provided mask or template.
*   **Image Processing**: Effortlessly remove watermarks from your `.png`, `.jpg`, `.jpeg`, `.bmp`, and `.gif` image files.
*   **Video Watermark Removal**: Clean watermarks from video formats such as `.mp4`, `.avi`, `.mov`, and `.mkv` by processing frame-by-frame.
*   **Audio Preservation**: Crucially, for video processing, the original audio track is automatically extracted and seamlessly re-merged with the watermark-free video, ensuring your content remains complete.
*   **Intuitive Graphical User Interface (GUI)**: A modern, dark-themed interface built with PySide6 provides a straightforward experience for selecting media and watermark templates.
*   **Cross-Platform Compatibility**: Developed in Python, this application is designed to run on various operating systems, including Windows, macOS, and Linux.
*   **Open-Source & Free**: Absolutely free to use, modify, and distribute. Empower yourself with a powerful tool without any hidden costs.
*   **Detailed Progress Tracking**: Real-time progress updates in the GUI, showing distinct stages of video processing (frame extraction, unmasking, audio handling, merging).

## Goals & Technology Stack
The primary goal of the **Ultimate Watermark Remover GUI** is to provide a reliable, efficient, and accessible tool for watermark removal. We aim to empower users with the ability to restore the pristine quality of their visual content.

This application is built upon a robust technology stack:
*   **Python**: The core programming language.
*   **PySide6**: For creating the responsive and modern graphical user interface.
*   **OpenCV (Open Source Computer Vision Library)**: The powerhouse behind image and video frame processing, specifically for watermark detection and inpainting.
*   **FFmpeg**: The essential command-line tool for high-performance video and audio manipulation, used for extracting audio, merging video streams, and ensuring broad format compatibility.

## Installation Guide

### Prerequisites
Before you begin, ensure you have:
*   **Python 3.11.4** installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
*   Basic command-line knowledge.

### Step 1: Clone the Repository
Open your terminal or command prompt and clone the project:
```bash
git clone https://github.com/ishandutta2007/ultimate-watermark-remover-gui.git
cd ultimate-watermark-remover-gui
```

### Step 2: Install Python Dependencies
Navigate to the project directory and install the required Python libraries using pip:
```bash
pip install -r requirements.txt
```
*Note: For Windows users, you can use the `install_packages.bat` script in the root directory to automate this step and check for FFmpeg.*

### Step 3: FFmpeg Installation (Crucial for Video)
**FFmpeg is absolutely critical for video watermark removal and audio re-integration.** Without it, the application can only process images.

*   **Download FFmpeg**:
    *   For **Windows**: Download a precompiled build from [Gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/). Choose the "release essentials" or "full" build.
    *   For **macOS**: Install via Homebrew: `brew install ffmpeg` or download binaries from [FFmpeg.org](https://ffmpeg.org/download.html).
    *   For **Linux**: Install via your package manager (e.g., `sudo apt install ffmpeg` for Debian/Ubuntu, `sudo pacman -S ffmpeg` for Arch).

*   **Configure PATH (or place executable)**:
    *   **Recommended**: Add the directory containing the `ffmpeg` executable (e.g., `ffmpeg.exe` on Windows) to your system's PATH environment variable. This allows the application to find FFmpeg from any location.
    *   **Alternative (Windows only)**: Place the `ffmpeg.exe` file directly into the root directory of this project (`ultimate-watermark-remover-gui/`).

## Usage
To launch the application, navigate to the project's root directory in your terminal or command prompt and run:
```bash
python src/main.py
```
The GUI will open, allowing you to:
1.  **Select the Watermark Template**: Choose an image file that represents the watermark you want to remove. This mask helps the application identify the watermark.
2.  **Select the Media to be Edited**: Browse for your image or video file (`.png`, `.jpg`, `.mp4`, etc.).
3.  **Start Processing**: Click the "Start Processing" button.

The application will display real-time logs and progress updates. Once complete, the watermark-free file will be saved in the same directory as your original media, appended with `_unmasked`.

## How It Works
The **Ultimate Watermark Remover GUI** employs a multi-stage process for watermark removal:

1.  **Input & Masking**: The user provides the media file and a watermark template (mask). This mask is crucial for OpenCV's inpainting algorithm to accurately identify and remove the unwanted elements.
2.  **Video Frame Extraction (for Videos)**: If a video file is provided, it is first decomposed into individual frames. Each frame is treated as a static image.
3.  **Watermark Inpainting**: For each frame (or the single image), OpenCV's inpainting algorithm is applied using the provided mask. This intelligently reconstructs the masked area based on surrounding pixels, effectively "erasing" the watermark.
4.  **Audio Extraction & Re-integration (for Videos)**: Concurrently, if a video was processed, FFmpeg extracts the original audio track. After all video frames are unmasked and reassembled into a new silent video, FFmpeg then precisely merges this new video stream with the preserved original audio track.
5.  **Output**: The final watermark-free image or video (with audio, if applicable) is saved, ready for use.

## Contributing
We welcome contributions from the community! If you have suggestions, bug reports, or would like to contribute code, please feel free to:
*   Open an issue on the [GitHub repository](https://github.com/ishandutta2007/ultimate-watermark-remover-gui/issues).
*   Submit a Pull Request with your proposed changes.

Please ensure your code adheres to the project's style and quality standards.

## License
This project is released under the [MIT License](LICENSE).

## Support
For any questions, issues, or feedback, please visit our [GitHub Issues page](https://github.com/ishandutta2007/ultimate-watermark-remover-gui/issues). We're here to help!


### ✨ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ishandutta2007/ultimate-watermark-remover-gui&type=date&legend=top-left)](https://www.star-history.com/#ishandutta2007/ultimate-watermark-remover-gui&type=date&legend=top-left)


