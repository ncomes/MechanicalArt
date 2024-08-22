#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DCC Launcher for mobu.

"""
# python imports
import sys
# software specific imports
# PySide6 imports
from PySide6.QtWidgets import QApplication
# project python imports


def mobu_init():
    from mca.launcher.dccs import mobu
    from mca.launcher.utils import path_utils, plastic

    # Spin up plastic server.
    #plastic.run_plastic_server()
    
    common_path = path_utils.get_common_path()
    deps_path = path_utils.get_dependencies_path()
    mobu.launch('2024', common_path, deps_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mobu_init()
    sys.exit(app.exec_())

