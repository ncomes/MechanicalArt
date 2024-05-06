#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox main UI
"""

# mca python imports
import sys
# PySide2 imports
from PySide2.QtWidgets import QApplication
# software specific imports
import unreal
# mca python imports
from mca.common.tools.toolbox import toolbox_ui, toolbox_editor
from mca.common.tools.toolbox import toolbox_data
from mca.common.startup.configs import consts
from mca.common import log

logger = log.MCA_LOGGER


class UnrealToolBox(toolbox_ui.ToolboxGui):

    def __init__(self,
                    toolbox_name,
                    dcc_app=consts.UNREAL,
                    is_floating=True,
                    area='left',
                    parent=None):

        toolbox_class = toolbox_data.get_toolbox_by_name(toolbox_name)

        super().__init__(toolbox_class=toolbox_class,
                         dcc_app=dcc_app,
                         is_floating=is_floating,
                         area=area,
                         parent=parent)

        app = None
        if not QApplication.instance():
            app = QApplication(sys.argv)
        try:
            window = self
            unreal.parent_external_window_to_slate(int(window.winId()))
            sys.exit(app.exec_())
        except Exception as e:
            print(e)


class UnrealToolBoxEditor(toolbox_editor.ToolboxEditor):

    def __init__(self, parent=None):

        super().__init__(parent=parent)

        app = None
        if not QApplication.instance():
            app = QApplication(sys.argv)
        try:
            window = self
            unreal.parent_external_window_to_slate(int(window.winId()))
            sys.exit(app.exec_())
        except Exception as e:
            print(e)
