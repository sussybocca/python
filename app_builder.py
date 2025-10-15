# editor/app_builder.py
import subprocess
import os
from editor.error_checker import check_and_fix_errors

class AppBuilder:
    def __init__(self, project_path):
        self.project_path = project_path
        self.app_file = os.path.join(project_path, "app.py")
        self.requirements_file = os.path.join(project_path, "requirements.txt")

    def install_requirements(self):
        if os.path.exists(self.requirements_file):
            with open(self.requirements_file) as f:
                for pkg in f:
                    pkg = pkg.strip()
                    if pkg:
                        subprocess.run(["pip", "install", pkg])

    def build_windows_exe(self):
        if not os.path.exists(self.app_file):
            print("app.py not found in project!")
            return False

        # Auto-fix errors before building
        check_and_fix_errors(self.app_file)

        # Install dependencies
        self.install_requirements()

        # Build Windows executable using PyInstaller
        try:
            subprocess.run([
                "pyinstaller",
                "--onefile",
                "--windowed",
                self.app_file
            ], check=True)
            print("Build successful! Executable is in the 'dist' folder.")
            return True
        except subprocess.CalledProcessError:
            print("Build failed.")
            return False
