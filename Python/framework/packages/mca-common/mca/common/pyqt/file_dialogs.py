"""
Module that provides a function to open a PySide2 file dialog.
"""

# python imports
# Qt imports
from mca.common.pyqt.pygui import qtwidgets
# software specific imports
# mca python imports
from mca.common.project import paths


def open_file_dialog(start_dir=paths.get_common_tools_path(), filters="All Files *.*", parent=None):
    """
    Opens a PySide2 file dialog and return the list of selected files from the dialog.

    :param str start_dir: The start directory of the file dialog.
    :param str filters: Filters the files that are shown in the dialog. "All Files *.*;;Images (*.tga *.png *.jpg)"
    :param QtWidgets parent: A ui widget that will be used as the parent of the dialog.
    :return: Return the list of selected files from the dialog.
    :rtype: list(str)
    """

    filenames = []
    dialog = qtwidgets.QFileDialog(parent)
    dialog.setDirectory(start_dir)
    dialog.setFileMode(qtwidgets.QFileDialog.FileMode.ExistingFiles)
    dialog.setNameFilter(filters)
    dialog.setViewMode(qtwidgets.QFileDialog.ViewMode.List)
    if dialog.exec():
        filenames = dialog.selectedFiles()
    return filenames

