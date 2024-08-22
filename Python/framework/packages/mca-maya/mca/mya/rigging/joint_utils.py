#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions for working with joints, and skeleton hierarchies.
"""

# python imports
# software specific imports
import maya.cmds as cmds
import pymel.core as pm

# Project python imports
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import skin_utils
from mca.mya.utils import attr_utils, dag_utils, fbx_utils, naming, namespace_utils

from mca.common.utils import fileio, list_utils, path_utils, pymaths
from mca.common.textio import jsonio, yamlio

from mca.common import log
logger = log.MCA_LOGGER

NAMING_ERROR_LIST = ['rower', 'reg']
BLACKLIST_ATTRS = ['noStaticAnim', 'noExport', 'SDK_Parent', 'driver_flag']

SIDE_LIST = ['left', 'right', 'center', 'front', 'back', 'top', 'bottom']


class SkeletonHierarchy(object):
    """
    Data class that represents and parses a given skeleton hierarchy.
    All joints are considered to be skeleton joints.
    Null joints are joints which should not be exported with animation.
    NOTE: We do not make a distinction between joints required for rigging, but not required for engine. This
        might be an oversight on my end but we'll burn that bridge when we get to it.
    Animated joints are joints which expect animation
    Twist joints are joints required for twist systems, they shouldn't be animated, but should be exported.

    """
    _root = None
    _all_joints = []
    _animated_joints = []
    
    _twist_joints = {}
    _null_joints = []

    _invalid_joints = {}
    _skel_hierarchy = {}
    _skel_chain_dict = {}

    CHECKED = False

    def __init__(self, root, check_for_errors=False):
        if not root:
            return

        self.root = root
        self.parse_joints(check_for_errors)

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, val):
        self._root = val

    @property
    def all_joints(self):
        return self._all_joints

    @property
    def exportable_joints(self):
        # NOTE: Sneaky python mutable here, copy the list into the var instead of directly assigning it.
        return_list = self.animated_joints[:]
        for skel_side, region_dict in self.twist_joints.items():
            for skel_region, joint_data_dict in region_dict.items():
                return_list+=[x for x in joint_data_dict.get('joints', []) if x not in return_list]
        return return_list

    @property
    def twist_joints(self):
        return self._twist_joints

    @property
    def animated_joints(self):
        return self._animated_joints

    @property
    def skel_hierarchy(self):
        return self._skel_hierarchy

    @property
    def invalid_joints(self):
        if self.CHECKED:
            return self._invalid_joints
        else:
            False

    def parse_joints(self, check_for_errors=False):
        """
        Check through the joint hierarchy and register each joint to the class's data structure.

        :param bool check_for_errors: If while parsing the skeleton we should check for errors.
        """
        self.CHECKED = True if check_for_errors else False

        self._all_joints = []
        self._animated_joints = [self.root]
        
        self._twist_joints = {}
        self._null_joints = []
        
        self._invalid_joints = {}       
        self._skel_hierarchy = {'root': self.root}
        self._skel_chain_dict = {'center':{'root':{'start': self.root, 'end':self.root, 'joints':[self.root]}}}

        for joint_node in dag_utils.get_ordered_hierarchy(self.root, pm.nt.Joint):
            wrapped_joint = JointMarkup(joint_node)

            # Adding joints to name lookup dict.
            joint_name = wrapped_joint.name
            if joint_name not in self._skel_hierarchy:
                self._skel_hierarchy[joint_name] = joint_node
            else:
                logger.error(f'{joint_name}: duplicate joint names are not permitted in a skeleton')
                if not check_for_errors:
                    return
                if 'name' not in self._invalid_joints:
                        self._invalid_joints['name'] = []
                self._invalid_joints['name'].append(joint_node)
                
            skel_side = wrapped_joint.side
            if skel_side not in SIDE_LIST:
                logger.error(f'{skel_side} on {wrapped_joint.name} is not a valid side option.')
                if 'side' not in self._invalid_joints and check_for_errors:
                    self._invalid_joints['side'] = []
                if check_for_errors:
                    self._invalid_joints['side'].append(joint_node)
            skel_region = wrapped_joint.region

            joint_parent = joint_node.getParent()
            if check_for_errors:
                # Name errors
                if any(True if x in wrapped_joint.name else False for x in NAMING_ERROR_LIST):
                    if 'typo' not in self._invalid_joints:
                        self._invalid_joints['typo'] = []
                    self._invalid_joints['typo'].append(joint_node)

                # Check for scale.
                if not all(True if x == 1.0 else False for x in joint_node.s.get()):
                    if 'scale' not in self._invalid_joints:
                        self._invalid_joints['scale'] = []
                    self._invalid_joints['scale'].append(joint_node)

                # Check for mismatched joint settings.
                if joint_parent:
                    # If this joint should be part of the core skeleton, its parent should be as well.
                    wrapped_parent = JointMarkup(joint_parent)
                    if wrapped_parent and wrapped_parent.null:
                        if 'skeleton' not in self._invalid_joints:
                            self._invalid_joints['skeleton'] = []
                        self._invalid_joints['skeleton'].append(joint_node)

                    if wrapped_joint.animated:
                        wrapped_parent = JointMarkup(joint_parent)
                        if wrapped_parent and not wrapped_parent.animated:
                            if 'animated' not in self._invalid_joints:
                                self._invalid_joints['animated'] = []
                            self._invalid_joints['animated'].append(joint_node)

                # Check for duplicate markup.
                for bookend, search_fnc in [(wrapped_joint.start, self.get_chain_start), (wrapped_joint.end, self.get_chain_end)]:
                    if bookend:
                        # If we have a start or end
                        found_joint = search_fnc(skel_side, skel_region)
                        if found_joint:
                            # we already have a register for this side/region.
                            if 'duplicates' not in self._invalid_joints:
                                self._invalid_joints['duplicates'] = []

                            if joint_node not in self._invalid_joints['duplicates']:
                                self._invalid_joints['duplicates'].append(joint_node)
                            if found_joint not in self._invalid_joints['duplicates']:
                                self._invalid_joints['duplicates'].append(found_joint)

            # Register the joint to all the class data structures
            self._all_joints.append(joint_node)
            is_animated = bool(wrapped_joint.animated)
            if is_animated:
                self._animated_joints.append(joint_node)

            if wrapped_joint.twist:
                if skel_side not in self._twist_joints:
                    self._twist_joints[skel_side] = {}
                if skel_region not in self._twist_joints[skel_side]:
                    self._twist_joints[skel_side][skel_region] = {}
                    self._twist_joints[skel_side][skel_region]['joints'] = []
                self._twist_joints[skel_side][skel_region]['joints'].append(joint_node)
            if wrapped_joint.null:
                self._null_joints.append(joint_node)

            if skel_side not in self._skel_chain_dict:
                self._skel_chain_dict[skel_side] = {}
            if skel_region not in self._skel_chain_dict[skel_side]:
                self._skel_chain_dict[skel_side][skel_region] = {}

            if wrapped_joint.start:
                self._skel_chain_dict[skel_side][skel_region]['start'] = joint_node
                self._skel_chain_dict[skel_side][skel_region]['joints'] = [joint_node]

            if 'joints' not in self._skel_chain_dict[skel_side][skel_region]:
                self._skel_chain_dict[skel_side][skel_region]['joints'] = []

            if joint_node not in self._skel_chain_dict[skel_side][skel_region]['joints']:
                self._skel_chain_dict[skel_side][skel_region]['joints'].append(joint_node)

            end_region = wrapped_joint.end
            if end_region:
                try:
                    self._skel_chain_dict[skel_side][end_region]['end'] = joint_node
                    if joint_node not in self._skel_chain_dict[skel_side][end_region]['joints']:
                        self._skel_chain_dict[skel_side][end_region]['joints'].append(joint_node)
                except:
                    logger.error(f'{joint_name}, End was attempted to be registered before the start')
                    if not check_for_errors:
                        return

        if check_for_errors:
            for skel_side, region_dict in self._skel_chain_dict.items():
                for skel_region, skel_dict in region_dict.items():
                    if skel_region not in self._twist_joints.get(skel_side, []):
                        if not skel_dict.get('end') or not skel_dict.get('start'):
                            if 'bookend' not in self._invalid_joints:
                                self._invalid_joints['bookend'] = []
                            for x in skel_dict.get('joints'):
                                self._invalid_joints['bookend'].append(x)

                    parent_list = []
                    for joint_node in skel_dict.get('joints'):
                        # Check for mirror. # This needs to be checked after the dicts are filled.
                        if skel_side != 'center':
                            mirror_chain_joints = self._skel_chain_dict.get(skel_side, {}).get(skel_region, {}).get('joints', [])
                            if mirror_chain_joints:
                                try:
                                    skel_index = mirror_chain_joints.index(joint_node)
                                    opposite_joint = None
                                    if skel_side == 'left':
                                        opposite_joint = list_utils.get_index_in_list(self._skel_chain_dict['right'][skel_region]['joints'], skel_index)
                                    elif skel_side == 'right':
                                        opposite_joint = list_utils.get_index_in_list(self._skel_chain_dict['left'][skel_region]['joints'], skel_index)
                                    elif skel_side == 'front':
                                        opposite_joint = list_utils.get_index_in_list(self._skel_chain_dict['back'][skel_region]['joints'], skel_index)
                                    elif skel_side == 'back':
                                        opposite_joint = list_utils.get_index_in_list(self._skel_chain_dict['front'][skel_region]['joints'], skel_index)
                                    elif skel_side == 'top':
                                        opposite_joint = list_utils.get_index_in_list(self._skel_chain_dict['bottom'][skel_region]['joints'], skel_index)
                                    elif skel_side == 'bottom':
                                        opposite_joint = list_utils.get_index_in_list(self._skel_chain_dict['top'][skel_region]['joints'], skel_index)

                                    if opposite_joint:
                                        joint_pos = joint_node.getTranslation(ws=True)
                                        opposite_pos = opposite_joint.getTranslation(ws=True)
                                        if opposite_pos:
                                            if not all(True if abs(round(x, 3)) == abs(round(y, 3)) else False for x, y in zip(joint_pos, opposite_pos)):
                                                # If not all absolute joint positions are equal there is a mirror error.
                                                # EG arm_lt is at [-15, 5, 10] and arm_rt is at [15, 5, 10]
                                                #    Their absolute values are the same, even though their x value is a mirror.
                                                if 'mirror' not in self._invalid_joints:
                                                    self._invalid_joints['mirror'] = []
                                                for x in [joint_node, opposite_joint]:
                                                    if x not in self._invalid_joints['mirror']:
                                                        self._invalid_joints['mirror'].append(x)
                                except:
                                    pass
                                
                        # Parent validation check.
                        parent_list.append(joint_node.getParent())

                    parent_list_length = len(list(set(parent_list)))
                    if (parent_list_length != 1 and parent_list_length != len(skel_dict.get('joints'))) or (parent_list_length > 2 and not all(True if x.getParent() in parent_list else False for x in list(reversed(parent_list))[:-1])):
                        # We neither have all the same parents, nor all unique parents.
                        # OR
                        # We have a list length greater than 2 joints. Where every parent other than the first, is present in our found parent list.
                        # Meaning all parents found are in a chain.
                        # This captures twist joints with different parents
                        # This should capture a stray joint not part of a chain
                        # Any chains longer than 2 with more than 1 unique parent.
                        if 'parent' not in self._invalid_joints:
                            self._invalid_joints['parent'] = []
                        self._invalid_joints['parent'] += self.get_full_chain(skel_side, skel_region)

    def get_chain_bookend(self, skel_side, skel_region):
        """
        Return the first and last joint of a given joint chain by way of side and region identification.

        :param str skel_side: The side markup for the requested joint.
        :param str skel_region: The region markup for the requested joint.
        :return: a list containing the first and last joint of a joint chain.
        :rtype: list(Joint, Joint)
        """
        joint_chain = self._skel_chain_dict.get(skel_side, {}).get(skel_region, {}).get('joints', [])
        return [] if not joint_chain else [joint_chain[0], joint_chain[-1]]

    def get_full_chain(self, skel_side, skel_region):
        """
        Return all joints of a joint chain by way of side and region identification.

        :param str skel_side: The side markup for the requested joint.
        :param str skel_region: The region markup for the requested joint.
        :return: A list containing all joints that match the lookup criteria.
        :rtype: list(Joint, ...)
        """
        return self._skel_chain_dict.get(skel_side, {}).get(skel_region, {}).get('joints', [])

    def get_chain_start(self, skel_side, skel_region):
        """
        Returns the first joint of a joint chain by way of side and region identification.

        :param str skel_side: The side markup for the requested joint.
        :param str skel_region: The region markup for the requested joint.
        :return: The first joint of the requested joint chain.
        :rtype: Joint
        """
        return self._skel_chain_dict.get(skel_side, {}).get(skel_region, {}).get('start', None)

    def get_chain_end(self, skel_side, skel_region):
        """
        Returns the last joint of a joint chain by way of side and region identification.

        :param str skel_side: The side markup for the requested joint.
        :param str skel_region: The region markup for the requested joint.
        :return: The last joint of the requested joint chain.
        :rtype: Joint
        """
        return self._skel_chain_dict.get(skel_side, {}).get(skel_region, {}).get('end', None)


class JointMarkup(object):
    """
    Wrapper for a Joint pynode that handles all the markup required for skeletons.

    """
    def __init__(self, joint_node):
        if not joint_node or not isinstance(joint_node, pm.nt.Joint):
            return
        self.pynode = joint_node

    @property
    def name(self):
        return naming.get_basename(self.pynode)
    
    @property
    def side(self):
        if self.pynode.hasAttr('skel_side'):
            return self.pynode.getAttr('skel_side')

    @side.setter
    def side(self, value):
        if not self.pynode.hasAttr('skel_side'):
            self.pynode.addAttr('skel_side', dt='string')
        if isinstance(value, str):
            self.pynode.setAttr('skel_side', value.lower())

    @property
    def region(self):
        if self.pynode.hasAttr('skel_region'):
            return self.pynode.getAttr('skel_region')

    @region.setter
    def region(self, value):
        if not self.pynode.hasAttr('skel_region'):
            self.pynode.addAttr('skel_region', dt='string')
        if isinstance(value, str):
            self.pynode.setAttr('skel_region', value.lower())

    @property
    def start(self):
        if self.pynode.hasAttr('skel_start'):
            return self.pynode.getAttr('skel_start')

    @start.setter
    def start(self, value):
        if not self.pynode.hasAttr('skel_start'):
            self.pynode.addAttr('skel_start', dt='string')
        if isinstance(value, str):
            self.pynode.setAttr('skel_start', value.lower())

    @property
    def end(self):
        if self.pynode.hasAttr('skel_end'):
            return self.pynode.getAttr('skel_end')

    @end.setter
    def end(self, value):
        if not self.pynode.hasAttr('skel_end'):
            self.pynode.addAttr('skel_end', dt='string')
        if isinstance(value, str):
            self.pynode.setAttr('skel_end', value.lower())

    @property
    def animated(self):
        # This joint is driven by animation. All of its parent joints should also be animated.
        if self.pynode.hasAttr('skel_animated'):
            return self.pynode.getAttr('skel_animated')
        return False

    @animated.setter
    def animated(self, val):
        if not self.pynode.hasAttr('skel_animated'):
            self.pynode.addAttr('skel_animated', at='bool', dv=True)
        self.pynode.setAttr('skel_animated', val)
        if val:
            # Animated joints must be valid bones.
            self.null = False
    
    @property
    def twist(self):
        # Twist joints are joints that are driven by the twist component, and are not animated.
        if self.pynode.hasAttr('skel_twist'):
            return self.pynode.getAttr('skel_twist')
        return False

    @twist.setter
    def twist(self, val):
        if not self.pynode.hasAttr('skel_twist'):
            self.pynode.addAttr('skel_twist', at='bool', dv=True)
        self.pynode.setAttr('skel_twist', val)
        if val:
            # Twist joints must be valid bones.
            self.null = False
            self.animated = False

    @property
    def null(self):
        # Null joints are skeleton joints, but are not animated, and never skinned to.
        # These might be rig related joints.
        if self.pynode.hasAttr('skel_null'):
            return self.pynode.getAttr('skel_null')
        return False

    @null.setter
    def null(self, val):
        if not self.pynode.hasAttr('skel_null'):
            self.pynode.addAttr('skel_null', at='bool', dv=True)
        self.pynode.setAttr('skel_null', val)
        if val:
            # Null joints cannot be animated.
            self.animated = False
            self.twist = False

    def getParent(self):
        self.pynode.getParent()

    def setParent(self, parent_node):
        if isinstance(parent_node, JointMarkup):
            parent_node = parent_node.pynode

        self.pynode.setParent(parent_node)


def duplicate_joint(joint_node, duplicate_name=None):
    """
    Duplicates given joint.

    :param PyNode joint_node: Joint to be duplicated
    :param str duplicate_name: optional name for duplicated joint. If None, append _dup to name.
    :return: str
    """

    if not isinstance(joint_node, pm.nt.Joint):
        return

    duplicate_name = duplicate_name or naming.get_basename(joint_node)
    duplicate_name = naming.get_unique_dagname(duplicate_name)

    new_joint_node = pm.duplicate(joint_node, po=True)[0]
    new_joint_node.rename(duplicate_name)

    attr_utils.set_attr_state(new_joint_node, locked=False)

    return new_joint_node


def duplicate_chain(start_joint, end_joint=None, suffix=None):
    """
    Duplicates a joint chain based on the given end and end joint.

    :param pm.PyNode start_joint: start joint of chain.
    :param pm.PyNode end_joint: end joint of chain. If None, use end of current chain.
    :param str suffix: A suffix to add to the end of each joint name.
    :return: list of duplicate joints.
    :rtype: list(str)
    """

    if not start_joint or not end_joint:
        return

    joint_chain = dag_utils.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

    return_list = []
    first_parent = joint_chain[0].getParent()
    for index, joint_node in enumerate(joint_chain):
        duplicate_name = f'{naming.get_basename(joint_node)}_{suffix}' if suffix else None
        duplicate_node = duplicate_joint(joint_node, duplicate_name)
        if index:
            if joint_node.getParent() != first_parent:
                # Only chain parent the duplicate joints if they don't share a parent.
                # This allows us to duplicate twist chains.
                duplicate_node.setParent(return_list[-1])

        return_list.append(duplicate_node)

    return return_list


@ma_decorators.ignore_prompts_decorator
def import_skeleton(file_path):
    """
    From a skeleton file import the skeleton hierarchy. Pitch all non joint nodes.

    :param str file_path: The absolute path to a skeleton file.
    :return: The imported skeleton root
    :rtype: pm.nt.Joint
    """
    root_joint = None
    if file_path.lower().endswith('.ma') or file_path.lower().endswith('.fbx'):
        imported_node_list = []
        if file_path.lower().endswith('.ma'):
            # .ma import
            imported_node_list = pm.importFile(file_path, returnNewNodes=True)
        elif file_path.lower().endswith('.fbx'):
            # fbx import
            imported_node_list = fbx_utils.import_fbx(file_path)

        things_to_delete = []
        root_joint = None
        for node in imported_node_list:
            if not isinstance(node, pm.nt.Joint):
                things_to_delete.append(node)
            elif not root_joint:
                root_joint = dag_utils.get_absolute_parent(node, pm.nt.Joint)
        if things_to_delete:
            pm.delete(things_to_delete)
    elif file_path.lower().endswith('.skl'):
        skel_file_data = jsonio.read_json(file_path)
        skel_data = skel_file_data.get('skel_data', {})
        root_joint = deserialize_skeleton(skel_data)

    if root_joint:
        if not root_joint.hasAttr('skel_path'):
            root_joint.addAttr('skel_path', dt='string')
        root_joint.setAttr('skel_path', str(path_utils.to_relative_path(file_path)).replace('\\', '\\\\'))
    return root_joint


@ma_decorators.keep_namespace_decorator
def import_merge_skeleton(file_path, root_joint=None):
    """
    Import and merge with an existing skeleton hierarchy. This will combine joints from the imported skel an already present skel.

    :param str file_path: The absolute path to a skeleton file.
    :param root_joint:
    :return: The imported skeleton root
    :rtype: pm.nt.Joint
    """
    if file_path.lower().endswith('.ma') or file_path.lower().endswith('.fbx'):
        imported_root = import_skeleton(file_path)
        if not imported_root:
            # Failed to import a skeleton.
            logger.debug(f'{file_path} failed to import this skeleton.')
            return root_joint

        if root_joint:
            existing_skel_dict = get_skel_dict(root_joint)
            imported_skel_dict = get_skel_dict(imported_root)

            for joint_name, joint_node in imported_skel_dict.items():
                if joint_name in existing_skel_dict:
                    # Skip any joints already in the skel.
                    continue
                imported_parent = imported_skel_dict.get(joint_name, {}).getParent()
                if imported_parent:
                    # If we have a parent
                    parent_name = naming.get_basename(imported_parent)
                    if parent_name in imported_skel_dict:
                        # If there parent is present in the imported skel dict
                        joint_node.setParent(imported_skel_dict[parent_name])
                    elif parent_name in existing_skel_dict:
                        # If the parent is present in the existing skel.
                        joint_node.setParent(existing_skel_dict[parent_name])
                else:
                    joint_node.setParent(existing_skel_dict['root'])
            # Remove any leftover joints. There should at a minimum always be a root.
            pm.delete(imported_root)
        else:
            # We are not merging, just taking the imported skel as is.
            root_joint = imported_root
    elif file_path.lower().endswith('.skl'):
        skel_file_data = yamlio.read_yaml(file_path, True)
        skel_data = skel_file_data.get('skel_data', {})
        root_joint = deserialize_skeleton(skel_data, root_joint)

    if naming.get_basename(root_joint) != 'root':
        # Make sure our latest imported skel is named root.
        optional_namespace = root_joint.namespace()
        search_str = '|root' if not optional_namespace else f'|{optional_namespace}:root'
        rename_root = list_utils.get_first_in_list(pm.ls(search_str))
        if rename_root:
            namespace_utils.set_namespace('')
            rename_root.rename(rename_root.name().replace('root', 'root1'))
        root_joint.rename(f'{optional_namespace}:root' if optional_namespace else 'root')

    if root_joint:
        if not root_joint.hasAttr('skel_path'):
            root_joint.addAttr('skel_path', dt='string')
            root_joint.setAttr('skel_path', str(path_utils.to_relative_path(file_path)).replace('\\', '\\\\'))

    return root_joint


def reset_bind_pose(file_path, root_joint):
    skel_file_data = yamlio.read_yaml(file_path, True)
    skel_data = skel_file_data.get('skel_data', {})
    root_joint = deserialize_skeleton(skel_data, root_joint, apply_markup=False, import_joints=False)


def reset_markup(file_path, root_joint):
    skel_file_data = yamlio.read_yaml(file_path, True)
    skel_data = skel_file_data.get('skel_data', {})
    root_joint = deserialize_skeleton(skel_data, root_joint, reset_bind=False, import_joints=False)


def get_skel_dict(root_joint):
    """
    Create a simple lookup dict of name to joint.

    :param Joint root_joint: The root joint of a given skeleton.
    :return: A dictionary of joint names to joint.
    :rtype: dict
    """
    skel_dict = {'root': root_joint}
    for joint_node in pm.listRelatives(root_joint, ad=True, type=pm.nt.Joint):
        joint_name = naming.get_basename(joint_node)
        if joint_name in skel_dict:
            logger.debug(f'! WARNING ! {joint_name} This joint is already present in the skeleton.')
        skel_dict[joint_name] = joint_node
    return skel_dict


def get_hierarchy_bind_roots(node):
    """
    From a given node find all potential bind roots for that hierarchy.

    :param Transform node: A node within the hierarchy to traverse.
    :return: A list of all potential bind roots.
    :rtype: list[Joint]
    """

    bind_root_list = []
    parent_node = dag_utils.get_absolute_parent(node)
    search_list = [parent_node] + pm.listRelatives(parent_node, ad=True, type=pm.nt.Transform)
    for node in search_list:
        bind_root = get_bind_root(node)
        if bind_root not in bind_root_list:
            bind_root_list.append(bind_root)
    return bind_root_list


def get_bind_root(node):
    """
    From a single node find the skeleton bind root.

    :param Transform node: A shaped transform to find the bind root for.
    :return: The found bind root.
    :rtype: Joint
    """

    if node and node.getShape():
        skin_cluster = skin_utils.get_skincluster(node)
        if skin_cluster:
            influence_list = skin_cluster.influenceObjects()
            if influence_list:
                return dag_utils.get_absolute_parent(influence_list[0], pm.nt.Joint)


def set_markup(joint_list, skel_side, skel_region, is_twist=False, is_null=False, is_animated=True):
    """
    For a given list of joints apply markup based on the args passed.

    :param list(Joint) joint_list: A list of joints in hierarchical order.
    :param str skel_side: The side markup to set.
    :param str skel_region: The region markup to set.
    :param bool is_twist: If the joint should be marked up as a twist joint.
    :param bool is_null: If the joint should be marked up as a null joint.
    :param bool is_animated: If the joint should be marked up as an animated joint.
    :return:
    """
    for index, joint_node in enumerate(joint_list):
        wrapped_joint = JointMarkup(joint_node)

        wrapped_joint.side = skel_side
        wrapped_joint.region = skel_region

        if not is_twist:
            if not index or len(joint_list) == 1:
                # Set start on first index.
                wrapped_joint.start = skel_region
            if joint_node == joint_list[-1]:
                # If we have the last joint
                wrapped_joint.end = skel_region
            elif index:
                # Start and end cannot be set to any except the first or last.
                if joint_node.hasAttr('skel_start'):
                    joint_node.skel_start.delete()
                if joint_node.hasAttr('skel_end'):
                    joint_node.skel_end.delete()

        if is_twist:
            wrapped_joint.twist = True
        if is_animated:
            wrapped_joint.animated = True
        if is_null:
            wrapped_joint.null = True

        if not is_null:
            wrapped_joint.null = False
        if not is_twist:
            wrapped_joint.twist = False
        if not is_animated:
            wrapped_joint.animated = False


def serialize_skeleton(root_joint):
    """
    Convert a skeleton into text data that can be used to reconstruct it.

    :param Joint root_joint: The root joint that represents a skeleton hierarchy.
    :return: A dictionary containing build instructions for this skeleton.
    :rtype: dict
    """

    if not root_joint or not isinstance(root_joint, pm.nt.Joint):
        logger.error(f'{root_joint} a valid Joint is required to serialize a skeleton.')
        return {}

    skel_data = {}
    for index, joint_node in enumerate([root_joint]+dag_utils.get_ordered_hierarchy(root_joint)):
        if index:
            joint_name = naming.get_basename(joint_node)
        else:
            # Force root joint name to 'root'
            joint_name = 'root'
        parent_joint = joint_node.getParent()
        joint_data = {}
        attr_list = joint_node.listAttr(ud=True)
        attr_data = {}

        for pyattr in attr_list:
            attr_name = pyattr.name().split('.')[-1]
            if attr_name in BLACKLIST_ATTRS:
                continue
            attr_val = pyattr.get()
            if isinstance(attr_val, pm.PyNode):
                # We cannot serialize a message attr connection. But we can keep the stub.
                attr_data[attr_name] = '$message'
            else:
                attr_data[attr_name] = attr_val

        joint_data['attr_data'] = attr_data
        joint_data['world_matrix'] = pm.xform(joint_node, matrix=True, query=True, worldSpace=True)
        if parent_joint and parent_joint == root_joint:
            parent_name = 'root'
        elif parent_joint:
            parent_name = naming.get_basename(parent_joint)
        else:
            parent_name = ''
        joint_data['parent'] = parent_name

        skel_data[joint_name] = joint_data

    return skel_data


def deserialize_skeleton(skel_data, root_joint=None, reset_bind=True, apply_markup=True, import_joints=True):
    """
    From skeleton data, reconstruct the skeleton with markup.

    :param dict skel_data: The dictionary that represents skeleton data.
    :param Joint root_joint: The root joint that represents a skeleton hierarchy.
    :param bool reset_bind: If the skeleton joint positions should be reset from the data.
    :param bool apply_markup: If the skeleton markup should be applied from the data. Note this does not clear existing data.
    :return: The imported root joint, or modified root joint.
    :rtype: Joint
    """
    
    skel_dict = {} if not root_joint else get_skel_dict(root_joint)
    new_joint_list = []
    for joint_name, joint_data in skel_data.items():
        cmds.select(None)
        if joint_name in skel_dict:
            new_joint = skel_dict[joint_name]
            new_joint.r.set([0, 0, 0])
        else:
            if not import_joints:
                continue
            new_joint = pm.joint(n=f'{joint_name}')
            new_joint_list.append(new_joint)
            skel_dict[joint_name] = new_joint

        if reset_bind:
            world_matrix = joint_data.get('world_matrix',
                                          [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
                                           1.0])
            pm.xform(new_joint, matrix=world_matrix, worldSpace=True)

            if not new_joint.getParent():
                joint_parent_name = joint_data['parent']
                joint_parent = skel_dict.get(joint_parent_name)
                if joint_parent:
                    new_joint.setParent(joint_parent)
                    new_joint_list.append(new_joint)
                else:
                    'something went horribly wrong'
        if apply_markup:
            for attr in new_joint.listAttr(ud=True):
                if 'skel_path' == attr.shortName():
                    continue
                attr.delete()
            attr_dict = {}
            for attr_name, attr_value in joint_data.get('attr_data', {}).items():
                if attr_value != '$message':
                    attr_dict[attr_name] = attr_value
                else:
                    new_joint.addAttr(attr_name, at='message')
            attr_utils.set_attribute(new_joint, attr_dict)
    if new_joint_list:
        pm.makeIdentity(new_joint_list, apply=True, t=True, r=True, s=True, n=False, pn=True)
    return skel_dict.get('root', None)


def export_skeleton(root_joint, file_path, force=False):
    """
    Serialize and export a skeleton to the given file path.

    :param Joint root_joint: The root joint that represents a skeleton hierarchy.
    :param str file_path: The file path to a given .skl file.
    :param bool force: By default the skeleton export will validate the skeleton before exporting.
    """

    serializer_version = 1.0
    # Pre Check:
    if not isinstance(root_joint, pm.nt.Joint):
        logger.error(f'{root_joint} is not a valid Joint node.')
        return

    scaled_joint_list = []
    rotated_joint_list = []
    for joint_node in [root_joint]+pm.listRelatives(root_joint, ad=True, type=pm.nt.Joint):
        if not all(True if x==1.0 else False for x in joint_node.s.get()):
            scaled_joint_list.append(joint_node)

        if not all(True if x==0.0 else False for x in joint_node.r.get()):
            rotated_joint_list.append(root_joint)

    if scaled_joint_list:
        concat_str = '/r/n'.join([x.name() for x in scaled_joint_list])
        logger.error(concat_str+"/r/n joints(s) have a non 1.0 scale value")

    if rotated_joint_list:
        concat_str = '/r/n'.join([x.name() for x in rotated_joint_list])
        logger.error(concat_str+"/r/n joints(s) have a non zeroed rotation")

    if not force and (scaled_joint_list or rotated_joint_list):
        logger.error('Skeleton export aborted, validation failed.')
        return

    # write to file
    skel_data = serialize_skeleton(root_joint)
    fileio.touch_path(file_path)
    # using JSON here because YAML doesn't keep order.
    jsonio.write_json(file_path, {'skel_data':skel_data, 'version':serializer_version})


def make_planar_chain(node_list):
    """
    For each trasnform in the 3 lon node list, create joints that are planar in place.
    :param list(Transform) node_list: A list of 3 Transforms representing a set of joints to make planar.
    :return: The three newly created planar joints.
    :rtype: list(Joint, Joint, Joint)
    """

    if len(node_list) != 3:
        return []

    primary_axis, is_positive = dag_utils.get_primary_axis(node_list[0])
    aim_list = tuple([(1.0 if is_positive else -1.0) if x == primary_axis else 0.0 for x in 'xyz'])

    pt1, pt2, pt3 = [pm.xform(x, ws=True, t=True, q=True) for x in node_list]

    norm_xprod = pymaths.get_planar_up(pt1, pt2, pt3)
    pt_look_at = pymaths.add_vectors(pt2, norm_xprod)
    look_at_loc = pm.spaceLocator()
    look_at_loc.t.set(pt_look_at)
    new_joint_list = []
    for node in node_list:
        cmds.select(None)
        new_joint = duplicate_joint(node, 'chain01')
        if new_joint_list:
            pm.delete(pm.aimConstraint(new_joint, new_joint_list[-1], aim=aim_list,  upVector=(0.0, 0.0, 1.0), wuo=look_at_loc, wut='object'))
            new_joint.setParent(new_joint_list[-1])
            pm.makeIdentity(new_joint_list[-1], apply=True, t=True, r=True, s=True, n=False, pn=True)
        new_joint_list.append(new_joint)
    pm.delete(look_at_loc)
    return new_joint_list


def reverse_joint_chain(joint_chain):
    """
    Reverses the parenting order of a list of joints.

    :param list(Joint, ...) joint_chain: A list of joints to reverse the parenting order of.
    :return: The reparented joints.
    :rtype: list(Joint, ...)
    """

    rev_joint_chain = []
    for index, joint_node in enumerate(reversed(joint_chain)):
        joint_node.setParent(None)
        if index:
            joint_node.setParent(rev_joint_chain[-1])
        rev_joint_chain.append(joint_node)
    pm.makeIdentity(rev_joint_chain, apply=True, t=True, r=True, s=True, n=False, pn=True)
    return rev_joint_chain


def attach_skeletons(driver_root, destination_root):
    """
    Using parent constraints and direct scale connection to attach two skeletons together.

    :param Joint driver_root: The root joint of the skeleton that will drive the pair.
    :param Joint destination_root: The root joint of the skeleton that will be puppeted by the driver.
    :return: A list of the names of custom attrs if any where connected.
    :rtype: list(str)
    """

    driver_skel_hierarchy = SkeletonHierarchy(driver_root)
    custom_attrs = []
    for joint_node in [destination_root]+pm.listRelatives(destination_root, ad=True, type=pm.nt.Joint):
        joint_name = naming.get_basename(joint_node)
        driver_joint = driver_skel_hierarchy.skel_hierarchy.get(joint_name)
        if driver_joint:
            pm.parentConstraint(driver_joint, joint_node)
            driver_joint.s > joint_node.s
            for ud_attr in joint_node.listAttr(ud=True, k=True):
                # Check for non Transform attrs and drive our attach skel for those attrs as well.
                attr_name = ud_attr.shortName()
                if driver_joint.hasAttr(attr_name):
                    custom_attrs.append(attr_name)
                    driver_joint.attr(attr_name) >> ud_attr
    return custom_attrs


@ma_decorators.undo_decorator
def position_twist_joints(twist_joint_list, parent_joint, child_joint):
    """
    Positions Twist joints in the correct location

    :param twist_joint_list:  A list of Twist Joints.  The joints should be listed from the closest joint to the parent
    joint to the furthest.
    :param parent_joint: The parent joint in the chain
    :param child_joint: The child joint in the chain
    """

    p_pos = pm.xform(parent_joint, q=True, ws=True, t=True)
    c_pos = pm.xform(child_joint, q=True, ws=True, t=True)

    twist_joint_list.reverse()
    ratio = 1 / (len(twist_joint_list) + 1)
    joint_ratio = 0.0
    for x, joint in enumerate(twist_joint_list):
        joint_ratio = (joint_ratio + ratio)
        pos = pymaths.get_midpoint_between_points(p_pos, c_pos, joint_ratio)
        pm.xform(joint, ws=True, t=pos)
        joint.jointOrient.set(0, 0, 0)

