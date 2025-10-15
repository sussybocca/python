# editor/file_manager.py
import os

class FileManager:
    def __init__(self, project_path):
        self.project_path = project_path
        os.makedirs(project_path, exist_ok=True)

    def list_files(self):
        return [f for f in os.listdir(self.project_path) if os.path.isfile(os.path.join(self.project_path, f))]

    def read_file(self, filename):
        path = os.path.join(self.project_path, filename)
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        return ""

    def write_file(self, filename, content):
        path = os.path.join(self.project_path, filename)
        with open(path, "w") as f:
            f.write(content)

    def add_file(self, filename):
        path = os.path.join(self.project_path, filename)
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("")  # create empty file
