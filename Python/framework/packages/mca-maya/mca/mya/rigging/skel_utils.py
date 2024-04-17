#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Maya Skeleton functions
"""

# System global imports
import os
import re
# software specific imports
import pymel.core as pm
import maya.cmds as cmds
#  python imports
from mca.common import log
from mca.common.textio import jsonio
from mca.common.paths import path_utils
from mca.common.utils import fileio, lists, strings
from mca.common.resources import resources
from mca.mya.utils import naming, dag, maya_utils, attr_utils, node_util
from mca.mya.rigging import chain_markup
from mca.mya.modifiers import ma_decorators


logger = log.MCA_LOGGER


SKIP_USER_ATTRIBUTES = ['lockInfluenceWeights', 'filmboxTypeID']


def create_skeleton_dict(root_joint):
    """
    Creates a name to object dictionary of the skeleton hierarchy. This is useful for making maps between skeletons.

    :return: A dictionary of absolute string names to the joint itself.
    :rtype dict{}:
    """

    skel_dict = {}
    for index, joint_node in enumerate([root_joint] + pm.listRelatives(root_joint, ad=True, type=pm.nt.Joint)):
        if not index:
            joint_name = 'root'
        else:
            joint_name = naming.get_basename(joint_node)
        skel_dict[joint_name] = joint_node
    return skel_dict


def import_skeleton(skl_path, set_radius=True):
    """
    From a .skl file import and build a serialized skeleton.

    :param str skl_path: Path to a given skl file.
    :param bool set_radius: Set the joint radi based on a global skeleton scale.
    :return: The root joint of the created skeleton
    :rtype: Joint
    """

    if skl_path.endswith('.skl'):
        skl_path = skl_path.replace('.skl', '')

    skel_root = SkeletonData(skl_path).import_data()

    if set_radius:
        scale_skel_radi(skel_root)

    return skel_root


def create_and_merge_skeletons_from_data(root_joint, skeleton_data_dict):
    """
    By name find shared parents and merge importable skeletons.

    :param Joint root_joint: The root joint of the hierarchy.
    :param dict skeleton_data_dict: The serialized skeleton dict.
    :return: The root joint of the imported hierarchy.
    :rtype: Joint
    """

    existing_hierarchy = None
    if root_joint and isinstance(root_joint, pm.nt.Joint):
        existing_hierarchy = chain_markup.ChainMarkup(root_joint)

    if not existing_hierarchy:
        logger.info(f'No existing skeleton found, importing skel instead.')
        return create_skeleton_from_data(skeleton_data_dict)

    hierarchy_start = existing_hierarchy.hierarchyStart

    skeleton_dict = {}
    for joint_name, joint_data_dict in skeleton_data_dict.items():
        if joint_name not in existing_hierarchy.skeleton_dict:
            new_joint = _create_serialized_joint(joint_name, joint_data_dict)
            skeleton_dict[joint_name] = new_joint

    for joint_name, joint_node in skeleton_dict.items():
        parent_name = skeleton_data_dict.get(joint_name, {}).get('parent_node', None)
        if parent_name in skeleton_dict:
            joint_node.setParent(skeleton_dict[parent_name])
        elif parent_name in existing_hierarchy.skeleton_dict:
            joint_node.setParent(existing_hierarchy.skeleton_dict[parent_name])
        else:
            joint_node.setParent(hierarchy_start) if hierarchy_start else joint_node.setParent(root_joint)

    return root_joint


def import_merge_skeleton(skl_path, root_joint, set_radius=True):
    """
    From a .skl file import and merge unique nodes with an existing hierarchy.

    :param str skl_path: Path to a given skl file.
    :param Joint root_joint: Root joint of an existing hierarchy. If None is passed the skeleton will be completed created from the skl.
    :param bool set_radius: Set the joint radi based on a global skeleton scale.
    :return: The root joint of the merged skeleton.
    :rtype: Joint
    """

    if skl_path.endswith('.skl'):
        skl_path = skl_path.replace('.skl', '')

    imported_skeleton_data_dict = SkeletonData(skl_path).read_data()

    skel_root = create_and_merge_skeletons_from_data(root_joint, imported_skeleton_data_dict)

    if set_radius:
        scale_skel_radi(skel_root)

    return skel_root


def scale_skel_radi(skel_root):
    """
    Set the joint radi for each joint based on a global scaling value.

    :param Joint skel_root: The root joint of the skeleton.
    """
    skel_bb = pm.xform(skel_root, q=True, bb=True)
    skel_size = sum(skel_bb[3:])
    skel_scale = skel_size / 125.0

    for index, x in enumerate(pm.listRelatives(skel_root, ad=True, type=pm.nt.Joint)):
        sca_mod = 1.0 - (.05 * len(dag.get_all_parents(x, node_type=pm.nt.Joint)))
        sca_mod = .4 if sca_mod < .4 else sca_mod
        x.radius.set(skel_scale*sca_mod)


def export_skeleton(skl_path, root_joint):
    """
    Serialize a joint hierarchy and save it to a .skl file.

    :param str skl_path: Path to a given skl file.
    :param Joint root_joint: Root joint the hierarchy to export.
    :return: Whether the action was completed successfully.
    :rtype: Bool
    """

    if skl_path.endswith('.skl'):
        skl_path = skl_path.replace('.skl', '')

    skeleton_data_dict = serialize_skeleton(root_joint)
    fileio.touch_path(skl_path)
    return SkeletonData(skl_path).save_data(skeleton_data_dict)


def serialize_skeleton(root_joint):
    """
    Function that returns dictionary with all skeleton data information.

    :param Joint root_joint: The root joint of the hierarchy.
    :return: A list of dictionaries representing each joint in the hierarchy.
    :rtype: dict
    """

    if not root_joint or not isinstance(root_joint, pm.nt.Joint):
        # early out if we're not given a root or a joint root.
        logger.warning(f'Skeleton root {root_joint} is not a valid root.')
        return

    joint_node_list = pm.listRelatives(root_joint, allDescendents=True, fullPath=True, type=pm.nt.Joint) or list()
    if not joint_node_list:
        logger.warning(f'This skeleton contains no sub joints.')
        return
    joint_node_list = [root_joint] + joint_node_list

    skeleton_data_dict = {}
    for index, joint_node in enumerate(joint_node_list):
        joint_data_dict = {}

        wrapped_joint_node = chain_markup.JointMarkup(joint_node)
        node_name = wrapped_joint_node.name

        joint_data_dict['world_matrix'] = wrapped_joint_node.get_world_matrix()
        wrapped_parent_node = wrapped_joint_node.getParent()
        if wrapped_parent_node and isinstance(wrapped_parent_node, (pm.nt.Joint, chain_markup.JointMarkup)):
            joint_data_dict['parent_node'] = wrapped_parent_node.name if wrapped_parent_node else None
        else:
            joint_data_dict['parent_node'] = None
        joint_data_dict['draw_label'] = joint_node.drawLabel.get()
        user_attributes = pm.listAttr(joint_node, userDefined=True)
        for user_attribute_name in user_attributes:
            if user_attribute_name in SKIP_USER_ATTRIBUTES:
                continue
            joint_data_dict.setdefault('attributes', list())
            joint_data_dict['attributes'].append(attr_utils.serialize_attribute(pm.PyNode(joint_node).attr(user_attribute_name)))

        skeleton_data_dict[node_name] = joint_data_dict
    if not skeleton_data_dict:
        logger.warning('No skeleton data found!')

    return skeleton_data_dict


def _create_serialized_joint(joint_name, joint_data_dict):
    """
    Utility function for creating a joint based on serialized dict.

    :param joint_name:
    :param joint_data_dict:
    :return:
    """

    cmds.select(None)
    new_joint = pm.joint(n=joint_name)
    import_namespace = new_joint.namespace()
    if naming.get_basename(new_joint) != joint_name:
        existing_joint = lists.get_first_in_list(pm.ls(joint_name))
        if existing_joint:
            existing_joint.rename(f'{joint_name}1')
        new_joint.rename(f'{import_namespace}:{joint_name}' if import_namespace else joint_name)
    wrapped_joint = chain_markup.JointMarkup(new_joint)
    new_joint.drawLabel.set(joint_data_dict.get('draw_label', False))
    new_joint.radius.set(joint_data_dict.get('radius', 1.0))
    joint_world_matrix = joint_data_dict.get('world_matrix', [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0])
    pm.xform(new_joint, matrix=joint_world_matrix, worldSpace=True)
    new_joint.scale.set([1, 1, 1])

    attributes = joint_data_dict.get('attributes', list())
    for attribute_data in attributes:
        node_util.add_attribute(new_joint, **attribute_data)
    return new_joint


@ma_decorators.keep_selection_decorator
def create_skeleton_from_data(skeleton_data_dict):
    """
    Creates a new skeleton from the given data and with the given positional and keyword arguments.

    :param dict skeleton_data_dict: A list containing the serialized information of a given joint.
    :return: The root joint of the imported hierarchy.
    :rtype: Joint
    """

    skeleton_dict = {}
    for joint_name, joint_data_dict in skeleton_data_dict.items():
        new_joint = _create_serialized_joint(joint_name, joint_data_dict)
        skeleton_dict[joint_name] = new_joint

    root_joint = None
    for joint_name, joint_node in skeleton_dict.items():
        parent_name = skeleton_data_dict.get(joint_name, {}).get('parent_node', None)
        if parent_name:
            joint_node.setParent(skeleton_dict[parent_name])
        else:
            root_joint = joint_node

    if root_joint:
        pm.makeIdentity(root_joint, apply=True, t=True, r=True, s=True, n=False, pn=True)

    return root_joint


def restore_skeleton_markup_from_data(root_joint, skeleton_data_dict):
    """
    From serialized skeleton data, re-apply markup.

    :param Joint root_joint: The root joint of the hierarchy.
    :param dict skeleton_data_dict: The serialized skeleton dict.
    """

    for joint_node in pm.listRelatives(root_joint, ad=True, type=pm.nt.Joint) + [root_joint]:
        wrapped_joint = chain_markup.JointMarkup(joint_node)

        joint_data_dict = skeleton_data_dict.get('root', {}) if joint_node == root_joint else skeleton_data_dict.get(wrapped_joint.name, {})

        if not joint_data_dict:
            logger.warning(f"Unable to find lookup for joint {naming.get_basename(joint_node)}")
            continue

        joint_node.setAttr('drawLabel', joint_data_dict.get('draw_label', False))
        joint_node.setAttr('radius', joint_data_dict.get('radius', 1.0))

        # purge existing attrs, sometimes we end up with garbage data here.
        for attr in joint_node.listAttr(ud=True):
            if attr.exists():
                attr.delete()

        attributes = joint_data_dict.get('attributes', list())
        for attribute_data in attributes:
            node_util.add_attribute(joint_node, **attribute_data)


def _return_child_joints_to_bind(root_joint, skeleton_data_dict, start=True):
    """
    From serialized skeleton data return a skeleton to its bind pose.

    :param Joint root_joint: The root joint of the hierarchy.
    :param dict skeleton_data_dict: The serialized skeleton dict.
    :param bool start: If this is our first run. We'll check to see if the dict has 'root' and set that first.
    """

    if not isinstance(root_joint, pm.nt.Joint):
        if start:
            logger.warning(f'Skeleton root {root_joint} is not a valid root.')
        else:
            logger.debug(f'Child {root_joint} is not a joint and will be skipped.')
        return

    if start:
        # Not using a name match here in case we've got a duplicat hierarchy.
        if 'root' in skeleton_data_dict:
            joint_name = 'root'
            joint_world_matrix = skeleton_data_dict.get(joint_name, {}).get(
                'world_matrix',
                [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0])
            pm.xform(root_joint, matrix=joint_world_matrix, worldSpace=True)

    for child_joint in root_joint.getChildren(type=pm.nt.Joint):
        joint_name = naming.get_basename(child_joint)
        if joint_name in skeleton_data_dict:
            joint_world_matrix = skeleton_data_dict.get(joint_name, {}).get(
                'world_matrix',
                [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0])
            pm.xform(child_joint, matrix=joint_world_matrix, worldSpace=True)

        _return_child_joints_to_bind(child_joint, skeleton_data_dict, False)


def return_skeleton_to_bind_pose_from_data(root_joint, skeleton_data_dict):
    """
    From serialized skeleton data return a skeleton to its bind pose.
    This wraps the recursive function that slow walks the hierarchy.

    :param Joint root_joint: The root joint of the hierarchy.
    :param dict skeleton_data_dict: The serialized skeleton dict.
    """

    _return_child_joints_to_bind(root_joint, skeleton_data_dict)


def restore_skeleton_bindpose(skl_path, root_joint):
    """
    From a .skl file restore all joints to their saved poses.

    :param str skl_path: Path to a given skl file.
    :param Joint root_joint: Root joint of an existing hierarchy.
    """

    if skl_path.endswith('.skl'):
        skl_path = skl_path.replace('.skl', '')

    imported_skeleton_data_dict = SkeletonData(skl_path).read_data()
    return_skeleton_to_bind_pose_from_data(root_joint, imported_skeleton_data_dict)


def restore_skeleton_markup(skl_path, root_joint):
    """
    From a .skl file restore all markup to joints.

    :param str skl_path: Path to a given skl file.
    :param Joint root_joint: Root joint of an existing hierarchy.
    """

    if skl_path.endswith('.skl'):
        skl_path = skl_path.replace('.skl', '')

    imported_skeleton_data_dict = SkeletonData(skl_path).read_data()
    restore_skeleton_markup_from_data(root_joint, imported_skeleton_data_dict)


class SkeletonData:
    """
    DataPart that represents Skeleton data.
    """

    DATA_TYPE = 'rig.skeleton'
    NICE_NAME = 'Skeleton'
    PRIORITY = 10
    VERSION = 1

    _has_trait = re.compile(r'\.skl$', re.I)

    def __init__(self, identifier):
        self._id = identifier

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    @classmethod
    def can_represent(cls, identifier, only_extension=False):
        """
        Overrides base DataPart can_represent function.
        Returns whether this data part can represent by the given identifier.

        :param str identifier: data identifier. This could be a URL, a file path, a UUID, etc.
        :param bool only_extension: If True, only trait (usually extension) will be checked.
        :return: True if the current data part can be represented by the given identifier; False otherwise.
        :rtype: bool
        """

        if SkeletonData._has_trait.search(identifier):
            if only_extension:
                return True
            if os.path.exists(identifier):
                return True

        return False

    @classmethod
    def extension(cls):
        """
        Overrides base DataPart extension function.
        Returns extension of this data part.

        :return: data part extension.
        :rtype: str
        """

        return '.skl'

    @classmethod
    def icon(cls):
        """
        Overrides base DataPart icon function.
        Returns the icon of this data part.

        :return: data part icon
        :rtype: QIcon
        """

        return resources.icon(r'default\skeleton.png')

    def functionality(self):
        """
        Overrides base DataPart functionality function.
        Exposes per-data functionality in the form of a dictionary where the key is the string accessor, and the value
        is callable.
        In a situation where multiple DataParts are bound then a single dictionary with all the entries combined is
        returned.

        :return: data part functionality dictionary.
        :rtype: dict
        """

        return dict(
            read_data=self.read_data,
            save_data=self.save_data,
            import_data=self.import_data,
            export_data=self.export_data,
        )

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def read_data(self):
        """
        Reads skeleton data containing in file.

        :return: dictionary containing all curve data.
        :rtype: dict
        """

        file_path = self._id
        file_path = strings.append_extension(file_path, self.extension())
        if not os.path.exists(file_path):
            logger.warning('Impossible to read skeleton data from non existent file: "{}"!'.format(file_path))
            return dict()

        logger.debug('Reading Skeleton data from file: "{}"'.format(file_path))

        return jsonio.read_json_file(file_path)

    def save_data(self, skeleton_data):
        """
        Saves given skeleton data into a file in disk.

        :param dict skeleton_data: curves data to save into file in disk.
        :return: True if the save operation was successful; False otherwise.
        :rtype: bool
        """

        file_path = self._id
        if not file_path:
            logger.warning('Impossible to save skeleton data to file because save file path not defined!')
            return False
        file_path = strings.append_extension(file_path, self.extension())

        jsonio.write_to_json_file(skeleton_data, file_path)

        return True

    def import_data(self, *args, **kwargs):
        """
        Imports skeleton data from file.

        :param list args: list of positional arguments.
        :param dict kwargs: keyword arguments
        """

        file_path = self._id
        file_path = strings.append_extension(file_path, self.extension())
        if not os.path.exists(file_path):
            logger.warning('Impossible to import skeleton data file "{}" because it does not exists!'.format(file_path))
            return None, list()

        skeleton_data = self.functionality()['read_data']()
        if not skeleton_data:
            logger.warning(
                'Impossible to import skeleton data file "{}" because it does not contains valid skeleton data!'.format(
                    file_path))
            return None, list()

        return create_skeleton_from_data(skeleton_data)

    def export_data(self, *args, **kwargs):
        """
        Exports skeleton data to file.

        :param list args: list of positional arguments.
        :param dict kwargs: keyword arguments
        :return:
        """

        file_path = self._id
        if not file_path:
            logger.warning('Impossible to save skeleton data file because export file path not defined!')
            return False
        file_path = strings.append_extension(file_path, self.extension())

        objects = kwargs.get('objects', None) or args
        if not objects:
            objects = pm.ls(sl=True)
        if not objects:
            logger.warning('No skeleton data to export!')
            return False
        objects = lists.force_list(objects)

        logger.debug('Saving {} | args: {} | kwargs: {}'.format(file_path, args, kwargs))

        skeleton_data = serialize_skeleton(objects[0])
        data_to_save = dict(
            joints=skeleton_data,
            dcc=dict(
                name='Maya',
                version=maya_utils.get_version(),
                up_axis=pm.upAxis(query=True, axis=True)
            ),
            version=self.VERSION
        )

        valid = self.functionality()['save_data'](skeleton_data=data_to_save)
        if not valid:
            logger.warning('Was not possible to save skeleton "{}" data properly in file: "{}"'.format(
                objects, file_path))
            return False

        return True
