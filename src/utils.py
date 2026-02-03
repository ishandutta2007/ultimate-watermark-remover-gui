import os
import sys


def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        # For one-dir mode, resources are directly in _MEIPASS
        # For one-file mode, they are also directly in _MEIPASS (or a subfolder if --add-data specified a subfolder)
        base_path = sys._MEIPASS
    else:
        # Normal development environment
        # Assumes utils.py is in src/ and resources are relative to the project root (one level up from src)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.join(base_path, relative_path)
