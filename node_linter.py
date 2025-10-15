import subprocess
import os

# Get absolute path to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def lint_js(code: str) -> str:
    """
    Lint JavaScript code using node_linter.js.
    Returns the linted/fixed code or the original code on error.
    """
    try:
        # Path to your Node.js linter script
        linter_path = os.path.join(PROJECT_ROOT, "node_linter.js")

        # Run the Node.js linter with the code as input
        result = subprocess.run(
            ["node", linter_path],
            input=code,
            text=True,
            capture_output=True,
            timeout=5
        )
        # Return output from Node.js or original code
        return result.stdout or code
    except Exception as e:
        print(f"Node linter error: {e}")
        return code
