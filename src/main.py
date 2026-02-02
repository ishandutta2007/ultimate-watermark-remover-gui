import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import QProcess


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python GUI Wrapper")
        self.setGeometry(100, 100, 600, 400)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # UI Elements
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setPlaceholderText("Output from the script will appear here...")

        self.start_button = QPushButton("Start Processing")

        # Add widgets to layout
        self.layout.addWidget(self.log_display)
        self.layout.addWidget(self.start_button)

        # QProcess setup
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)

        # Connect signals
        self.start_button.clicked.connect(self.start_worker_process)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.finished.connect(self.handle_finished)
        self.process.errorOccurred.connect(self.handle_error)

    def start_worker_process(self):
        self.log_display.clear()
        self.log_display.append("Starting worker process...")
        self.start_button.setEnabled(False)
        # We use python -u for unbuffered output
        self.process.start("python", ["-u", "src/worker.py"])

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
