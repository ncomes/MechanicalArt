#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
Face Skinning Tool
"""

# python imports
import os
# software specific imports
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
# mca python imports
from mca.common.modifiers import decorators
from mca.common import log

from mca.mya.pyqt import mayawindows
from mca.mya.modeling import vert_utils
from mca.mya.rigging import mesh_markup_rig
from mca.mya.face.face_utils import face_skinning, face_util


logger = log.MCA_LOGGER


class FaceSkinning(mayawindows.MCAMayaWindow):

    VERSION = '1.0.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'face_skinning_ui.ui')
        super().__init__(title='Face Skinning',
                         ui_path=ui_path,
                         version=FaceSkinning.VERSION)

        self._is_path_relative = False

        # dcc data

        # ==============================
        # Signals
        # ==============================
        
        self.ui.copy_weightsButton.clicked.connect(self._on_copy_weights_button_clicked)
        self.ui.mirror_weightsButton.clicked.connect(self._on_mirror_weights_button_clicked)
        self.ui.select_verticesButton.clicked.connect(self._on_select_vertices_button_clicked)
        self.ui.smooth_weightsButton.clicked.connect(self._on_smooth_weights_button_clicked)
        self.ui.toggle_visButton.clicked.connect(self._on_toggle_vis_button_clicked)
        self.ui.skin_to_headButton.clicked.connect(self._on_skin_to_head_clicked)
        self.ui.loadButton.clicked.connect(self._on_load_data_button_clicked)
        self.ui.mirror_selectionButton.clicked.connect(self._on_mirror_selection_button_clicked)
        self.ui.copy_paste_weightsButton.clicked.connect(self._copy_paste_vertex_weights_clicked)
        
    # ==============================
    # Slots
    # ==============================
    
    def _on_load_data_button_clicked(self):
        """
        Sets up region combo box

        """

        face_data = face_util.get_common_face_region_data('head_mesh')
        if not face_data:
            return

        region_vertex_data = face_data.get_vertex_default_regions()
        regions_list = region_vertex_data.data.keys()
        for each_region in regions_list:
            self.ui.regionsBox.addItem(each_region)

    
    def _on_copy_weights_button_clicked(self):
        """
        Copies weights from head mesh and applies them to another mesh

        """

        markup = mesh_markup_rig.RigMeshMarkup.create()
        face_data = face_util.get_common_face_region_data('head_mesh')
        face_mesh = str(markup.get_mesh_list_in_region('head_mesh')[0])
        if not face_mesh:
            return

        obj_to_skin = pm.ls(sl=True, fl=True)
        if not obj_to_skin:
            return

        face_skinning.copy_weights_from_head(face_mesh, face_data, obj_to_skin)
        pm.select(obj_to_skin)

    
    def _on_mirror_weights_button_clicked(self):
        """
        Mirrors vertex weights

        """

        vertex_selection = cmds.ls(sl=True, fl=True)

        if not vertex_selection:
            return

        markup = mesh_markup_rig.RigMeshMarkup.create()
        face_data = face_util.get_common_face_region_data('head_mesh')
        if not face_data:
            return

        face_mesh = str(markup.get_mesh_list_in_region('head_mesh')[0])
        if not face_mesh:
            return

        face_skinning.mirror_face_weights(vertex_selection, str(face_mesh), face_data)

    
    def _on_select_vertices_button_clicked(self):
        """
        Selects vertices in a particular region
        """

        face_data = face_util.get_common_face_region_data('head_mesh')
        if not face_data:
            return

        markup = mesh_markup_rig.RigMeshMarkup.create()
        region_vertex_data = face_data.get_vertex_default_regions()
        skinned_head = str(markup.get_mesh_list_in_region('head_mesh')[0])
        if not skinned_head:
            return

        region = self.ui.regionsBox.currentText()

        keep_previous_sel = self.ui.keep_prev_selBox.isChecked()
        current_selection = pm.ls(sl=True, fl=True)
        pm.select(cl=True)

        eval(f'region_vertex_data.select_{region}' + '(skinned_head)')

        if keep_previous_sel:
            pm.select(current_selection, add=True)

    
    def _on_smooth_weights_button_clicked(self):
        """
        Smooths selected vertex weights (Note: this works for now but will be updated)

        """
        tolerance_slider_value = self.ui.smooth_toleranceSlider.value()
        tolerance_value = tolerance_slider_value * 0.1

        selected_verts = pm.ls(sl=True, fl=True)

        if not selected_verts:
            return

        if not isinstance(selected_verts[0], pm.general.MeshVertex):
            return

        obj_to_skin = str(selected_verts[0]).split('.vtx')[0]
        obj_clus = pm.listConnections(obj_to_skin, type='skinCluster')

        pm.skinCluster(obj_clus, edit=True, smoothWeights=tolerance_value)

    
    def _on_toggle_vis_button_clicked(self):
        """
        Toggle visibility of blendshape and skinned mesh

        """

        markup = mesh_markup_rig.RigMeshMarkup.create()

        skinned_head = markup.get_mesh_list_in_region('head_mesh')[0]
        blend_head = markup.get_mesh_list_in_region('head_blendshape')[0]

        skinned_mouth = markup.get_mesh_list_in_region('mouth_mesh')[0]
        blend_mouth = markup.get_mesh_list_in_region('mouth_blendshape')[0]

        if not skinned_head:
            logger.warning('Head mesh not found.')
            return
        if not blend_head:
            logger.warning('Head blendshape mesh not found.')
            return

        skinned_head_vis = pm.getAttr(f'{skinned_head}.visibility')
        blend_head_vis = pm.getAttr(f'{blend_head}.visibility')

        if skinned_head_vis:
            pm.setAttr(f'{skinned_head}.visibility', 0)
            pm.setAttr(f'{blend_head}.visibility', 1)
            logger.info('Blendshape head now visible')

        elif blend_head_vis or skinned_head_vis and blend_head_vis:
            pm.setAttr(f'{blend_head}.visibility', 0)
            pm.setAttr(f'{skinned_head}.visibility', 1)
            logger.info('Skinned head now visible')

        if skinned_mouth and blend_mouth:
            skinned_mouth_vis = pm.getAttr(f'{skinned_mouth}.visibility')
            blend_mouth_vis = pm.getAttr(f'{blend_mouth}.visibility')

            if skinned_mouth_vis:
                pm.setAttr(f'{skinned_mouth}.visibility', 0)
                pm.setAttr(f'{blend_mouth}.visibility', 1)

            elif blend_mouth_vis or skinned_mouth_vis and blend_head_vis:
                pm.setAttr(f'{blend_mouth}.visibility', 0)
                pm.setAttr(f'{skinned_mouth}.visibility', 1)

    
    def _on_skin_to_head_clicked(self):
        """
        Hard skins selection to head

        """
        check_for_root = pm.objExists('root')
        if not check_for_root:
            return

        root_joint = pm.PyNode('root')
        selected_objs = pm.ls(sl=True, fl=True)

        face_skinning.skin_to_head_joint(selected_objs, root_joint)

    
    def _on_mirror_selection_button_clicked(self):
        """
        Mirrors selection based on vertex data

        """
        vertex_selection = cmds.ls(sl=True, fl=True)
        markup = mesh_markup_rig.RigMeshMarkup.create()
        face_data = face_util.get_common_face_region_data('head_mesh')
        if not face_data:
            return

        face_mesh = str(markup.get_mesh_list_in_region('head_mesh')[0])
        if not face_mesh:
            return

        mirror_data = face_data.get_mirror_data()
        vert_mirror_data = mirror_data.mirror_map
        keep_previous_sel = self.ui.keep_prev_selBox.isChecked()

        if not keep_previous_sel:
            cmds.select(cl=True)

        for x, vertex in enumerate(vertex_selection):
            vertex_number = vert_utils.get_vertices_as_numbers(vertex)[0]
            mir = vert_mirror_data.get(str(vertex_number))
            if not mir:
                pass
            else:
                mirror_vert_name = f'{face_mesh}.vtx[{mir}]'
                cmds.select(mirror_vert_name, add=True)

    
    def _copy_paste_vertex_weights_clicked(self):
        """
        Copies first selected vertex weight and pastes onto rest of selection

        """
        verts = cmds.ls(fl=True, os=True)

        if len(verts) < 2:
            return

        cmds.select(verts[0])
        mel.eval('artAttrSkinWeightCopy')
        cmds.select(verts)
        mel.eval('artAttrSkinWeightPaste')
