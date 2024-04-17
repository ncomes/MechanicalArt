#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Summoner tool implementation
"""

# mca python imports
import inspect
import os.path
from functools import partial
# software specific imports
# PySide2 imports
from PySide2.QtWidgets import QFileDialog
# mca python imports
from mca.common.paths import project_paths
from mca.common.utils import process
from mca.common.modifiers import decorators
from mca.common.resources import resources
from mca.common.tools.dcctracking import dcc_tracking
from mca.mya.pyqt import mayawindows

from mca.mya.tools.flags_exporter import flags_exporter


class FlagsExporter(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'
    
    def __init__(self):
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        ui_path = os.path.join(root_path, 'ui', 'flagsExporterUI.ui')
        super().__init__(title='Save Skinning',
                            ui_path=ui_path,
                            version=FlagsExporter.VERSION)
        default_folder = project_paths.MCA_PROJECT_ROOT
        try:
            default_folder = flags_exporter.LAST_SELECTED_FLAG_EXPORT_FOLDER
        except Exception:
            pass

        # Tracking
        process.cpu_threading(dcc_tracking.ddc_tool_entry(FlagsExporter))

        self.ui.exportPathLine.setText(default_folder)
        self.ui.exportPathBrowseButton.setIcon(resources.icon(r'default\folder.png'))
        self.ui.exportPathResetButton.setIcon(resources.icon(r'default\close.png'))
        self.ui.exportButton.setIcon(resources.icon(r'default\export.png'))
        self.ui.exportCloseButton.setIcon(resources.icon(r'default\export.png'))
        
        # ==============================
        # Signals
        # ==============================
        self.ui.exportPathLine.textChanged.connect(self._on_export_path_line_text_changed)
        self.ui.exportPathBrowseButton.clicked.connect(self._on_export_path_browse_button_clicked)
        self.ui.exportPathResetButton.clicked.connect(self._on_export_path_reset_button_clicked)
        self.ui.exportButton.clicked.connect(partial(self._on_export_button_clicked, close=False))
        self.ui.exportCloseButton.clicked.connect(partial(self._on_export_button_clicked, close=True))
    
    # ==============================
    # Slots
    # ==============================
    def refresh(self):
        current_directory = self.ui.exportPathLine.text()
        self.ui.exportButton.setEnabled(True if current_directory and os.path.exists(current_directory) else False)
        self.ui.exportCloseButton.setEnabled(True if current_directory and os.path.exists(current_directory) else False)

    def _on_export_path_line_text_changed(self, text):
        """
        Internal callback function that is called each time export path line text changes.

        :param  str text: current path line text.
        """

        self.refresh()
    
    @decorators.track_fnc
    def _on_export_path_browse_button_clicked(self):
        """
        Internal callback function that is called each time export path browse button is clicked by the user.
        """

        folder = get_folder(self.ui.exportPathLine.text())
        if not folder:
            return
        self.ui.exportPathLine.setText(folder)
    
    @decorators.track_fnc
    def _on_export_path_reset_button_clicked(self):
        """
        Internal callback function that is called each time reset button is clicked by the user.
        """

        self.ui.exportPathLine.setText('')
    
    @decorators.track_fnc
    def _on_export_button_clicked(self, close=False):
        """
        Internal callback function that is called each time Export button or Export & Close button are clicked.

        :param bool close: whether tool window should be closed.
        """

        result = flags_exporter.export_flag(
            export_directory=self.ui.exportPathLine.text(), export_color=self.ui.exportFlagCbx.isChecked())
        if result and close:
            self.close()


def get_folder(directory=None, title='Select Folder', show_files=False, parent=None):
    """
    Shows an open folder dialog.

    :param str directory: root directory.
    :param str title: select folder dialog title.
    :param QWWidget parent: get folder parent widget.
    :return: selected folder or None if no folder is selected.
    :rtype: str
    """

    file_dialog = QFileDialog(parent)
    if show_files:
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, False)
    if directory:
        file_dialog.setDirectory(directory)
    directory = file_dialog.getExistingDirectory(parent, title)
    if directory:
        return directory
