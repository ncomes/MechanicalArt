#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Build a Rig UI.

"""

# python imports
import os

# software specific imports
import pymel.core as pm

from PySide2.QtWidgets import QSizePolicy, QSpacerItem, QComboBox, QMessageBox, QHBoxLayout, QWidget, QListWidget, QAbstractItemView

# mca python imports
from mca.common import log

from mca.common.assetlist import assetlist
from mca.common.paths import paths
from mca.common.pyqt import messages
from mca.common.resources import resources
from mca.common.tools.dcctracking import dcc_tracking
from mca.common.utils import lists, pymaths

from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import mayawindows
from mca.mya.rigging import chain_markup, frag, rig_utils, skel_utils
from mca.mya.rigging.flags import frag_flag
from mca.mya.utils import attr_utils, dag, naming

from mca.mya.tools.buildarig import buildarig_data, buildarig_utils

logger = log.MCA_LOGGER

COMPONENT_CATEGORY_WHITE_LIST = {'Arms': {'Simple FK': buildarig_data.FKComponentRigBuilder,
                                          'IK Fk Switch': buildarig_data.IKFKComponentRigBuilder},

                                 'Legs': {'Leg & Reverse Foot': buildarig_data.ReverseFootComponentRigBuilder,
                                          'Z Leg & Reverse Foot': buildarig_data.ZLegComponentRigBuilder,
                                          'IK Fk Switch': buildarig_data.IKFKComponentRigBuilder},

                                 'Spine': {'Simple FK': buildarig_data.FKComponentRigBuilder,
                                           'Pelvis': buildarig_data.PelvisComponentRigBuilder,
                                           'Reverse FK': buildarig_data.RFKComponentRigBuilder},

                                 'Tails': {'Simple FK': buildarig_data.FKComponentRigBuilder,
                                           'Ribbon': buildarig_data.SplineIKRibbonComponentRigBuilder,
                                           'Spline IK': buildarig_data.SplineIKComponentRigBuilder},

                                 'Misc': {'Cog': buildarig_data.CogComponentRigBuilder,
                                          'World': buildarig_data.WorldComponentRigBuilder}}


FLAG_SHAPE_DIR = os.path.join(paths.get_common_tools_path(), 'Common\\Rigging\\Flag Shapes\\')


def new_rig_prompt():
    """
    New toolbox prompt

    :return: Selected Asset Id
    :rtype: str
    """

    message_box = messages.MCAMessageBox(title='New Rig',
                            text='Select an existing Asset ID as the base for this rig.',
                            detail_text=None,
                            style=None,
                            sound=None,
                            parent=None)
    message_box.setIconPixmap(resources.icon('question', typ=resources.ResourceTypes.PIXMAP))

    # MessageBox UI overrides.
    message_box_layout = message_box.layout()
    asset_list_comboBox = QComboBox()
    asset_name_dict = {}
    for subcategory, entry_dict in assetlist.AssetListRegistry().CATEGORY_DICT.get('model', {}).items():
        for asset_id, mca_asset in entry_dict.items():
            asset_name_dict[mca_asset.asset_name] = mca_asset
    asset_list_comboBox.addItems(list(sorted(asset_name_dict)))
    message_box_layout.addWidget(asset_list_comboBox, 3, 0, 1, -1)
    message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    horizontal_layout = QHBoxLayout()
    message_box_layout.addLayout(horizontal_layout, 5, 0, 1, -1)
    for prompt_button in message_box.buttons():
        horizontal_layout.addWidget(prompt_button)
    message_box.exec_()
    return_val = asset_list_comboBox.currentText()
    return 'Cancel' if message_box.result == 'Cancel' else asset_name_dict[return_val]


class BuildARig(mayawindows.MCAMayaWindow):
    VERSION = '1.0.1'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'buildarig_ui.ui')
        super().__init__(title='BuildARig',
                         ui_path=ui_path,
                         version=BuildARig.VERSION)

        self.current_component = None
        self.frag_rig = None

        self.vertical_spacer = None
        self.initialize_component_list()
        self.setup_signals()
        self.setup_info_panel(buildarig_data.WorldComponentRigBuilder)

    class ComponentsListWidget(QListWidget):
        def __init__(self, parent, parent_ui, parent_tab, components_list):
            super().__init__(parent)
            self.class_parent = parent_ui
            self.parent_tab = parent_tab
            self.addItems(components_list)

            self.itemClicked.connect(lambda: self.class_parent.setup_info_panel(self.get_active_component()))

        def get_active_component(self):
            return COMPONENT_CATEGORY_WHITE_LIST.get(self.parent_tab, {}).get(self.currentItem().text())


    def setup_signals(self):
        # Main Tab
        self.ui.add_component_pushButton.clicked.connect(self.build_component_clicked)
        self.ui.remove_component_pushButton.clicked.connect(self.remove_component_clicked)

        self.ui.attach_pushButton.clicked.connect(self.attach_component_clicked)

        self.ui.create_new_rig_pushButton.clicked.connect(self.create_new_rig)

        self.ui.save_rig_pushButton.clicked.connect(self.save_rig_clicked)
        self.ui.load_rig_pushButton.clicked.connect(self.load_rig_clicked)

        # Flags Tab
        self.ui.lock_axis_pushButton.clicked.connect(self.lock_flag_axis_clicked)
        self.ui.flag_toggle_pushButton.clicked.connect(self.flag_toggle_clicked)

        self.ui.add_multiconstraint_pushButton.clicked.connect(self.add_multiconstraint_clicked)
        self.ui.remove_multiconstraint_pushButton.clicked.connect(self.remove_multiconstraint_clicked)

        self.ui.save_new_flag_pushButton.clicked.connect(self.save_new_flag_shape_clicked)
        self.ui.delete_flag_shape_pushButton.clicked.connect(self.delete_flag_shape_clicked)

        self.ui.copy_shape_pushButton.clicked.connect(self.copy_shape_to_selected_flags_clicked)
        self.ui.mirror_shape_pushButton.clicked.connect(self.mirror_shape_clicked)
        self.ui.replace_shape_pushButton.clicked.connect(self.replace_flags_with_selected_shapes_clicked)

        self.ui.export_rig_flags_pushButton.clicked.connect(self.export_rig_flags_clicked)
        self.ui.refresh_rig_flags_pushButton.clicked.connect(self.refresh_rig_flags_clicked)

    def initialize_component_list(self):
        self.setup_component_picker_tabs()

        self.ui.import_flag_comboBox.clear()
        self.ui.import_flag_comboBox.addItems(sorted([x.split('.')[0] for x in os.listdir(FLAG_SHAPE_DIR)]))

    def setup_component_picker_tabs(self):
        self.ui.component_list_tabWidget.clear()
        for tab_name, component_dict in sorted(COMPONENT_CATEGORY_WHITE_LIST.items()):
            new_tab_widget = QWidget()
            self.ui.component_list_tabWidget.addTab(new_tab_widget, tab_name)
            tab_layout = QHBoxLayout(new_tab_widget)
            new_list_widget = self.ComponentsListWidget(new_tab_widget, self, tab_name, sorted(component_dict.keys()))
            new_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            tab_layout.addWidget(new_list_widget)

    def setup_info_panel(self, active_component):
        self.clear_layout(self.ui.additional_ops_verticalLayout)
        self.current_component = active_component(self)
        self._add_vertical_spacer()

    def clear_layout(self, layout):
        """
        Removes all QWidgets from a QLayout

        :param QLayout layout:
        """

        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().close()
                    child.widget().setParent(None)
                elif child.layout() is not None:
                    self.clear_layout(child.layout())

    def _add_vertical_spacer(self):
        """
        This removes and then adds the vertical spacer to the end of the additional_ops_verticalLayout.

        """

        try:
            if self.vertical_spacer:
                self.ui.additional_ops_verticalLayout.removeWidget(self.vertical_spacer.widget())
        except:
            pass

        self.vertical_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ui.additional_ops_verticalLayout.addItem(self.vertical_spacer)

    def get_frag_rig(self):
        """
        From the selection or a list of the frag roots in the scene set the first found frag rig.

        """

        self.frag_rig = None

        selection = lists.get_first_in_list(pm.selected())
        if not self.frag_rig and selection:
            # Find frag rig by selection
            self.frag_rig = frag.get_frag_rig(selection)

        if not self.frag_rig:
            # Find first frag rig in scene
            frag_root = lists.get_first_in_list(frag.get_all_frag_roots())
            self.frag_rig = None
            if frag_root:
                self.frag_rig = frag_root.get_rig()

        if not self.frag_rig:
            # Couldn't find a frag rig so lets build a new one.
            if messages.question_message('Unable to find FragRig', 'Would you like to create a new frag rig?') != 'Yes':
                return

            asset_id = None
            if isinstance(selection, pm.nt.Joint):
                skel_root = dag.get_absolute_parent(selection, pm.nt.Joint)
                if skel_root.hasAttr('asset_id'):
                    asset_id = skel_root.getAttr('asset_id')
            self.create_new_rig(asset_id)

    def create_new_rig(self, asset_id=None):
        """
        Build the combination FRAGRoot/FragRig from a list of assets or from the skeleton's asset_id.

        :param str asset_id: The asset id that represents an assetlist entry.
        """

        mca_asset = assetlist.get_asset_by_id(asset_id) or new_rig_prompt()
        if mca_asset == 'Cancel':
            logger.info('Rig choice aborted.')
            return

        if not mca_asset:
            logger.error(f'Failed to find asset data register under id: {asset_id}')
            return

        skel_root = lists.get_first_in_list(pm.ls('|*', type=pm.nt.Joint))
        if not skel_root:
            skel_path = mca_asset.skel_path
            if os.path.exists(skel_path):
                skel_root = skel_utils.import_skeleton(skel_path)
                # Just make sure our asset_id is set correctly.
                skel_root.setAttr('asset_id', mca_asset.asset_id)

        if not skel_root:
            logger.error(f'Failed to import skeleton from id: {mca_asset.asset_name}')
            return

        frag_root = frag.FRAGRoot.create(skel_root, mca_asset.asset_type, mca_asset.asset_id)
        frag.SkeletalMesh.create(frag_root)
        self.frag_rig = frag.FRAGRig.create(frag_root)

        # Auto Build world root component.
        world_component = frag.WorldComponent.create(self.frag_rig,
                                                     skel_root,
                                                     'center',
                                                     'world')
        world_flag = world_component.get_flags()[0]
        root_flag = world_component.root_flag
        offset_flag = world_component.offset_flag

        # Root Multiconstraint
        frag.MultiConstraint.create(self.frag_rig,
                                    side='center',
                                    region='root',
                                    source_object=root_flag,
                                    target_list=[world_flag,
                                                 offset_flag])
        flag_path = mca_asset.flags_path
        for my_flag in world_component.get_flags():
            frag_flag.swap_flags([frag_flag.Flag(my_flag)], flag_path)

    @ma_decorators.undo_decorator
    @ma_decorators.keep_selection_decorator
    def build_component_clicked(self):
        """

        From the selected rig component in the drop down build it on the selected joints for the active frag rig.
        """

        selection = pm.selected()
        if not selection:
            messages.error_message('Selection Error', 'Please select joints to continue.')
            return

        self.get_frag_rig()
        if not self.frag_rig:
            messages.error_message('Build Error', 'A Frag Rig must be established to add components.')
            return

        asset_id = self.frag_rig.get_root().asset_id
        mca_asset = assetlist.get_asset_by_id(asset_id)
        flag_path = mca_asset.flags_path

        found_list = []
        skel_hierarchy = None
        for x in selection:
            found_frag_rig = frag.get_frag_rig(x)
            if not found_frag_rig:
                logger.warning('Selection does not have a valid frag rig.')
                continue

            if found_frag_rig != self.frag_rig:
                self.frag_rig = found_frag_rig

            if not skel_hierarchy:
                root_joint = dag.get_absolute_parent(x)
                skel_hierarchy = chain_markup.ChainMarkup(root_joint)
            wrapped_joint = chain_markup.JointMarkup(x)
            current_side = wrapped_joint.side
            current_region = wrapped_joint.region
            build_list = [skel_hierarchy.get_start(current_region, current_side)]

            if self.ui.mirror_component_checkBox.isChecked():
                opposite_side = None
                if current_side == 'right':
                    opposite_side = 'left'
                elif current_side == 'left':
                    opposite_side = 'right'
                if opposite_side:
                    build_list.append(skel_hierarchy.get_start(current_region, opposite_side))

            for found_start in build_list:
                if found_start and found_start not in found_list:
                    found_list.append(found_start)
                    new_component = self.current_component.build_component(found_start)
                    if new_component:
                        for my_flag in new_component.get_flags():
                            frag_flag.swap_flags([frag_flag.Flag(my_flag)], flag_path)

        self.frag_rig.color_flags()

    @ma_decorators.undo_decorator
    def remove_component_clicked(self):
        """
        Calls the local remove fnc on each component selected.

        """

        selection = pm.selected()
        component_list = []
        for x in selection:
            if frag_flag.is_flag_node(x):
                wrapped_flag = frag_flag.Flag(x)
                component_list.append(frag.FRAGNode(wrapped_flag.fragParent.get()))

        for component in list(set(component_list)):
            component.remove()

    @ma_decorators.undo_decorator
    @ma_decorators.keep_selection_decorator
    def attach_component_clicked(self):
        """
        Calls the local attach fnc for each selected component. All build components should automatically attach
        themselves to their parent joint.

        """

        selection = pm.selected()
        if len(selection) < 2:
            messages.error_message('Selection Error', 'At least two objects must be selected. One or more flags or '
                                                      'joints must be selected at the objects which will drive the '
                                                      'attach, and the last object selected must be a flag on the '
                                                      'component which will follow.')
            return
        source_object_list = selection[:-1]
        attach_object = selection[-1]

        if not frag_flag.is_flag_node(attach_object):
            messages.error_message('Selection Error', 'The last selected object must be a component\'s flag.')
            return

        frag_parent_list = []
        for x in source_object_list:
            try:
                frag_node = frag.FRAGNode(lists.get_first_in_list(x.listConnections(type=pm.nt.Network)))
                frag_parent_list.append(frag_node)
            except:
                pass

        if not frag_parent_list:
            frag_parent_list = frag.get_frag_rig(attach_object)

        my_flag = frag_flag.Flag(attach_object)
        rig_component = frag.FRAGNode(my_flag.fragParent.get())

        rig_component.attach_component(frag_parent_list, source_object_list, self.ui.attach_translation_checkBox.isChecked(), self.ui.attach_rotation_checkBox.isChecked())

    def save_rig_clicked(self):
        """
        From a selected rig, serialize it to a .rig file.

        """
        selection = pm.selected()
        if not selection:
            frag_root_list = frag.get_all_frag_roots()
            if len(frag_root_list) == 1:
                selection = frag_root_list[0].get_rig().pynode
                pm.select(selection)
        if not selection:
            messages.error_message('Selection Error', 'Please select a rig to continue.')
            return

        buildarig_utils.save_serialized_rig_cmd()

    @ma_decorators.undo_decorator
    def load_rig_clicked(self):
        """
        From a .rig file load the rig onto the current frag rig.

        """

        if not self.frag_rig or not pm.objExists(self.frag_rig.pynode):
            self.get_frag_rig()
        if pm.objExists(self.frag_rig.pynode):
            pm.select(self.frag_rig)
            buildarig_utils.load_serialized_rig_cmd(None)


    @ma_decorators.undo_decorator
    @ma_decorators.keep_selection_decorator
    def lock_flag_axis_clicked(self):
        """
        For each selected flag toggle locks on the transform atrtibutes.

        """

        selection = pm.selected()
        if not selection:
            messages.error_message('Selection Error', 'Please select flags to continue.')

        attr_list = []
        for checkbox, attr_name in zip([self.ui.translate_x_checkBox, self.ui.translate_y_checkBox, self.ui.translate_z_checkBox,
                                        self.ui.rotate_x_checkBox, self.ui.rotate_y_checkBox, self.ui.rotate_z_checkBox],
                                       attr_utils.TRANSLATION_ATTRS+attr_utils.ROTATION_ATTRS):
            if checkbox.isChecked():
                attr_list.append(attr_name)

        if self.ui.scale_lock_checkBox.isChecked():
            attr_list += attr_utils.SCALE_ATTRS

        for x in selection:
            if not frag_flag.is_flag_node(x):
                continue

            attr_utils.set_attr_state(x, locked=False, attr_list=attr_utils.TRANSFORM_ATTRS, visibility=True)
            attr_utils.set_attr_state(x, attr_list=attr_list, visibility=True)

    @ma_decorators.undo_decorator
    @ma_decorators.keep_selection_decorator
    def flag_toggle_clicked(self):
        """
        For each selected flag toggle the flag type toggles and recolor them.

        """

        selection = pm.selected()
        if not selection:
            messages.error_message('Selection Error', 'Please select flags to continue.')

        attr_list = ['isContact', 'isDetail', 'isSub', 'isUtil']
        val_list = []
        for checkbox in [self.ui.flag_iscontact_checkBox, self.ui.flag_isdetail_checkBox,
                         self.ui.flag_issub_checkBox, self.ui.flag_isutil_checkBox]:
            val_list.append(checkbox.isChecked())

        finalize_rig = False
        for x in selection:
            if not frag_flag.is_flag_node(x):
                continue

            for attr_name, val in zip(attr_list, val_list):
                x.setAttr(attr_name, val)
                if attr_name in ['isContact', 'isDetail'] or not any(val_list):
                    # If the flag is being added or removed from contact or details we'll need to finalize the rig.
                    finalize_rig = True
                    pm.editDisplayLayerMembers("defaultLayer", x)

        self.get_frag_rig()
        if self.frag_rig and pm.objExists(self.frag_rig.get_root().pynode):
            if finalize_rig:
                self.frag_rig.finalize_rig()
            else:
                self.frag_rig.color_flags()

    @ma_decorators.undo_decorator
    @ma_decorators.keep_selection_decorator
    def add_multiconstraint_clicked(self):
        """
        For each object selected in order add them to final selection as a new multiconstraint.

        """

        selection = pm.selected()
        if len(selection) < 2:
            messages.info_message('Selection Error', 'At least two flags from the same rig must be selected.', icon='error')
            return
        constraint_list = selection[:-1]
        prime_object = selection[-1]

        if not frag_flag.is_flag_node(prime_object):
            messages.info_message('Selection Error', 'The final selection object must be a flag, and will be the constrained object.', icon='error')
            return

        if prime_object.hasAttr('sourceMultiConstraint'):
            multiconstraint_node = prime_object.getAttr('sourceMultiConstraint')
            if multiconstraint_node:
                multiconstraint_node = frag.FRAGNode(multiconstraint_node)
            if multiconstraint_node:
                multiconstraint_node.remove()

        my_flag = frag_flag.Flag(prime_object)
        rig_component = frag.FRAGNode(my_flag.fragParent.get())
        switch_object = None
        if isinstance(rig_component, frag.IKFKComponent) and my_flag.node == rig_component.ik_flag.node:
            switch_object = rig_component.switch_flag
        frag_rig = rig_component.get_frag_parent()
        frag_root = frag_rig.get_frag_parent()
        skel_hierarchy = pm.listRelatives(frag_root.root_joint, ad=True, type=pm.nt.Joint)

        flag_list = frag_rig.get_flags()
        filtered_list = []
        for constraint_object in constraint_list:
            if not frag_flag.is_flag_node(constraint_object) and constraint_object not in skel_hierarchy:
                logger.error(f'{constraint_object}: Is not a valid flag object, or is not part of the rig\'s skeleton hierarchy.')
                continue

            if frag_flag.is_flag_node(constraint_object):
                wrapped_flag = frag_flag.Flag(constraint_object)
                if wrapped_flag not in flag_list:
                    logger.error(f'{constraint_object}: Is not part of the same frag rig as the source object.')
                    continue

            filtered_list.append(constraint_object)

        if not filtered_list:
            messages.error_message('Selection Error', 'Choose flags from the same rig as the final flag selection. All constraint targets were invalid selections.')

        base_name = naming.get_basename(prime_object)[2:]
        frag.MultiConstraint.create(frag_rig,
                                    rig_component.side,
                                    base_name,
                                    prime_object,
                                    filtered_list,
                                    switch_obj=switch_object)

    @ma_decorators.undo_decorator
    @ma_decorators.keep_selection_decorator
    def remove_multiconstraint_clicked(self):
        """
        For each flag remove their multiconstraints.

        """

        selection = pm.selected()
        if not selection:
            messages.error_message('Selection Error', 'At least two flags from the same rig must be selected.')
            return

        for node in selection:
            if not frag_flag.is_flag_node(node):
                # Filter out non flags.
                continue

            if node.hasAttr('sourceMultiConstraint'):
                multiconstraint_node = node.getAttr('sourceMultiConstraint')
                if multiconstraint_node:
                    multiconstraint_node = frag.FRAGNode(multiconstraint_node)
                if multiconstraint_node:
                    multiconstraint_node.remove()
                    continue

            logger.info(f'Selected node had no multiconstraint.')

    @ma_decorators.keep_selection_decorator
    def save_new_flag_shape_clicked(self):
        """
        From the selected curved transform, serialize and save it as a new flag shape.

        """
        selection = pm.selected()
        if not selection or not isinstance(selection[0], pm.nt.Transform):
            messages.error_message('Selection Error', 'Please select a transform with a curve to continue.')
            return

        flag_name = messages.text_prompt_message('Save New Flag Shape', 'Please enter the name of the new flag shape.')
        if not flag_name or flag_name == 'Cancel':
            return

        frag_flag.export_flag(selection[0], os.path.join(FLAG_SHAPE_DIR, f'{flag_name.lower()}.flag'))
        self.initialize_component_list()

    def delete_flag_shape_clicked(self):
        """
        Delete the selected flag shape.

        """
        current_flag_shape = self.ui.import_flag_comboBox.currentText()

        if messages.question_message('Delete Flag Shape', f'Are you sure you want to delete the "{current_flag_shape}" selected flag shape?') != 'Yes':
            return

        flag_path = os.path.join(FLAG_SHAPE_DIR, f'{current_flag_shape}.flag')
        if os.path.exists(flag_path):
            os.remove(flag_path)
            self.ui.import_flag_comboBox.removeItem(self.ui.import_flag_comboBox.currentIndex())

    @ma_decorators.undo_decorator
    def copy_shape_to_selected_flags_clicked(self):
        """
        From the selected flag shape import and duplicate it to all selected flags.

        """
        selection = pm.selected()

        if not selection:
            messages.error_message('Selection Error', 'Please select the flags to edit.')
            return

        current_flag_shape = self.ui.import_flag_comboBox.currentText()

        flag_path = os.path.join(FLAG_SHAPE_DIR, f'{current_flag_shape}.flag')
        new_shape = frag_flag.import_flag(flag_path)

        if not new_shape:
            messages.error_message('Import Error', f'Could not import the "{current_flag_shape}" flag shape.')
            return

        new_shape_list = []
        for flag_node in selection:
            if not frag_flag.is_flag_node(flag_node):
                continue

            duplicate_shape = pm.duplicate(new_shape)[0]
            duplicate_shape.setParent(flag_node)
            duplicate_shape.t.set(0, 0, 0)
            duplicate_shape.r.set(0, 0, 0)

            bb = pm.exactWorldBoundingBox(flag_node)
            sca = pymaths.find_distance_between_points(bb[:3], bb[3:])*.66

            duplicate_shape.s.set(sca, sca, sca)
            new_shape_list.append(duplicate_shape)
        pm.delete(new_shape)
        pm.select(new_shape_list)

    # Note this process doesn't undo properly
    @ma_decorators.not_undoable_decorator
    def replace_flags_with_selected_shapes_clicked(self):
        """
        From the selected shaped transforms, replace all parent flags with the selected shapes.

        """
        selection = pm.selected()

        if not selection:
            messages.error_message('Selection Error', 'Please select flag replacement shapes.')
            return

        flags_to_select = []
        frag_rig = None
        for new_shape in selection:
            shape_parent = new_shape.getParent()
            if not frag_flag.is_flag_node(shape_parent):
                continue

            if not isinstance(new_shape.getShape(), pm.nt.NurbsCurve):
                continue

            if not frag_rig:
                wrapped_flag = frag_flag.Flag(shape_parent)
                rig_component = frag.FRAGNode(wrapped_flag.fragParent.get())
                frag_rig = rig_component.get_frag_parent()

            flags_to_select.append(shape_parent)

            new_shape.setParent(shape_parent.getParent())
            pm.refresh()
            pm.makeIdentity(new_shape, t=True, r=True, s=True, n=False, pn=True, apply=True)
            pm.refresh()
            dag.parent_shape_node(new_shape, shape_parent, maintain_offset=True)
        frag_rig.color_flags()
        pm.select(flags_to_select)

    @ma_decorators.not_undoable_decorator
    def mirror_shape_clicked(self):
        """
        For each selected flag duplicate and mirror across the X axis. Find the opposite flag and replace the shape.

        """
        selection = pm.selected()

        if not selection:
            messages.error_message('Selection Error', 'Please select a shape to mirror.')
            return

        mirror_list = []
        identifier_dict = {}
        frag_rig = None
        for selected_node in selection:
            if frag_flag.is_flag_node(selected_node):
                if not frag_rig:
                    wrapped_flag = frag_flag.Flag(selected_node)
                    rig_component = frag.FRAGNode(wrapped_flag.fragParent.get())
                    frag_rig = rig_component.get_frag_parent()

                object_identifiers = buildarig_utils.get_object_identifier(selected_node)
                object_side = object_identifiers.get('side')
                if object_side == 'right':
                    object_identifiers['side'] = 'left'
                elif object_side == 'left':
                    object_identifiers['side'] = 'right'
                else:
                    # Skip all center flags or non directional flags.
                    continue

                found_flag = buildarig_utils.get_object_from_identifiers(frag_rig, object_identifiers)
                if not found_flag:
                    # Skip mirrors if there isn't a mirrored flag to copy to.
                    continue

                node_to_mirror = pm.duplicate(selected_node)[0]
                shape_list = node_to_mirror.getShapes()
                pm.delete([x for x in node_to_mirror.getChildren() if x not in shape_list])

                attr_utils.set_attr_state(node_to_mirror, False, attr_utils.TRANSFORM_ATTRS)
                empty_transform = pm.group(w=True, em=True)
                pm.delete(pm.parentConstraint(node_to_mirror, empty_transform))
                dag.parent_shape_node(node_to_mirror, empty_transform, maintain_offset=True)
                mirror_list.append(empty_transform)

                identifier_dict[empty_transform] = found_flag

        if mirror_list:
            mirror_grp = pm.group(em=True, w=True)
            pm.parent(mirror_list, mirror_grp)
            mirror_grp.s.set(-1, 1, 1)

            for mirror_node in mirror_list:
                found_flag = identifier_dict.get(mirror_node)
                if found_flag:
                    mirror_node.setParent(found_flag.getParent())
                    pm.refresh()
                    pm.makeIdentity(mirror_node, t=True, r=True, s=True, n=False, pn=True, apply=True)
                    pm.refresh()
                    dag.parent_shape_node(mirror_node, found_flag, maintain_offset=True)
            frag_rig.color_flags()
            pm.delete(mirror_grp)

    def export_rig_flags_clicked(self):
        """
        From selection export each frag rig's flags to its local flags directory.

        """
        rig_utils.export_flag_shapes_cmd()

    def refresh_rig_flags_clicked(self):
        """
        From selection refresh each frag rig's flags.

        """
        selection = pm.selected()

        if not selection:
            messages.error_message('Selection Error', 'Please select a rig component.')
            return

        refreshed_rig_list = []
        for x in selection:
            frag_rig = frag.get_frag_rig(x)
            if frag_rig not in refreshed_rig_list:
                refreshed_rig_list.append(frag_rig)

                frag_root = frag_rig.get_root()
                asset_id = frag_root.asset_id
                mca_asset = assetlist.get_asset_by_id(asset_id)
                for wrapped_flag in frag_rig.get_flags():
                    frag_flag.swap_flags([wrapped_flag], mca_asset.flags_path)
                frag_rig.color_flags()