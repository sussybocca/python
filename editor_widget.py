# editor_widget.py
from PyQt6.QtWidgets import QPlainTextEdit, QToolTip
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter, QKeyEvent
from PyQt6.QtCore import Qt, QTimer
import jedi
import pygments
from pygments.lexers import PythonLexer
from pygments.token import Token
import autopep8
import black
import subprocess
import threading
import os

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.lexer = PythonLexer()

    def highlightBlock(self, text):
        for token, content in pygments.lex(text, self.lexer):
            length = len(content)
            if length == 0:
                continue
            fmt = QTextCharFormat()
            if token in Token.Keyword:
                fmt.setForeground(QColor("blue"))
                fmt.setFontWeight(QFont.Weight.Bold)
            elif token in Token.Name.Builtin:
                fmt.setForeground(QColor("darkMagenta"))
            elif token in Token.Literal.String:
                fmt.setForeground(QColor("darkGreen"))
            elif token in Token.Comment:
                fmt.setForeground(QColor("darkGray"))
                fmt.setFontItalic(True)
            else:
                fmt.setForeground(QColor("black"))
            start_index = text.find(content)
            if start_index != -1:
                self.setFormat(start_index, length, fmt)

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Consolas", 12))
        self.highlighter = PythonHighlighter(self.document())
        self.file_path = None
        self.lint_timer = QTimer()
        self.lint_timer.timeout.connect(self.run_linter)
        self.lint_timer.start(2000)  # run lint every 2 seconds

    # ------------------- Jedi Autocomplete -------------------
    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.text().isalpha() or event.key() == Qt.Key.Key_Period:
            self.show_autocomplete()

    def show_autocomplete(self):
        try:
            code = self.toPlainText()
            cursor = self.textCursor()
            row = cursor.blockNumber() + 1
            col = cursor.columnNumber()
            script = jedi.Script(code, path=getattr(self, 'file_path', None))
            completions = script.complete(row, col)
            if completions:
                QToolTip.showText(self.mapToGlobal(self.cursorRect().bottomRight()),
                                  ", ".join([c.name for c in completions]))
        except Exception:
            pass  # ignore autocomplete errors

    # ------------------- Code Formatting -------------------
    def format_code_autopep8(self):
        try:
            new_code = autopep8.fix_code(self.toPlainText())
            self.setPlainText(new_code)
        except Exception as e:
            print("AutoPEP8 error:", e)

    def format_code_black(self):
        try:
            new_code = black.format_str(self.toPlainText(), mode=black.Mode())
            self.setPlainText(new_code)
        except Exception as e:
            print("Black error:", e)

    # ------------------- Real-time Linting -------------------
    def run_linter(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            return
        def lint():
            try:
                result = subprocess.run(
                    ['flake8', self.file_path],
                    capture_output=True, text=True
                )
                output = result.stdout.strip()
                if output:
                    print(f"Linting issues in {self.file_path}:\n{output}")
            except Exception:
                pass
        threading.Thread(target=lint, daemon=True).start()
