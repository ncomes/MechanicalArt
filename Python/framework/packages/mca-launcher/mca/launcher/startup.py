"""
Start script for the MCA Launcher
"""

# System global imports
import sys
# PySide2 imports
from PySide2.QtWidgets import QApplication
# Software specific imports
# mca python imports


def path_check():
    """
    Checks if the path has been set correctly in the preferences folder in the documents folder.
    """

    from mca.launcher.utils import path_utils, p4v
    prefs_file = path_utils.get_mca_python_root_path()
    if prefs_file:
        return True

    # depots = p4v.get_p4_workspaces()
    # if depots:
    #     from mca.launcher.utils import path_utils
    #     prefs = path_utils.MCAProjectPrefs.load()
    #     prefs.project_path = depots
    #     prefs.save()
    #     return True
    return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if path_check():
        # If the preferences is set correctly, launch the main Launcher.
        from mca.launcher.ui import mca_launcher
        window = mca_launcher.DCCLauncher()
    else:
        # If the preferences is not set correctly, launch the path launcher.  This ui will set the preferences.
        from mca.launcher.ui import mca_path_ui
        window = mca_path_ui.DCCPathLauncher()
    sys.exit(app.exec_())


