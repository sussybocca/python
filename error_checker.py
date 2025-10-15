# editor/error_checker.py
import autopep8

def check_and_fix_errors(file_path):
    try:
        with open(file_path, "r") as f:
            code = f.read()
        compile(code, file_path, "exec")
        print(f"No syntax errors in {file_path}")
    except SyntaxError as e:
        print(f"Syntax error found: {e}")
        print("Attempting to auto-fix using autopep8...")
        fixed_code = autopep8.fix_code(code)
        with open(file_path, "w") as f:
            f.write(fixed_code)
        print("Errors fixed automatically.")
