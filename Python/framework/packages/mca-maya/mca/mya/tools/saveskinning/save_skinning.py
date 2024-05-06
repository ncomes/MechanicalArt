#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Test tool implementation.
"""

# System global imports
import os
# Software specific imports
import pymel.core as pm
# PySide2 imports
from PySide2.QtWidgets import QFileDialog
# mca python imports
from mca.common import log
from mca.common.paths import paths, project_paths, path_utils
from mca.common.modifiers import decorators
from mca.common.assetlist import assetlist
from mca.mya.deformations import skin_utils
from mca.mya.pyqt import mayawindows


logger = log.MCA_LOGGER


class SaveSkinning(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'
    
    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'skinningUI.ui')
        super().__init__(title='Save Skinning',
                         ui_path=ui_path,
                         version=SaveSkinning.VERSION)

        self._is_path_relative = False

        asset_items = []
        # for asset_id, asset_entry in assetlist.get_asset_category_dict(None).items():
        #     asset_items.append(asset_entry.asset_name)

        self.ui.asset_idLine.addItems(sorted(asset_items))
        self.ui.asset_idLine.setCurrentText('Select an asset')

        # ==============================
        # Signals
        # ==============================
        self.ui.importButton.clicked.connect(self._on_import_button_clicked)
        self.ui.exportButton.clicked.connect(self._on_export_button_clicked)
        self.ui.pathButton.clicked.connect(self._on_path_button_clicked)
        self.ui.get_idButton.clicked.connect(self._on_get_id_button_clicked)
        self.ui.asset_idLine.currentTextChanged.connect(self._on_combobox_changed)
        self.ui.pathField.textChanged.connect(self._on_ui_path_field_text_changed)

    # ==============================
    # Slots
    # ==============================

    @decorators.track_fnc
    def _on_path_button_clicked(self):
        """
        Internal callback function that is called when Select Directory button is clicked by the user.
        """

        sel_dir = QFileDialog.getExistingDirectory(None, 'Select a directory:', project_paths.MCA_PROJECT_ROOT, QFileDialog.ShowDirsOnly)
        if not sel_dir:
            return

        print_name = path_utils.to_relative_path(sel_dir)
        if not print_name:
            print_name = sel_dir

        self.ui.pathField.setText(print_name)

    @decorators.track_fnc
    def _on_import_button_clicked(self):
        """
        Internal callback function that is called when Import button is clicked by the user.
        """

        dw_path = project_paths.MCA_PROJECT_ROOT
        project_path = self.ui.pathField.text()
        if dw_path in project_path:
            asset_path = self.ui.pathField.text()
        else:
            asset_path = os.path.join(dw_path, project_path)

        if not os.path.exists(asset_path):
            logger.warning('Please select an existing directory')
            return

        skin_utils.apply_skin_weights_cmd(asset_path)


    @decorators.track_fnc
    def _on_export_button_clicked(self):
        """
        Internal callback function that is called when Export button is clicked by the user.
        """

        if self._is_path_relative:
            dw_path = project_paths.MCA_PROJECT_ROOT
            project_path = self.ui.pathField.text()
            asset_path = os.path.join(dw_path, project_path)
        else:
            asset_path = self.ui.pathField.text()

        if not os.path.exists(asset_path):
            logger.warning('Please select an existing directory')
            return
        else:
            skin_utils.save_skin_weights_cmd(asset_path)


    @decorators.track_fnc
    def _on_get_id_button_clicked(self):
        """
        Internal callback function that is called when ID button is clicked by the user.
        """

        if pm.objExists('FRAGRoot'):
            id = pm.getAttr(pm.PyNode('FRAGRoot') + '.assetID')
            self.ui.asset_idLine.setCurrentText(id)
            asset_entry = assetlist.get_asset_by_id(id)
            skin_path = asset_entry.skin_data_path
            print_name = path_utils.to_relative_path(skin_path)
            if not print_name:
                print_name = skin_path
            self.ui.pathField.setText(print_name)
        else:
            logger.warning("No rig found, please select asset from dropdown box or choose skin data folder manually")

    def _on_combobox_changed(self, value):
        """
        Internal callback function that is called each time a combo box item is selected by the user.
        """
        if not value:
            return

        asset_entry = assetlist.get_asset_by_name(value)

        if not asset_entry:
            self.ui.pathField.setText('')
            return

        skin_path = asset_entry.skin_data_path
        if skin_path:
            print_name = path_utils.to_relative_path(skin_path)
            if not print_name:
                print_name = skin_path
            self.ui.pathField.setText(print_name)
        else:
            self.ui.pathField.setText('')

    def _on_ui_path_field_text_changed(self, text):
        """
        Internal callback function that is called each time path field text changes.

        :param str text: new path line text
        """

        project_path = project_paths.MCA_PROJECT_ROOT

        if not text or project_path in text:
            self._is_path_relative = False
            return

        if os.path.exists(os.path.join(project_path, text)):
            self._is_path_relative = True
        else:
            self._is_path_relative = False

