"""
Module that contains the mca decorators at a base python level
"""

# python imports
from PySide2.QtWidgets import QPlainTextEdit
# software specific imports
# mca python imports
from mca.common.pyqt import syntax_highlighter
from mca.mya.pyqt import mayawindows


class PythonEditor(mayawindows.MCAMayaWindow):
	VERSION = '1.0.0'
	
	def __init__(self, parent=None):
		super().__init__(title='Python Editor', version=PythonEditor.VERSION, parent=parent)
		
		self.resize(600, 600)
		
		self.editor = QPlainTextEdit()
		self.highlight = syntax_highlighter.PythonHighlighter(self.editor.document())
		self.main_layout.addWidget(self.editor)
		
		self.show()

