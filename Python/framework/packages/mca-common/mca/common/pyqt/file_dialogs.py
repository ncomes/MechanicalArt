#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that provides a function to open a PySide2 file dialog.
"""

# mca python imports
# PySide2 imports
from PySide2.QtWidgets import QFileDialog
# software specific imports
# mca python imports
from mca.common.paths import paths


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
    dialog = QFileDialog(parent)
    dialog.setDirectory(start_dir)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    dialog.setNameFilter(filters)
    dialog.setViewMode(QFileDialog.ViewMode.List)
    if dialog.exec():
        filenames = dialog.selectedFiles()
    return filenames

