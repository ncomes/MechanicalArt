#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
from PySide2.QtCore import QObject, QFile
from PySide2.QtUiTools import QUiLoader

# software specific imports

# mca python imports


def ui_importer(ui_path):
	"""
	Returns the QT Designer UI as a widget

	:param str ui_path: Full path and file name of the .ui file
	:return: Returns the QT Designer UI as a widget
	:rtype: .ui file
	"""
	
	ui_file = QFile(ui_path)
	ui_file.open(QFile.ReadOnly)
	loader = QUiLoader()
	ui_window = loader.load(ui_file)
	ui_file.close()
	return ui_window

