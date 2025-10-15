# main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QFileDialog, QTabWidget, QMessageBox
)
from PyQt6.QtGui import QAction
from editor.editor_widget import CodeEditor
from editor.project_manager import ProjectManager
import os
import sys
import subprocess
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyPythonEditor")
        self.resize(1200, 800)

        self.project_manager = ProjectManager()

        # ------------------- Tabs -------------------
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # ------------------- Menu Bar -------------------
        menu = self.menuBar()

        # File Menu
        file_menu = menu.addMenu("File")

        new_action = QAction("New File", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Open File", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save File", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        run_action = QAction("Run File", self)
        run_action.triggered.connect(self.run_file)
        file_menu.addAction(run_action)

        # Tools Menu
        tools_menu = menu.addMenu("Tools")

        autopep8_action = QAction("Format with AutoPEP8", self)
        autopep8_action.triggered.connect(self.format_autopep8)
        tools_menu.addAction(autopep8_action)

        black_action = QAction("Format with Black", self)
        black_action.triggered.connect(self.format_black)
        tools_menu.addAction(black_action)

        lint_action = QAction("Lint File", self)
        lint_action.triggered.connect(self.run_linter)
        tools_menu.addAction(lint_action)

        build_action = QAction("Build EXE", self)
        build_action.triggered.connect(self.build_exe)
        tools_menu.addAction(build_action)

    # ------------------- File Operations -------------------
    def new_file(self):
        editor = CodeEditor()
        self.tabs.addTab(editor, "untitled.py")
        self.tabs.setCurrentWidget(editor)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Python Files (*.py)")
        if file_path:
            editor = CodeEditor()
            with open(file_path, "r", encoding="utf-8") as f:
                editor.setPlainText(f.read())
            editor.file_path = file_path
            self.tabs.addTab(editor, os.path.basename(file_path))
            self.tabs.setCurrentWidget(editor)

    def save_file(self):
        editor = self.current_editor()
        if not editor:
            return
        if hasattr(editor, "file_path") and editor.file_path:
            path = editor.file_path
        else:
            path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py)")
            if not path:
                return
            editor.file_path = path
        with open(editor.file_path, "w", encoding="utf-8") as f:
            f.write(editor.toPlainText())
        self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(editor.file_path))

    def run_file(self):
        editor = self.current_editor()
        if not editor or not hasattr(editor, "file_path") or not editor.file_path:
            QMessageBox.warning(self, "Error", "File must be saved before running.")
            return
        os.system(f'python "{editor.file_path}"')

    # ------------------- Tools -------------------
    def format_autopep8(self):
        editor = self.current_editor()
        if editor:
            editor.format_code_autopep8()

    def format_black(self):
        editor = self.current_editor()
        if editor:
            editor.format_code_black()

    def run_linter(self):
        editor = self.current_editor()
        if editor:
            editor.run_linter()

    # ------------------- Build EXE -------------------
    def build_exe(self):
        editor = self.current_editor()
        if not editor or not hasattr(editor, "file_path") or not editor.file_path:
            QMessageBox.warning(self, "Error", "File must be saved before building EXE.")
            return

        file_path = editor.file_path

        # Ask user for output folder
        output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not output_folder:
            return

        # Build command for PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--distpath", output_folder,
            file_path
        ]

        # Inform user that building started
        QMessageBox.information(self, "Building", f"Building EXE for {file_path}...\nPlease wait.")

        # Run PyInstaller in a background thread
        def run_build():
            subprocess.run(cmd)
            QMessageBox.information(self, "Build Complete", f"Executable created in {output_folder}")

        threading.Thread(target=run_build, daemon=True).start()

    # ------------------- Utility -------------------
    def current_editor(self):
        widget = self.tabs.currentWidget()
        if isinstance(widget, CodeEditor):
            return widget
        return None
