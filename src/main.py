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

        # File input layout
        self.file_input_layout = QHBoxLayout()
        self.file_path_display = QLineEdit()
        self.file_path_display.setPlaceholderText("Select a file...")
        self.browse_button = QPushButton("Browse")
        self.file_input_layout.addWidget(self.file_path_display)
        self.file_input_layout.addWidget(self.browse_button)

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
        self.color_label = QLabel("Watermark Color:")
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
        self.tolerance_label = QLabel("Color Tolerance:")
        self.tolerance_slider = QSlider(Qt.Horizontal)
        self.tolerance_slider.setRange(0, 100)
        self.tolerance_slider.setValue(10)
        self.tolerance_value_label = QLabel("10")
        self.tolerance_layout.addWidget(self.tolerance_label)
        self.tolerance_layout.addWidget(self.tolerance_slider)
        self.tolerance_layout.addWidget(self.tolerance_value_label)


        # UI Elements
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setPlaceholderText("Output from the script will appear here...")

        self.start_button = QPushButton("Start Processing")

        # Add widgets to layout
        self.layout.addLayout(self.file_input_layout)
        self.layout.addLayout(self.steps_layout)
        self.layout.addLayout(self.color_layout)
        self.layout.addLayout(self.tolerance_layout)
        self.layout.addWidget(self.log_display)
        self.layout.addWidget(self.start_button)

        # QProcess setup
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)

        # Connect signals
        self.browse_button.clicked.connect(self.open_file_dialog)
        self.color_button.clicked.connect(self.open_color_dialog)
        self.tolerance_slider.valueChanged.connect(self.update_tolerance_label)
        self.start_button.clicked.connect(self.start_worker_process)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.finished.connect(self.handle_finished)
        self.process.errorOccurred.connect(self.handle_error)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File")
        if file_path:
            self.file_path_display.setText(file_path)

    def open_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.update_color_display()

    def update_color_display(self):
        self.color_display.setStyleSheet(f"background-color: {self.selected_color.name()}")

    def update_tolerance_label(self, value):
        self.tolerance_value_label.setText(str(value))

    def start_worker_process(self):
        file_path = self.file_path_display.text()
        if not file_path:
            self.log_display.append("Please select a file first.")
            return

        steps = self.steps_input.value()
        color = self.selected_color.name()
        tolerance = self.tolerance_slider.value()

        self.log_display.clear()
        self.log_display.append("Starting worker process...")
        self.start_button.setEnabled(False)
        # We use python -u for unbuffered output
        self.process.start("python", ["-u", "src/worker.py", file_path, str(steps), color, str(tolerance)])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        self.log_display.append(data.data().decode("utf-8").strip())

    def handle_finished(self, exit_code, exit_status):
        status = "finished" if exit_status == QProcess.NormalExit else "crashed"
        self.log_display.append(f"Process {status} with exit code: {exit_code}.")
        self.start_button.setEnabled(True)

    def handle_error(self, error):
        self.log_display.append(f"An error occurred: {error.name}")
        self.start_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
