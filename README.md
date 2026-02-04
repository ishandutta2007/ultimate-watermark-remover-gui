# 🌟 Ultimate Watermark Remover GUI 🌟
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.11.4-blue.svg)](https://www.python.org/downloads/release/python-3114/)
[![Built with PySide6](https://img.shields.io/badge/Built_with-PySide6-green.svg)](https://doc.qt.io/qtforpython/PySide6/index.html)
[![Powered by OpenCV](https://img.shields.io/badge/Powered_by-OpenCV-orange.svg)](https://opencv.org/)
[![Uses FFmpeg](https://img.shields.io/badge/Uses-FFmpeg-red.svg)](https://ffmpeg.org/)
[![GitHub Stars](https://img.shields.io/github/stars/ishandutta2007/ultimate-watermark-remover-gui?style=social)](https://github.com/ishandutta2007/ultimate-watermark-remover-gui/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ishandutta2007/ultimate-watermark-remover-gui?style=social)](https://github.com/ishandutta2007/ultimate-watermark-remover-gui/network/members)

---

## 🚀 Project Overview
Tired of intrusive watermarks degrading your precious photos and videos? The **Ultimate Watermark Remover GUI** is your go-to, powerful, and absolutely **free open-source desktop application**! 🚀 Designed with simplicity and efficiency in mind, it seamlessly erases unwanted watermarks from both images and videos.

Built with Python and PySide6, this intuitive tool provides a robust solution for content creators, photographers, and anyone looking to enhance their media. Whether it's a pesky logo, distracting text, or any overlay, our advanced processing engine, powered by the mighty 🧠 **OpenCV** and versatile 🎬 **FFmpeg**, delivers pristine, watermark-free results.

---

## ✨ Key Features

-   **Intelligent Watermark Removal** 🎨: Leveraging cutting-edge OpenCV inpainting algorithms, our tool expertly identifies and reconstructs areas covered by watermarks, ensuring natural-looking results.
-   **Broad Image Support** 🖼️: Process popular image formats including `.png`, `.jpg`, `.jpeg`, `.bmp`, and `.gif` with ease.
-   **Seamless Video Cleaning** 🎥: Remove watermarks from your favorite video formats suchs as `.mp4`, `.avi`, `.mov`, and `.mkv` through efficient frame-by-frame processing.
-   **Automatic Audio Preservation** 🎧: For video processing, the original audio track is intelligently extracted and perfectly re-merged with your watermark-free video, keeping your content's integrity intact.
-   **Modern & Intuitive GUI** 🖥️: Enjoy a sleek, dark-themed interface crafted with PySide6, offering a straightforward and pleasant user experience for all your media cleaning tasks.
-   **Cross-Platform Power** 🌐: Written in Python, this application runs smoothly across Windows, macOS, and Linux environments.
-   **100% Open-Source & Free** 💖: Empower yourself with a high-quality tool at no cost. Modify, distribute, and contribute freely!
-   **Granular Progress Tracking** 📈: Stay informed with real-time updates showcasing distinct processing stages:
    *   **Extracting frames** 🎞️
    *   **Unmasking each frame** ✨
    *   **Extracting audio** 🎤
    *   **Consolidating video and audio** 🔗

---

## 🎯 Goals

Our core mission with the **Ultimate Watermark Remover GUI** is to offer an accessible, reliable, and highly efficient solution for watermark removal. We're dedicated to helping users restore the original beauty of their visual content.

---

## 💻 Installation

For detailed setup instructions, including Python environment configuration, FFmpeg installation, and building from source, please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) guide.

---

## ▶️ Usage

To launch the **Ultimate Watermark Remover GUI** from source, navigate to the project's root directory in your terminal or command prompt and run:
```bash
python src/main.py
```

### 🖼️ See it in action!
*(**TODO**: Insert a GIF demonstrating the application's usage here.
A short GIF showing:
1.  Opening the app.
2.  Selecting a media file (image or video).
3.  Selecting a watermark mask.
4.  Clicking "Start Processing".
5.  Showing the progress bar and stage updates.
6.  Briefly showing the output.
This will greatly enhance user understanding and engagement!)*

Once the GUI appears, follow these simple steps:
1.  **Select Watermark Template** 🏷️: Provide an image file that serves as a mask for the watermark you wish to remove. This guides the application in identifying the target.
2.  **Select Media to be Edited** 📁: Choose your target image or video file (e.g., `.png`, `.jpg`, `.mp4`, etc.).
3.  **Start Processing** ▶️: Click the dedicated "Start Processing" button.

Observe the real-time logs and dynamic progress updates. Upon completion, your watermark-free file will be conveniently saved in the same directory as your original media, clearly identified with an `_unmasked` suffix.

---

## 🚀 Getting Started

### Non-Technical Users (Pre-built Executables) 🎁

If you're not comfortable with command-line tools or Python environments, pre-built, ready-to-use executable files (like `UltimateWatermarkRemover_v2.0.0.exe`) for Windows are available directly from the project's [GitHub Releases page](https://github.com/ishandutta2007/ultimate-watermark-remover-gui/releases). Simply download the latest version, extract it, and double-click the executable to launch the application!

### Developers & Contributors

For setup, installation from source, and building instructions, please see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## ⚙️ How It Works

The **Ultimate Watermark Remover GUI** orchestrates a sophisticated, multi-stage process to achieve impeccable watermark removal:

1.  **Input & Precise Masking** 🎯: You provide both the media file and a crucial watermark template (mask). This mask is instrumental for OpenCV's inpainting algorithm, ensuring accurate identification and removal of unwanted elements.
2.  **Intelligent Video Frame Extraction** (for Videos) 🎞️: When a video file is supplied, it's meticulously broken down into its constituent frames. Each frame is then treated as an individual image for processing.
3.  **Advanced Watermark Inpainting** ✨: For every frame (or the standalone image), OpenCV's powerful inpainting algorithm is applied using the provided mask. This intelligently reconstructs the masked area based on surrounding pixel data, effectively "erasing" the watermark seamlessly.
4.  **Flawless Audio Extraction & Re-integration** (for Videos) 🎤🔗: Simultaneously, if a video is being processed, FFmpeg efficiently extracts its original audio track. Once all video frames are unmasked and reassembled into a new silent video, FFmpeg then precisely merges this pristine video stream with the preserved original audio track, ensuring perfect synchronization.
5.  **Clean Output** ✅: The final, watermark-free image or video (complete with audio, if applicable) is then saved, ready for immediate use.

---

## 🤝 Contributing

Your contributions make this project even better! We warmly welcome ideas, bug reports, and code contributions. Here's how you can help:
*   **Report Issues** 🐞: Open an issue on our [GitHub repository](https://github.com/ishandutta2007/ultimate-watermark-remover-gui/issues) for any bugs, suggestions, or feature requests.
*   **Submit Pull Requests** 💡: Share your improvements by submitting a Pull Request. Please ensure your code aligns with our project's coding standards.

---

## 📄 License
This project is proudly released under the generous [MIT License](LICENSE). Feel free to explore, modify, and innovate!

---

## ❓ Support

Got questions? Encountered a snag? Need assistance?
Please visit our [GitHub Issues page](https://github.com/ishandutta2007/ultimate-watermark-remover-gui/issues) for help and discussions. We're here to support you!


---

### ✨ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ishandutta2007/ultimate-watermark-remover-gui&type=date&legend=top-left)](https://www.star-history.com/#ishandutta2007/ultimate-watermark-remover-gui&type=date&legend=top-left)
