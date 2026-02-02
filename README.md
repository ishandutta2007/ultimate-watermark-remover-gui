# Ultimate Watermark Remover GUI

A desktop application to remove watermarks from images and videos.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ishandutta2007/ultimate-watermark-remover-gui.git
    cd ultimate-watermark-remover-gui
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **FFmpeg Installation (for video processing):**
    This is required to process videos and to add the audio back to the processed video.

    - Download a precompiled build of FFmpeg (e.g., from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)).
    - Extract the `ffmpeg.exe` binary and place it in the root directory of this project, or make sure it is available in your system's PATH.

## Usage

Run the main application:
```bash
python src/main.py
```

Provide the path to the media you want to edit and the watermark mask image. The application will then process the media and save the output in the same directory as the input file with an `_unmasked` suffix.