import autopep8

def lint_and_fix(code):
    return autopep8.fix_code(code)
