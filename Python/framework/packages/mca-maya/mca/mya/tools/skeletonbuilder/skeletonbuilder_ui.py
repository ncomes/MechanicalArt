#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Skeleton Builder main UI.
"""

# System global imports
import os

# PySide2 imports
from mca.common.pyqt.pygui import qtwidgets, qtcore, qtgui

# software specific imports
import maya.cmds as cmds
import pymel.all as pm

# mca python imports
from mca.common.assetlist import assetlist
from mca.common.resources import resources
from mca.common.project import paths
from mca.common.pyqt import messages
from mca.common.utils import fileio

from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import mayawindows, maya_dialogs
from mca.mya.rigging import frag, joint_utils
from mca.mya.utils import dag_utils, naming, namespace_utils

from mca.common import log
logger = log.MCA_LOGGER

MISSING_ICON = resources.icon(r'color\question.png')

# Common misspellings due to skeleton mirrors.
NAMING_ERROR_LIST = ['rower', 'reg']
BLACKLIST_ATTRS = ['fragParent', 'fragRootJoint', 'noStaticAnim', 'noExport', 'SDK_Parent', 'driver_flag']

DEFAULT_COLOR = qtgui.QColor(1, 0, 0, 0)
NEGATIVE_COLOR = qtgui.QColor('#521424')
CONFLICT_COLOR = qtgui.QColor('#664D00')

DEFAULT_SKELETONS_PATH = os.path.join(paths.get_common_tools_path(), 'Skeleton Builder')
PREBUILT_SKELETONS_PATH = os.path.join(DEFAULT_SKELETONS_PATH, 'Prebuilt Skeletons')
SKELETON_PARTS = os.path.join(DEFAULT_SKELETONS_PATH, 'Skeleton Parts')

class SkeletonBuilder(mayawindows.MCAMayaWindow):
    _version = 2.0
    previous_sel = []

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'skeletonbuilderUI.ui')
        super().__init__(title='Skeleton Builder',
                         ui_path=ui_path,
                         version=SkeletonBuilder._version)
        

        self.root_joint = None
        self.ui.set_skeleton_root_pushButton.setStyleSheet("background-color: #fb8b23")

        self.entry = qtgui.QStandardItemModel()
        self.ui.archetype_skeleton_listView.setModel(self.entry)
        self.ui.archetype_skeleton_listView.setSpacing(2)
        self.ui.archetype_skeleton_listView.setIconSize(qtcore.QSize(64, 64))

        self.setup_signals()

        self.initialize_lists()

    class AssetItem(qtgui.QStandardItem):
        ASSET_ENTRY = None
        def __init__(self, asset_entry):
            super().__init__()
            self.ASSET_ENTRY = asset_entry

            self.setEditable(False)

            self.setText(asset_entry.asset_name)
            asset_icon = None
            if asset_entry.mesh_path:
                asset_icon_path = f'{asset_entry.mesh_path[:-3]}jpg'
                if os.path.exists(asset_icon_path):
                    asset_icon = qtgui.QIcon(asset_icon_path)
            self.setIcon(asset_icon or MISSING_ICON)

    class HierarchyJointItem(qtwidgets.QTreeWidgetItem):
        pynode = None
        joint_index = None
        def __init__(self, joint_node, joint_index):
            joint_name = naming.get_basename(joint_node)
            if joint_name.startswith('root'):
                joint_name = 'root'
            super().__init__([joint_name])

            self.pynode = joint_node
            self.joint_index = joint_index

        def select_joint(self):
            if self.pynode and pm.objExists(self.pynode):
                mods = cmds.getModifiers()
                if mods in [1,4,5]:
                    pm.select(self.pynode, add=True)
                else:
                    pm.select(self.pynode, add=False)

    def setup_signals(self):
        # build a rig tab
        self.ui.import_skeleton_pushButton.clicked.connect(self.import_skeleton_clicked)
        self.ui.add_new_entry_pushButton.clicked.connect(self.add_skeleton_clicked)
        self.ui.remove_skeleton_pushButton.clicked.connect(self.remove_skeleton_clicked)
        self.ui.add_a_joint_pushButton.clicked.connect(self.add_joint_clicked)
        self.ui.make_planar_pushButton.clicked.connect(self.make_planar_clicked)

        self.ui.prebuilt_skeleton_listWidget.itemDoubleClicked.connect(self.import_skeleton_clicked)
        self.ui.skeleton_parts_listWidget.itemDoubleClicked.connect(self.import_skeleton_clicked)
        self.ui.archetype_skeleton_listView.doubleClicked.connect(self.import_skeleton_clicked)

        # markup tab
        self.ui.set_skeleton_root_pushButton.clicked.connect(self._set_root_skeleton_clicked)

        self.ui.validate_skeleton_pushButton.clicked.connect(self.validate_skeleton)

        self.ui.skeleton_view_treeWidget.setColumnCount(2)
        self.ui.skeleton_view_treeWidget.setHeaderLabels(["Name", "Status"])
        self.ui.skeleton_view_treeWidget.setIndentation(7)

        self.ui.skeleton_view_treeWidget.clicked.connect(self._select_joint)
        self.ui.set_markup_pushButton.clicked.connect(self.set_markup_clicked)

        self.ui.export_skeleton_pushButton.clicked.connect(self.export_skeleton_clicked)

    def initialize_lists(self):
        """
        Collect all files for each list, and display them.

        """
        self.ui.prebuilt_skeleton_listWidget.clear()
        fileio.touch_path(os.path.join(PREBUILT_SKELETONS_PATH, ''))
        self.ui.prebuilt_skeleton_listWidget.addItems(os.listdir(PREBUILT_SKELETONS_PATH))

        self.ui.skeleton_parts_listWidget.clear()
        fileio.touch_path(os.path.join(SKELETON_PARTS, ''))
        self.ui.skeleton_parts_listWidget.addItems(os.listdir(SKELETON_PARTS))

        self.entry.clear()
        asset_registry = assetlist.get_registry()
        for asset_entry in [x for x in sorted(asset_registry.ASSET_ID_DICT.values(), key=lambda x: x.asset_name) if not x.asset_parent]:
            self.entry.appendRow(self.AssetItem(asset_entry))

        self.ui.skeleton_side_comboBox.clear()
        self.ui.skeleton_side_comboBox.addItems(joint_utils.SIDE_LIST)
            
    
    def _set_root_skeleton_clicked(self):
        selection = pm.selected()
        self.root_joint = None
        self.ui.set_skeleton_root_pushButton.setStyleSheet("background-color: #fb8b23")
        if not selection:
            return
        root_joint = dag_utils.get_absolute_parent(selection[0], node_type=pm.nt.Joint)
        if isinstance(root_joint, pm.nt.Joint):
            self.root_joint = root_joint
            self.ui.set_skeleton_root_pushButton.setStyleSheet("background-color: #1b4197")
            self.validate_skeleton()
            self.previous_sel = []

    def validate_skeleton(self):
        """
        From our registered skeleton check for a list of common errors then in place edit the treeview items to show status

        """
        if not self.root_joint or not pm.objExists(self.root_joint):
            return
        
        tree_selection = self.ui.skeleton_view_treeWidget.selectedItems()
        previous_selection = None
        if tree_selection:
            tree_selection = tree_selection[1:]+[tree_selection[0]]
            previous_selection = [x.pynode for x in tree_selection]

        skel_hierarchy = joint_utils.SkeletonHierarchy(self.root_joint, True)
        self.ui.skeleton_view_treeWidget.clear()

        self.item_node_dict = {}
        for index, joint_node in enumerate(skel_hierarchy.all_joints):
            parent_node = None
            if index:
                parent_node = joint_node.getParent()

            tree_item = self.HierarchyJointItem(joint_node, index)
            if parent_node and parent_node in self.item_node_dict:
                self.item_node_dict[parent_node].addChild(tree_item)
            else:
                self.ui.skeleton_view_treeWidget.insertTopLevelItem(0, tree_item)

            if joint_node not in self.item_node_dict:
                self.item_node_dict[joint_node] = tree_item

        header = self.ui.skeleton_view_treeWidget.header()
        header.setSectionResizeMode(qtwidgets.QHeaderView.ResizeToContents)

        if skel_hierarchy.invalid_joints:
            for index, error_type in enumerate(['mirror', 'typo', 'side', 'name', 'duplicates', 'scale', 'parent', 'bookend', 'skeleton', 'animated']):
                joints_list = skel_hierarchy.invalid_joints.get(error_type, [])
                for joint_node in joints_list:
                    tree_item = self.item_node_dict.get(joint_node)
                    if not tree_item:
                        continue
                    # A mirror is not a serious fault, all others are.
                    tree_item.setBackgroundColor(0, NEGATIVE_COLOR) if index > 1 else tree_item.setBackgroundColor(0, CONFLICT_COLOR)
                    conflict_text = tree_item.text(1)
                    if conflict_text and f'{error_type}' not in conflict_text:
                        tree_item.setText(1, f'{conflict_text}, {error_type}')
                    else:
                        tree_item.setText(1, f'{error_type}')
        self.ui.skeleton_view_treeWidget.expandAll()

        if previous_selection:
            tree_item_list = [self.item_node_dict.get(x) for x in previous_selection]
            for tree_item in tree_item_list:
                tree_item.setSelected(True)

    def _select_joint(self):
        """
        Select the joint represented by an entry in the treewidget.

        """
        tree_selection = self.ui.skeleton_view_treeWidget.selectedItems()
        if len(tree_selection) == 1:
            self.previous_sel = tree_selection
        else:
            if len(tree_selection) == len(self.previous_sel)+1:
                # We've added a single selection:
                self.previous_sel = self.previous_sel+[x for x in tree_selection if x not in self.previous_sel]
            elif len(tree_selection) == len(self.previous_sel)-1:
                # We've deselected one.
                self.previous_sel = [x for x in self.previous_sel if x in tree_selection]
            else:
                # We've shift selected a large group
                self.previous_sel = self.previous_sel + [x for x in sorted(tree_selection, key=lambda x: x.joint_index) if x not in self.previous_sel]

        if self.previous_sel:
            pm.select([x.pynode for x in self.previous_sel])

    @ma_decorators.keep_selection_decorator
    @ma_decorators.undo_decorator
    def set_markup_clicked(self):
        """
        Apply markup to the selected joints represented by the treewidget.

        """
        skel_region = self.ui.skeleton_region_lineEdit.text()
        skel_side = self.ui.skeleton_side_comboBox.currentText()
        tree_selection = self.previous_sel
        if tree_selection:
            joint_list = [x.pynode for x in tree_selection]
            joint_utils.set_markup(joint_list, skel_side, skel_region, self.ui.is_twist_checkBox.isChecked(),
                                                                       self.ui.is_null_checkBox.isChecked(),
                                                                       self.ui.is_animated_checkBox.isChecked())
            self.validate_skeleton()

    @ma_decorators.keep_namespace_decorator
    def import_skeleton_clicked(self, *args, **kwargs):
        """
        From the selected skeleton entry import merge that skeleton.

        """
        namespace_utils.set_namespace('')

        skeleton_path = None
        if self.ui.prebuilt_skeleton_listWidget.isVisible():
            selected_element = self.ui.prebuilt_skeleton_listWidget.currentItem()
            if selected_element:
                # We're importing a full fresh skel.
                skeleton_path = os.path.join(PREBUILT_SKELETONS_PATH, selected_element.text())
                joint_utils.import_merge_skeleton(skeleton_path, None)
        elif self.ui.skeleton_parts_listWidget.isVisible():
            selection = pm.selected()
            selected_element = self.ui.skeleton_parts_listWidget.currentItem()
            if selected_element:
                skeleton_path = os.path.join(SKELETON_PARTS, selected_element.text())
                root_joint = joint_utils.import_merge_skeleton(skeleton_path, None)
                if selection:
                    # Import and attach to a selection since we're dealing with a part.
                    # Maybe rename some stuff here? Reset markup?
                    # $TODO Make importing parts allow for renaming on the fly. Likely requrie a new format for .skel files maybe .skelpart or something
                    # Would also need to pass a string to do renames on the fly. Double bonus points for checking against the existing skeletal markup so someone doesn't double up.
                    # Bonus bonus is import/mirror here. Right now I'm going to punt on that and just let the user use Maya's internal mirror.
                    parent_node = selection[0]
                    children_nodes = root_joint.getChildren()
                    for x in children_nodes:
                        x.setParent(parent_node)
                        x.t.set([0,0,0])
                        x.r.set([0,0,0])
                    pm.delete(root_joint)
        elif self.ui.archetype_skeleton_listView.isVisible():
            list_ui = self.ui.archetype_skeleton_listView
            for index in list_ui.selectedIndexes():
                asset_entry = list_ui.model().itemFromIndex(index).ASSET_ENTRY
                skeleton_path = asset_entry.skeleton_path
                joint_utils.import_merge_skeleton(skeleton_path, None)
                break
    
    def add_skeleton_clicked(self):
        """
        Add a new entry to ther skeleton archetype registry

        """
        selection = pm.selected()
        if not selection or not isinstance(selection[0], pm.nt.Joint):
            return
        root_joint = dag_utils.get_absolute_parent(selection[0], pm.nt.Joint)

        is_part = False
        if root_joint != selection[0]:
            is_part = True

        skeleton_name = messages.text_prompt_message('Pick skeleton name', 'Please name this new skeleton addition.')
        if not skeleton_name:
            return
        file_name = f'{skeleton_name}.skl'
        
        if is_part:
            if file_name in os.listdir(SKELETON_PARTS):
                result = maya_dialogs.question_prompt('Overwrite Existing Skeleton?', f'A skeleton part with the name "{skeleton_name}" already exists, would you like to overwrite it?')
                if result != 'Yes':
                    return
            part_copy = pm.duplicate(selection[0])
            part_copy.setParent(None)
            part_copy.rename(naming.get_basename(selection[0]))
            new_root = pm.joint('root')
            part_copy.setParent(new_root)
            joint_utils.export_skeleton(new_root, os.path.join(SKELETON_PARTS, file_name))
        else:
            if file_name in os.listdir(PREBUILT_SKELETONS_PATH):
                result = maya_dialogs.question_prompt('Overwrite Existing Skeleton?', f'A skeleton with the name "{skeleton_name}" already exists, would you like to overwrite it?')
                if result != 'Yes':
                    return
            joint_utils.export_skeleton(root_joint, os.path.join(PREBUILT_SKELETONS_PATH, file_name))
        self.initialize_lists()

    def remove_skeleton_clicked(self):
        skeleton_path = None
        if self.ui.prebuilt_skeleton_listWidget.isVisible():
            # We're removing a full skeleton
            selected_element = self.ui.prebuilt_skeleton_listWidget.currentItem()
            if selected_element:
                skeleton_path = os.path.join(PREBUILT_SKELETONS_PATH, selected_element.text())

        elif self.ui.skeleton_parts_listWidget.isVisible():
            # We're removing a skeleton part.
            selected_element = self.ui.skeleton_parts_listWidget.currentItem()
            if selected_element:
                skeleton_path = os.path.join(SKELETON_PARTS, selected_element.text())

        if skeleton_path:
            skeleton_name = os.path.basename(skeleton_path).split('.')[0]
            result = maya_dialogs.question_prompt('Remove Skeleton', f'Are you sure you want to remove the skeleton "{skeleton_name}"')
            if result != 'Yes':
                return
            
            fileio.touch_path(skeleton_path, True)
        self.initialize_lists()
    
    @ma_decorators.keep_namespace_decorator
    def add_joint_clicked(self):
        selection = pm.selected()
        if selection:
            namespace_utils.set_namespace(selection[0].namespace())
        else:
            namespace_utils.set_namespace('')
        cmds.select(None)
        new_joint = pm.joint()
        if selection and isinstance(selection[0], pm.nt.Joint):
            new_joint.setParent(selection[0])
            new_joint.t.set([0,0,0])
            new_joint.r.set([0,0,0])

    def make_planar_clicked(self):
        selection = pm.selected()
        if len(selection) == 3:
            planar_chain = joint_utils.make_planar_chain(selection)
            for joint_node, planar_node in zip(selection, planar_chain):
                joint_children = joint_node.getChildren()
                if joint_children:
                    pm.parent(joint_children, None)
                pm.delete(pm.parentConstraint(planar_node, joint_node))
                if joint_children:
                    pm.parent(joint_children, joint_node)
            pm.makeIdentity(selection, apply=True, t=0, r=1, s=0, n=0)
            pm.delete(planar_chain)
        else:
            maya_dialogs.error_prompt('Selection Error', 'Exactly 3 objects must be selected to make them planar.')
    
    @ma_decorators.keep_selection_decorator
    def export_skeleton_clicked(self):
        """
        From the selected skeleton check the asset_id and export to the associated .skl file.

        """
        selection = pm.selected()
        if not selection:
            logger.error('Select a joint to continue')
            maya_dialogs.error_prompt('Selection Error', 'Select a joint to continue.')
            return
        
        root_joint = dag_utils.get_absolute_parent(selection[0], pm.nt.Joint)
        if not root_joint or not isinstance(root_joint, pm.nt.Joint):
            logger.error('Unable to find a valid root from selection')
            maya_dialogs.error_prompt('Selection Error', 'Unable to find a valid root from selection.')
            return

        skeleton_path = None
        if root_joint.hasAttr('skeleton_path'):
            skeleton_path = root_joint.getAttr('skeleton_path')

        if not skeleton_path:
            skeleton_path, _ = qtwidgets.QFileDialog.getSaveFileName(None, 'Select Skel', paths.get_art_characters_path()+'\\', 'Skeleton (*.skl)')

        if not skeleton_path:
            return
        
        joint_utils.export_skeleton(root_joint, skeleton_path)
