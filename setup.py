# setup.py
import sys
from cx_Freeze import setup, Executable

# Include only necessary packages and your editor folder
build_exe_options = {
    "packages": ["os", "sys", "PyQt6", "editor"],
    "include_files": ["editor/"],  # only your editor folder
}

# Use "Win32GUI" base to hide console for GUI apps
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="MyPythonEditor",
    version="1.0",
    description="Custom Python IDE",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
