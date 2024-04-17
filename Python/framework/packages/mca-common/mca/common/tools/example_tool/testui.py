#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox main UI
"""

# mca python imports
import os.path

# PySide2 imports

# software specific imports

# mca python imports
from mca.common.pyqt import common_windows
from mca.common.paths import paths


class ExampleUI(common_windows.MCAMainWindow):
	VERSION = '1.0.0'
	
	def __init__(self, style=None, parent=None):
		ui_path = os.path.join(paths.get_common_tools_path(), 'example_tool', 'ui', 'testui.ui')
		super().__init__(title='Example UI', ui_path=ui_path, version=ExampleUI.VERSION, style=style, parent=parent)
		self.setMinimumHeight(80)
		self.setMinimumWidth(200)
		self.ui.setMinimumHeight(80)
		self.ui.setMinimumWidth(200)
		self.ui_path = ui_path
		
		self.ui.test_pushButton.clicked.connect(self.test_print)
		
	def test_print(self):
		print('THE TEST UI IS WORKING!!!')