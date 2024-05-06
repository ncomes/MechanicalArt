#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox main UI
"""

# mca python imports

# PySide2 imports

# software specific imports

# mca python imports
from mca.common.tools.toolbox import toolbox_ui
from mca.common.startup.configs import consts
from mca.mobu.pyqt.utils import mo_main_windows

MOBU_MAIN_WINDOW = mo_main_windows.get_mobu_window()


class MobuToolBox(toolbox_ui.ToolboxGui):
    def __init__(self, toolbox_class, is_floating=False, area='right', dcc_app=consts.MOBU, parent=MOBU_MAIN_WINDOW):
        super().__init__(toolbox_class=toolbox_class,
                         dcc_app=dcc_app,
                         is_floating=is_floating,
                         area=area,
                         parent=parent)

