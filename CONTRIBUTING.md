# 🤝 Contributing to Ultimate Watermark Remover GUI

Thank you for your interest in contributing! This document covers setup, development, and build instructions for developers and contributors.

---

## 🛠️ Technology Stack

Before getting started, familiarize yourself with our core technologies:

-   **Python**: The versatile programming language underpinning the entire application.
-   **PySide6**: Powers the responsive, modern, and cross-platform graphical user interface.
-   **OpenCV (Open Source Computer Vision Library)**: The intelligent core for all image and video frame manipulation, specializing in watermark detection and sophisticated inpainting.
-   **FFmpeg**: The indispensable command-line utility for high-performance video and audio handling, enabling seamless audio extraction, precise video stream merging, and extensive format compatibility.

---

## ⚡️ Installation Guide

### 📋 Prerequisites

Before diving in, ensure you have:
*   **Python 3.11.4** installed. Download it from the official [Python website](https://www.python.org/downloads/).
*   Basic familiarity with command-line operations.

### Step 1: Clone the Repository 📥

Open your terminal or command prompt and fetch the project:
```bash
git clone https://github.com/ishandutta2007/ultimate-watermark-remover-gui.git
cd ultimate-watermark-remover-gui
```

### Step 2: Install Python Dependencies 🐍

Navigate to the project directory and install the necessary Python libraries:
```bash
pip install -r requirements.txt
```

*✨ **Pro Tip for Windows Users**: Execute `install_packages.bat` located in the root directory. This script automates dependency installation and verifies FFmpeg presence for a smoother setup.*

### Step 3: FFmpeg Installation (Crucial for Video Processing!) 🎬

**FFmpeg is absolutely essential for video watermark removal and seamless audio re-integration. Without it, the application will only be able to process images.**

*   **Download FFmpeg**:
    *   For **Windows**: Grab a precompiled build from [Gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/). We recommend the "release essentials" or "full" version.
    *   For **macOS**: Install effortlessly via Homebrew: `brew install ffmpeg`. Alternatively, download binaries from [FFmpeg.org](https://ffmpeg.org/download.html).
    *   For **Linux**: Install using your distribution's package manager (e.g., `sudo apt install ffmpeg` for Debian/Ubuntu, `sudo pacman -S ffmpeg` for Arch).

*   **Configure PATH (Highly Recommended)**:
    *   **Best Practice**: Add the directory containing the `ffmpeg` executable (e.g., `ffmpeg.exe` on Windows) to your system's PATH environment variable. This allows the application to locate FFmpeg from any working directory.
    *   **Windows Alternative**: For convenience, you can place the `ffmpeg.exe` file directly into the root directory of this project (`ultimate-watermark-remover-gui/`).

---

## ▶️ Running from Source

To launch the **Ultimate Watermark Remover GUI** from source, navigate to the project's root directory in your terminal or command prompt and run:

```bash
python src/main.py
```

---

## 📦 Building Executables

For users who prefer to run the application as a standalone executable on Windows, the project can be bundled using [PyInstaller](https://pyinstaller.org/). This creates a double-clickable `.exe` file that includes all necessary Python dependencies, removing the need for a local Python installation or manual dependency setup for end-users.

### Building the Executable:

1.  **Ensure PyInstaller is installed**:
    ```bash
    pip install pyinstaller
    ```

2.  **Navigate to the project root** in your terminal.

3.  **Run PyInstaller**: Use the following command to create a one-folder bundle (recommended for PySide6 apps) with your application:
    ```bash
    pyinstaller UltimateWatermarkRemover.spec
    ```
    
    Or use the manual command:
    ```bash
    pyinstaller --noconfirm --onedir --windowed --add-data "masks;masks" --add-data "videos;videos" --add-data "__version__.py;." --name "Ultimate Watermark Remover" src/main.py
    ```
    
    Command options:
    *   `--noconfirm`: Overwrites previous builds without prompt.
    *   `--onedir`: Creates a single directory containing the executable and all its dependencies.
    *   `--windowed`: Prevents a console window from appearing with the GUI.
    *   `--add-data "masks;masks"`: Includes the `masks` directory.
    *   `--add-data "videos;videos"`: Includes the `videos` directory.
    *   `--add-data "__version__.py;."`: Explicitly adds the version file.
    *   `--name "Ultimate Watermark Remover"`: Sets the name of the executable and its containing folder.

4.  **Find the executable**: The generated application will be located in the `dist/Ultimate Watermark Remover/` directory.

---

## 🐛 Reporting Issues & Contributing

Your contributions make this project even better! We warmly welcome ideas, bug reports, and code contributions.

### How to Contribute:

*   **Report Issues** 🐞: Open an issue on our [GitHub repository](https://github.com/ishandutta2007/ultimate-watermark-remover-gui/issues) for any bugs, suggestions, or feature requests.

*   **Submit Pull Requests** 💡: Share your improvements by submitting a Pull Request. Please ensure your code aligns with our project's coding standards.

*   **Code Standards**: When contributing code:
    - Write clear, concise commit messages
    - Add comments only where necessary for clarity
    - Follow existing code style and conventions
    - Test your changes before submitting

---

## 📚 Project Structure

Understanding the project layout will help you contribute effectively:

- `src/main.py` - Main application entry point
- `src/` - Source code directory
- `masks/` - Example watermark mask files
- `videos/` - Example video files
- `models/` - Machine learning models (if applicable)
- `requirements.txt` - Python package dependencies
- `UltimateWatermarkRemover.spec` - PyInstaller specification file
- `install_packages.bat` - Windows installation helper script

---

## 📄 License

When contributing, remember that your contributions will be part of this project, which is released under the [MIT License](LICENSE).

---

## ❓ Need Help?

If you have questions about contributing, please visit our [GitHub Issues page](https://github.com/ishandutta2007/ultimate-watermark-remover-gui/issues) for help and discussions. We're here to support you!
