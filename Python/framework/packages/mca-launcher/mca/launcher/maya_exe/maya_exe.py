#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DCC Launcher for CPG.

"""
# python imports
import sys
# software specific imports
# PySide2 imports
from PySide2.QtWidgets import QApplication
# CPG python imports


def maya_init():
    from mca.launcher.dcc import maya
    from mca.launcher.utils import path_utils
    
    common_path = path_utils.get_common_path()
    deps_path = path_utils.get_dependencies_path()
    maya.launch('2024', common_path, deps_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    maya_init()
    sys.exit(app.exec_())

