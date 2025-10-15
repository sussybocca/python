from flask import Flask, render_template, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Directory to store projects
PROJECT_DIR = "projects"
os.makedirs(PROJECT_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save_file():
    filename = request.form.get("filename")
    code = request.form.get("code")
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
    filename = request.form.get("filename")
    path = os.path.join(PROJECT_DIR, filename)
    if os.path.exists(path):
        try:
            # Run the Python code and capture output
            result = subprocess.run(
                ["python3", path],  # PythonAnywhere uses python3
                capture_output=True,
                text=True,
                timeout=5
            )
            return jsonify({"output": result.stdout + result.stderr})
        except subprocess.TimeoutExpired:
            return jsonify({"output": "Execution timed out"})
    return jsonify({"output": "File not found"})

# Only run locally; PythonAnywhere WSGI will use 'application'
if __name__ == "__main__":
    app.run(debug=True)
