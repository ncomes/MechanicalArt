"""
Module that contains Build a Rig UI.

"""

# python imports
import inspect
import os
# software specific imports
import pymel.core as pm
from mca.common.pyqt.pygui import qtwidgets

# mca python imports
from mca.common.assetlist import assetlist
from mca.common.project import project_paths
from mca.common.pyqt import messages
from mca.common.pyqt.qt_utils import general_utils
from mca.common.resources import resources
from mca.common.utils import list_utils, pymaths

from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import mayawindows
from mca.mya.rigging import flags, frag, joint_utils, skin_utils
from mca.mya.utils import attr_utils, dag_utils, naming
from mca.mya.tools.buildarig import buildarig_data

from mca.common import log
logger = log.MCA_LOGGER


COMPONENT_CATEGORY_WHITE_LIST = {'Arms': {'Simple FK': buildarig_data.FKComponentRigBuilder,
                                          'IK Fk Switch': buildarig_data.IKFKComponentRigBuilder,
                                          'Two Point IK': buildarig_data.TwoPointIKComponentRigBuilder,
                                          'Two Point IK/FK Switch': buildarig_data.TwoPointIKFKComponentRigBuilder},

                                 'Legs': {'Leg & Reverse Foot': buildarig_data.ReverseFootComponentRigBuilder,
                                          'IK Fk Switch': buildarig_data.IKFKComponentRigBuilder,
                                          'Two Point IK': buildarig_data.TwoPointIKComponentRigBuilder,
                                          'Two Point IK/FK Switch': buildarig_data.TwoPointIKFKComponentRigBuilder},

                                 'Spine': {'Simple FK': buildarig_data.FKComponentRigBuilder,
                                           'Pelvis': buildarig_data.PelvisComponentRigBuilder,
                                           'RFK': buildarig_data.RFKComponentRigBuilder},

                                 'Tails': {'Simple FK': buildarig_data.FKComponentRigBuilder},

                                 'Misc': {'Cog': buildarig_data.CogComponentRigBuilder,
                                          'World': buildarig_data.WorldComponentRigBuilder,
                                          'Piston': buildarig_data.PistonComponentRigBuilder}}

LOCAL_PATH = os.path.dirname(inspect.getabsfile(inspect.currentframe()))


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
    asset_list_comboBox = qtwidgets.QComboBox()
    asset_name_dict = {}
    asset_registry = assetlist.get_registry()
    for asset_id, asset_entry in asset_registry.ASSET_ID_DICT.items():
        if 'rig' in asset_entry.asset_type:
            asset_name_dict[asset_entry.asset_name] = asset_entry
    asset_list_comboBox.addItems(list(sorted(asset_name_dict)))
    message_box_layout.addWidget(asset_list_comboBox, 3, 0, 1, -1)
    message_box.setStandardButtons(qtwidgets.QMessageBox.Ok | qtwidgets.QMessageBox.Cancel)
    horizontal_layout = qtwidgets.QHBoxLayout()
    message_box_layout.addLayout(horizontal_layout, 5, 0, 1, -1)
    for prompt_button in message_box.buttons():
        horizontal_layout.addWidget(prompt_button)
    message_box.exec_()
    return_val = asset_list_comboBox.currentText()
    return 'Cancel' if message_box.result == 'Cancel' else asset_name_dict[return_val]


class BuildARig(mayawindows.MCAMayaWindow):
    _version = '1.0.2'

    def __init__(self):
        ui_path = os.path.join(LOCAL_PATH, 'uis', f'buildarig_ui.ui')
        super().__init__(title='BuildARig',
                         ui_path=ui_path,
                         version=BuildARig._version)

        self.current_component = None
        self.frag_rig = None

        self.ui.flag_rotate_order_comboBox.addItems(['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx'])

        self.vertical_spacer = None
        self.initialize_component_list()
        self.setup_signals()
        self.setup_info_panel(buildarig_data.WorldComponentRigBuilder)

    class ComponentsListWidget(qtwidgets.QListWidget):
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
        self.ui.finish_rig_pushButton.clicked.connect(self.finish_rig_clicked)

        # Flags Tab
        self.ui.lock_axis_pushButton.clicked.connect(self.lock_flag_axis_clicked)
        self.ui.flag_toggle_pushButton.clicked.connect(self.flag_toggle_clicked)
        self.ui.flag_rotate_order_pushButton.clicked.connect(self.set_flag_rotate_order_clicked)

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
        self.ui.import_flag_comboBox.addItems(sorted([x.split('.')[0] for x in os.listdir(flags.DEFAULT_FLAGS_PATH)]))

    def setup_component_picker_tabs(self):
        self.ui.component_list_tabWidget.clear()
        for tab_name, component_dict in sorted(COMPONENT_CATEGORY_WHITE_LIST.items()):
            new_tab_widget = qtwidgets.QWidget()
            self.ui.component_list_tabWidget.addTab(new_tab_widget, tab_name)
            tab_layout = qtwidgets.QHBoxLayout(new_tab_widget)
            new_list_widget = self.ComponentsListWidget(new_tab_widget, self, tab_name, sorted(component_dict.keys()))
            new_list_widget.setSelectionMode(qtwidgets.QAbstractItemView.SelectionMode.SingleSelection)
            tab_layout.addWidget(new_list_widget)

    def setup_info_panel(self, active_component):
        self.clear_layout(self.ui.additional_ops_verticalLayout)
        self.clear_layout(self.ui.picture_horizontalLayout)
        self.current_component = active_component(self)
        self._add_vertical_spacer()

    def clear_layout(self, layout):
        """
        Removes all qtwidgets.QWidgets from a QLayout

        :param QLayout layout:
        """

        general_utils.delete_items_of_layout(layout)

    def _add_vertical_spacer(self):
        """
        This removes and then adds the vertical spacer to the end of the additional_ops_verticalLayout.

        """

        try:
            if self.vertical_spacer:
                self.ui.additional_ops_verticalLayout.removeWidget(self.vertical_spacer.widget())
        except:
            pass

        self.vertical_spacer = qtwidgets.QSpacerItem(40, 20, qtwidgets.QSizePolicy.Minimum, qtwidgets.QSizePolicy.Expanding)
        self.ui.additional_ops_verticalLayout.addItem(self.vertical_spacer)

    def get_frag_rig(self):
        """
        From the selection or a list of the frag roots in the scene set the first found frag rig.

        """

        self.frag_rig = None

        selection = list_utils.get_first_in_list(pm.selected())
        if not self.frag_rig and selection:
            # Find frag rig by selection
            self.frag_rig = frag.get_frag_rig(selection)

        if not self.frag_rig:
            # Find first frag rig in scene
            frag_root = list_utils.get_first_in_list(frag.get_all_frag_roots())
            self.frag_rig = None
            if frag_root:
                self.frag_rig = frag_root.frag_rig

        if not self.frag_rig:
            # Couldn't find a frag rig so lets build a new one.
            if messages.question_message('Unable to find FragRig', 'Would you like to create a new frag rig?') != 'Yes':
                return

            asset_id = None
            if isinstance(selection, pm.nt.Joint):
                root_joint = dag_utils.get_absolute_parent(selection, pm.nt.Joint)
                if root_joint.hasAttr('asset_id'):
                    asset_id = root_joint.getAttr('asset_id')
            self.create_new_rig(asset_id)

    def create_new_rig(self, asset_id=None):
        """
        Build the combination FRAGRoot/FragRig from a list of assets or from the skeleton's asset_id.

        :param str asset_id: The asset id that represents an assetlist entry.
        """

        asset_entry = assetlist.get_asset_by_id(asset_id) or new_rig_prompt()
        if asset_entry == 'Cancel':
            logger.info('Rig choice aborted.')
            return

        if not asset_entry:
            logger.error(f'Failed to find asset data register under id: {asset_id}')
            return

        root_joint = list_utils.get_first_in_list(pm.ls('|*', type=pm.nt.Joint))
        if not root_joint:
            skeleton_path = asset_entry.skeleton_path
            if os.path.exists(skeleton_path):
                root_joint = joint_utils.import_skeleton(skeleton_path)
                # Just make sure our asset_id is set correctly.
                root_joint.setAttr('asset_id', asset_entry.asset_id)

        if not root_joint:
            logger.error(f'Failed to import skeleton from id: {asset_entry.asset_name}')
            return

        frag_root = frag.FRAGRoot.create(root_joint, asset_entry.asset_id)
        frag_mesh = frag.FRAGMesh.create(frag_root)
        frag.FRAGDisplay.create(frag_root)
        self.frag_rig = frag.FRAGRig.create(frag_root)
        node_list = skin_utils.get_skeleton_meshes(root_joint)
        shared_parent_list = []
        for node in node_list:
            node_parent = dag_utils.get_absolute_parent(node)
            if node_parent and not node_parent in shared_parent_list:
                shared_parent_list.append(node_parent)
                node_parent.setParent(frag_mesh.add_mesh_group())
            else:
                node_parent.setParent(frag_mesh.add_mesh_group())

        frag_root.organize_content()

        # Auto Build world root component.
        current_component = self.current_component
        self.setup_info_panel(buildarig_data.WorldComponentRigBuilder)
        self.current_component.build_component(root_joint)
        self.setup_info_panel(current_component.__class__)


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

        found_list = []
        skel_hierarchy = None
        for x in selection:
            found_frag_rig = frag.get_frag_rig(x)
            if not found_frag_rig:
                logger.warning('Selection does not have a valid frag rig.')
                continue

            if found_frag_rig != self.frag_rig:
                self.frag_rig = found_frag_rig

            for frag_component in self.frag_rig.get_frag_children(frag_type=frag.FRAGAnimatedComponent):
                if isinstance(frag_component, frag.CogComponent):
                    continue
                bind_joints = frag_component.joints
                if bind_joints:
                    found_list.append(bind_joints[0])

            if not skel_hierarchy:
                root_joint = dag_utils.get_absolute_parent(x, pm.nt.Joint)
                skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)
            wrapped_joint = joint_utils.JointMarkup(x)
            current_side = wrapped_joint.side
            current_region = wrapped_joint.region
            build_list = [skel_hierarchy.get_chain_start(current_side, current_region)]

            if self.ui.mirror_component_checkBox.isChecked():
                opposite_side = None
                if current_side == 'right':
                    opposite_side = 'left'
                elif current_side == 'left':
                    opposite_side = 'right'
                if opposite_side:
                    build_list.append(skel_hierarchy.get_chain_start(opposite_side, current_region))

            for found_start in build_list:
                if found_start and found_start not in found_list:
                    found_list.append(found_start)
                    new_component = self.current_component.build_component(found_start)

        self.frag_rig.finish_rig()

    @ma_decorators.undo_decorator
    def remove_component_clicked(self):
        """
        Calls the local remove fnc on each component selected.

        """

        selection = pm.selected()
        component_list = []
        for x in selection:
            wrapped_flag = flags.is_flag(x)
            if wrapped_flag:
                found_component = wrapped_flag.frag_parent
                if found_component and found_component not in component_list:
                    component_list.append(found_component)
            elif isinstance(x, pm.nt.Joint):
                network_node_list = pm.listConnections(type=pm.nt.Network)
                for y in network_node_list:
                    found_component = frag.FRAGNode(y)
                    if found_component and found_component not in component_list:
                        component_list.append(found_component)

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

        if not flags.is_flag(attach_object):
            messages.error_message('Selection Error', 'The last selected object must be a component\'s flag.')
            return

        rig_component = frag.get_component(attach_object)

        if rig_component:
            rig_component.attach_component(source_object_list, self.ui.attach_translation_checkBox.isChecked(), self.ui.attach_rotation_checkBox.isChecked())

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

        save_serialized_rig_cmd()

    @ma_decorators.undo_decorator
    def load_rig_clicked(self):
        """
        From a .rig file load the rig onto the current frag rig.

        """

        if not self.frag_rig or not pm.objExists(self.frag_rig.pynode):
            self.get_frag_rig()
        if self.frag_rig and pm.objExists(self.frag_rig.pynode):
            pm.select(self.frag_rig.pynode)
            load_serialized_rig_cmd(None)


    def finish_rig_clicked(self):
        if not self.frag_rig or not pm.objExists(self.frag_rig.pynode):
            self.get_frag_rig()

        if self.frag_rig and pm.objExists(self.frag_rig.pynode):
            self.frag_rig.finish_rig()

    @ma_decorators.undo_decorator
    @ma_decorators.keep_selection_decorator
    def lock_flag_axis_clicked(self):
        """
        For each selected flag toggle locks on the transform atrtibutes.

        """

        selection = pm.selected()
        if not selection:
            messages.error_message('Selection Error', 'Please select flags to continue.')
            return

        attr_list = []
        for checkbox, attr_name in zip([self.ui.translate_x_checkBox, self.ui.translate_y_checkBox, self.ui.translate_z_checkBox,
                                        self.ui.rotate_x_checkBox, self.ui.rotate_y_checkBox, self.ui.rotate_z_checkBox],
                                       attr_utils.TRANSLATION_ATTRS+attr_utils.ROTATION_ATTRS):
            if checkbox.isChecked():
                attr_list.append(attr_name)

        if self.ui.scale_lock_checkBox.isChecked():
            attr_list += attr_utils.SCALE_ATTRS

        for x in selection:
            if not flags.is_flag(x):
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
            return

        attr_list = ['contact', 'detail', 'sub', 'utility']
        val_list = []
        for checkbox in [self.ui.flag_iscontact_checkBox, self.ui.flag_isdetail_checkBox,
                         self.ui.flag_issub_checkBox, self.ui.flag_isutil_checkBox]:
            val_list.append(checkbox.isChecked())

        for x in selection:
            flag_node = flags.is_flag(x)
            if not flag_node:
                continue

            for attr_name, val in zip(attr_list, val_list):
                setattr(flag_node, attr_name, val)
                if attr_name in ['contact', 'detail'] or not any(val_list):
                    # If the flag is being added or removed from contact or details we'll need to finalize the rig.
                    pm.editDisplayLayerMembers("defaultLayer", x)

        self.get_frag_rig()
        if self.frag_rig and pm.objExists(self.frag_rig.get_frag_root().pynode):
            self.frag_rig.finish_rig()

    @ma_decorators.undo_decorator
    @ma_decorators.keep_selection_decorator
    def set_flag_rotate_order_clicked(self):
        """
        For each selected flag toggle the rotation order on a given flag, and it's align group.

        """

        selection = pm.selected()
        if not selection:
            messages.error_message('Selection Error', 'Please select flags to continue.')
            return

        rotation_type = self.ui.flag_rotate_order_comboBox.currentIndex()

        for x in selection:
            flag_node = flags.is_flag(x)
            if not flag_node:
                continue
            temp_align = pm.spaceLocator()
            
            align_group = flag_node.align_group
            pm.delete(pm.parentConstraint(align_group, temp_align))
            align_group.rotateOrder.set(rotation_type)
            x.rotateOrder.set(rotation_type)
            pm.delete(pm.parentConstraint(temp_align, align_group))
            pm.delete(temp_align)

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
        source_node = selection[-1]

        if not flags.is_flag(source_node):
            messages.info_message('Selection Error', 'The final selection object must be a flag, and will be the constrained object.', icon='error')
            return

        if source_node.hasAttr('sourceMultiConstraint'):
            multiconstraint_node = source_node.getAttr('sourceMultiConstraint')
            if multiconstraint_node:
                multiconstraint_node = frag.FRAGNode(multiconstraint_node)
            if multiconstraint_node:
                multiconstraint_node.remove()

        my_flag = flags.Flag(source_node)
        rig_component = frag.FRAGNode(my_flag.frag_parent)
        switch_object = None
        if isinstance(rig_component, frag.IKFKComponent) and my_flag.pynode == rig_component.pynode.ik_flag.get():
            switch_object = rig_component.pynode.switch_flag.get()
        frag_rig = rig_component.frag_parent
        frag_root = frag_rig.frag_parent
        skel_hierarchy = pm.listRelatives(frag_root.root_joint, ad=True, type=pm.nt.Joint)

        flag_pynode_list = [x.pynode for x in frag_rig.get_all_flags()]
        filtered_list = []
        for constraint_object in constraint_list:
            if not flags.is_flag(constraint_object) and constraint_object not in skel_hierarchy:
                logger.error(f'{constraint_object}: Is not a valid flag object, or is not part of the rig\'s skeleton hierarchy.')
                continue
            
            wrapped_flag = flags.is_flag(constraint_object)
            if wrapped_flag and wrapped_flag.pynode not in flag_pynode_list:
                logger.error(f'{constraint_object}: Is not part of the same frag rig as the source object.')
                continue

            filtered_list.append(constraint_object)

        if not filtered_list:
            messages.error_message('Selection Error', 'Choose flags from the same rig as the final flag selection. All constraint targets were invalid selections.')
            return

        frag.MultiConstraintComponent.create(frag_rig,
                                             source_node,
                                             filtered_list,
                                             switch_obj=switch_object,
                                             translate=self.ui.translation_multiconstraint_checkBox.isChecked(),
                                             rotate=self.ui.rotation_multiconstraint_checkBox.isChecked())

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
            if not flags.is_flag(node):
                # Filter out non flags.
                continue

            if node.hasAttr('source_multi_constraint'):
                multiconstraint_node = node.getAttr('source_multi_constraint')
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

        flags.export_flag(selection[0], os.path.join(flags.DEFAULT_FLAGS_PATH, f'{flag_name.lower()}.flag'))
        self.initialize_component_list()

    def delete_flag_shape_clicked(self):
        """
        Delete the selected flag shape.

        """

        current_flag_shape = self.ui.import_flag_comboBox.currentText()

        if messages.question_message('Delete Flag Shape', f'Are you sure you want to delete the "{current_flag_shape}" selected flag shape?') != 'Yes':
            return

        flag_path = os.path.join(flags.DEFAULT_FLAGS_PATH, f'{current_flag_shape}.flag')
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

        flag_path = os.path.join(flags.DEFAULT_FLAGS_PATH, f'{current_flag_shape}.flag')
        new_shape = flags.import_flag(flag_path)

        if not new_shape:
            messages.error_message('Import Error', f'Could not import the "{current_flag_shape}" flag shape.')
            return

        new_shape_list = []
        for flag_node in selection:
            if not flags.is_flag(flag_node):
                continue

            duplicate_shape = pm.duplicate(new_shape)[0]
            duplicate_shape.setParent(flag_node)
            duplicate_shape.t.set(0, 0, 0)
            duplicate_shape.r.set(0, 0, 0)

            bb = pm.exactWorldBoundingBox(flag_node)
            sca = pymaths.get_distance_between_points(bb[:3], bb[3:]) * 0.0356275303643725

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
            wrapped_flag = flags.is_flag(shape_parent)
            if not wrapped_flag:
                continue

            if not isinstance(new_shape.getShape(), pm.nt.NurbsCurve):
                continue

            if not frag_rig:
                rig_component = wrapped_flag.frag_parent
                frag_rig = rig_component.frag_parent

            flags_to_select.append(shape_parent)

            new_shape.setParent(shape_parent.getParent())
            pm.refresh()
            pm.makeIdentity(new_shape, t=True, r=True, s=True, n=False, pn=True, apply=True)
            pm.refresh()
            dag_utils.parent_shape_node(new_shape, shape_parent, maintain_offset=True)
        frag_rig._sort_flags()
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
            wrapped_flag = flags.is_flag(selected_node)
            if wrapped_flag:
                if not frag_rig:
                    rig_component = wrapped_flag.frag_parent
                    frag_rig = rig_component.frag_parent

                object_identifiers = frag.get_object_identifier(selected_node)
                object_side = object_identifiers.get('side')
                if object_side == 'right':
                    object_identifiers['side'] = 'left'
                elif object_side == 'left':
                    object_identifiers['side'] = 'right'
                else:
                    # Skip all center flags or non directional flags.
                    continue

                found_flag = frag.get_object_from_identifiers(frag_rig, object_identifiers)
                if not found_flag:
                    # Skip mirrors if there isn't a mirrored flag to copy to.
                    continue

                node_to_mirror = pm.duplicate(selected_node)[0]
                shape_list = node_to_mirror.getShapes()
                pm.delete([x for x in node_to_mirror.getChildren() if x not in shape_list])

                attr_utils.set_attr_state(node_to_mirror, False, attr_utils.TRANSFORM_ATTRS)
                empty_transform = pm.group(w=True, em=True)
                pm.delete(pm.parentConstraint(node_to_mirror, empty_transform))
                dag_utils.parent_shape_node(node_to_mirror, empty_transform, maintain_offset=True)
                mirror_list.append(empty_transform)

                identifier_dict[empty_transform] = found_flag

        if mirror_list:
            mirror_grp = pm.group(em=True, w=True)
            pm.parent(mirror_list, mirror_grp)
            mirror_grp.s.set(-1, 1, 1)

            for mirror_node in mirror_list:
                found_flag = identifier_dict.get(mirror_node)
                if found_flag:
                    mirror_node.setParent(found_flag.pynode.getParent())
                    pm.refresh()
                    pm.makeIdentity(mirror_node, t=True, r=True, s=True, n=False, pn=True, apply=True)
                    pm.refresh()
                    dag_utils.parent_shape_node(mirror_node, found_flag.pynode, maintain_offset=True)
            frag_rig._sort_flags()
            pm.delete(mirror_grp)

    def export_rig_flags_clicked(self):
        """
        From selection export each frag rig's flags to its local flags directory.

        """

        if not self.frag_rig or not pm.objExists(self.frag_rig.pynode):
            self.get_frag_rig()

        if self.frag_rig and pm.objExists(self.frag_rig.pynode):
            asset_id = self.frag_rig.asset_id
            asset_entry = assetlist.get_asset_by_id(asset_id)
            if asset_entry:
                flags_dir = asset_entry.flags_path
                for wrapped_flag in self.frag_rig.get_all_flags():
                    flag_path = os.path.join(flags_dir, f'{naming.get_basename(wrapped_flag.pynode)}.flag')
                    flags.export_flag(flag_path, wrapped_flag.pynode)

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

                asset_id = frag_rig.asset_id
                asset_entry = assetlist.get_asset_by_id(asset_id)
                for wrapped_flag in frag_rig.get_all_flags():
                    wrapped_flag.swap_shape(flag_path=os.path.join(asset_entry.flags_path, f'{naming.get_basename(wrapped_flag.pynode)}.flag'))
                frag_rig.finish_rig()

def load_serialized_rig_cmd(rig_path):
    """
    From the given path read the build instructions for a rig and build them on the FRAG Rig.

    :param str rig_path: The full path to where the rig build instructions are.
    """

    selection = pm.selected()
    frag_rig = None
    for selected_node in selection:
        # find us a valid frag_rig
        frag_rig = frag.get_frag_rig(selected_node)
        if frag_rig:
            break

    if not frag_rig:
        return

    start_path = os.path.join(project_paths.MCA_PROJECT_ROOT, 'Characters')
    if not rig_path:
        asset_id = frag_rig.asset_id
        try:
            asset_entry = assetlist.get_asset_by_id(asset_id)
            if asset_entry:
                start_path = asset_entry.rig_path
        except:
            pass
        
    rig_path, _ = qtwidgets.QFileDialog.getOpenFileName(None, 'Select Rig', start_path, 'MCARig (*.rig)')
    if not rig_path:
        return

    frag.load_serialized_rig(frag_rig, rig_path)

def save_serialized_rig_cmd():
    """
    From selection find the FRAG Rig and serialize the build instructions for each component.

    """

    selection = pm.selected()
    frag_rig = None
    for selected_node in selection:
        # find us a valid frag_rig
        frag_rig = frag.get_frag_rig(selected_node)
        if frag_rig:
            break

    if not frag_rig:
        return

    asset_id = frag_rig.asset_id
    mca_asset = assetlist.get_asset_by_id(asset_id)

    start_path = mca_asset.rig_path if mca_asset else os.path.join(project_paths.MCA_PROJECT_ROOT, 'Characters')

    found_path, _ = qtwidgets.QFileDialog.getSaveFileName(None, 'Select Rig', start_path, 'MCARig (*.rig)')
    if not found_path:
        return

    frag.save_serialized_rig(frag_rig, found_path)