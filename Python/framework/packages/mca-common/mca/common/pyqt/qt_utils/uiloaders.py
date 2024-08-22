"""
Module that contains the mca decorators at a base python level
"""

# python imports
# Qt imports
from mca.common.pyqt.pygui import qtwidgets, qtuitools
# software specific imports
# mca python imports


def ui_importer(ui_path):
	"""
	Returns the QT Designer UI as a widget

	:param str ui_path: Full path and file name of the .ui file
	:return: Returns the QT Designer UI as a widget
	:rtype: .ui file
	"""
	
	ui_file = qtwidgets.QFile(ui_path)
	ui_file.open(qtwidgets.QFile.ReadOnly)
	loader = qtuitools.QUiLoader()
	ui_window = loader.load(ui_file)
	ui_file.close()
	return ui_window

