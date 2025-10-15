# ------------------------------
# Python Editor Setup Script
# ------------------------------
# This script sets up:
# - Python virtual environment
# - Flask + Waitress
# - Project folder structure
# - Example app.py
# ------------------------------

# Set your project path
$projectPath = "E:\PY.EDITOR"

# Create project folder if it doesn't exist
if (!(Test-Path $projectPath)) {
    Write-Host "Creating project folder..."
    New-Item -ItemType Directory -Path $projectPath
}

# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (!$python) {
    Write-Host "Python not found. Please install Python from https://www.python.org/downloads/windows/ and add to PATH."
    exit
}

# Navigate to project folder
Set-Location $projectPath

# Create virtual environment
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
& "$projectPath\.venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install required packages
Write-Host "Installing Flask and Waitress..."
pip install flask waitress

# Create folder structure
$folders = @("templates", "static", "projects", "extensions", "ui")
foreach ($f in $folders) {
    $path = Join-Path $projectPath $f
    if (!(Test-Path $path)) {
        New-Item -ItemType Directory -Path $path
    }
}

# Create example app.py if it doesn't exist
$appFile = Join-Path $projectPath "app.py"
if (!(Test-Path $appFile)) {
@"
from flask import Flask, render_template, request, jsonify
from waitress import serve
import os

app = Flask(__name__)

# Folder to store projects
PROJECT_DIR = "projects"
os.makedirs(PROJECT_DIR, exist_ok=True)

@app.route("/")
def index():
    return "<h2>Python Editor Running!</h2><p>Use /save, /run, /open routes in JSON format.</p>"

@app.route("/save", methods=["POST"])
def save_file():
    filename = request.json.get("filename")
    code = request.json.get("code")
    path = os.path.join(PROJECT_DIR, filename)
    with open(path, "w") as f:
        f.write(code)
    return jsonify({"status": "saved"})

@app.route("/open", methods=["GET"])
def open_file():
    filename = request.args.get("filename")
    path = os.path.join(PROJECT_DIR, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            code = f.read()
        return jsonify({"code": code})
    return jsonify({"error": "File not found"})

@app.route("/run", methods=["POST"])
def run_file():
    filename = request.json.get("filename")
    path = os.path.join(PROJECT_DIR, filename)
    if os.path.exists(path):
        try:
            import subprocess
            result = subprocess.run(["python", path], capture_output=True, text=True, timeout=5)
            return jsonify({"output": result.stdout + result.stderr})
        except subprocess.TimeoutExpired:
            return jsonify({"output": "Execution timed out"})
    return jsonify({"output": "File not found"})

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
"@ | Out-File -Encoding UTF8 $appFile
    Write-Host "Created example app.py"
}

Write-Host "Setup complete! Activate your environment and run:"
Write-Host "`tcd $projectPath"
Write-Host "`t.venv\Scripts\Activate.ps1"
Write-Host "`tpython app.py"
