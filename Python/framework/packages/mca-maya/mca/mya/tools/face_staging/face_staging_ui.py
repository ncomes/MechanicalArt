#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source data for faces.

"""
# python imports
from __future__ import print_function, division, absolute_import

import logging
import os
import inspect
import subprocess
import webbrowser
import time

# PySide2 imports
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QWidget, QAbstractItemView, QDialogButtonBox, QHBoxLayout, QLayout, QLabel, QListWidgetItem
from PySide2.QtWidgets import QPushButton, QSizePolicy

# software specific imports
import pymel.core as pm
import maya.cmds as cmds

# mca python imports
from mca.common import log
from mca.common.paths import paths
from mca.common.utils import fileio, sounds, lists
from mca.common.modifiers import decorators
from mca.common.assetlist import assetlist
from mca.common.tools.progressbar import progressbar_ui
from mca.common.resources import resources
from mca.common.pyqt.qt_utils import listwidget_utils

from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import frag, skel_utils
from mca.mya.modeling import face_model
from mca.mya.face import source_meshes, face_vertex_data, source_data
from mca.mya.rigging.flags import flag_utils, frag_flag, serialize_flag
from mca.mya.rigging import mesh_markup_rig, chain_markup
from mca.mya.face.face_utils import face_util, face_import_export, eyelash_snapping, face_skinning
from mca.mya.face.face_poses import pose_files
from mca.mya.face.face_poses import face_pose_edit
from mca.mya.utils import optionvars, fbx_utils, naming, display_layers, textures
from mca.mya.deformations import skin_utils
from mca.mya.pyqt import mayawindows
from mca.mya.tools.faceskinning import face_skinning_tool
from mca.mya.tools.assetregister import ma_asset_register
from mca.mya.pyqt import dialogs


logger = log.MCA_LOGGER
TEMPLATES_PATH = 'mca.mya.rigging.templates'

STAGING_COLOR_GREEN = '(0, 255, 0)'
STAGING_COLOR_RED = '(255, 0, 0)'
STAGING_COLOR_WHITE = '(255, 255, 255)'
STAGING_COLOR_GREY = '(150, 150, 150)'
STAGING_BUTTON_COLORS = 'background-color: rgb{0.207843, 0.207843, 0.207843, 1.000000};'
STAGING_BUTTON_ACTIVE_COLORS = 'background-color: #696969; color: black;'
STAGING_BACKGROUND_GREY = 'background-color: #808080;'
REGION_LOGO_PATH = os.path.join(paths.get_common_face(), r'Icons')


class MCAFaceStagingOptionVars(optionvars.MCAOptionVars):
    """
    Option vars for the Face Staging UI
    """

    # strings
    MCAFaceStagingContentPath = {'default_value': paths.get_common_face(), 'docstring': 'Branch content path.'}

    # bools
    MCAFaceStagingShowSkeleton = {'default_value': 0, 'docstring': 'Face Mesh Edit Show Skeleton.'}
    MCAFaceStagingAutoMeshExport = {'default_value': 1, 'docstring': 'Auto Export mesh after editing.'}
    MCAFaceStagingAutoMeshMirror = {'default_value': 1, 'docstring': 'Auto Mirror mesh after editing.'}
    MCAFaceStagingTransferJoints = {'default_value': 0, 'docstring': 'Transfers Joints to the editing mesh.'}
    MCAFaceStagingSymmetry = {'default_value': 1, 'docstring': 'Sets the symmetry options when editing.'}
    MCAFaceStagingSaveBlendShapes = {'default_value': 0, 'docstring': 'Sets whether to save the blendshape rig scene.'}
    MCAFaceStagingExportShapes = {'default_value': 0, 'docstring': 'Sets whether to export blend shapes.'}
    MCAFaceStagingExportSK = {'default_value': 0, 'docstring': 'Sets whether to export SK.'}
    MCAFaceStagingProcessSkinning = {'default_value': 0, 'docstring': 'Sets whether to process skinning.'}
    MCAFaceStagingSaveRig = {'default_value': 0, 'docstring': 'Sets whether to save out cleaned up rig.'}
    MCAFaceStagingImportSourceHead = {'default_value': 0, 'docstring': 'Sets whether to import the source head.'}
    MCAFaceStagingOpeningSound = {'default_value': 1, 'docstring': 'Plays and opening sound if True.'}
    # int/float
    MCAFaceStagingUITab = {'default_value': 0, 'docstring': 'Latest Tab opened.'}
    MCAFaceStagingSourceHead = {'default_value': 0, 'docstring': 'Source head for this rig.'}
    MCAFaceStagingAssetID = {'default_value': 0, 'docstring': 'Asset id for this rig.'}


    ######################
    # For easier reading
    ######################
    @property
    def common_folder(self):
        """
        Returns an easier name for the latest tab selected.
        :return string: Returns an easier name for the latest tab selected.
        :rtype: Int
        """

        return self.MCAFaceStagingContentPath

    @common_folder.setter
    def common_folder(self, value):
        """
        Sets an easier name for the latest tab selected.
        :param value: Sets an easier name for the latest tab selected.
        """

        self.MCAFaceStagingContentPath = value

    @property
    def tabs(self):
        """
        Returns an easier name for the latest tab selected.
        :return string: Returns an easier name for the latest tab selected.
        :rtype: Int
        """

        return self.MCAFaceStagingUITab

    @tabs.setter
    def tabs(self, value):
        """
        Sets an easier name for the latest tab selected.
        :param value: Sets an easier name for the latest tab selected.
        """

        self.MCAFaceStagingUITab = value

    @property
    def open_sound(self):
        """
        Returns an easier name for the latest tab selected.
        :rtype: Int
        """

        return self.MCAFaceStagingOpeningSound

    @open_sound.setter
    def open_sound(self, value):
        """
        Sets an easier name for the latest tab selected.
        :param value: Sets an easier name for the latest tab selected.
        """

        self.MCAFaceStagingOpeningSound = value

    @property
    def source_head_selection(self):
        """
        Returns Source head index in combo box.
        :rtype: Int
        """

        return self.MCAFaceStagingSourceHead

    @source_head_selection.setter
    def source_head_selection(self, value):
        """
        Sets source head index in combo box.
        :rtype: Int
        """

        self.MCAFaceStagingSourceHead = value

    @property
    def asset_id_selection(self):
        """
        Returns asset id index in combo box.
        :rtype: Int
        """

        return self.MCAFaceStagingAssetID

    @asset_id_selection.setter
    def asset_id_selection(self, value):
        """
        Sets asset id index in combo box.
        :rtype: Int
        """

        self.MCAFaceStagingAssetID = value


class FaceStagingUI(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        ui_path = os.path.join(root_path, 'ui', 'face_staging_ui.ui')
        super().__init__(title='Face Staging',
                         ui_path=ui_path,
                         version=FaceStagingUI.VERSION)

        self.optionvars = MCAFaceStagingOptionVars()

        self.source_face_data = None
        self.region_data = None
        self.face_component = None
        self.mesh_markup = None
        self.edit_node = None

        self._on_startup()

        ###############################
        # Signals
        ###############################
        
        # Tabs
        self.ui.staging_tabWidget.currentChanged.connect(self._set_tabs)

        # Tool Bar
        self.ui.zero_flags_pushButton.clicked.connect(self.zero_flags)
        self.ui.flags_v_pushButton.clicked.connect(self.flags_visibility)
        self.ui.mirror_toolbar_pushButton.clicked.connect(self._mirror_selected_vertices)
        self.ui.eyelash_snap_pushButton.clicked.connect(self.eyelash_snap)
        self.ui.apply_animation_pushButton.clicked.connect(self.calibration_animation)
        self.ui.cut_animation_pushButton.clicked.connect(self.cut_animation)
        self.ui.overlay_on_pushButton.clicked.connect(self.add_overlay_texture)
        self.ui.overlay_off_pushButton.clicked.connect(self.remove_overlay_texture)
        self.ui.skinning_toolbar_pushButton.clicked.connect(self.open_skinning_tools)
        self.ui.new_head_plus_pushButton.clicked.connect(self.register_new_head)

        # asset id - top
        self.ui.asset_comboBox.currentIndexChanged.connect(self._asset_id_change)
        self.ui.open_model_pushButton.clicked.connect(self.import_model_file)
        self.ui.open_model_build_pushButton.clicked.connect(self._open_model_build_rig)
        self.ui.source_head_comboBox.currentIndexChanged.connect(self._set_source_head_selection_optionvars)

        # Mesh Info
        self.ui.add_tags_pushButton.clicked.connect(self._add_markup)
        self.ui.regions_listWidget.itemDoubleClicked.connect(self._add_markup)
        self.ui.remove_tags_pushButton.clicked.connect(self._remove_markup)
        self.ui.select_mesh_pushButton.clicked.connect(self._select_marked_up_meshes)
        self.ui.create_rig_pushButton.clicked.connect(self._create_rig_existing)
        self.ui.create_process_rig_pushButton.clicked.connect(self._create_rig_generate)
        self.ui.regions_listWidget.itemSelectionChanged.connect(self._populate_tagged_meshes)
        self.ui.tagged_listWidget.itemDoubleClicked.connect(self._remove_markup)
        self.ui.regions_listWidget.itemSelectionChanged.connect(self.set_region_logo)

        # Mesh Edit
        self.ui.toggle_local_axis_pushButton.clicked.connect(self._set_local_axis_display)
        self.ui.update_bs_list_pushButton.clicked.connect(self._populate_edit_meshes)
        self.ui.bs_list_listWidget.itemSelectionChanged.connect(self._populate_poses)
        self.ui.bs_list_listWidget.itemClicked.connect(self._populate_poses)
        self.ui.update_poses_pushButton.clicked.connect(self._populate_poses)
        self.ui.base_edit_pushButton.clicked.connect(self.base_edit_toggle)
        self.ui.base_edit_cancel_pushButton.clicked.connect(self.base_edit_cancel)
        self.ui.edit_replace_pushButton.clicked.connect(self.replace_base_mesh)
        self.ui.single_edit_pushButton.clicked.connect(self.single_pose_toggle)
        self.ui.cancel_edit_pushButton.clicked.connect(self.pose_edit_cancel)
        self.ui.multi_pose_edit_pushButton.clicked.connect(self.multi_pose_toggle)
        self.ui.paint_neutral_pushButton.clicked.connect(self.paint_neutral_toggle)
        self.ui.bs_list_listWidget.itemDoubleClicked.connect(self._select_blendshape_edit_meshes)
        self.ui.skin_list_listWidget.itemDoubleClicked.connect(self._select_skinned_edit_meshes)
        self.ui.pose_flag_listWidget.itemDoubleClicked.connect(self._select_pose_flag)
        self.ui.mirror_pose_pushButton.clicked.connect(self.mirror_pose_from_listwidget)
        self.ui.mirror_all_poses_pushButton.clicked.connect(self.mirror_all_poses)

        # Rigging
        self.ui.sl_rest_skin_pushButton.clicked.connect(self.restore_skinning)
        self.ui.sl_exp_skin_pushButton.clicked.connect(self.export_skinning)
        self.ui.sl_proc_skin_pushButton.clicked.connect(self.process_skinning_delete_mesh)
        self.ui.all_proc_skin_pushButton.clicked.connect(self.all_meshes_process_skinning)
        self.ui.save_rig_pushButton.clicked.connect(self.finish_save_rig)
        self.ui.all_exp_skin_pushButton.clicked.connect(self.export_all_skinning)

        ##### Check boxes
        self.ui.show_skeleton_checkBox.clicked.connect(self._set_edit_show_skeleton)
        self.ui.export_bs_checkBox.clicked.connect(self._set_auto_export_mesh)
        self.ui.auto_mirror_checkBox.clicked.connect(self._set_auto_mirror_mesh)
        self.ui.edit_transfer_joints_checkBox.clicked.connect(self._set_transfer_joints)
        self.ui.symmetry_checkBox.clicked.connect(self._set_edit_symmetry)
        self.ui.save_blendshape_scene_checkBox.clicked.connect(self._set_save_blendshape_optionvars)
        self.ui.export_shapes_checkBox.clicked.connect(self._set_export_shapes_optionvars)
        self.ui.export_sk_checkBox.clicked.connect(self._set_export_sk_optionvars)
        self.ui.generate_process_skinning_checkBox.clicked.connect(self._set_process_skinning_optionvars)
        self.ui.save_rig_checkBox.clicked.connect(self._set_save_rig_optionvars)
        self.ui.import_source_checkBox.clicked.connect(self._set_import_source_head_optionvars)
        self.ui.opening_sound_checkBox.clicked.connect(self._set_opening_sound_optionvars)

        # Menu Bar
        self.ui.actionRefresh_UI.triggered.connect(self.refreshUI)
        self.ui.actionSelected_Blend_Shapes.triggered.connect(self._export_selected)
        self.ui.actionAll_Blend_Shapes.triggered.connect(self._export_all_blendshapes)
        self.ui.actionModel_File_2.triggered.connect(self.export_skin_meshes_as_ma)
        self.ui.actionBase_Meshes_as_FBX.triggered.connect(self.export_skin_meshes_as_fbx)
        self.ui.actionFrom_Common_Location.triggered.connect(self.import_from_common)
        self.ui.actionFrom_Asset_Location.triggered.connect(self.import_from_asset_location)
        self.ui.actionCommone_Models.triggered.connect(self.open_common_in_explorer)
        self.ui.actionAsset_Location.triggered.connect(self.open_asset_location_in_explorer)
        self.ui.actionImportSkeleton.triggered.connect(self.import_skeleton)
        self.ui.actionExport_Skeleton.triggered.connect(self.export_skeleton)
        self.ui.actionDocumentation.triggered.connect(self.tools_documentation)
        self.ui.actionPipeline_Documentation.triggered.connect(self.pipeline_documentation)
        self.ui.actionPose_Documentation.triggered.connect(self.sculpting_documentation)
        self.ui.actionSkeletal_Mesh.triggered.connect(self.export_skeletal_mesh)
        self.ui.actionAnimation_Pose_File.triggered.connect(self.export_pose_file)
        self.ui.actionAnimation_Poses.triggered.connect(self.create_pose_file)
        self.ui.actionFrame_Poses.triggered.connect(self.print_frame_pose)
        self.ui.actionSource_Head_And_Data.triggered.connect(self.export_source_meshes)
        self.ui.actionRe_Connect_Blendshapes.triggered.connect(self._reconnect_shapes_to_rig)
        self.ui.actionSave_Animation_File.triggered.connect(self.save_calibration_animation)
        self.ui.actionRun_Skin_Converter_No_Delete_Source.triggered.connect(self.process_skinning_keep_mesh)

        # Vertex Snapping
        self.ui.expand_snapping_tools_pushButton.clicked.connect(self._on_expand_snapping_tools_clicked)
        self.ui.top_to_bottom_pushButton.clicked.connect(self._on_top_to_bottom_clicked)
        self.ui.bottom_to_top_pushButton.clicked.connect(self._on_bottom_to_top_clicked)
        self.ui.meet_at_middle_pushButton.clicked.connect(self._on_meet_at_middle_clicked)

    ###############################
    # Slots
    ###############################
    def _on_startup(self):
        """
        Initial commands on when opening the UI
        """

        self.asset_id_dict = {}
        self.asset_id = None
        self._populate_asset_ids()
        self.asset_id = self.get_asset_id_from_name()
        # Updates the regions
        self._populate_source_heads()

        self.ui.staging_tabWidget.setCurrentIndex(self.optionvars.tabs)
        self.ui.asset_comboBox.setCurrentIndex(self.optionvars.asset_id_selection)
        self._asset_id_change()

        self.ui.source_head_comboBox.setCurrentIndex(self.optionvars.source_head_selection)

        self.ui.tagged_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.pose_flag_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.engine_meshes_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.blendshape_skin_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Button Icons
        my_icon = resources.icon(r'default\flag_white.png')
        flags_vis = resources.icon(r'default\font_awesome_flag_64px.png')
        mirror_vert_icon = resources.icon(r'default\reflection.png')
        eyelash_icon = resources.icon(r'default\eye_closed.png')
        animation_icon = resources.icon(r'default\animation.png')
        cut_anim_icon = resources.icon(r'default\unavailable.png')
        overlay_icon = resources.icon(r'default\queue.png')
        overlay_close_icon = resources.icon(r'default\close.png')
        skin_tools_icon = resources.icon(r'default\tool.png')
        new_head_plus_icon = resources.icon(r'default\plus.png')
        expand_snapping_tools_icon = resources.icon(r'default\expand.png')
        self.ui.zero_flags_pushButton.setIcon(my_icon)
        self.ui.mirror_toolbar_pushButton.setIcon(mirror_vert_icon)
        self.ui.eyelash_snap_pushButton.setIcon(eyelash_icon)
        self.ui.flags_v_pushButton.setIcon(flags_vis)
        self.ui.apply_animation_pushButton.setIcon(animation_icon)
        self.ui.cut_animation_pushButton.setIcon(cut_anim_icon)
        self.ui.overlay_on_pushButton.setIcon(overlay_icon)
        self.ui.overlay_off_pushButton.setIcon(overlay_close_icon)
        self.ui.skinning_toolbar_pushButton.setIcon(skin_tools_icon)
        self.ui.new_head_plus_pushButton.setIcon(new_head_plus_icon)
        self.ui.expand_snapping_tools_pushButton.setIcon(expand_snapping_tools_icon)

        self.ui.vertex_snapping_frame.hide()

        # Set face region Icon
        self.set_region_logo()

        # Set the edit buttons
        self.set_ui_on_open()

        # set check boxes
        self.ui.show_skeleton_checkBox.setChecked(self.optionvars.MCAFaceStagingShowSkeleton)
        self.ui.export_bs_checkBox.setChecked(self.optionvars.MCAFaceStagingAutoMeshExport)
        self.ui.auto_mirror_checkBox.setChecked(self.optionvars.MCAFaceStagingAutoMeshMirror)
        self.ui.edit_transfer_joints_checkBox.setChecked(self.optionvars.MCAFaceStagingTransferJoints)
        self.ui.symmetry_checkBox.setChecked(self.optionvars.MCAFaceStagingSymmetry)
        self.ui.save_blendshape_scene_checkBox.setChecked(self.optionvars.MCAFaceStagingSaveBlendShapes)
        self.ui.export_shapes_checkBox.setChecked(self.optionvars.MCAFaceStagingExportShapes)
        self.ui.export_sk_checkBox.setChecked(self.optionvars.MCAFaceStagingExportSK)
        self.ui.generate_process_skinning_checkBox.setChecked(self.optionvars.MCAFaceStagingProcessSkinning)
        self.ui.save_rig_checkBox.setChecked(self.optionvars.MCAFaceStagingSaveRig)
        self.ui.import_source_checkBox.setChecked(self.optionvars.MCAFaceStagingImportSourceHead)
        self.ui.import_source_checkBox.setChecked(self.optionvars.MCAFaceStagingImportSourceHead)
        self.ui.opening_sound_checkBox.setChecked(self.optionvars.open_sound)

        # Color dividers
        self.ui.tool_divider_pushButton.setStyleSheet("background-color: black")
        self.ui.flags_divide_pushButton.setStyleSheet("background-color: black")
        self.ui.overlay_divide_pushButton.setStyleSheet("background-color: black")
        self.ui.eyelash_divide_pushButton.setStyleSheet("background-color: black")
        self.ui.mirror_divide_pushButton.setStyleSheet("background-color: black")
        self.ui.skin_tools_divide_pushButton.setStyleSheet("background-color: black")

        if self.ui.opening_sound_checkBox.isChecked():
            sounds.sound_tada()

    def tab_start_ups(self):
        index = self.ui.staging_tabWidget.currentIndex()
        if index == 0:
            self._populate_tagged_meshes()
            if not self.source_face_data:
                return
            skinned_regions = self.source_face_data.skinned_regions_list
            self._populate_regions(skinned_regions)
        elif index == 1:
            self._populate_poses()
            self._populate_blendshape_meshes()
            self._populate_edit_meshes()
        elif index == 2:
            self._populate_skinning_meshes()

    def set_region_logo(self):
        """
        Sets the logo that corresponds with the selected region in the list Widget on the mesh info.
        """

        region = listwidget_utils.get_qlist_widget_selected_items(self.ui.regions_listWidget)
        if not region:
            self.ui.region_icons_pushButton.setIcon(QIcon())
            return
        region = region[0]
        race = self.source_face_data.race
        logo = os.path.join(REGION_LOGO_PATH, f'{race}_{region}.JPG')
        if not os.path.exists(logo):
            self.ui.region_icons_pushButton.setIcon(QIcon())
            return
        self.ui.region_icons_pushButton.setIcon(QIcon(logo))
        # self.ui.region_icons_pushButton.setIconSize(QtCore.QSize(150,200))

    def tools_documentation(self):
        """
        Opens the Confluence page for the face tools.
        """

        webbrowser.open('https://counterplay.atlassian.net/wiki/spaces/CGH/pages/1911488547/Face+Staging+Tool')

    def pipeline_documentation(self):
        """
        Opens the Confluence page for the face tools.
        """

        webbrowser.open('https://counterplay.atlassian.net/wiki/spaces/CGH/pages/1700921367/Face+Workflow+and+Pipeline')

    def sculpting_documentation(self):
        """
        Opens the Confluence page for the face tools.
        """

        webbrowser.open('https://counterplay.atlassian.net/wiki/spaces/CGH/pages/1923776513/Sculpting+Poses')

    ##############################################
    # Set optionvars on Check boxes, Tabs, etc...
    ##############################################
    def _set_tabs(self):
        """
        Sets the optionvar that keeps track of which tab was selected and updates the tab info.
        """

        index = self.ui.staging_tabWidget.currentIndex()
        self.optionvars.tabs = index
        self.tab_start_ups()

    def _set_edit_show_skeleton(self):
        """
        Set the optionvar checkbox to show the skeleton when editing a mesh.
        """

        self.optionvars.MCAFaceStagingShowSkeleton = self.ui.show_skeleton_checkBox.isChecked()

    def _set_auto_export_mesh(self):
        """
        Set the optionvar checkbox to Auto Export mesh after editing.
        """

        self.optionvars.MCAFaceStagingAutoMeshExport = self.ui.export_bs_checkBox.isChecked()

    def _set_auto_mirror_mesh(self):
        """
        Set the optionvar checkbox to Auto Mirror mesh after editing.
        """

        self.optionvars.MCAFaceStagingAutoMeshMirror = self.ui.auto_mirror_checkBox.isChecked()

    def _set_edit_symmetry(self):
        """
        Set the optionvar checkbox for setting symmetry automatically when needed.
        """

        self.optionvars.MCAFaceStagingSymmetry = self.ui.symmetry_checkBox.isChecked()

    def _set_transfer_joints(self):
        """
        Set the optionvar checkbox for trasnfer joints.
        """

        self.optionvars.MCAFaceStagingTransferJoints = self.ui.edit_transfer_joints_checkBox.isChecked()

    def _set_save_blendshape_optionvars(self):
        """
        Set the optionvar checkbox for saving blendshape.
        """

        self.optionvars.MCAFaceStagingSaveBlendShapes = self.ui.save_blendshape_scene_checkBox.isChecked()

    def _set_export_shapes_optionvars(self):
        """
        Set the optionvar checkbox for exporting shapes.
        """

        self.optionvars.MCAFaceStagingExportShapes = self.ui.export_shapes_checkBox.isChecked()

    def _set_export_sk_optionvars(self):
        """
        Set the optionvar checkbox for exporting shapes.
        """

        self.optionvars.MCAFaceStagingExportSK = self.ui.export_sk_checkBox.isChecked()

    def _set_process_skinning_optionvars(self):
        """
        Set the optionvar checkbox for exporting shapes.
        """

        self.optionvars.MCAFaceStagingProcessSkinning = self.ui.generate_process_skinning_checkBox.isChecked()

    def _set_save_rig_optionvars(self):
        """
        Set the optionvar checkbox for exporting shapes.
        """

        self.optionvars.MCAFaceStagingSaveRig = self.ui.save_rig_checkBox.isChecked()

    def _set_import_source_head_optionvars(self):
        """
        Set the optionvar checkbox for importing source head.
        """

        self.optionvars.MCAFaceStagingImportSourceHead = self.ui.import_source_checkBox.isChecked()

    def _set_opening_sound_optionvars(self):
        """
        Set the optionvar checkbox for opening sound.
        """

        self.optionvars.open_sound = self.ui.opening_sound_checkBox.isChecked()

    def _set_source_head_selection_optionvars(self):
        """
        Set the optionvar for source head selection.
        """

        self.optionvars.source_head_selection = self.ui.source_head_comboBox.currentIndex()

    def _set_asset_id_selection_optionvars(self):
        """
        Set the optionvar for asset_id selection
        """

        self.optionvars.asset_id_selection = self.ui.asset_comboBox.currentIndex()

    def _populate_source_heads(self):
        """
        Populates the source head comboBox.
        """

        face_path = os.path.join(paths.get_common_face(), 'SourceHeads')
        source_files = [str(x) for x in os.listdir(face_path) if '.' not in x]
        self.ui.source_head_comboBox.addItems(source_files)

    def _populate_asset_ids(self):
        """
        Populates the asset ids in the combo box.
        """
        self.asset_id_dict = {}

        head_asset_dict = assetlist.get_asset_category_dict('head')

        for asset_id, mca_asset in head_asset_dict.items():
            self.asset_id_dict.setdefault(mca_asset.asset_name, mca_asset)
            self.ui.asset_comboBox.addItem(mca_asset.asset_name)

        """
        asset_list = assetlist.AssetList()
        self.asset_id_dict = {}
        display_names = []
        asset_id_list = asset_list.get_asset_ids('head')
        for asset_id in asset_id_list:
            asset = assetlist.AssetIDList(asset_id)
            self.asset_id_dict.setdefault(asset.display_name, asset)
            display_names.append(asset.display_name)

        self.ui.asset_comboBox.addItems(display_names)
        """

    def get_asset_id_from_name(self):
        """
        Returns the asset id of the chosen rig's Display Name

        :return: Returns the asset id of the chosen rig's Display Name
        :rtype: str
        """

        display_name = str(self.ui.asset_comboBox.currentText()).strip()
        asset = self.asset_id_dict.get(display_name, None)
        if not asset:
            return None
        return asset.asset_id

    def get_asset_sm_name_path(self):
        """
        Returns the asset name of the chosen rig's Display Name

        :return: Returns the asset name of the chosen rig's Display Name
        :rtype: str
        """
        
        display_name = str(self.ui.asset_comboBox.currentText()).strip()
        asset = self.asset_id_dict.get(display_name, None)
        full_path = asset.sm_path
        return full_path

    def get_asset_sk_name_path(self):
        """
        Returns the asset name of the chosen rig's Display Name

        :return: Returns the asset name of the chosen rig's Display Name
        :rtype: str
        """

        display_name = str(self.ui.asset_comboBox.currentText()).strip()
        asset = self.asset_id_dict.get(display_name, None)
        full_path = asset.sk_path
        return full_path

    def get_face_region_data(self, region):
        """
        Gets the face data from a text file.  Sets the FaceMeshRegionData.

        :param str region: The data associated with a specific type of mesh.
        """

        self.region_data = source_data.FaceMeshRegionData(region, self.source_face_data.data)

    def reset_pose_edit_buttons(self, keep_single=False):
        """
        Sets the edit buttons in the UI back to it's original colors.
        :param bool keep_single: If True, the single pose edit buttons will not reset.
        """

        if not keep_single:
            self.set_edit_buttons_inactive(self.ui.single_edit_pushButton, self.ui.single_edit_color_frame)
        self.set_edit_buttons_inactive(self.ui.paint_neutral_pushButton, self.ui.paint_neutral_frame)
        self.set_edit_buttons_inactive(self.ui.multi_pose_edit_pushButton, self.ui.multi_pose_edit_frame)
        self.set_edit_buttons_inactive(self.ui.base_edit_pushButton, self.ui.base_color_edit_frame)

    def set_ui_on_open(self):
        """
        Updates the Pose Edit buttons on start up, depending on what state the scene is in.
        """

        edit_node = self._get_edit_node()
        if not edit_node:
            self.reset_pose_edit_buttons()
            self.tab_start_ups()
            return
        if edit_node.edit_inst.single_pose:
            self.set_edit_buttons_active(self.ui.single_edit_pushButton, self.ui.single_edit_color_frame)
        elif edit_node.edit_inst.multi_pose:
            self.set_edit_buttons_active(self.ui.multi_pose_edit_pushButton, self.ui.multi_pose_edit_frame)
        elif edit_node.edit_inst.base_edit:
            self.set_edit_buttons_active(self.ui.base_edit_pushButton, self.ui.base_color_edit_frame)
        if edit_node.edit_inst.paint_neutral and edit_node.edit_inst.single_pose:
            self.set_edit_buttons_active(self.ui.paint_neutral_pushButton, self.ui.paint_neutral_frame)

    def set_edit_buttons_active(self, button, frame):
        """
        Sets a QPushButton and a Qframe to the active color.

        :param QPushButton button: The QT button that the color is being applied.
        :param Qframe frame: The QT Frame that the color is being applied.
        """

        button.setStyleSheet(STAGING_BUTTON_ACTIVE_COLORS)
        frame.setStyleSheet(STAGING_BACKGROUND_GREY)

    def set_edit_buttons_inactive(self, button, frame):
        """
        Sets a QPushButton and a Qframe to the inactive color.

        :param QPushButton button: The QT button that the color is being applied.
        :param Qframe frame: The QT Frame that the color is being applied.
        """

        button.setStyleSheet(STAGING_BUTTON_COLORS)
        frame.setStyleSheet(STAGING_BUTTON_COLORS)

    def get_display_layers(self):
        """
        Gets all the display layers from frag.DisplayLayers
        """

        frag_rig = self.get_rig()
        dsp_lyrs = frag_rig.get_frag_children(of_type=frag.DisplayLayers)
        if not dsp_lyrs:
            return
        return dsp_lyrs[0]

    ####################
    # Menu Bar
    ####################
    # File
    # Export

    def print_frame_pose(self):
        """
        Prints a list of frame numbers with the pose name

        :return: Returns a dictionary with frame numbers with the pose name
        :rtype: Dictionary
        """

        frame_pose = {}
        parameters = face_util.get_parameters_region_instance(self.asset_id, 'head_blendshape')
        parameters_list = parameters.get_parameters_list(sort_by_frame=True)

        for parameter in parameters_list:
            print(f'{parameter.frame}:{parameter.parameter_name}')
            frame_pose.setdefault(parameter.frame, parameter.parameter_name)
        return frame_pose

    @decorators.track_fnc
    def add_overlay_texture(self):
        """
        Adds a Clown Mask to the selected objs.
        """

        objs = pm.selected()
        objs = [x for x in objs if x.hasAttr(mesh_markup_rig.MCA_MESH_MARKUP)]
        if not objs:
            return
        for obj in objs:
            obj = face_model.FaceModel(obj)
            region_data = face_util.get_face_region_data(self.asset_id, obj.region)
            overlay_path = region_data.clown_mask
            if not overlay_path:
                return
            overlay_path = os.path.join(paths.get_common_face(), overlay_path)
            textures.add_overlay_textures(objs, overlay_path)

    def remove_overlay_texture(self):
        """
        Removes the Clown Mask from selected objs.
        """

        textures.remove_overlay_textures()

    @decorators.track_fnc
    def _export_selected(self):
        """
        Exports selected blend shapes to the asset directory.
        """

        selection = cmds.ls(sl=True)
        # Check to see if the there is source data loaded.  # Data about the face meshes
        if not self.source_face_data:
            return
        path = paths.get_face_blendshape_path(self.asset_id)
        region_list = self.source_face_data.regions_list

        blendshape_regions = []
        for region in region_list:
            category = self.source_face_data.data['regions'][region].get('mesh_category', None)
            if category and category == 'blendshape_mesh':
                blendshape_regions.append(region)
        verified_pose = []
        for region in blendshape_regions:
            parameter_inst = face_util.get_parameters_region_instance(self.asset_id, region)
            pose_list = parameter_inst.get_pose_list()
            [verified_pose.append(x) for x in selection if x in pose_list]

        message = ', '.join(verified_pose)
        result = pm.confirmDialog(title='Export and Save Pose?',
                                    message=f'Export these poses?\n{message}',
                                    button=['Yes', 'No'],
                                    defaultButton='Yes',
                                    cancelButton='No',
                                    dismissString='No')
        if result == 'No':
            return

        pose_grp = self.get_pose_grp()
        pm.parent(verified_pose, w=True)

        face_import_export.export_blendshapes(path=path, meshes=verified_pose, remove_mtls=True)
        if pose_grp:
            pm.parent(verified_pose, pose_grp)
        dialogs.display_view_message(text='Blend Shapes Exported', header='Face Staging', fade_time=220)

    @decorators.track_fnc
    def _export_all_blendshapes(self, skip_dialog=False):
        """
        Exports all blend shape poses in the scene.
        """
        if not skip_dialog:
            result = pm.confirmDialog(title='Export and Save Pose?',
                                        message=f'Export all blend shapes?',
                                        button=['Yes', 'No'],
                                        defaultButton='Yes',
                                        cancelButton='No',
                                        dismissString='No')
            if result == 'No':
                return

        if not self.source_face_data:
            return
        region_list = self.source_face_data.regions_list
        regions = []
        for region in region_list:
            category = self.source_face_data.data['regions'][region].get('mesh_category', None)
            if category and category == 'blendshape_mesh':
                regions.append(region)
        for region in regions:
            face_import_export.export_all_blendshapes(self.asset_id, region)
        dialogs.display_view_message(text='All Blend Shapes Exported', header='Face Staging', fade_time=220)

    def import_skeleton(self):
        """
        Imports .skl skeleton.
        """

        mca_asset = assetlist.get_asset_by_id(self.asset_id)

        skel_path = mca_asset.skel_path
        if os.path.exists(os.path.join(skel_path)):
            skel = skel_utils.import_skeleton(skel_path)
        else:
            skel_path = paths.get_common_face_skeletons()
            skel_path = os.path.join(skel_path, 'human_face_skeleton.skl')
            skel = skel_utils.import_skeleton(skel_path)
        if not skel:
            logger.warning('No skeleton file exists to import')
            return
        pm.select(skel, hi=True)
        [x.radius.set(0.5) for x in pm.selected()]
        [x.drawStyle.set(2) for x in pm.selected() if x.hasAttr('chainEnd') and x.chainEnd.get() == 'neck']

    @decorators.track_fnc
    def export_skeleton(self):
        """
        Exports the .skl skeleton to the asset location.
        """

        result = dialogs.question_prompt(title='Export Skeleton?', text='Export Skeleton?')
        if result != 'Yes':
            return

        multipleFilters = "Maya ASCII (*.skl)"
        asset_dir = paths.get_asset_path(self.asset_id)

        export_path = pm.fileDialog2(fileFilter=multipleFilters, dialogStyle=1, fm=0, dir=asset_dir)
        if not export_path:
            return
        path = export_path[0]
        skel_utils.export_skeleton(path, pm.PyNode('root'))

    @decorators.track_fnc
    def export_skin_meshes_as_ma(self):
        """
        Exports the skinned meshes as .ma
        """

        self.export_skinned_meshes(fbx_export=False)

    @decorators.track_fnc
    def export_skin_meshes_as_fbx(self):
        """
        Exports the skinned meshes as fbx
        """

        self.export_skinned_meshes(fbx_export=True)

    @decorators.track_fnc
    @ma_decorators.keep_selection_decorator
    def export_skinned_meshes(self, fbx_export=True):
        """
        Export the skinned meshes.

        :param bool fbx_export: if True, the meshes will be exported as an FBX.
        """

        meshes = self.get_all_skinned_meshes()
        if not meshes:
            return

        if fbx_export:
            multipleFilters = "Fbx (*.fbx;*.FBX)"
        else:
            multipleFilters = "Maya ASCII (*.ma)"

        asset_dir = paths.get_asset_path(self.asset_id)

        export_path = pm.fileDialog2(fileFilter=multipleFilters, dialogStyle=1, fm=0, dir=asset_dir)
        if not export_path:
            return
        export_path = export_path[0]

        temp_meshes = []
        for mesh in meshes:
            dup_mesh = pm.duplicate(str(mesh))[0]
            pm.parent(dup_mesh, w=True)
            temp_meshes.append(dup_mesh)
            dup_mesh.rename(str(mesh))
            dup_mesh.v.set(1)

        display_layers.remove_objects_from_layers(temp_meshes)
        try:
            pm.select(temp_meshes)
            cmds.file(rename=export_path)
            if fbx_export:
                fbx_utils.export_fbx(fbx_path=export_path, node_list=temp_meshes)
            else:
                cmds.file(force=True, exportSelected=True, type="mayaAscii", mergeNamespaceWithRoot=True)
            logger.info(f'Success!\nMeshes were exported.\n\n{export_path}')
        except:
            raise
        finally:
            pm.delete(temp_meshes)
            dialogs.display_view_message(text=f'Meshes Exported Successfully!', header='Face Staging', fade_time=220)

    @decorators.track_fnc
    def open_common_in_explorer(self):
        """
        Opens the face common folder in Windows Explorer.
        """

        common_directory = os.path.join(paths.get_common_face(), 'CommonModels')
        common_directory = os.path.normpath(common_directory)
        subprocess.Popen(r'explorer ' + common_directory)
        return

    @decorators.track_fnc
    def open_asset_location_in_explorer(self):
        """
        Opens the asset folder in Windows Explorer.
        """

        asset_directory = paths.get_asset_path(asset_id=self.asset_id, full_path=True)
        asset_directory = os.path.normpath(asset_directory)
        subprocess.Popen(r'explorer ' + asset_directory)
        return

    @decorators.track_fnc
    def import_from_common(self):
        """
        Imports .ma files from starting from the common file directory.
        """

        multiple_filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
        starting_directory = os.path.join(paths.get_common_face(), 'CommonModels')
        filepath = pm.fileDialog2(fileFilter=multiple_filters,
                                    dialogStyle=1,
                                    dir=starting_directory,
                                    fm=4)
        if filepath:
            [pm.importFile(x) for x in filepath]
            self._populate_tagged_meshes()

    @decorators.track_fnc
    def import_from_asset_location(self):
        """
        Imports .ma files from starting from the asset file directory.
        """

        multiple_filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
        starting_directory = paths.get_asset_path(asset_id=self.asset_id, full_path=True)
        filepath = pm.fileDialog2(fileFilter=multiple_filters,
                                    dialogStyle=1,
                                    dir=starting_directory,
                                    fm=4)
        if filepath:
            [pm.importFile(x) for x in filepath]
            self._populate_tagged_meshes()

    @decorators.track_fnc
    def create_pose_file(self):
        pose_files.create_face_pose_file(create_skeleton=False)

    @decorators.track_fnc
    def export_skeletal_mesh(self):
        """
        Exports head SK
        """

        meshes = self.get_all_skinned_meshes()
        frag_root = frag.get_frag_root_by_assetid(self.asset_id)
        root_joint = frag_root.rootJoint.listConnections()[0]
        sk_path = self.get_asset_sk_name_path()

        face_util.export_head_sk(meshes, root_joint, sk_path)

        dialogs.display_view_message(text=f'SK Export Successful!', header='Face Staging', fade_time=220)

    @decorators.track_fnc
    def export_pose_file(self):
        """
        Exports a duplicate skeleton file with the poses bake.

        """

        result = pm.confirmDialog(title='Export Pose File?',
                                    message='Export the animated pose file?',
                                    button=['Yes', 'No'],
                                    defaultButton='Yes',
                                    cancelButton='No',
                                    dismissString='No')
        if result == 'No':
            return
        multiple_filters = "Fbx (*.fbx;*.FBX);;All Files (*.*)"
        asset_directory = paths.get_asset_path(asset_id=self.asset_id, full_path=True)
        asset_directory = os.path.normpath(asset_directory)
        file_path = pm.fileDialog2(fileFilter=multiple_filters,
                                    dialogStyle=1,
                                    dir=asset_directory,
                                    fm=3)
        if not file_path:
            return
        pose_files.export_face_pose_file(file_path[0])
        dialogs.display_view_message(text=f'Pose File Successful!', header='Face Staging', fade_time=220)

    @decorators.track_fnc
    def import_model_file(self):
        """
        Imports the model file

        """
        result = dialogs.question_prompt(title='Open model file?', text='Open model file?')
        if result != 'Yes':
            return False
        pm.newFile(f=True)
        sm_path = self.get_asset_sm_name_path()
        if not os.path.exists(sm_path):
            dialogs.info_prompt(title="File Doesn't Exist",
                                    text='The SM FBX File does not exist or is not named correctly.\n'
                                    f'The name should be:\n{sm_path}')
            return
        imported_objs = fbx_utils.import_fbx(sm_path)
        if imported_objs:
            imported_list = [x for x in imported_objs if isinstance(x, pm.nt.Transform)]
            face_util.face_scene_setup(imported_list[0])
        self.set_ui_on_open()
        dialogs.display_view_message(text=f'Model File Imported Successfully!', header='Face Staging', fade_time=220)
        return True

    @decorators.track_fnc
    def export_source_meshes(self):
        """
        Exports the source meshes and creates a new source rig.\
        """

        result = dialogs.question_prompt(title='Export Source Files?', text='Export Source Files?')
        if result != 'Yes':
            return

        face_component = self.get_face_component()
        if not face_component:
            dialogs.info_prompt(title='Need A Rig', text='Need to be in a rig file.\nNo Face Mesh Component or Rig found.')
            return

        blendshape_meshes = self.get_all_blendshape_meshes()
        if not blendshape_meshes:
            dialogs.info_prompt(title='No Blend Shapes Meshes',
                                text='No blend shapes meshes found.')
            return
        save_source_data = False
        mca_asset = assetlist.get_asset_by_id(self.asset_id)
        asset_name = mca_asset.asset_name
        face_path = os.path.join(paths.get_common_face(), 'SourceHeads', asset_name)
        files = os.listdir(face_path)

        if not source_data.FACE_FILE_NAME in files:
            save_source_data = True
        else:
            result = dialogs.question_prompt(title='Re-Save Face Data?', text='The source text files already exist.\n'
                                                'Re-Export Source Data Files?\n'
                                                'This is not the Meshes!\nThis is the text data associated with '
                                                'the mesh file.')
            if result != 'Yes':
                save_source_data = False

        source_list = source_meshes.convert_all_to_source_mesh(mesh_list=blendshape_meshes,
                                                                asset_id=self.asset_id,
                                                                mesh_component=face_component.pynode)

        source_meshes.export_source_shapes(source_list=source_list,
                                            asset_id=self.asset_id,
                                            save_source_data=save_source_data)
        dialogs.display_view_message(text=f'Source Meshes Exported Successfully!', header='Face Staging', fade_time=220)

    ####################
    # Side Toolbar
    ####################
    def get_rigs(self):
        """
        Returns a list of all the frag rigs in the scene.

        :return: Returns a list of all the frag rigs in the scene.
        :rtype: list(FRAGRig)
        """

        all_roots = frag.get_all_frag_roots()
        all_frag_rigs = list(map(lambda x: x.get_rig(), all_roots))
        all_frag_rigs = list(set(all_frag_rigs))
        return all_frag_rigs

    def get_rig(self):
        """
        Returns the frag by the asset ID.

        :return: Returns the frag by the asset ID.
        :rtype: FRAGRig
        """

        frag_root = frag.get_frag_root_by_assetid(self.asset_id)
        if not frag_root:
            return
        return frag_root.get_rig()

    def get_pose_grp(self):
        """
        Returns the pose grp.  The grp that the blend shapes are under.

        :return: Returns the pose grp.  The grp that the blend shapes are under.
        :rtype: pm.nt.Transform
        """

        frag_rig = self.get_rig()
        if not frag_rig:
            return
        if not frag_rig.hasAttribute('facePoseGrp'):
            logging.warning(f'There is no pose group attached to the {frag_rig}.')
            pose_grp = [x.node() for x in pm.ls('*.isPoseGrp', r=True, o=True, type=pm.nt.Transform)]
            if not pose_grp:
                logging.warning(f'Cannot find the pose group in the scene!')
                return
            else:
                return pose_grp[0]
        return frag_rig.facePoseGrp.get()

    def get_parameter_node(self):
        """
        Returns the FRAG parameters node.

        :return: Returns the FRAG parameters node.
        :rtype: FragFaceParameters
        """

        frag_rig = self.get_rig()
        if not frag_rig:
            return
        parameter_node = frag_rig.get_frag_children(of_type=frag.FragFaceParameters)
        if not parameter_node:
            return
        return parameter_node[0]

    def get_face_component(self):
        """
        Returns the FRAG face mesh component.

        :return: Returns the FRAG face mesh component.
        :rtype: FaceMeshComponent
        """

        frag_root = frag.get_frag_root_by_assetid(self.asset_id)
        if not frag_root:
            return
        skeletal_mesh = frag_root.get_skeletal_mesh()
        face_components = skeletal_mesh.get_frag_children(of_type=frag.FaceMeshComponent)
        if not face_components:
            return
        self.face_component = face_components[0]
        return self.face_component

    def get_all_skinned_meshes(self):
        """
        Returns a list of meshes that get skinned.

        :return: Returns a list of meshes that get skinned.
        :rtype: list(pm.nt.Transform)
        """

        face_component = self.get_face_component()
        if not face_component:
            return
        skinned_meshes = face_component.get_all_category_meshes(frag.FACE_SKINNED_CATEGORY)
        return skinned_meshes

    def get_all_blendshape_meshes(self):
        """
        Returns a list of meshes that are blend shapes.

        :return: Returns a list of meshes that are blend shapes.
        :rtype: list(pm.nt.Transform)
        """

        face_component = self.get_face_component()
        if not face_component:
            return
        blendshape_meshes = face_component.get_all_category_meshes(frag.FACE_BLENDSHAPE_CATEGORY)
        return blendshape_meshes

    @decorators.track_fnc
    def eyelash_snap(self):
        """
        Snaps eyelash/shadow/tear to head mesh based on UV coordinates for asset ID
        """

        eyelash_snapping.eyelash_snap_action()

    @decorators.track_fnc
    def calibration_animation(self):
        """
        Adds an animation to the rig scene
        """

        frag_rig = self.get_rig()
        if not frag_rig:
            return
        flags = frag_rig.get_flags()

        path = os.path.join(paths.get_common_face(), 'Animations', 'face_calibration.ma')
        anim_curves_component = frag.AnimatedCurvesComponent.import_animated_curve_data(path)
        anim_curves_component.restore_all_animation_curves(flags)
        pm.playbackOptions(min=anim_curves_component.startFrame.get(), max=anim_curves_component.endFrame.get())
        anim_curves_component.remove()
        dialogs.display_view_message(text=f'Animation Applied Successfully!', header='Face Staging', fade_time=220)

    def cut_animation(self):
        """
        Removes the animation from the rig.
        """

        frag_rig = self.get_rig()
        if not frag_rig:
            return
        flag_utils.cut_all_flag_animations(frag_rig)
        dialogs.display_view_message(text=f'Animation Cut Successfully!', header='Face Staging', fade_time=220)

    @decorators.track_fnc
    def save_calibration_animation(self):
        """
        Saves an animation to a file
        """
        result = dialogs.question_prompt(title='Save Animation?', text='Overwrite the Calibration Animation?')
        if result != 'Yes':
            return

        frag_rig = self.get_rig()
        if not frag_rig:
            return
        flags = frag_rig.get_flags()

        anim_curves_component = frag.AnimatedCurvesComponent.create(frag_rig)
        anim_curves_component.store_all_animation_curves(flags)

        path = os.path.join(paths.get_common_face(), 'Animations', 'face_calibration.ma')
        anim_curves_component.export(path)
        anim_curves_component.remove()
        dialogs.display_view_message(text=f'Animation Saved Successfully!', header='Face Staging', fade_time=220)

    @decorators.track_fnc
    def zero_flags(self):
        """
        Zeros out the flags.
        """

        selection = pm.selected()
        if selection:
            flag_utils.zero_flags(selection)
            self.tab_start_ups()
            return

        all_frag_rigs = self.get_rigs()
        flag_utils.zero_flags(all_frag_rigs)
        self.tab_start_ups()

    @decorators.track_fnc
    def flags_visibility(self):
        """
        Sets the flags to invisible using the layers.
        """

        selection = pm.selected()
        if selection:
            flag_utils.flags_visibility(selection, toggle=True)
            return

        all_frag_rigs = self.get_rigs()
        flag_utils.flags_visibility(all_frag_rigs, toggle=True)

    @decorators.track_fnc
    def refreshUI(self):
        """
        Refreshes the UI.
        """

        FaceStagingUI()

    @decorators.track_fnc
    def _mirror_selected_vertices(self):
        """
        Mirrors selected vertices.
        """

        selected = cmds.ls(sl=True, fl=True)
        if not selected:
            dialogs.info_prompt(title='Select Vertices', text='Please select the vertices you wish to mirror')
            return

        mesh = pm.ls(selected[0], o=True)[0].getParent()
        mesh = face_model.FaceModel(mesh)
        if not mesh.region:
            logger.warning('Cannot mirror.  The mesh does not have any markup.')
            return

        region_data = face_util.get_face_region_data(self.asset_id, mesh.region)

        mirror_data = region_data.get_mirror_data()
        mirror_data.mirror_vertices(mesh.mesh, selected, axis=(-1, 1, 1))

    def save_blendshape_rig(self, just_rename=False):
        """
        Saves the scene as the blend shape rig scene.
        """
        mca_asset = assetlist.get_asset_by_id(self.asset_id)
        scene_name = os.path.join(mca_asset.rigs_path, f'{mca_asset.file_name}_blendshape_rig.ma')

        cmds.file(rename=scene_name)
        if not just_rename:
            cmds.file(save=True, type='mayaAscii')

    @decorators.track_fnc
    def register_new_head(self):
        """
        Opens asset register tool UI and pre-sets category to head.
        """

        asset_reg_tool = ma_asset_register.MayaAssetRegister()
        asset_reg_tool.ui.categoryBox.setCurrentText('head')
        asset_reg_tool.on_new_button_pressed()

    @decorators.track_fnc
    def open_skinning_tools(self):
        """
        Opens face skinning tools UI.
        """
        face_skinning_tool.FaceSkinning()

    ####################
    # Asset ID
    ####################
    def _asset_id_change(self):
        """
        Updates ui data based on the current asset id change.
        """

        self.asset_id = self.get_asset_id_from_name()
        if not self.asset_id:
            return
        try:
            self.source_face_data = face_util.get_source_face_data(self.asset_id)
        except FileNotFoundError:
            self.source_face_data = face_util.get_common_face_data()

        skinned_regions = self.source_face_data.skinned_regions_list
        self._populate_regions(skinned_regions)
        self._set_asset_id_selection_optionvars()

    ####################
    # Mesh Info
    ####################
    def _populate_regions(self, regions_list, selected_region=None):
        """
        Populates a QlistWidget with the names of the regions.

        :param list(str) regions_list: A list of regions.  Region is the top level name for the mesh data.
        :param str selected_region: A region name
        """

        self.ui.regions_listWidget.clear()
        self.ui.regions_listWidget.addItems(regions_list)
        if not selected_region:
            self.ui.regions_listWidget.setCurrentRow(0)
        region = listwidget_utils.get_qlist_widget_selected_items(self.ui.regions_listWidget)[0]
        # Update the self.region_data, head_blendshape, head_mesh, eye_left_mesh, etc...
        self.get_face_region_data(region)
        self._populate_tagged_meshes()

    def _populate_tagged_meshes(self):
        """
        Populates a QlistWidget with the names tagged meshes.  These meshes are associated with the region data.
        """

        # Get the region
        region = listwidget_utils.get_qlist_widget_selected_items(self.ui.regions_listWidget)
        if not region:
            return
        region = region[0]
        self.ui.tagged_listWidget.clear()
        # Get all the meshes in the scene with markup
        self.mesh_markup = mesh_markup_rig.RigMeshMarkup.create()
        items = self.mesh_markup.get_mesh_list_in_region(region, as_string=True)
        [QLabelTextButtonQWidget.create(self.ui.tagged_listWidget, x, color=STAGING_COLOR_GREEN) for x in items]
        #self.ui.tagged_listWidget.addItems(items)
        if items:
            self.ui.tagged_listWidget.setCurrentRow(0)

    def select_tagged_meshes(self):
        """
        Selects a mesh in a QList Widget.
        """

        self.select_item_from_list_widget(self.ui.tagged_listWidget)

    def _add_markup(self):
        meshes = pm.selected()
        usable_meshes = []
        for mesh in meshes:
            mesh_children = lists.get_first_in_list(mesh.listRelatives(children=True))
            if isinstance(mesh_children, pm.nt.Mesh):
                usable_meshes.append(str(mesh))

        if not usable_meshes:
            dialogs.info_prompt(title='No Mesh Usable Meshes Selected', text='Select a mesh and try again')
            return

        region = listwidget_utils.get_qlist_widget_selected_items(self.ui.regions_listWidget)[0]
        # Update the self.region_data, head_blendshape, head_mesh, eye_left_mesh, etc...
        self.get_face_region_data(region)

        #markups = self.region_data.get_mesh_dict()
        q_items = self.get_text_from_list_widget(self.ui.tagged_listWidget)
        meshes = [x for x in usable_meshes if str(x) not in q_items]
        #self.ui.tagged_listWidget.addItems(meshes)
        [QLabelTextButtonQWidget.create(self.ui.tagged_listWidget, str(x), color=STAGING_COLOR_GREEN) for x in meshes]

        # Adds the markup
        if meshes:
            type_name = self.region_data.mesh_type_name
            category = self.region_data.mesh_category
            side = self.region_data.side
            mirror_type = self.region_data.mirror_type
            source_head = self.region_data.source_head
            for mesh in meshes:
                mesh_markup_rig.MeshMarkup.create(mesh=pm.PyNode(mesh),
                                                    type_name=type_name,
                                                    category=category,
                                                    side=side,
                                                    mirror_type=mirror_type,
                                                    source_head=source_head,
                                                    region=region)

        self._populate_tagged_meshes()

    def _remove_markup(self):
        """
        Removes the attributes that has the mesh data.
        """

        selected_meshes = self.get_text_from_list_widget(self.ui.tagged_listWidget)
        if not selected_meshes:
            return

        result = dialogs.question_prompt(title='Remove the mesh markup?', text='Remove the mesh markup?')
        if result != 'Yes':
            return

        [cmds.deleteAttr(f'{x}.{mesh_markup_rig.MCA_MESH_MARKUP}') for x in selected_meshes]
        self._populate_tagged_meshes()

    def _select_marked_up_meshes(self):
        """
        Selects meshes that are in a QListWidget.
        """
        self._select_qwidget_objs(self.ui.tagged_listWidget)

    def _select_blendshape_edit_meshes(self):
        """
        Selects meshes that are in a QListWidget.
        """
        self._select_qwidget_objs(self.ui.bs_list_listWidget)

    def _select_skinned_edit_meshes(self):
        """
        Selects meshes that are in a QListWidget.
        """
        self._select_qwidget_objs(self.ui.skin_list_listWidget)

    def _select_pose_flag(self):
        """
        Selects meshes that are in a QListWidget.
        """
        self._select_qwidget_objs(self.ui.pose_flag_listWidget)

    def _select_qwidget_objs(self, qlist_widget):
        selected_meshes = self.get_text_from_list_widget(qlist_widget)
        if selected_meshes:
            pm.select(selected_meshes)

    ###############################
    # Create Rig
    ###############################
    def _create_rig(self, source_head_name=None, skip_dialog=False):
        """
        Runs the Rig template and creates the blend shape rig.
        """

        mca_asset = assetlist.get_asset_by_id(self.asset_id)

        template = self.source_face_data.rig_template
        if not template:
            logger.warning(f'{mca_asset.asset_name}: Rig does not have a rig template set in the source data.')
            return

        if not skip_dialog:
            result = dialogs.question_prompt(title='Create Head Rig?', text='Do you wish to build the Head Rig?')
            if result != 'Yes':
                return

        mesh_check = face_util.get_all_scene_face_meshes()
        if not mesh_check:
            logger.warning('No tagged face mesh found in scene.')
            return

        self.import_skeleton()
        # import the template module
        exec(f'from {TEMPLATES_PATH} import {template.split(".")[0]}')

        # Execute the Rig Template
        head_template = eval(f'{template}()')
        # Make sure the asset id is correct.
        head_template.asset_id = self.asset_id
        if source_head_name:
            head_template.source_head_name = source_head_name
            head_template.generate_shapes = True
        head_template.rig()

        # populate listWidgets
        self.tab_start_ups()
        if self.ui.save_blendshape_scene_checkBox.isChecked():
            self.save_blendshape_rig()
        else:
            self.save_blendshape_rig(just_rename=True)

        face_component = self.get_face_component()
        if not face_component:
            return
        head_mesh = face_component.head_blendshape
        parameter_node = self.get_parameter_node()
        face_util.face_scene_setup(focus_object=head_mesh.mesh, rig_node=parameter_node.pynode)

        if source_head_name or self.ui.import_source_checkBox.isChecked():
            if not source_head_name:
                source_head_name = mca_asset.asset_name
            source_meshes.connect_source_meshes_to_rig(source_head_name, parameter_node)

        dialogs.display_view_message(text='Rig Build Complete', header='Face Staging Tool', fade_time=220)

    @decorators.track_fnc
    def _create_rig_existing(self):
        """
        Creates the rig with existing blend shapes.
        """

        self._create_rig()
        dialogs.display_view_message(text='Blend shapes were imported successfully', header='Face Staging', fade_time=220)
        pm.select(cl=True)

    @decorators.track_fnc
    def _create_rig_generate(self):
        """
        Creates the rig and generates new blend shapes.
        """

        mca_asset = assetlist.get_asset_by_id(self.asset_id)

        result = dialogs.question_prompt(title='Create Head Rig?', text=f'Do you wish to build a new head rig for '
                                                                        f'{mca_asset.asset_name}?')
        if result != 'Yes':
            return
        s = time.time()
        asset_directory = mca_asset.general_path
        source_name = mca_asset.asset_name
        self._create_rig(source_name, skip_dialog=True)

        create_flags = self.create_flags_from_common()

        skel_utils.export_skeleton(mca_asset.skel_path, pm.PyNode('root'))
        meshes = self.get_all_skinned_meshes()

        if self.ui.generate_process_skinning_checkBox.isChecked():
            self.all_meshes_process_skinning(skip_dialog=True)
            fileio.touch_path(mca_asset.skin_data_path)
            list(map(lambda x: face_skinning.export_face_skinning_to_file(self.asset_id, x), meshes))

        if self.ui.export_shapes_checkBox.isChecked():
            self._export_all_blendshapes(skip_dialog=True)

        if self.ui.export_sk_checkBox.isChecked():
            unskinned_list = [x for x in meshes if not skin_utils.get_skin_cluster_from_geometry(x)]
            if unskinned_list:
                logger.warning(f'These meshes were not skinned: {unskinned_list}')
            self.export_skeletal_mesh()
            file_path = os.path.join(asset_directory, 'Animations')
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            pose_files.export_face_pose_file(file_path)
            self.cut_animation()

        if self.ui.save_rig_checkBox.isChecked():
            face_util.clean_and_save_face_rig(self.asset_id)
            pm.select(cl=True)

        dialogs.display_view_message(text='Blend shapes were generated successfully', header='Face Staging',
                                     fade_time=220)
        pm.select(cl=True)
        e = time.time()
        x = e-s
        logger.info(f'Rig built in {x/60} minutes')

    def _open_model_build_rig(self):
        model_file = self.import_model_file()
        if not model_file:
            return
        self._create_rig(skip_dialog=True)
        dialogs.display_view_message(text='Blend shapes were imported successfully', header='Face Staging', fade_time=220)
        pm.select(cl=True)

    ####################################
    # Vertex Snapping Tools
    ####################################
    def switch_vertex_snapping_icon(self):
        expand_snapping_tools_icon = resources.icon(r'default\expand.png')
        collapse_snapping_tools_icon = resources.icon(r'default\collapse.png')
        if self.ui.vertex_snapping_frame.isVisible():
            self.ui.expand_snapping_tools_pushButton.setIcon(expand_snapping_tools_icon)
        else:
            self.ui.expand_snapping_tools_pushButton.setIcon(collapse_snapping_tools_icon)

    def _on_expand_snapping_tools_clicked(self):
        if self.ui.vertex_snapping_frame.isVisible():
            self.switch_vertex_snapping_icon()
            self.ui.snappable_regions_comboBox.clear()
            self.ui.vertex_snapping_frame.hide()
            return
        else:
            self.switch_vertex_snapping_icon()
            snappable_items = ['Lips', 'Right Eyelid', 'Left Eyelid']
            list(map(lambda x: self.ui.snappable_regions_comboBox.addItem(x), snappable_items))
            self.ui.vertex_snapping_frame.show()

    def _on_bottom_to_top_clicked(self):
        """
        Snaps verts in selected region from bottom to top.
        """
        smooth_mesh = self.ui.snap_smoothing_checkBox.isChecked()
        smooth_amount = self.ui.snap_smoothing_horizontalSlider.value()

        common_data_path = os.path.join(paths.get_common_face(), 'rig_source_data.json')
        vertex_snap_data = face_vertex_data.SourceFaceEyelashShelf.load_vertex_data(common_data_path, 'head_blendshape')
        region = self.ui.snappable_regions_comboBox.currentText()
        head = pm.selected()
        if not head:
            logger.warning('Please first select head mesh')
            return
        else:
            head = naming.get_basename(head[0])
        if region == 'Lips':
            vertex_snap_data.snap_lips_bottom_to_top(head, smooth=smooth_mesh, smooth_amount=smooth_amount)
        elif region == 'Right Eyelid':
            vertex_snap_data.snap_side_bottom_blink('right', head, smooth=smooth_mesh, smooth_amount=smooth_amount)
        else:
            vertex_snap_data.snap_side_bottom_blink('left', head, smooth=smooth_mesh, smooth_amount=smooth_amount)

    def _on_top_to_bottom_clicked(self):
        """
        Snaps verts in selected region from top to bottom.
        """
        smooth_mesh = self.ui.snap_smoothing_checkBox.isChecked()
        smooth_amount = self.ui.snap_smoothing_horizontalSlider.value()

        common_data_path = os.path.join(paths.get_common_face(), 'rig_source_data.json')
        vertex_snap_data = face_vertex_data.SourceFaceEyelashShelf.load_vertex_data(common_data_path, 'head_blendshape')
        region = self.ui.snappable_regions_comboBox.currentText()
        head = pm.selected()
        if not head:
            logger.warning('Please first select head mesh')
            return
        else:
            head = naming.get_basename(head[0])

        if region == 'Lips':
            vertex_snap_data.snap_lips_top_to_bottom(head, smooth=smooth_mesh, smooth_amount=smooth_amount)
        elif region == 'Right Eyelid':
            vertex_snap_data.snap_side_top_blink('right', head, smooth=smooth_mesh, smooth_amount=smooth_amount)
        else:
            vertex_snap_data.snap_side_top_blink('left', head, smooth=smooth_mesh, smooth_amount=smooth_amount)

    def _on_meet_at_middle_clicked(self):
        """
        Snaps verts in selected region to midpoint between top and bottom.
        """
        smooth_mesh = self.ui.snap_smoothing_checkBox.isChecked()
        smooth_amount = self.ui.snap_smoothing_horizontalSlider.value()
        common_data_path = os.path.join(paths.get_common_face(), 'rig_source_data.json')
        vertex_snap_data = face_vertex_data.SourceFaceEyelashShelf.load_vertex_data(common_data_path, 'head_blendshape')
        region = self.ui.snappable_regions_comboBox.currentText()
        head = pm.selected()
        if not head:
            logger.warning('Please first select head mesh')
            return
        else:
            head = naming.get_basename(head[0])
        if region == 'Lips':
            vertex_snap_data.snap_lips_to_middle(head, smooth=smooth_mesh, smooth_amount=smooth_amount)
        elif region == 'Right Eyelid':
            vertex_snap_data.snap_eye_blink_to_middle('right', head, smooth=smooth_mesh, smooth_amount=smooth_amount)
        else:
            vertex_snap_data.snap_eye_blink_to_middle('left', head, smooth=smooth_mesh, smooth_amount=smooth_amount)
    ####################################
    # Edit Tools - Auto Edit
    ####################################
    def _set_local_axis_display(self):
        """
        Sets the local axis display on the face joints.
        """

        frag_rigs = self.get_rigs()
        #Return all the frag rigs
        if not frag_rigs:
            return
        # Get the root joint
        frag_rig = frag_rigs[0]
        root_joint = frag.get_root_joint(frag_rig)
        if not root_joint:
            return
        # Get all the pose joints
        root_joint.listRelatives(ad=True)
        all_joints = [x for x in root_joint.listRelatives(ad=True) if isinstance(x, pm.nt.Joint)]
        joints = [x for x in all_joints if x.hasAttr('isPoseJoint') and x.isPoseJoint.get()]
        if not joints:
            return
        # Set the local axis display on or off depending on what state the 1st joint is in.
        state = not joints[0].displayLocalAxis.get()
        [x.displayLocalAxis.set(state) for x in joints if x.hasAttr('displayLocalAxis')]

    ####################################
    # Edit Tools - Poses
    ####################################
    def _populate_blendshape_meshes(self):
        """
        Populates the blend shape names in a QListWidget.
        """

        self.ui.bs_list_listWidget.clear()
        markup = mesh_markup_rig.RigMeshMarkup.create()
        blendshape_meshes = markup.get_mesh_list_in_category('blendshape_mesh', as_string=True)
        if not blendshape_meshes:
            return

        [QLabelTextButtonQWidget.create(self.ui.bs_list_listWidget, x, color=STAGING_COLOR_GREEN) for x in blendshape_meshes]
        self.ui.bs_list_listWidget.setCurrentRow(0)

    def _populate_skin_meshes(self):
        """
        Populates the names of the meshes that get skinned in a QListWidget.
        """

        self.ui.skin_list_listWidget.clear()
        skin_meshes = self.get_all_skinned_meshes()
        if not skin_meshes:
            return

        skin_meshes = list(map(lambda x: str(x), skin_meshes))
        [QLabelTextButtonQWidget.create(self.ui.skin_list_listWidget, x, color=STAGING_COLOR_GREY) for x in skin_meshes]
        self.ui.skin_list_listWidget.setCurrentRow(0)

    def _populate_edit_meshes(self):
        """
        Populates the blend shape and skin mesh QListWidgets:
        """

        self._populate_blendshape_meshes()
        self._populate_skin_meshes()

    def _populate_poses(self):
        """
        Populates the names of poses that have been activated.
        """

        # Clear List widgets
        self.ui.pose_list_listWidget.clear()
        self.ui.edit_percent_listWidget.clear()
        self.ui.pose_flag_listWidget.clear()

        # Check to see if the blend shape mesh has that pose.
        mesh = self.get_text_from_list_widget(self.ui.bs_list_listWidget)
        if not mesh:
            return
        if not pm.objExists(mesh[0]):
            return
        mesh = face_model.FaceModel(mesh[0])
        parameters_inst = face_util.get_parameters_region_instance(self.asset_id, mesh.region)
        parameter_list = parameters_inst.get_parameters_list()
        pose_list = [x.connection for x in parameter_list]

        # Grab the parameter node and get the poses and the values
        parameter_node = self.get_parameter_node()
        if not parameter_node:
            return
        pose_dict = parameter_node.get_all_active_poses_and_value()
        if not pose_dict:
            return
        full_active = {}
        part_active = {}
        for key, values in pose_dict.items():
            if values['value'] < 1 and key in pose_list:
                part_active.update({key:values})
            elif values['value'] >= 1 and key in pose_list:
                full_active.update({key: values})

        for pose_name, values in full_active.items():
            percent_value = round(values['value'] * 100, 1)
            pose_flag = f'{values["flag"]}'
            QLabelTextQWidget.create(self.ui.pose_list_listWidget,
                                        text=pose_name,
                                        color=STAGING_COLOR_GREEN)
            QLabelTextQWidget.create(self.ui.edit_percent_listWidget, f'{percent_value}%', STAGING_COLOR_GREEN)
            QLabelTextQWidget.create(self.ui.pose_flag_listWidget, pose_flag, STAGING_COLOR_GREEN)

        for pose_name, values in part_active.items():
            percent_value = round(values['value'] * 100, 1)
            pose_flag = f'{values["flag"]}'
            QLabelTextQWidget.create(self.ui.pose_list_listWidget,
                                        text=pose_name,
                                        color=STAGING_COLOR_RED)
            QLabelTextQWidget.create(self.ui.edit_percent_listWidget, f'{percent_value}%', STAGING_COLOR_RED)
            QLabelTextQWidget.create(self.ui.pose_flag_listWidget, pose_flag, STAGING_COLOR_RED)
        self.ui.pose_list_listWidget.setCurrentRow(0)

    def mirror_pose_from_listwidget(self):
        blendshape_mesh = self._get_blendshape_mesh_from_qlistwidget()
        pose_name = self._get_pose_from_listwidget()
        if not pose_name:
            dialogs.info_prompt(title='No Pose Selected', text='Please Select a pose from the pose list and try again')
            return

        if not cmds.objExists(pose_name):
            dialogs.info_prompt(title='Mesh Does Not Exist',
                                text=f'The mesh, "{pose_name}" does not exist in the scene.\n'
                                        f'Please import all poses first.')
            return

        result = dialogs.question_prompt(title='Mirror Pose?',
                                        text=f'Do you wish mirror {pose_name} from {blendshape_mesh}?')
        if result != 'Yes':
            return

        blendshape_mesh = pm.PyNode(blendshape_mesh)
        pose_mesh = pm.PyNode(pose_name)
        pose_mesh, mirror_mesh = pose_files.mirror_pose(pose_mesh=pose_mesh,
                                                mesh=blendshape_mesh,
                                                pose_connection=pose_name,
                                                asset_id=self.asset_id)
        dialogs.display_view_message(text=f'Mirrored {pose_mesh} Successfully', header='Face Staging', fade_time=220)
        if self.ui.auto_mirror_checkBox.isChecked():
            pm.select([mirror_mesh, pose_mesh])
            self._export_selected()

        self._reconnect_shapes_to_rig()

    def mirror_all_poses(self):
        """
        Mirrors left side poses to the right side
        """

        mesh = self.get_text_from_list_widget(self.ui.bs_list_listWidget)
        if not mesh:
            return
        mesh = face_model.FaceModel(mesh[0])

        # Should come back to this later and make it a user choice of left or right side being mirrored
        side_to_mirror = 'left'

        data_path = os.path.join(paths.get_face_data_path(self.asset_id), 'rig_source_data.json')
        source_face_data = source_data.FaceMeshRegionData.load(data_path, 'head_blendshape')

        params = source_face_data.parameters
        poses_to_mirror = []
        for param in params:
            poses = params.get(param)
            for pose in poses:
                pose_data = poses.get(pose)
                pose_side = pose_data.get('side')
                if pose_side == side_to_mirror:
                    poses_to_mirror.append(pose)

        result = dialogs.question_prompt(title='Mirror Pose?',
                                        text=f'Do you wish mirror all poses from {mesh.mesh}?')

        if result != 'Yes':
            return

        prog_ui = progressbar_ui.ProgressBarStandard()
        prog_ui.update_status(0, 'Starting Up')

        meshes_to_export = []

        i = 100.0 / (len(poses_to_mirror) + 1)

        for x, pose_name in enumerate(poses_to_mirror):
            step = x + i
            prog_ui.update_status(step, f'Mirroring {pose_name}...')
            blendshape_mesh = pm.PyNode(mesh.mesh)
            pose_mesh = pm.PyNode(pose_name)
            pose_mesh, mirror_mesh = pose_files.mirror_pose(pose_mesh=pose_mesh,
                                                            mesh=blendshape_mesh,
                                                            pose_connection=pose_name,
                                                            asset_id=self.asset_id)
            meshes_to_export.append(pose_mesh)
            meshes_to_export.append(mirror_mesh)

        prog_ui.update_status(100, 'Finished')
        dialogs.display_view_message(text=f'Mirrored all {side_to_mirror} side poses successfully', header='Face Staging', fade_time=220)

        if self.ui.auto_mirror_checkBox.isChecked():
            pm.select(meshes_to_export)
            self._export_selected()

        self._reconnect_shapes_to_rig()

    def _reconnect_shapes_to_rig(self):
        """
        Reconnects the blend shapes to the rig.
        """

        face_component = self.get_face_component()
        blendshape_list = face_component.get_all_category_meshes(frag.FACE_BLENDSHAPE_CATEGORY)
        for blendshape in blendshape_list:
            blendshape = face_model.FaceModel(blendshape)
            blendshape.reconnect_shapes_to_rig(self.asset_id)
            dialogs.display_view_message(text=f'{blendshape.mesh} Blend Shapes Successfully Reconnected',
                                            header='Face Staging',
                                            fade_time=170)


    def _get_pose_from_listwidget(self):
        """
        Returns the name of an active selected pose from a QListWidget.

        :return: Returns the name of an active selected pose from a QListWidget.
        :rtype: str
        """

        items = self.ui.pose_list_listWidget.selectedItems()
        selected = []
        for i in range(len(items)):
            selected.append(self.ui.pose_list_listWidget.selectedItems()[i])
        if not selected:
            return
        return selected[0].data(0).text()

    def _get_percent(self):
        """
        Returns the percent the pose is active.

        :return: Returns the percent the pose is active.
        :rtype: flaot
        """

        idx = self.ui.pose_list_listWidget.currentRow()
        percent_item = self.ui.edit_percent_listWidget.item(idx)
        if not percent_item:
            return
        percent = float((percent_item.data(0).text())[:-1])
        return percent

    def _get_blendshape_mesh_from_qlistwidget(self):
        """
        Returns the name of a selected mesh from a QListWidget.

        :return: Returns the name of a selected mesh from a QListWidget.
        :rtype: str
        """

        items = self.ui.bs_list_listWidget.selectedItems()
        selected = []
        for i in range(len(items)):
            selected.append(self.ui.bs_list_listWidget.selectedItems()[i])
        if not selected:
            return
        return selected[0].data(0).text()

    def _pose_edit_start_check(self):
        """
        Checks to see if specific data is set before starting a pose edit.

        :return: Returns a FRAGRig
        :rtype: FRAGRig
        """

        if self._get_percent() and self._get_percent() < 100.0:
            dialogs.info_prompt(title='Pose Not At 100%',
                                text='The pose needs to be completely set.\n'
                                        'Please make sure the Flag is set to the max.')
            return None
        frag_rigs = self.get_rigs()
        if not frag_rigs:
            dialogs.info_prompt(title='No Rig', text='Cannot not find the FRAG Rig node.\nNo rig in the scene.')
            return frag_rigs
        return frag_rigs[0]

    def _get_edit_node(self):
        frag_rigs = self.get_rigs()
        if not frag_rigs:
            return
        edit_node = frag.get_face_edit_node(frag_rigs[0], skip_dialog=True)
        if not edit_node:
            return
        return face_pose_edit.FacePoseEdit(edit_inst=edit_node)

    ####################################
    # Edit Tools - Poses edits
    ####################################
    ###### SINGLE POSE EDITS ########
    def single_pose_toggle(self):
        """
        Is a toggle for starting the single pose edit.
        """

        edit_node = self._get_edit_node()
        frag_rig = self._pose_edit_start_check()
        if not frag_rig:
            return
        if not edit_node:
            self.single_pose_edit_start(frag_rig)
            dialogs.display_view_message(text='Entered Single Pose Edit', header='Face Staging Tool', fade_time=220)
        elif edit_node and edit_node.edit_inst.single_pose and not edit_node.edit_inst.paint_neutral:
            edit_node.pose_edit_end(due_mirror=self.ui.auto_mirror_checkBox.isChecked(),
                                    due_export=self.ui.export_bs_checkBox.isChecked(),
                                    transfer_jnts = self.ui.edit_transfer_joints_checkBox.isChecked())
            self.reset_pose_edit_buttons()
            self.reparent_rivet_group()
            dialogs.display_view_message(text='Single Pose Edit Successful!', header='Face Staging Tool', fade_time=220)
        elif edit_node and edit_node.edit_inst.single_pose and edit_node.edit_inst.paint_neutral:
            edit_node.paint_neutral_end()
            edit_node.pose_edit_end(due_mirror=self.ui.auto_mirror_checkBox.isChecked(),
                                    due_export=self.ui.export_bs_checkBox.isChecked(),
                                    transfer_jnts=self.ui.edit_transfer_joints_checkBox.isChecked())
            self.reset_pose_edit_buttons()
            self.reparent_rivet_group()
            dialogs.display_view_message(text='Paint Neutral Successful!', header='Face Staging Tool', fade_time=220)
            dialogs.display_view_message(text='Single Pose Edit Successful!', header='Face Staging Tool', fade_time=220)

    @decorators.track_fnc
    def single_pose_edit_start(self, frag_rig):
        """
        Starts the Single pose edit.

        :param FRAGRig frag_rig: FRAG Rig Component.
        """

        mesh = self._get_blendshape_mesh_from_qlistwidget()
        if not mesh:
            return

        pose_name = self._get_pose_from_listwidget()
        if not pose_name:
            dialogs.info_prompt(title='No Pose Selected', text='Please select a pose from the active pose list.')
            return

        edit_node = face_pose_edit.FacePoseEdit.create(main_pose=pose_name, mesh=mesh, frag_node=frag_rig)
        edit_node.pose_edit_start(show_skel=self.ui.show_skeleton_checkBox.isChecked(),
                                    symmetry=self.ui.symmetry_checkBox.isChecked(),
                                    transfer_jnts=self.ui.edit_transfer_joints_checkBox.isChecked())
        self.ui.single_edit_pushButton.setStyleSheet(STAGING_BUTTON_ACTIVE_COLORS)
        self.ui.single_edit_color_frame.setStyleSheet(STAGING_BACKGROUND_GREY)

    ###### Multi POSE EDITS ########
    def multi_pose_toggle(self):
        """
        Is a toggle for starting the multi pose edit.
        """

        edit_node = self._get_edit_node()
        frag_rig = self._pose_edit_start_check()
        if not frag_rig:
            return
        if not edit_node:
            start_multi = self.multi_pose_edit_start(frag_rig)
            if not start_multi:
                return
            self.ui.multi_pose_edit_pushButton.setStyleSheet(STAGING_BUTTON_ACTIVE_COLORS)
            self.ui.multi_pose_edit_frame.setStyleSheet(STAGING_BACKGROUND_GREY)
            dialogs.display_view_message(text='Entered Multi Pose Edit', header='Face Staging Tool', fade_time=220)
        elif edit_node and edit_node.edit_inst.multi_pose and not edit_node.edit_inst.paint_neutral:
            edit_node.pose_edit_end(multi_edit=True,
                                    due_mirror=self.ui.auto_mirror_checkBox.isChecked(),
                                    due_export=self.ui.export_bs_checkBox.isChecked(),
                                    transfer_jnts=self.ui.edit_transfer_joints_checkBox.isChecked())
            self.reset_pose_edit_buttons()
            self.reparent_rivet_group()
            dialogs.display_view_message(text='Multi Pose Edit Successful!', header='Face Staging Tool', fade_time=220)

    @decorators.track_fnc
    def multi_pose_edit_start(self, frag_rig):
        """
        Starts the Single pose edit.

        :param FRAGRig frag_rig: FRAG Rig Component.
        """

        mesh = self._get_blendshape_mesh_from_qlistwidget()
        if not mesh:
            return False
        pose_name = self._get_pose_from_listwidget()
        if not pose_name:
            dialogs.info_prompt(title='No Pose Selected', text='Please select a pose from the active pose list.')
            return False
        edit_node = face_pose_edit.FacePoseEdit.create(main_pose=pose_name, mesh=mesh, frag_node=frag_rig)
        edit_node.pose_edit_start(multi_edit=True,
                                    show_skel=self.ui.show_skeleton_checkBox.isChecked(),
                                    symmetry=self.ui.symmetry_checkBox.isChecked(),
                                    transfer_jnts=self.ui.edit_transfer_joints_checkBox.isChecked())
        return True

    def pose_edit_cancel(self):
        """
        Cancels the Single and Multi pose edits.
        """

        edit_node = self._get_edit_node()
        if not edit_node:
            return
        mesh = self._get_blendshape_mesh_from_qlistwidget()
        if not mesh:
            return

        if edit_node.edit_inst.paint_neutral and not edit_node.edit_inst.multi_pose:
            edit_node.paint_neutral_cancel()
            self.reset_pose_edit_buttons(keep_single=True)
            dialogs.display_view_message(text='Paint Neutral Canceled', header='Face Staging Tool', fade_time=220)
        else:
            if self.ui.edit_transfer_joints_checkBox.isChecked():
                blendshape = face_model.FaceModel(mesh)
                blendshape.connect_joints(asset_id=self.asset_id)
                self.reparent_rivet_group()
            edit_node.pose_edit_cancel()
            self.reset_pose_edit_buttons()
            self.ui.pose_list_listWidget.clear()
            self.ui.edit_percent_listWidget.clear()
            self.ui.pose_flag_listWidget.clear()
            dialogs.display_view_message(text='Pose Edit Canceled', header='Face Staging Tool', fade_time=220)

    ####### Paint Neutral ##########
    def paint_neutral_toggle(self):
        """
        Blend Shape mode refers to "Paint Neutral Pose" on the UI.  The button is a toggle.
        This determines which function to execute.
        """

        edit_node = self._get_edit_node()
        frag_rig = self._pose_edit_start_check()
        if not frag_rig:
            return
        pose_name = self._get_pose_from_listwidget()
        if not pose_name:
            dialogs.info_prompt(title='No Pose Selected', text='Please select a pose from the active pose list.')
            return

        if not edit_node:
            self.single_pose_edit_start(frag_rig)
            dialogs.display_view_message(text='Entered Single Pose Edit', header='Face Staging Tool', fade_time=220)
            edit_node = self._get_edit_node()
            self.paint_neutral_start(edit_node)
            # set button color
            self.set_edit_buttons_active(self.ui.paint_neutral_pushButton, self.ui.paint_neutral_frame)
            dialogs.display_view_message(text='Entered Paint Neutral Pose', header='Face Staging Tool', fade_time=220)

        elif edit_node and edit_node.edit_inst.single_pose and not edit_node.edit_inst.paint_neutral:
            self.paint_neutral_start(edit_node)
            dialogs.display_view_message(text='Entered Paint Neutral Pose', header='Face Staging Tool', fade_time=220)
            self.set_edit_buttons_active(self.ui.paint_neutral_pushButton, self.ui.paint_neutral_frame)

        elif edit_node and edit_node.edit_inst.single_pose and edit_node.edit_inst.paint_neutral:
            edit_node = self._get_edit_node()
            edit_node.paint_neutral_end()
            self.reset_pose_edit_buttons(keep_single=True)
            dialogs.display_view_message(text='Paint Neutral Successful!', header='Face Staging Tool', fade_time=220)

    @decorators.track_fnc
    def paint_neutral_start(self, edit_node):
        """
        Blend Shape mode refers to "Paint Neutral Pose" on the UI.
        In order for this function to work the user must be in edit mode.
        This creates a blend shape from the base head to the pose mesh that is being modified.
        This will allow the user to paint back
        the neutral pose onto the pose mesh.
        """

        symmetry = self.ui.symmetry_checkBox.isChecked()
        edit_node.paint_neutral_start(symmetry)

    ####### Base Mesh Edit ##########
    def base_edit_toggle(self, skip_dialog=False):
        """
        Blend Shape mode refers to "Paint Neutral Pose" on the UI.  The button is a toggle.
        This determines which function to execute.
        """

        edit_node = self._get_edit_node()
        frag_rig = self.get_rig()
        if not frag_rig:
            dialogs.info_prompt(title='No Rig', text='Cannot not find the FRAG Rig node.\nNo rig in the scene.')

        if not frag_rig:
            return

        if not edit_node:
            self.base_edit_start(frag_rig)
            self.ui.base_edit_pushButton.setStyleSheet(STAGING_BUTTON_ACTIVE_COLORS)
            self.ui.base_color_edit_frame.setStyleSheet(STAGING_BACKGROUND_GREY)
            dialogs.display_view_message(text='Entered Base Edit Mode', header='Face Staging Tool', fade_time=220)
        elif edit_node and edit_node.edit_inst.base_edit:
            if not skip_dialog:
                result = dialogs.question_prompt(title='Finish Editing?',
                                                    text=f'Do you wish to continue?  The changes will be propagated out '
                                                            'to all of the blend shapes.')
                if result != 'Yes':
                    return

            edit_node.base_edit_end(due_export=self.ui.export_bs_checkBox.isChecked())
            if self.ui.export_bs_checkBox.isChecked():
                self.export_skin_meshes_as_fbx()
            edit_node.edit_inst.set_all_flag_block_values()
            pm.delete(edit_node.edit_inst.pynode)
            self.reset_pose_edit_buttons()
            dialogs.display_view_message(text='Base Edit Successful!', header='Face Staging Tool', fade_time=220)

    @decorators.track_fnc
    def base_edit_start(self, frag_rig):
        """
        Starts the editing process where the base mesh can be edited.

        :param FRAGRig frag_rig: FRAG Rig Component.
        """

        mesh = self._get_blendshape_mesh_from_qlistwidget()
        if not mesh:
            return
        edit_node = face_pose_edit.FacePoseEdit.create(mesh=mesh, main_pose=None, frag_node=frag_rig)
        edit_node.base_edit_start(symmetry=self.ui.symmetry_checkBox.isChecked(),
                                    show_skel=self.ui.show_skeleton_checkBox.isChecked())

    def base_edit_cancel(self):
        """
        Cancels the Base Edit mode and returns the scene back to a clean state.
        """

        edit_node = self._get_edit_node()
        if not edit_node:
            return
        mesh = self._get_blendshape_mesh_from_qlistwidget()
        if not mesh:
            return

        edit_node.base_edit_cancel()
        self.reset_pose_edit_buttons()
        dialogs.display_view_message(text='Base Edit Mode Canceled', header='Face Staging Tool', fade_time=220)

    @decorators.track_fnc
    def replace_base_mesh(self):
        """
        Replaces the base mesh with a newer mesh with the same vert count.
        """
        result = dialogs.question_prompt(title='Replace Base Mesh?',
                                        text='Do you wish to continue?')
        if result != 'Yes':
            return

        selection = pm.selected()
        if not selection and not selection[0].listRelatives(s=True):
            dialogs.info_prompt(title='Select a Mesh', text='Please select a valid mesh')
            return

        replacement_mesh = selection[0]

        frag_rig = self.get_rig()
        if not frag_rig:
            dialogs.info_prompt(title='No Rig', text='Cannot not find the FRAG Rig node.\n'
                                                        'No rig in the scene.')
            return
        mesh = self._get_blendshape_mesh_from_qlistwidget()
        if not mesh:
            return
        edit_node = face_pose_edit.FacePoseEdit.create(mesh=mesh, main_pose=None, frag_node=frag_rig)
        edit_node.replace_base(replacement_mesh, due_export=self.ui.export_bs_checkBox.isChecked())
        if self.ui.export_bs_checkBox.isChecked():
            self.export_skin_meshes_as_fbx()
        edit_node.edit_inst.set_all_flag_block_values()
        pm.delete(edit_node.edit_inst.pynode)
        self.reset_pose_edit_buttons()

    def print_test(self):
        """
        A Function to test things.
        """

        color = self.ui.single_edit_pushButton.palette().button().color()
        self.ui.single_edit_pushButton.setStyleSheet(
            'background-color: rgb{0.207843, 0.207843, 0.207843, 1.000000};')
        print(color)

    def get_text_from_list_widget(self, qlist_widget):
        """
        Returns a string from a selected row in a list Widget.

        :param QListWidget qlist_widget: A QT QListWidget.
        :return: Returns a string from a selected row in a list Widget.
        :rtype: str
        """

        items = qlist_widget.selectedItems()
        selected = []
        for i in range(len(items)):
            selected.append(qlist_widget.selectedItems()[i])
        if not selected:
            return []
        selected = [x.data(0).text() for x in selected]
        return selected

    def select_item_from_list_widget(self, qlist_widget):
        """
        Selects objs from the QListWidget.
        :param QListWidget qlist_widget: A QT QListWidget.
        """

        items = self.get_text_from_list_widget(qlist_widget)
        objs = [x for x in items if pm.objExists(x)]
        pm.select(objs)

    ################################################
    # Rigging Tab
    ################################################
    def get_rigging_selected_meshes(self):
        """
        Returns a list of mesh names from the QListWidgets

        :return: Returns a list of mesh names from the QListWidgets
        :rtype: list(str)
        """
        skinned_meshes = self.get_text_from_list_widget(self.ui.engine_meshes_listWidget)
        blendshapes_meshes = self.get_text_from_list_widget(self.ui.blendshape_skin_listWidget)

        meshes = skinned_meshes + blendshapes_meshes
        return [x for x in meshes if pm.objExists(x)]

    def _populate_skinning_meshes(self):
        """
        Populates the mesh QListWidgets.
        """

        # Clear List widgets
        self.ui.engine_meshes_listWidget.clear()
        self.ui.blendshape_skin_listWidget.clear()

        skinned_meshes = self.get_all_skinned_meshes()
        blendshapes_meshes = self.get_all_blendshape_meshes()

        if not skinned_meshes and not blendshapes_meshes:
            return
        if skinned_meshes:
            skinned_meshes = list(map(lambda x: str(x), skinned_meshes))
        if blendshapes_meshes:
            blendshapes_meshes = list(map(lambda x: str(x), blendshapes_meshes))

        # Check to see if they have skinning data
        for mesh in skinned_meshes:
            if face_util.has_skinning_data(mesh, self.asset_id):
                QLabelTextButtonQWidget.create(self.ui.engine_meshes_listWidget, mesh, color=STAGING_COLOR_GREEN)
            else:
                QLabelTextButtonQWidget.create(self.ui.engine_meshes_listWidget, mesh, color=STAGING_COLOR_RED)

        for mesh in blendshapes_meshes:
            if face_util.has_skinning_data(mesh, self.asset_id):
                QLabelTextButtonQWidget.create(self.ui.blendshape_skin_listWidget, mesh, color=STAGING_COLOR_GREEN)
            else:
                QLabelTextButtonQWidget.create(self.ui.blendshape_skin_listWidget, mesh, color=STAGING_COLOR_RED)

    @decorators.track_fnc
    def restore_skinning(self):
        """
        Restores skinning from saved skin weights in a .sknr file.
        """

        result = dialogs.question_prompt(title='Restore Skinning?',
                                        text='Restore Skinning?')
        if result != QDialogButtonBox.StandardButton.Yes:
            return

        meshes = self.get_rigging_selected_meshes()
        not_skinned = []
        for mesh in meshes:
            if face_util.has_skinning_data(mesh, self.asset_id):
                face_skinning.apply_face_skinning_from_file(self.asset_id, mesh)
            else:
                not_skinned.append(mesh)

        if not_skinned:
            message = ', '.join(not_skinned)
            dialogs.info_prompt(title='Meshes were not skinned',
                                text='These meshes were not skinned\n'
                                        f'{message}')

        self.ui.engine_meshes_listWidget.clearSelection()
        self.ui.blendshape_skin_listWidget.clearSelection()

    @decorators.track_fnc
    def export_skinning(self, all_meshes=False):
        """
        Export the skin weights to a .json file.
        """

        result = dialogs.question_prompt(title='Export Skinning?',
                                        text='Export Skinning?')
        if result != 'Yes':
            return
        if all_meshes:
            meshes = self.get_all_skinned_meshes()
        else:
            meshes = self.get_rigging_selected_meshes()
        not_exported = []
        for mesh in meshes:
            skin_saved = face_skinning.export_face_skinning_to_file(self.asset_id, mesh)

            if not skin_saved:
                not_exported.append(mesh)
        if not_exported:
            message = ', '.join(not_exported)
            result = dialogs.info_prompt(title='Meshes were not skinned',
                                            text=f'These meshes were not skinned\n'
                                            f'{message}')

        self.ui.engine_meshes_listWidget.clearSelection()
        self.ui.blendshape_skin_listWidget.clearSelection()
        self._populate_skinning_meshes()

    @decorators.track_fnc
    def export_all_skinning(self):
        self.export_skinning(all_meshes=True)

    def process_skinning(self, skinned_meshes, delete_decomp_mesh=True, skip_dialog=False):
        """
        Processes skinning on a list of meshes based on information in rig source data

        :param list(pm.nt.Transform) skinned_meshes: Face meshes to process skinning on
        :param bool delete_decomp_mesh: Deletes the mesh created by LSD process.
        """

        # Making sure head is first so other meshes can potentially be copied from it
        markup = mesh_markup_rig.RigMeshMarkup.create()
        face_mesh = str(markup.get_mesh_list_in_region('head_mesh')[0])
        face_blendshape = str(markup.get_mesh_list_in_region('head_blendshape')[0])

        if face_mesh in skinned_meshes:
            skinned_meshes.remove(face_mesh)
            skinned_meshes.insert(0, face_mesh)

        display_names = [naming.get_basename(skinned_mesh) for skinned_mesh in skinned_meshes]

        message = str(display_names)[1:-1]
        if not skip_dialog:
            result = dialogs.question_prompt(title='Process Skinning?',
                                            text=f'Process skinning for:\n{message}')
            if result != 'Yes':
                return
        prog_ui = progressbar_ui.ProgressBarStandard()
        prog_ui.update_status(0, 'Starting Up')
        i = 100.0 / len(skinned_meshes) + 1

        if not skin_utils.get_skin_cluster_from_geometry(pm.PyNode(face_blendshape)):
            face_skinning.apply_common_skinning(pm.PyNode(face_blendshape), 'head_mesh')

        for x, skinned_mesh in enumerate(skinned_meshes):
            step = x * i
            prog_ui.update_status(step, f'Skinning {skinned_mesh}...')
            face_component = self.get_face_component()
            blendshape_mesh = face_component.get_counterpart_mesh(skinned_mesh)

            skin_mesh = face_model.FaceModel(skinned_mesh)

            region_data = source_data.FaceMeshRegionData(skin_mesh.region, self.source_face_data.data)
            skinned_joints = region_data.joints_skinned

            initial_skinning_process = region_data.skinning_initial
            if not skinned_joints:
                continue

            if initial_skinning_process == "copy":
                face_skinning.copy_weights_from_head(face_mesh, region_data, [skin_mesh.mesh])

            elif initial_skinning_process == "process" and blendshape_mesh:
                start_frame = pm.playbackOptions(q=True, min=True)
                end_frame = pm.playbackOptions(q=True, max=True)
                if not pm.keyframe(pm.PyNode(skinned_joints[0]).listAttr(k=True)[0], query=True, keyframeCount=True):
                    self.calibration_animation()

                if pm.mel.findRelatedSkinCluster(str(skin_mesh.mesh)) != '':
                    pm.skinCluster(skin_mesh.mesh.getShape(), e=True, ub=True)
                face_skinning.face_skinning_converter_cmd(blendshape_mesh=str(blendshape_mesh.mesh),
                                                          skin_mesh=str(skin_mesh.mesh),
                                                          joints=skinned_joints,
                                                          start_frame=start_frame,
                                                          end_frame=end_frame,
                                                          delete_decomp_mesh=delete_decomp_mesh)

                self.cut_animation()

                frag_rigs = self.get_rigs()
                frag_rig = frag_rigs[0]
                root_joint = frag.get_root_joint(frag_rig)
                wrapped_root = chain_markup.ChainMarkup(root_joint)

                face_skinning.post_lsd_face_cleanup(skin_mesh.mesh,
                                                    region_data,
                                                    wrapped_root,
                                                    asset_id=self.asset_id)

                blendshape_mesh.connect_joints(self.asset_id, delete_old_rivet_grp=False)

            elif initial_skinning_process == "saved":
                self.zero_flags()
                face_skinning.apply_common_skinning(skin_mesh.mesh, skin_mesh.region)

            elif initial_skinning_process == "maya_default":
                if pm.mel.findRelatedSkinCluster(str(skin_mesh.mesh)) != '':
                    pm.skinCluster(skin_mesh.mesh.getShape(), e=True, ub=True)
                pm.skinCluster(skinned_joints, skin_mesh.mesh, tsb=True)

            dialogs.display_view_message(text=f'{skin_mesh.mesh} Skinned Successfully',
                                         header='Face Staging Tool',
                                         fade_time=220)
        prog_ui.update_status(100, 'Finished')

    @decorators.track_fnc
    def all_meshes_process_skinning(self, skip_dialog=False):
        """
        Processes the skinning for all tagged skinned face meshes.
        """

        meshes = self.get_all_skinned_meshes()
        self.process_skinning(meshes, delete_decomp_mesh=True, skip_dialog=skip_dialog)

    def process_skinning_keep_mesh(self):
        """
        Processes the skinning and then Does not delete the mesh that the LSD gives after the process.
        """

        meshes = self.get_text_from_list_widget(self.ui.engine_meshes_listWidget)
        self.process_skinning(meshes, delete_decomp_mesh=False)

    @decorators.track_fnc
    def process_skinning_delete_mesh(self):
        """
        Processes the skinning and then deletes the mesh that the LSD gives after the process.
        """

        meshes = self.get_text_from_list_widget(self.ui.engine_meshes_listWidget)
        self.process_skinning(meshes, delete_decomp_mesh=True)

    def reparent_rivet_group(self):
        """
        Re-parents rivet group under DNT group
        """

        rivet_group = next((xform for xform in pm.ls(type=pm.nt.Transform) if xform.hasAttr('isRivetGrp')), None)
        if rivet_group:
            frag_rig = self.get_rig()
            dnt_group = frag_rig.getAttr('doNotTouch')
            rivet_group.setParent(dnt_group)

    @decorators.track_fnc
    def finish_save_rig(self):
        """
        Saves and cleans up the final rig file.
        """

        result = dialogs.question_prompt(title='Save Rig?', text='Clean up the File and Save Rig?')
        if result != QDialogButtonBox.StandardButton.Yes:
            return

        face_util.clean_and_save_face_rig(self.asset_id)
        pm.select(cl=True)
        dialogs.display_view_message(text='Rig File Saved Successfully', header='Face Staging Tool', fade_time=220)

    def create_flags_from_common(self):
        flag_path = os.path.join(paths.get_asset_rig_path(self.asset_id), 'Flags')
        if not os.path.exists(flag_path):
            os.makedirs(flag_path)
        if not os.listdir(flag_path):
            common_flag_path = os.path.join(paths.get_common_face(), 'Flags')
            frag_rig = self.get_rig()
            flags = frag_rig.get_flags()
            frag_flag.swap_flags(flags, common_flag_path)
            frag_rig.color_flags()
            list(map(lambda x: serialize_flag.export_flag(pm.PyNode(x), flag_path), flags))
            return True
        else:
            return False

class QLabelTextQWidget(QWidget):
    def __init__(self, parent=None):
        super(QLabelTextQWidget, self).__init__(parent)
        self.text_QHBoxLayout = QHBoxLayout()
        self.text_QLabel = QLabel()
        self.text_QHBoxLayout.addWidget(self.text_QLabel)
        self.text_QHBoxLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.setLayout(self.text_QHBoxLayout)

        self.text_QHBoxLayout.setContentsMargins(1, 1, 1, 1)
        self.text_QLabel.setAlignment(Qt.AlignLeft)

    def set_text(self, text, color=STAGING_COLOR_GREEN):
        """
        Sets a nested text to be added to a QListWidget.

        :param str text: Sets a nested text to be added to a QListWidget.
        :param str color: The color of the text.
        """

        self.text_QLabel.setStyleSheet(f'''color: rgb{color};''')
        self.text_QLabel.setText(text)

    @classmethod
    def create(cls, qlist_widget, text, color=STAGING_COLOR_GREEN):
        """
        Creates a nested text to be added to a QListWidget.

        :param QListWidget qlist_widget: A QT QListWidget.
        :param str text: Sets a nested text to be added to a QListWidget.
        :param str color: The color of the text.
        """

        myQCustomQWidget = cls()
        myQCustomQWidget.set_text(text, color)
        # Create QListWidgetItem
        myQListWidgetItem = QListWidgetItem(qlist_widget)
        myQListWidgetItem.setData(0, myQCustomQWidget.text_QLabel)
        # Set size hint
        myQListWidgetItem.setSizeHint(myQCustomQWidget.minimumSizeHint())
        # Add QListWidgetItem into QListWidget
        qlist_widget.addItem(myQListWidgetItem)
        qlist_widget.setItemWidget(myQListWidgetItem, myQCustomQWidget)


class QLabelTextButtonQWidget(QWidget):
    def __init__(self, parent=None):
        super(QLabelTextButtonQWidget, self).__init__(parent)
        self.text_QHBoxLayout = QHBoxLayout()
        self.text_QLabel = QLabel()
        self.button = QPushButton()
        self.text_QHBoxLayout.addWidget(self.text_QLabel)
        self.text_QHBoxLayout.addWidget(self.button)
        self.text_QHBoxLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.setLayout(self.text_QHBoxLayout)

        self.text_QHBoxLayout.setContentsMargins(1, 1, 1, 1)
        self.text_QHBoxLayout.setAlignment(Qt.AlignLeft)

        self.button.setMaximumSize(18, 14)
        self.button.setContentsMargins(1, 1, 1, 1)

        self.text_QLabel.setAlignment(Qt.AlignLeft)
        self.text_QLabel.setAlignment(Qt.AlignVCenter)
        self.text_QLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.text_QLabel.setContentsMargins(1, 1, 1, 1)
        self.text_QLabel.setMinimumHeight(14)

        self.button.clicked.connect(self.set_vis)

    def set_vis(self):
        """
        Sets the vis of the mesh.
        """

        obj = self.check_obj()
        if obj:
            obj.v.set(not obj.v.get())
            self.check_button_text(obj.v.get())

    def check_obj(self):
        """
        Checks to make sure a object exists.

        :return: Returns a pynode of the object.
        :rtype: pm.nt.DagNode
        """

        label = self.text_QLabel.text()
        if pm.objExists(label):
            return pm.PyNode(label)
        return

    def check_button_text(self, value):
        """
        Sets the v in the visibility button.

        :param value:
        """

        if value:
            self.button.setText('V')
        else:
            self.button.setText('')

    def set_text(self, text, color=STAGING_COLOR_WHITE):
        """
        Sets the text for the QLabel

        :param str text: The text to be entered into the Qlabel
        :param str color: The RBG color code
        """
        self.text_QLabel.setStyleSheet(f'''color: rgb{color};''')
        self.text_QLabel.setText(text)

    def set_button_text(self, text, color=STAGING_COLOR_WHITE):
        """
        Sets the text for the QPushButton

        :param str text: The text put onto the QPushButton
        :param str color: The RBG color code
        """

        self.button.setStyleSheet(f'''color: rgb{color};''')
        self.button.setFont(QFont('Arial', 7))
        self.button.setStyleSheet("text-align: Center;")
        self.button.setText(text)

    @classmethod
    def create(cls, qlist_widget, text, button_text='V', color=STAGING_COLOR_WHITE):
        """
        Creates a nested text with a nested button to be added to a QListWidget.

        :param QListWidget qlist_widget: A QT QListWidget.
        :param str text: Sets a nested text to be added to a QListWidget.
        :param str button_text: Sets the text in the button.
        :param str color: The color of the text.
        """

        myQCustomQWidget = cls()
        myQCustomQWidget.set_text(text, color)
        myQCustomQWidget.set_button_text(button_text, color)
        obj = myQCustomQWidget.check_obj()
        if obj:
            myQCustomQWidget.check_button_text(obj.v.get())
        # Create QListWidgetItem
        myQListWidgetItem = QListWidgetItem(qlist_widget)
        myQListWidgetItem.setData(0, myQCustomQWidget.text_QLabel)
        myQListWidgetItem.setData(1, myQCustomQWidget.button)
        # Set size hint
        myQListWidgetItem.setSizeHint(myQCustomQWidget.minimumSizeHint())
        # Add QListWidgetItem into QListWidget

        qlist_widget.addItem(myQListWidgetItem)
        qlist_widget.setItemWidget(myQListWidgetItem, myQCustomQWidget)