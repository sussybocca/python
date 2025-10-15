# main.py
import sys
from PyQt6.QtWidgets import QApplication
from editor.main_window import MainWindow
import subprocess

def check_dependencies():
    """Ensure all required packages are installed."""
    packages = [
        "PyQt6", "PySide6", "Pygments", "jedi", "pylint",
        "autopep8", "black", "flake8", "watchdog", "rope"
    ]
    import importlib
    import subprocess
    import sys
    for pkg in packages:
        if importlib.util.find_spec(pkg) is None:
            print(f"Installing missing package: {pkg}")
            subprocess.run([sys.executable, "-m", "pip", "install", pkg])

def main():
    # Check dependencies
    check_dependencies()

    # Start Qt Application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    print(">>> Starting MyPythonEditor...")
    main()
