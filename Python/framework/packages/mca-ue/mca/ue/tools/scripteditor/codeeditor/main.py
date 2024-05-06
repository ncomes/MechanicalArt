import sys

from PySide2 import QtWidgets

from mca.ue.tools.scripteditor.codeeditor import code_editor
# from mca.ue.tools.scripteditor.codeeditor.highlighter.py_highlight import PythonHighlighter
from mca.common.pyqt import syntax_highlighter

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    editor = code_editor.CodeEditor()
    editor.setWindowTitle("Code Editor Example")
    highlighter = syntax_highlighter.PythonHighlighter(editor.document())
    editor.show()

    sys.exit(app.exec_())

