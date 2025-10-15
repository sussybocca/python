# editor/code_editor.py
from editor.file_manager import FileManager
from editor.error_checker import check_and_fix_errors

class CodeEditor:
    def __init__(self, file_manager: FileManager):
        self.fm = file_manager

    def edit_file(self, filename, new_content):
        self.fm.write_file(filename, new_content)
        check_and_fix_errors(self.fm.project_path + "/" + filename)

    def add_file(self, filename):
        self.fm.add_file(filename)

    def view_file(self, filename):
        return self.fm.read_file(filename)

    def list_files(self):
        return self.fm.list_files()
