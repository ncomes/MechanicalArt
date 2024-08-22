#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Apply Skinning UI.
Allows user to save single mesh skinning locally and reapply it.
"""

# System global imports
import os
# software specific imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.mya.pyqt import mayawindows
from mca.common.project import paths
from mca.mya.rigging import skin_utils
from mca.common.textio import jsonio
from mca.common.utils import list_utils, fileio
from mca.mya.pyqt import maya_dialogs

logger = log.MCA_LOGGER

class ApplySkinningUi(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'applyskinningUI.ui')
        super().__init__(title='Apply Skinning UI',
                         ui_path=ui_path,
                         version=ApplySkinningUi.VERSION)

        paths.get_local_tools_prefs_folder('mya', 'applySkinning')

        # ==============================
        # Signals
        # ==============================

        self.ui.S1_pushButton.clicked.connect(self.S1_clicked)
        self.ui.A1_pushButton.clicked.connect(self.A1_clicked)
        self.ui.S2_pushButton.clicked.connect(self.S2_clicked)
        self.ui.A2_pushButton.clicked.connect(self.A2_clicked)
        self.ui.S3_pushButton.clicked.connect(self.S3_clicked)
        self.ui.A3_pushButton.clicked.connect(self.A3_clicked)
        self.ui.S4_pushButton.clicked.connect(self.S4_clicked)
        self.ui.A4_pushButton.clicked.connect(self.A4_clicked)
        self.ui.S5_pushButton.clicked.connect(self.S5_clicked)
        self.ui.A5_pushButton.clicked.connect(self.A5_clicked)
        self.ui.S6_pushButton.clicked.connect(self.S6_clicked)
        self.ui.A6_pushButton.clicked.connect(self.A6_clicked)


    # ==============================
    # Slots
    # ==============================

    def save_skin_weights_modified(self, filename):
        """
        Saves selected meshes skin weights, modified to fit this tool

        :param str filename: name for the saved skin file
        """

        selected_nodes = pm.selected()
        if not selected_nodes:
            logger.warning('Please select a mesh to save skinning from')
            maya_dialogs.info_prompt('Selection Error', 'Please select a mesh to save skinning from')
            return

        folderPath = paths.get_local_tools_prefs_folder('mya', 'applySkinning')

        for node in selected_nodes:
            if isinstance(node, pm.nt.Transform):
                skin_data = skin_utils.get_skin_weights(node)
                skin_data_file = os.path.join(folderPath, f'{filename}_skin_data.json')
                if os.path.exists(skin_data_file):
                    fileio.touch_path(folderPath)
                jsonio.write_to_json_file(skin_data, skin_data_file)


    def apply_skin_weights_cmd_modified(self, skin_data_path, name_override):
        """
        Applies previously saved skin weights to selected meshes or vertices, modified to fit this tool

        :param str skin_data_path: Path to skin data folder to pull weight data file from
        :param str name_override: Name for skin file to pull from
        """

        selected_nodes = pm.selected(fl=True)
        first_node = list_utils.get_first_in_list(selected_nodes)
        if not first_node:
            logger.warning('Please select meshes or vertices to apply skinning to')
            maya_dialogs.info_prompt('Selection Error', 'Please select either vertices or mesh to apply weights on')
            return
        first_type = type(first_node)
        is_same_type = all(isinstance(item, first_type) for item in selected_nodes)
        if not is_same_type and (isinstance(first_node, pm.MeshVertex)
                                 or isinstance(first_node, pm.nt.Transform)):
            logger.warning('Please select either vertices or meshes to apply weights on')
            maya_dialogs.info_prompt('Selection Error', 'Please select either vertices or mesh to apply weights on')
            return

        if first_type == pm.MeshVertex:
            # In case vertices from multiple meshes are selected, separating them by mesh here
            skin_utils.apply_skinning_to_verts(selected_nodes, skin_data_path, name_override)
            logger.info('Skinning applied to verts')

        else:
            skin_utils.apply_skinning_to_mesh(selected_nodes, skin_data_path, name_override)
            logger.info('Skinning applied to mesh')

    def S1_clicked(self):
        """
        Saves skin data to S1_skin_data.json
        """

        self.save_skin_weights_modified('S1')

    def A1_clicked(self):
        """
        Applies skin data from S1_skin_data.json
        """

        folderPath = paths.get_local_tools_prefs_folder('mya', 'applySkinning')
        self.apply_skin_weights_cmd_modified(folderPath, 'S1')

    def S2_clicked(self):
        """
        Saves skin data to S2_skin_data.json
        """

        self.save_skin_weights_modified('S2')

    def A2_clicked(self):
        """
        Applies skin data from S2_skin_data.json
        """

        folderPath = paths.get_local_tools_prefs_folder('mya', 'applySkinning')
        self.apply_skin_weights_cmd_modified(folderPath, 'S2')

    def S3_clicked(self):
        """
        Saves skin data to S3_skin_data.json
        """

        self.save_skin_weights_modified('S3')

    def A3_clicked(self):
        """
        Applies skin data from S3_skin_data.json
        """

        folderPath = paths.get_local_tools_prefs_folder('mya', 'applySkinning')
        self.apply_skin_weights_cmd_modified(folderPath, 'S3')

    def S4_clicked(self):
        """
        Saves skin data to S4_skin_data.json
        """

        self.save_skin_weights_modified('S4')

    def A4_clicked(self):
        """
        Applies skin data from S4_skin_data.json
        """

        folderPath = paths.get_local_tools_prefs_folder('mya', 'applySkinning')
        self.apply_skin_weights_cmd_modified(folderPath, 'S4')

    def S5_clicked(self):
        """
        Saves skin data to S5_skin_data.json
        """

        self.save_skin_weights_modified('S5')

    def A5_clicked(self):
        """
        Applies skin data from S5_skin_data.json
        """

        folderPath = paths.get_local_tools_prefs_folder('mya', 'applySkinning')
        self.apply_skin_weights_cmd_modified(folderPath, 'S5')

    def S6_clicked(self):
        """
        Saves skin data to S6_skin_data.json
        """

        self.save_skin_weights_modified('S6')

    def A6_clicked(self):
        """
        Applies skin data from S6_skin_data.json
        """

        folderPath = paths.get_local_tools_prefs_folder('mya', 'applySkinning')
        self.apply_skin_weights_cmd_modified(folderPath, 'S6')