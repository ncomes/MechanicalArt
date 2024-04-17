#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox main UI
"""

# python imports
# PySide2 imports
# software specific imports

# mca python imports
from mca.common import log

from mca.common.pyqt.qt_utils import qt_menus
from mca.common.resources import resources
from mca.common.startup.configs import consts
from mca.common.tools.toolbox import toolbox_data, toolbox_editor, toolbox_ui

from mca.mya.pyqt.utils import ma_main_window

MAYA_MAIN_WINDOW = ma_main_window.get_maya_window()

logger = log.MCA_LOGGER


class MayaToolBox(toolbox_ui.ToolboxGui):

    def __init__(self,
                 toolbox_class,
                 dcc_app=consts.MAYA,
                 is_floating=False,
                 area='left',
                 parent=MAYA_MAIN_WINDOW):

        super().__init__(toolbox_class=toolbox_class,
                         dcc_app=dcc_app,
                         is_floating=is_floating,
                         area=area,
                         parent=parent)
        

class MayaToolboxEditor(toolbox_editor.ToolboxEditor):
    def __init__(self):
        super().__init__(parent=MAYA_MAIN_WINDOW)
        
    def refresh_menu_cmd(self):
        """
        Pitch all found toolbars and reload them.

        """
        menu_tools_inst = qt_menus.MainWindowsMenus.create('Toolbox', MAYA_MAIN_WINDOW)
        for x in menu_tools_inst.menu.actions():
            if x.text() == 'ToolBox':
                menu_tools_inst.menu.removeAction(x)
                break

        menu_toolbars = qt_menus.MainWindowsMenus(menu_tools_inst.menu, MAYA_MAIN_WINDOW)
        menu_toolbars.add_menu('ToolBox')
        for toolbox_name, toolbox_class in toolbox_data.ToolboxRegistry().TOOLBOX_NAME_DICT.items():
            menu_toolbars.add_action(toolbox_name,
                                     lambda sacrificial=False, toolbox_class=toolbox_class: MayaToolBox(toolbox_class=toolbox_class),
                                     icon=resources.icon(r'software\mca.png'))
