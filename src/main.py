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
    QColorDialog,
    QSlider,
    QProgressBar,
)
from PySide6.QtGui import QColor
from PySide6.QtCore import QProcess, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python GUI Wrapper")
        self.setGeometry(100, 100, 600, 400)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # File input for "watermark mask to be deleted" (now watermark template)
        (
            self.watermark_mask_deleted_layout,
            self.watermark_mask_deleted_path_display,
            self.watermark_mask_deleted_browse_button,
        ) = self._create_file_input(
            "watermark template:",
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

        # Steps input
        self.steps_layout = QHBoxLayout()
        self.steps_label = QLabel("Processing Steps:")
        self.steps_input = QSpinBox()
        self.steps_input.setMinimum(1)
        self.steps_input.setValue(5)
        self.steps_layout.addWidget(self.steps_label)
        self.steps_layout.addWidget(self.steps_input)

        # Color selection
        self.color_layout = QHBoxLayout()
        self.color_label = QLabel("Watermark Color (ignored):")
        self.color_button = QPushButton("Select Color")
        self.color_display = QLabel()
        self.color_display.setFixedSize(20, 20)
        self.selected_color = QColor("white")
        self.update_color_display()
        self.color_layout.addWidget(self.color_label)
        self.color_layout.addWidget(self.color_button)
        self.color_layout.addWidget(self.color_display)

        # Tolerance slider
        self.tolerance_layout = QHBoxLayout()
        self.tolerance_label = QLabel("Detection Threshold (0-100):")
        self.tolerance_slider = QSlider(Qt.Horizontal)
        self.tolerance_slider.setRange(0, 100)
        self.tolerance_slider.setValue(80)  # Default for template matching threshold
        self.tolerance_value_label = QLabel("80")
        self.tolerance_layout.addWidget(self.tolerance_label)
        self.tolerance_layout.addWidget(self.tolerance_slider)
        self.tolerance_layout.addWidget(self.tolerance_value_label)

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
        self.layout.addLayout(
            self.watermark_mask_deleted_layout
        )  # Now watermark template
        self.layout.addLayout(self.steps_layout)
        self.layout.addLayout(self.color_layout)
        self.layout.addLayout(self.tolerance_layout)
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
        self.color_button.clicked.connect(self.open_color_dialog)
        self.tolerance_slider.valueChanged.connect(self.update_tolerance_label)
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

    def open_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.update_color_display()

    def update_color_display(self):
        self.color_display.setStyleSheet(
            f"background-color: {self.selected_color.name()}"
        )

    def update_tolerance_label(self, value):
        self.tolerance_value_label.setText(str(value))

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
                "Please select both a watermark template and a media file to be edited."
            )
            return

        # Check if paths are valid files
        if not (
            os.path.exists(watermark_template_path)
            and (self.is_image_file(watermark_template_path))
        ):
            self.log_display.append(
                "Please provide a valid image file for the watermark template."
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
                str(self.steps_input.value()),
                self.selected_color.name(),
                str(self.tolerance_slider.value()),
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

    def handle_finished(self, exit_code, exit_status):
        status = "finished" if exit_status == QProcess.NormalExit else "crashed"
        self.log_display.append(f"Process {status} with exit code: {exit_code}.")
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(0)  # Reset or set to 100 upon completion

    def handle_error(self, error):
        self.log_display.append(f"An error occurred: {error.name}")
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(0)  # Reset on error

    def is_image_file(self, path):
        image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
        return path.lower().endswith(image_extensions)

    def is_video_file(self, path):
        video_extensions = (".mp4", ".avi", ".mov", ".mkv")
        return path.lower().endswith(video_extensions)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
