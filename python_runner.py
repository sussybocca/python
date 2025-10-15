import subprocess
import tempfile
import os

def run_python(code: str) -> str:
    """Run Python code safely and return output."""
    try:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()
            result = subprocess.run(
                ["python3", f.name],
                capture_output=True,
                text=True,
                timeout=5
            )
        os.unlink(f.name)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "Execution timed out"
    except Exception as e:
        return f"Error: {e}"
