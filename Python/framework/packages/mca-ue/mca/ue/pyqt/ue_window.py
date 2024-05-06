# -*- coding: utf-8 -*-

"""
Hidden UI Window to parent to.
"""

# mca python imports
import sys
# PySide2 imports
from PySide2.QtWidgets import QApplication
# software specific imports
import unreal
# mca python imports
from mca.common.pyqt import common_windows
from mca.common import log

logger = log.MCA_LOGGER


class MATUnrealWindow(common_windows.MCAMainWindow):

    def __init__(self,
                    title='UE_Window',
                    ui_path=None,
                    version='1.0.0',
                    style=None,
                    parent=None):

        super().__init__(title=title, ui_path=ui_path, version=version, style=style, parent=parent)
        app = None
        if not QApplication.instance():
            app = QApplication(sys.argv)
        try:
            unreal.parent_external_window_to_slate(int(self.winId()))
            sys.exit(app.exec_())
        except Exception as e:
            print(e)


class MATUnrealTestWindow(common_windows.MCAMainWindow):

    def __init__(self,
                    title='UE_TestWindow',
                    ui_path=None,
                    version='1.0.0',
                    style=None,
                    parent=None):

        super().__init__(title=title, ui_path=ui_path, version=version, style=style, parent=parent)

        app = None
        if not QApplication.instance():
            app = QApplication(sys.argv)
        try:
            window = self
            unreal.parent_external_window_to_slate(int(window.winId()))
            sys.exit(app.exec_())
        except Exception as e:
            print(e)


