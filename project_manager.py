# project_manager.py
import os

class ProjectManager:
    def __init__(self):
        self.projects = {}

    def add_project(self, name, path):
        self.projects[name] = path

    def get_project_files(self, name):
        path = self.projects.get(name)
        if not path:
            return []
        files = []
        for root, dirs, filenames in os.walk(path):
            for f in filenames:
                if f.endswith(".py"):
                    files.append(os.path.join(root, f))
        return files
