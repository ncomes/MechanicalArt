#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Helios main UI.
"""

# System global imports
import os
# PySide2 imports
from PySide2 import QtWidgets, QtGui
# software specific imports
import pymel.all as pm
# mca python imports
from mca.common import log
from mca.common.assetlist import assetlist
from mca.common.modifiers import decorators
from mca.common.paths import path_utils
from mca.common.utils import fileio, lists, process, pymaths
from mca.common.tools.dcctracking import dcc_tracking

from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import mayawindows, dialogs
from mca.mya.rigging import chain_markup, rig_utils, skel_utils
from mca.mya.utils import dag, naming

from mca.mya.tools.skeletonbuilder import skeletonbuilder_registry

logger = log.MCA_LOGGER

# Common misspellings due to skeleton mirrors.
NAMING_ERROR_LIST = ['rower', 'reg']
BLACKLIST_ATTRS = ['fragParent', 'fragRootJoint', 'noStaticAnim', 'noExport', 'SDK_Parent', 'driver_flag']

DEFAULT_COLOR = QtGui.QColor(1, 0, 0, 0)
NEGATIVE_COLOR = QtGui.QColor('#521424')
CONFLICT_COLOR = QtGui.QColor('#664D00')


class SkeletonBuilder(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'skeletonbuilderUI.ui')
        super().__init__(title='Skeleton Builder',
                         ui_path=ui_path,
                         version=SkeletonBuilder.VERSION)
        

        self.item_name_dict = {}
        self._root_joint = None
        self.setup_signals()

        self.setup_treeview()
        self.setup_listview()

    def setup_signals(self):

        self.ui.validate_treeWidget.setColumnCount(2)
        self.ui.validate_treeWidget.setHeaderLabels(["Name", "Status"])
        self.ui.validate_treeWidget.setIndentation(7)

        self.ui.validate_treeWidget.clicked.connect(self.select_item)
        self.ui.validate_pushButton.clicked.connect(self.validate_skeleton)

        self.ui.apply_markup_pushButton.clicked.connect(self.apply_markup)

        self.ui.add_archetype_pushButton.clicked.connect(self.add_skeleton_entry)
        self.ui.remove_archetype_pushButton.clicked.connect(self.remove_skeleton_entry)

        self.ui.import_archetype_pushButton.clicked.connect(self.import_skeleton)
        self.ui.export_skeleton_pushButton.clicked.connect(self.export_skeleton)

    def setup_treeview(self):
        """
        Setup our main treeview widget in the UI. This checks through a selected hierarchy and registers each joint to
        an item in the treeview widget.

        """
        selection = lists.get_first_in_list(pm.selected())
        if not selection:
            return

        hierarchy_root = dag.get_absolute_parent(selection, node_type=pm.nt.Joint)

        if not isinstance(hierarchy_root, pm.nt.Joint):
            return

        self._root_joint = hierarchy_root

        self.ui.validate_treeWidget.clear()
        skel_hierarchy = chain_markup.ChainMarkup(self._root_joint)

        self.item_name_dict = {}
        for index, joint_node in enumerate(skel_hierarchy.joints):
            joint_name = 'root'
            parent_name = None
            if index:
                joint_name = naming.get_basename(joint_node)
                parent_name = naming.get_basename(joint_node.getParent())

            tree_item = QtWidgets.QTreeWidgetItem([joint_name])
            if parent_name:
                self.item_name_dict[parent_name][0].addChild(tree_item)
            else:
                self.ui.validate_treeWidget.insertTopLevelItem(0, tree_item)

            if joint_name not in self.item_name_dict:
                self.item_name_dict[joint_name] = [tree_item, joint_node]
            else:
                logger.warning(f'rename {joint_name} a joint has already been registered with this name.')
                return

        header = self.ui.validate_treeWidget.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.ui.validate_treeWidget.expandAll()
        self.validate_skeleton()

    def setup_listview(self):
        """
        From the skeleton archetype registry display all entries.

        """
        self.ui.archetype_listWidget.clear()

        # Pull our list of skeleton archetypes.
        skeleton_registry = skeletonbuilder_registry.SkeletonArchetypeRegistry()
        skeleton_registry.reload(force=True)
        for skel_name in skeleton_registry.REGISTRY_DICT:
            self.ui.archetype_listWidget.addItem(skel_name)

    @decorators.track_fnc
    def validate_skeleton(self):
        """
        From our registered skeleton check for a list of common errors then in place edit the treeview items to show status

        """
        if not self.item_name_dict or not self.item_name_dict['root'][-1].exists():
            self.setup_treeview()
            return

        skel_hierarchy = chain_markup.ChainMarkup(self.item_name_dict['root'][-1])

        if len(self.item_name_dict) != len(skel_hierarchy.joints):
            pm.select(skel_hierarchy.root)
            self.setup_treeview()
            return

        validation_markup_dict = {}
        # Make sure our root has space for the asset_id of this skel.
        if not skel_hierarchy.root.hasAttr('asset_id'):
            skel_hierarchy.root.addAttr('asset_id', dt='string')

        for joint_name, (tree_item, joint_node) in self.item_name_dict.items():
            if not joint_node.exists() or (joint_name != 'root' and naming.get_basename(joint_node) != joint_name):
                pm.select(self._root_joint)
                self.setup_treeview()
                return

            # Reset item look.
            tree_item.setBackgroundColor(0, DEFAULT_COLOR)
            tree_item.setText(1, '')

            wrapped_joint = chain_markup.JointMarkup(joint_node)
            joint_region = wrapped_joint.region
            joint_side = wrapped_joint.side
            chain_twist = wrapped_joint.chainTwist
            chain_start = wrapped_joint.chainStart
            chain_end = wrapped_joint.chainEnd

            error_str = tree_item.text(1)
            error_color = DEFAULT_COLOR

            # Purge attrs that fuck with other systems.
            for attr_name in BLACKLIST_ATTRS:
                if joint_node.hasAttr(attr_name):
                    pm.deleteAttr(joint_node, at=attr_name)

            # Check for missing markup
            if not joint_region or not joint_side:
                if 'Missing Markup' not in error_str:
                    error_str += 'Missing Markup. '
                tree_item.setBackground(0, NEGATIVE_COLOR)
                tree_item.setText(1, error_str)
                # Hit the next joint we can't do any other lookups if we're missing markup.
                continue

            if joint_region not in validation_markup_dict:
                validation_markup_dict[joint_region] = {}

            if joint_side not in validation_markup_dict[joint_region]:
                validation_markup_dict[joint_region][joint_side] = {'joints': []}

            # Check for chain start
            chain_dict = validation_markup_dict[joint_region][joint_side]
            if chain_start:
                if 'chain_start' not in chain_dict:
                    if chain_start == joint_region:
                        chain_dict['chain_start'] = joint_name
                    else:
                        error_str += 'Region Mismatch. '
                        error_color = NEGATIVE_COLOR
                else:
                    error_str += 'Duplicate Start. '
                    error_color = NEGATIVE_COLOR
                    conflict_item = self.item_name_dict[chain_dict['chain_start']][0]
                    conflict_text = conflict_item.text(1)
                    if conflict_text and 'Duplicate Start. ' not in conflict_text:
                        conflict_item.setText(1, f'{conflict_text}Duplicate Start. ')
                    else:
                        conflict_item.setBackground(0, NEGATIVE_COLOR)
                        conflict_item.setText(1, 'Duplicate Start. ')


            # Check for chain end
            if chain_end:
                if not chain_dict.get('chain_start'):
                    error_str += 'No Region Start. '
                    error_color = NEGATIVE_COLOR
                elif chain_dict.get('chain_end'):
                    error_str += 'Duplicate End. '
                    error_color = NEGATIVE_COLOR
                    conflict_item = self.item_name_dict[chain_dict['chain_end']][0]
                    conflict_text = conflict_item.text(1)
                    if conflict_text and 'Duplicate End. ' not in conflict_text:
                        conflict_item.setText(1, f'{conflict_text}Duplicate End. ')
                    else:
                        conflict_item.setBackground(0, NEGATIVE_COLOR)
                        conflict_item.setText(1, 'Duplicate End. ')
                else:
                    if chain_end == joint_region and 'chain_end' not in chain_dict:
                        chain_dict['chain_end'] = joint_name
                    elif chain_end in validation_markup_dict:
                        if 'chain_end' not in validation_markup_dict[chain_end][joint_side]:
                            validation_markup_dict[chain_end][joint_side]['chain_end'] = joint_name

            # Check if joint has a registered chain start.
            chain_start_joint = skel_hierarchy.skeleton_dict.get(chain_dict.get('chain_start'))
            all_parents_list = dag.get_all_parents(joint_node, pm.nt.Joint)
            joint_parent = joint_node.getParent()

            if not chain_start_joint and not chain_twist:
                error_str += 'Invalid Chain. '
                error_color = NEGATIVE_COLOR

            if chain_twist:
                if not chain_dict.get('parent'):
                    chain_dict['parent'] = joint_parent

            # check if we're animation exportable, but our parent is not.
            if joint_parent:
                if joint_node.hasAttr('animationExport'):
                    if joint_parent.hasAttr('animationExport'):
                        if joint_node.getAttr('animationExport') and not joint_parent.getAttr('animationExport'):
                            error_str += 'Parent not animation exportable. '
                            error_color = CONFLICT_COLOR

                # check if we're skel exportable, but our parent is not.
                if joint_node.hasAttr('skExport'):
                    if joint_parent.hasAttr('skExport'):
                        if joint_node.getAttr('skExport') and not joint_parent.getAttr('skExport'):
                            error_str += 'Parent not skel exportable. '
                            error_color = NEGATIVE_COLOR

            # Check if chain start is in the parent structure.
            # Or if we've a chain twist joint with same markup but different parent.
            # If not we've duplicate markup with non shared parents.
            if (chain_start_joint and joint_node != chain_start_joint and chain_start_joint not in all_parents_list) or (chain_twist and joint_parent != chain_dict.get('parent')) and 'leaf' not in joint_name:
                error_str += 'Duplicate Markup. '
                error_color = NEGATIVE_COLOR
                for conflict_joint_name in chain_dict['joints']:
                    conflict_item = self.item_name_dict[conflict_joint_name][0]
                    conflict_text = conflict_item.text(1)
                    if conflict_text and 'Duplicate Markup. ' not in conflict_text:
                        conflict_item.setText(1, f'{conflict_text}Duplicate Markup. ')
                    else:
                        conflict_item.setText(1, f'Duplicate Markup. ')
                    conflict_item.setBackground(0, NEGATIVE_COLOR)


            # Check Mirror
            rev_joint_name = joint_name
            if '_l_' in joint_name:
                rev_joint_name = joint_name.replace('_l_', '_r_')
            elif joint_name.endswith('_l'):
                rev_joint_name = joint_name[:-2] + '_r'
            elif '_r_' in joint_name:
                rev_joint_name = joint_name.replace('_r_', '_l_')
            elif joint_name.endswith('_r'):
                rev_joint_name = joint_name[:-2] + '_l'

            if rev_joint_name != joint_name:
                rev_joint = skel_hierarchy.skeleton_dict.get(rev_joint_name)
                if rev_joint:
                    joint_distance = pymaths.find_vector_length(pm.xform(joint_node, q=True, ws=True, t=True))
                    rev_joint_distance = pymaths.find_vector_length(pm.xform(rev_joint, q=True, ws=True, t=True))
                    if not abs(joint_distance - rev_joint_distance) < .01:
                        error_str += 'Not Mirrored. '
                        if error_color != NEGATIVE_COLOR:
                            error_color = CONFLICT_COLOR

                        if rev_joint_name not in self.item_name_dict:
                            pm.select(self._root_joint)
                            self.setup_treeview()
                            return

                        conflict_item = self.item_name_dict[rev_joint_name][0]
                        conflict_text = conflict_item.text(1)
                        if conflict_text and 'Not Mirrored. ' not in conflict_text:
                            conflict_item.setText(1, f'{conflict_text}Not Mirrored. ')
                        else:
                            conflict_item.setBackground(0, CONFLICT_COLOR)
                            conflict_item.setText(1, 'Not Mirrored. ')

            # Check for naming errors
            if any(True if x in joint_name else False for x in NAMING_ERROR_LIST):
                error_str += 'Check Name. '
                if error_color != NEGATIVE_COLOR:
                    error_color = CONFLICT_COLOR

            chain_dict['joints'].append(joint_name)

            if error_str:
                # Apply all errors found and markup with color.
                tree_item.setText(1, error_str)
                tree_item.setBackgroundColor(0, error_color)

        for joint_region, side_dict in validation_markup_dict.items():
            # Check back over all entries if any are missing a chain end or a chain start that entire chain is invalid.
            # We should have already caught all chain starts, but this gets us our chain ends as well.
            for joint_side, data_dict in side_dict.items():
                if not data_dict.get('parent') and (not (data_dict.get('chain_end') or not data_dict.get('chain_start'))):
                    for joint_name in data_dict.get('joints', []):
                        tree_item = self.item_name_dict[joint_name][0]
                        tree_item.setBackgroundColor(0, NEGATIVE_COLOR)
                        conflict_text = tree_item.text(1)
                        if conflict_text and 'Invalid Chain. ' not in conflict_text:
                            tree_item.setText(1, f'{conflict_text}Invalid Chain. ')
                        else:
                            tree_item.setText(1, f'Invalid Chain. ')

    def select_item(self):
        """
        Select the joint represented by an entry in the treewidget.

        """
        tree_item = self.ui.validate_treeWidget.selectedItems()[0]
        joint_name = tree_item.text(0)
        joint_node = self.item_name_dict[joint_name][1]
        pm.select(joint_node)

    @ma_decorators.keep_selection_decorator
    @decorators.track_fnc
    def apply_markup(self):
        """
        Apply markup to the selected joints represented by the treewidget.

        """
        skel_region = self.ui.region_label_lineEdit.text()
        skel_side = self.ui.side_label_lineEdit.text()

        logger.debug(f'region:{skel_region}, side:{skel_side}')
        node_list = []
        if skel_region or skel_side:
            for item in self.ui.validate_treeWidget.selectedItems():
                node_list.append(self.item_name_dict[item.text(0)][1])
            apply_markup_cmd(node_list, skel_region, skel_side, self.ui.is_twist_checkBox.isChecked(),
                                                                self.ui.exportable_checkBox.isChecked(),
                                                                self.ui.animatable_checkBox.isChecked())

        pm.select(self._root_joint)
        self.validate_skeleton()

    @decorators.track_fnc
    def import_skeleton(self):
        """
        From the selected skeleton entry import merge that skeleton.

        """
        selected_skel = lists.get_first_in_list(self.ui.archetype_listWidget.selectedItems())
        skel_name = selected_skel.text()
        skeleton_registry = skeletonbuilder_registry.SkeletonArchetypeRegistry()
        skel_entry = skeleton_registry.get_entry(skel_name)

        skel_path = skel_entry.skel_path
        if not os.path.exists(skel_path):
            dialogs.info_prompt(title='Missing File', text=f'{skel_path} was not found on disk, verify the file exists.')
            logger.warning(f'{skel_path} was not found on disk, verify the file exists.')
            return

        root_joint = skel_utils.import_merge_skeleton(skel_path, lists.get_first_in_list(pm.selected()))

    @ma_decorators.keep_selection_decorator
    @decorators.track_fnc
    def export_skeleton(self):
        """
        From the registered skeleton check the asset_id and export to the associated .skl file.

        """
        if not self._root_joint.exists():
            dialogs.info_prompt(title='Reload Skeleton', text='Validate a new skeleton, the registered root was not found.')
            logger.warning('Validate a new skeleton, the registered root was not found.')
            return
        pm.select(self._root_joint)
        asset_id = self._root_joint.getAttr('asset_id')
        if not asset_id:
            dialogs.info_prompt(title='Set Asset ID', text='Set a valid Asset ID. The current Asset ID is empty.')
            logger.warning('Set a valid Asset ID. The current Asset ID is empty.')
            return

        if asset_id.endswith('.skl'):
            skel_path = path_utils.to_full_path(asset_id)
        else:
            skel_path = rig_utils.get_asset_skeleton(asset_id)
            if not skel_path:
                dialogs.info_prompt(title='Lookup Failed', text=f'Verify Asset ID "{asset_id}" is registered, we were unable to lookup the skel path.')
                logger.warning(f'Verify Asset ID "{asset_id}" is registered, we were unable to lookup the skel path.')
                return

        fileio.touch_path(skel_path)
        skel_utils.export_skeleton(skel_path, self._root_joint)

    @decorators.track_fnc
    def add_skeleton_entry(self):
        """
        Add a new entry to ther skeleton archetype registry

        """

        if not self._root_joint.exists():
            dialogs.info_prompt(title='Reload Skeleton', text='Validate a new skeleton, the registered root was not found.')
            logger.warning('Validate a new skeleton, the registered root was not found.')
            return

        asset_id = self._root_joint.getAttr('asset_id')
        if not asset_id:
            dialogs.info_prompt(title='Set Asset ID', text='Set a valid Asset ID. The current Asset ID is empty.')
            logger.warning('Set a valid Asset ID. The current Asset ID is empty.')
            return

        mca_asset = assetlist.get_asset_by_id(asset_id)
        if not mca_asset:
            dialogs.info_prompt(title='Lookup Failed', text=f'Verify Asset ID "{asset_id}" is registered, we were unable to lookup the skel path.')
            logger.warning(f'Verify Asset ID "{asset_id}" is registered, we were unable to lookup the skel path.')
            return

        skel_name = mca_asset.asset_name
        skel_path = rig_utils.get_asset_skeleton(asset_id)
        skeleton_registry = skeletonbuilder_registry.SkeletonArchetypeRegistry()
        skeleton_registry.register_archetype(skeletonbuilder_registry.SkeletonArchetype({'name': skel_name, 'skel_path': skel_path}), commit=True)
        self.setup_listview()

    @decorators.track_fnc
    def remove_skeleton_entry(self):
        """
        From the selected skeleton entry remove it from the registry.

        """
        selected_skel = lists.get_first_in_list(self.ui.archetype_listWidget.selectedItems())
        skel_name = selected_skel.text()
        skeleton_registry = skeletonbuilder_registry.SkeletonArchetypeRegistry()
        skeleton_registry.remove_entry(skel_name, commit=True)
        self.setup_listview()



@ma_decorators.keep_selection_decorator
def apply_markup_cmd(node_list, skel_region, skel_side, is_twist=False, sk_exportable=True, animatable=True):
    """
    From a list of ORDERED joints, apply Frag markup for us to traverse the skeleton.

    :param list[Joint] node_list: A list of joint nodes in hierarchical order.
    :param str skel_region: The name of the skeletal region. IE: "leg", "arm"
    :param str skel_side: The name of the skeleton side. IE: "right", "left", "center"
    :param bool is_twist: If this joint should be marked up as a twist joint.
    :param bool sk_exportable: If this joint should be exported as part of the SK.
    :param bool animatable: If this joint should be marked up for animation export.
    """
    node_list = node_list or pm.selected()
    for index, x in enumerate(node_list):
        wrapped_joint = chain_markup.JointMarkup(x)

        wrapped_joint.is_sk_export = sk_exportable
        wrapped_joint.is_animation_export = animatable

        if 'null' in wrapped_joint.name:
            # Null joints can neither have animation nor should they be exported.
            wrapped_joint.is_sk_export = False
            wrapped_joint.is_animation_export = False

        if index:
            # If our joint has a chain start that matches the region markup we're using, but is not
            # the first joint, delete that markup
            if wrapped_joint.chainStart == skel_region:
                wrapped_joint.node.chainStart.delete()

        if is_twist:
            if skel_region:
                wrapped_joint.chainTwist = skel_region
            # Twist joints cannot accept animation, but they should be part of the primary skeleton.
            wrapped_joint.is_sk_export = True
            wrapped_joint.is_animation_export = False

        if not index and not is_twist:
            # Only the first joint should get chainStart markup
            if skel_region:
                wrapped_joint.chainStart = skel_region

        if skel_side:
            wrapped_joint.side = skel_side

        if skel_region:
            wrapped_joint.region = skel_region

        if index + 1 == len(node_list) and not is_twist:
            # Only the last joint should get chainEnd markup
            if skel_region:
                wrapped_joint.chainEnd = skel_region
        else:
            # If we have a joint that is not the last joint, and it has chainEnd markup
            # delete that attribute.
            if wrapped_joint.chainEnd == skel_region:
                wrapped_joint.node.chainEnd.delete()
