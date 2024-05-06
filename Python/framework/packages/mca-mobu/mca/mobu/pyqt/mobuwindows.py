#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports

# software specific imports

# mca python imports
from mca.common.pyqt import common_windows
from mca.mobu.pyqt.utils import mo_main_windows


MOBU_MAIN_WINDOW = mo_main_windows.get_mobu_window()


class MATMobuWindow(common_windows.MCAMainWindow):
	def __init__(self, title='MCA Mobu Tool', ui_path=None, version='', parent=MOBU_MAIN_WINDOW):
		super().__init__(title=title, ui_path=ui_path, version=version, parent=parent)
