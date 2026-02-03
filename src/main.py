import os
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QFileDialog,
    QHBoxLayout,
    QSpinBox,
    QLabel,
    QProgressBar,
)
from PySide6.QtCore import QProcess, Qt

# Add the project root to sys.path to allow importing __version__.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from __version__ import __version__


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"Ultimate Watermark Remover - v{__version__}")
        self.setGeometry(100, 100, 600, 400)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # File input for "watermark mask to be deleted" (now watermark mask)
        (
            self.watermark_mask_deleted_layout,
            self.watermark_mask_deleted_path_display,
            self.watermark_mask_deleted_browse_button,
        ) = self._create_file_input(
            "watermark mask:",
            "Select image file (e.g., .jpg, .png)...",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)",
        )
        self.watermark_mask_deleted_path_display.setText("masks/notebookllm_mask.png")

        # File input for "video to be edited" (now media to be edited)
        (
            self.video_to_be_edited_layout,
            self.video_to_be_edited_path_display,
            self.video_to_be_edited_browse_button,
        ) = self._create_file_input(
            "media to be edited:",
            "Select video or image file (e.g., .mp4, .avi, .jpg, .png)...",
            "Media Files (*.mp4 *.avi *.mov *.mkv *.png *.jpg *.jpeg *.bmp *.gif)",
        )
        self.video_to_be_edited_path_display.setText("videos/sample_video.mp4")

        # Progress label
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignCenter)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # UI Elements
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setPlaceholderText(
            "Output from the script will appear here..."
        )

        self.start_button = QPushButton("Start Processing")

        # Add widgets to layout
        self.layout.addLayout(self.video_to_be_edited_layout)  # Now media to be edited
        self.layout.addLayout(self.watermark_mask_deleted_layout)  # Now watermark mask
        self.layout.addWidget(self.progress_label)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.log_display)
        self.layout.addWidget(self.start_button)

        # QProcess setup
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)

        # Connect signals
        self.watermark_mask_deleted_browse_button.clicked.connect(
            lambda: self.open_file_dialog(
                self.watermark_mask_deleted_path_display,
                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)",
            )
        )
        self.video_to_be_edited_browse_button.clicked.connect(
            lambda: self.open_file_dialog(
                self.video_to_be_edited_path_display,
                "Media Files (*.mp4 *.avi *.mov *.mkv *.png *.jpg *.jpeg *.bmp *.gif)",
            )
        )
        self.start_button.clicked.connect(self.start_worker_process)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.finished.connect(self.handle_finished)
        self.process.errorOccurred.connect(self.handle_error)

    def _create_file_input(self, label_text, placeholder_text, file_filter):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        path_display = QLineEdit()
        path_display.setPlaceholderText(placeholder_text)
        browse_button = QPushButton("Browse")

        layout.addWidget(label)
        layout.addWidget(path_display)
        layout.addWidget(browse_button)
        return layout, path_display, browse_button

    def open_file_dialog(self, path_display_widget, file_filter):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a File", "", file_filter
        )
        if file_path:
            path_display_widget.setText(file_path)

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def start_worker_process(self):
        watermark_template_path = self.watermark_mask_deleted_path_display.text()
        media_to_be_edited_path = self.video_to_be_edited_path_display.text()

        # Simplified check for demonstration. In a real app, you might want more robust validation.
        is_image_processing = watermark_template_path and self.is_image_file(
            watermark_template_path
        )
        is_video_processing = media_to_be_edited_path and self.is_video_file(
            media_to_be_edited_path
        )

        if not (watermark_template_path and media_to_be_edited_path):
            self.log_display.append(
                "Please select both a watermark mask and a media file to be edited."
            )
            return

        # Check if paths are valid files
        if not (
            os.path.exists(watermark_template_path)
            and (self.is_image_file(watermark_template_path))
        ):
            self.log_display.append(
                "Please provide a valid image file for the watermark mask."
            )
            return
        if not (
            os.path.exists(media_to_be_edited_path)
            and (
                self.is_image_file(media_to_be_edited_path)
                or self.is_video_file(media_to_be_edited_path)
            )
        ):
            self.log_display.append(
                "Please provide a valid image or video file for media to be edited."
            )
            return

        self.progress_bar.setValue(0)  # Reset progress bar
        self.progress_label.setText(
            "Starting processing..."
        )  # Set initial progress label
        self.log_display.clear()
        self.log_display.append("Starting worker process...")
        self.start_button.setEnabled(False)
        # We use python -u for unbuffered output
        self.process.start(
            "python",
            [
                "-u",
                "src/worker.py",
                watermark_template_path,
                "",  # watermark_mask_applied_path (now ignored)
                media_to_be_edited_path,
                "",  # steps (now ignored)
                "",
                "",
            ],
        )

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = data.data().decode("utf-8").strip()
        self.log_display.append(stdout)

        # Check for progress updates
        if stdout.startswith("PROGRESS:"):
            try:
                progress_value = int(stdout.split(":")[1])
                self.update_progress_bar(progress_value)
            except ValueError:
                pass  # Ignore malformed progress messages
        elif stdout.startswith("STAGE:"):
            self.progress_label.setText(
                stdout[6:].strip()
            )  # Update progress label with stage message

    def handle_finished(self, exit_code, exit_status):
        status = "finished" if exit_status == QProcess.NormalExit else "crashed"
        self.log_display.append(f"Process {status} with exit code: {exit_code}.")
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(0)  # Reset or set to 100 upon completion
        self.progress_label.setText(
            "Finished."
        )  # Clear progress label or set to finished

    def handle_error(self, error):
        self.log_display.append(f"An error occurred: {error.name}")
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(0)  # Reset on error
        self.progress_label.setText("Error occurred.")  # Set progress label to error

    def is_image_file(self, path):
        image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
        return path.lower().endswith(image_extensions)

    def is_video_file(self, path):
        video_extensions = (".mp4", ".avi", ".mov", ".mkv")
        return path.lower().endswith(video_extensions)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Modern Dark Theme Stylesheet
    QSS = """
QMainWindow {
    background-color: #2b2b2b; /* Dark background */
    color: #f0f0f0; /* Light text */
}

QWidget {
    background-color: #2b2b2b;
    color: #f0f0f0;
    font-family: "Segoe UI", "Roboto", "Helvetica Neue", sans-serif;
    font-size: 10pt;
}

QLabel {
    color: #f0f0f0;
    padding: 2px;
}

QLineEdit, QTextEdit, QSpinBox {
    background-color: #3c3c3c; /* Slightly lighter dark for input fields */
    border: 1px solid #5a5a5a;
    border-radius: 4px;
    padding: 5px;
    color: #f0f0f0;
    selection-background-color: #0078d7; /* Accent blue for selection */
}

QPushButton {
    background-color: #0078d7; /* Accent blue for buttons */
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 8px 15px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #0060ad; /* Darker blue on hover */
}

QPushButton:pressed {
    background-color: #004c8c; /* Even darker blue when pressed */
}

QProgressBar {
    text-align: center;
    background-color: #3c3c3c;
    border: 1px solid #5a5a5a;
    border-radius: 5px;
    color: #f0f0f0;
}

QProgressBar::chunk {
    background-color: #0078d7; /* Accent blue for progress */
    border-radius: 5px;
}

QFileDialog {
    background-color: #2b2b2b;
    color: #f0f0f0;
}

/* For the file input layouts, to ensure consistent background */
QHBoxLayout, QVBoxLayout {
    background-color: #2b2b2b;
}

QWidget#central_widget { /* Targeting the central widget for padding */
    padding: 10px;
}
"""
    app.setStyleSheet(QSS)
    window = MainWindow()
    window.show()
    exit_code = app.exec()
    sys.exit(exit_code)
