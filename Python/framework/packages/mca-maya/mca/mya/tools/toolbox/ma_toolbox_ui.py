"""
Toolbox main UI
"""

# python imports
# software specific imports
# mca python imports
from mca.common import log
from mca.common.pyqt.qt_utils import windows
from mca.common.startup.configs import consts
from mca.common.tools.toolbox import toolbox_data, toolbox_editor, toolbox_prefs, toolbox_ui

from mca.mya.startup import start_menus
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
        maya_main_window = ma_main_window.get_maya_window()
        windows.close_all_mca_docked_windows(maya_main_window)
        start_menus.create_menus()

        # Check to see if any Toolboxes need to be opened.
        TOOLBOX_P = toolbox_prefs.ToolBoxPreferences(dcc=consts.MAYA)
        all_on_start = TOOLBOX_P.get_all_on_startups()
        if all_on_start:
            for toolbox_name in all_on_start:
                toolbox_class = toolbox_data.ToolboxRegistry().TOOLBOX_NAME_DICT.get(toolbox_name)
                if toolbox_class:
                    MayaToolBox(toolbox_class)
