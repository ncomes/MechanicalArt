#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A way to interact with joint chains in rigs.
"""

# System global imports
# Software specific imports
import pymel.core as pm
#  python imports
from mca.common import log
from mca.mya.utils import dag, naming
from mca.mya.startup.configs import ma_consts
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import joint_utils


logger = log.MCA_LOGGER


class JointMarkup(object):
    def __init__(self, joint_node):
        self.node = joint_node

    @property
    def joint(self):
        """
        Returns the joint that is being evaluated.

        :return: Returns the joint that is being evaluated.
        :rtype: pm.nt.Joint
        """

        return self.node

    # side markup
    @property
    def side(self):
        """
        Returns the side in which the joint is on.

        :return: Returns the side in which the joint is on.
        :rtype: str
        """

        if self.joint.hasAttr('skelSide'):
            return self.joint.skelSide.get()

        value = self.joint.side.get()
        return ma_consts.SIDE_LABELS[value].lower()

    @side.setter
    def side(self, value):
        """
        Sets the joint's side.

        :param  int/str value: Sets the joint's side.
        """

        if not self.joint.hasAttr('skelSide'):
            self.joint.addAttr('skelSide', dt='string')
        if isinstance(value, str):
            self.joint.skelSide.set(value.lower())
        elif isinstance(value, int):
            self.joint.skelSide.set(ma_consts.SIDE_LABELS[value].lower())

    @property
    def region(self):
        """
        Returns the list of regions a joint belongs to.

        This is a read only property.
        :return: Returns the list of regions a joint belongs to.
        :rtype list[str]:
        """
        if self.joint.hasAttr('skelRegion'):
            return self.joint.skelRegion.get()
        return self.chainStart or self.chainEnd or self.chainTwist or None

    @region.setter
    def region(self, val):
        """
        Sets a joint to be marked as a twist joint

        :param str val: Sets whether the joint is a twist joint or not.
        """

        if not self.joint.hasAttr('skelRegion'):
            self.joint.addAttr('skelRegion', dt='string')
        self.joint.skelRegion.set(val)

    # regional chain markup attrs
    @property
    def chainTwist(self):
        """
        Returns whether the joint is a twist joint or not.

        :return: Returns whether the joint is a twist joint or not.
        :rtype str or bool:
        """

        if self.joint.hasAttr('chainTwist'):
            return self.joint.chainTwist.get()
        return False

    @chainTwist.setter
    def chainTwist(self, val):
        """
        Sets a joint to be marked as a twist joint

        :param str val: Sets whether the joint is a twist joint or not.
        """

        if not self.joint.hasAttr('chainTwist'):
            self.joint.addAttr('chainTwist', dt='string')
        self.joint.chainTwist.set(val)

    @property
    def chainStart(self):
        """
        Returns whether the joint is the start of a chain.

        :return: Returns whether the joint is the start of a chain.
        :rtype str or bool:
        """

        if self.joint.hasAttr('chainStart'):
            return self.joint.chainStart.get()
        return False

    @chainStart.setter
    def chainStart(self, val):
        """
        Sets the joint as is_start and adds the region.

        :param str val: A name used to define a joint chain.
        """

        if not self.joint.hasAttr('chainStart'):
            if val:
                self.joint.addAttr('chainStart', dt='string')
                if not self.joint.hasAttr('skelRegion'):
                    self.joint.addAttr('skelRegion', dt='string')
        elif not val:
            self.node.chainStart.delete()
            return

        self.joint.chainStart.set(val)
        self.joint.skelRegion.set(val)

    def remove_is_start(self):
        """
        Removes the chainStart Attribute.
        """

        if self.joint.hasAttr('chainStart'):
            self.joint.deleteAttr('chainStart')

    @property
    def chainEnd(self):
        """
        Returns whether the joint is the end of a chain.

        :return: Returns whether the joint is the end of a chain.
        :rtype str or bool:
        """

        if self.joint.hasAttr('chainEnd'):
            return self.joint.chainEnd.get()
        return False

    @chainEnd.setter
    def chainEnd(self, val):
        """
        Sets the joint as is_start and adds the region.

        :param str region: A name used to define a joint chain.
        """

        if not self.joint.hasAttr('chainEnd'):
            if val:
                self.joint.addAttr('chainEnd', dt='string')
        elif not val:
            self.node.chainEnd.delete()
            return

        self.joint.chainEnd.set(val)

    def remove_is_end(self):
        """
        Removes the chainEnd Attribute.
        """

        if self.joint.hasAttr('chainEnd'):
            self.joint.deleteAttr('chainEnd')

    # informational markup
    @property
    def is_sk_export(self):
        """
        Returns whether the joint should be exported in the sk skeleton.

        :return: Returns whether the joint should be exported in the sk skeleton.
        :rtype: bool
        """

        if not self.joint.hasAttr('skExport'):
            self.joint.addAttr('skExport', at='bool', dv=True)
        return self.joint.skExport.get()

    @is_sk_export.setter
    def is_sk_export(self, val):
        """
        Sets a joint to be exported in the sk skeleton.

        :param  bool value: Sets whether the joint should be exported in the sk skeleton.
        """

        if not val:
            if self.joint.hasAttr('skExport'):
                self.joint.skExport.delete()
            return
        self.is_sk_export
        self.joint.skExport.set(val)

    @property
    def is_animation_export(self):
        """
        Returns whether the joint should be exported in the animation skeleton.

        :return: Returns whether the joint should be exported in the animation skeleton.
        :rtype: bool
        """

        if not self.joint.hasAttr('animationExport'):
            self.joint.addAttr('animationExport', at='bool', dv=True)
        return self.joint.animationExport.get()

    @is_animation_export.setter
    def is_animation_export(self, val):
        """
        Sets a joint to be exported in the animation skeleton.

        :param bool val: Sets whether the joint should be exported in the animation skeleton.
        """

        if not val:
            if self.joint.hasAttr('animationExport'):
                self.joint.animationExport.delete()
            return
        self.is_animation_export
        self.joint.animationExport.set(val)

    @property
    def hierarchyStart(self):
        """
        Returns whether the joint is tagged as first in hierarchy.

        :return: Returns whether the joint is first in hierarchy.
        :rtype: bool
        """

        if not self.joint.hasAttr('hierarchyStart'):
            return False
        return self.joint.hierarchyStart.get()

    @hierarchyStart.setter
    def hierarchyStart(self, val):
        """
        Sets a joint to be tagged as first in hierarchy.

        :param bool val: Sets whether the joint should be tagged as first in hierarchy.
        """

        if not val:
            if self.joint.hasAttr('hierarchyStart'):
                self.joint.hierarchyStart.delete()
            return
        self.joint.addAttr('hierarchyStart', at='bool', dv=True)
        self.joint.hierarchyStart.set(val)

    @property
    def name(self):
        """
        Returns the absolute joint name.

        :return: Returns the absolute joint name.
        :rtype: str
        """

        return naming.get_basename(self.joint.name())

    # helper functions
    def get_joint_index(self):
        """
        Returns the index position of this joint within a region

        :return:
        """

        root_joint = dag.get_absolute_parent(self.joint, node_type=pm.nt.Joint)
        skel_hierarchy = ChainMarkup(root_joint)
        joint_chain_list = skel_hierarchy.get_full_chain(self.region, self.side)
        return joint_chain_list.index(self.node) if joint_chain_list else None

    def get_world_matrix(self):
        """
        Returns the world matrix array for this joint.

        :return:
        """

        return pm.xform(self.joint, matrix=True, query=True, worldSpace=True)

    def getParent(self):
        """
        Returns this node's immediate parent.

        :return:
        """

        parent_node = self.joint.getParent()
        if parent_node:
            if isinstance(parent_node, pm.nt.Joint):
                return JointMarkup(parent_node)
            return parent_node
        return

    def getChildren(self):
        """

        :return:
        """

        children_nodes = self.joint.getChildren(type=pm.nt.Joint)
        return [JointMarkup(x) for x in children_nodes]

class ChainMarkup(object):
    def __init__(self, root):
        self._root = root
        self._hierarchyStart = None

        self._skJoints = []
        self._animationJoints = []
        self._joints = []
        self._twist_joints = {}
        self._chain = {}
        self._invalid_joints = []

        self.parse_joints()

        self.skeleton_dict = joint_utils.create_skeleton_dict(root)

    @property
    def is_valid(self):
        """
        Returns the root joint.

        :return: Returns the root joint.
        :rtype: pm.nt.Joint
        """

        return not any(self._invalid_joints)

    @property
    def root(self):
        """
        Returns the root joint.

        :return: Returns the root joint.
        :rtype: pm.nt.Joint
        """

        return self._root

    @property
    def hierarchyStart(self):
        """
        Returns the joint with markup for hierarchy start.

        :return: Returns the root joint.
        :rtype: pm.nt.Joint
        """

        return self._hierarchyStart

    @property
    def joints(self):
        """
        Returns a list of JointMarkup data for each start, end, and twist joints.
        :return: Returns a list of JointMarkup data for each start, end, and twist joints.
        :rtype: list(JointMarkup)
        """
        return self._joints

    @property
    def chain(self):
        """
        Returns a dictionary of all the joint markups.

        :return: Returns a dictionary of all the joint markups.
        :rtype: dictionary
        """

        return self._chain

    @property
    def twist_joints(self):
        """
        Returns a dictionary of all the twist joints

        :return: Returns a dictionary of all the twist joints.
        :rtype: dictionary
        """

        return self._twist_joints

    @ma_decorators.keep_selection_decorator
    def parse_joints(self):
        """
        Registers each joint in the JointMarkup class and returns it if it is a start, end or twist joint.

        :return: Returns a list of start, end, and twist joints registered in the JointMarkup class.
        :rtype: list(JointMarkup)
        """

        self._joints = dag.get_children_in_order(self.root, pm.nt.Joint)

        chain_dict = {}
        self._skJoints = []
        self._animationJoints = []
        self._twist_joints = {}
        for joint_node in self._joints:
            # use the wrapped joint for lookups, but store the OG PyNode in the class lookups.
            # we're normally using the PyNodes to do ops after so it's better for use to store them.
            wrapped_joint = JointMarkup(joint_node)

            if wrapped_joint.hierarchyStart:
                self._hierarchyStart = joint_node

            if wrapped_joint.is_sk_export:
                self._skJoints.append(joint_node)

            if wrapped_joint.is_animation_export:
                self._animationJoints.append(joint_node)

            if wrapped_joint.chainTwist:
                if wrapped_joint.side not in self._twist_joints:
                    self._twist_joints[wrapped_joint.side] = {}
                if wrapped_joint.chainTwist not in self._twist_joints[wrapped_joint.side]:
                    self._twist_joints[wrapped_joint.side][wrapped_joint.chainTwist] = {'parent': joint_node.getParent(), 'joints': []}
                self._twist_joints[wrapped_joint.side][wrapped_joint.chainTwist]['joints'].append(joint_node)

            skel_region = wrapped_joint.region
            if not skel_region:
                self._invalid_joints.append(joint_node)
                continue
            elif skel_region not in chain_dict:
                chain_dict[skel_region] = {}

            skel_side = wrapped_joint.side
            if not skel_side:
                continue
            elif skel_side not in chain_dict[skel_region]:
                chain_dict[skel_region][skel_side] = {'joints': []}

            if wrapped_joint.chainStart:
                chain_dict[skel_region][skel_side]['chain_start'] = joint_node
            if wrapped_joint.chainEnd:
                chain_end_region = wrapped_joint.chainEnd
                if chain_end_region != skel_region:
                    if chain_end_region not in chain_dict:
                        chain_dict[chain_end_region] = {}
                    if skel_side not in chain_dict[chain_end_region]:
                        chain_dict[chain_end_region][skel_side] = {}
                    chain_dict[chain_end_region][skel_side]['chain_end'] = joint_node
                else:
                    chain_dict[skel_region][skel_side]['chain_end'] = joint_node
            if not wrapped_joint.chainStart and not wrapped_joint.chainEnd:
                chain_dict[skel_region][skel_side]['joints'].append(joint_node)

        self._chain = chain_dict

    def get_start(self, region, side):
        """
        Returns a start joint in a specific region and side.

        :param str region: A name used to define a joint chain.
        :param str side: Side in which the chain is on.
        :return: Returns a start joint in a specific region and side.
        :rtype: pm.nt.Joint
        """

        skel_region_dict = self._chain.get(region, {}).get(side, {})

        return skel_region_dict.get('chain_start', None)

    def get_end(self, region, side):
        """
        Returns an end joint in a specific region and side.

        :param str region: A name used to define a joint chain.
        :param str side: Side in which the chain is on.
        :return: Returns an end joint in a specific region and side.
        :rtype: pm.nt.Joint
        """

        skel_region_dict = self._chain.get(region, {}).get(side, {})

        return skel_region_dict.get('chain_end', None)

    def get_chain(self, region, side):
        """
        Returns the start and end joint for a specific side and region.

        :param str region: A name used to define a joint chain.
        :param str side: Side in which the chain is on.
        :return: Returns the start and end joint for a specific side and region.
        :rtype: list(pm.nt.Joint)
        """
        skel_region_dict = self._chain.get(region, {}).get(side, {})

        return skel_region_dict.get('chain_start', None), skel_region_dict.get('chain_end', None) if skel_region_dict else []

    def get_full_chain(self, region, side):
        """
        Returns all the joints in a chain for a specific side and region.

        :param str region: A name used to define a joint chain.
        :param str side: Side in which the chain is on.
        :return: Returns all the joints in a chain for a specific side and region.
        :rtype: list(pm.nt.Joint)
        """

        skel_region_dict = self._chain.get(region, {}).get(side, {})
        joint_list = []
        if skel_region_dict:
            chain_start = skel_region_dict.get('chain_start', None)
            if chain_start:
                joint_list += [chain_start]

            mid_joints = skel_region_dict.get('joints', [])
            if mid_joints:
                joint_list += mid_joints

            chain_end = skel_region_dict.get('chain_end', None)
            if chain_end:
                joint_list += [chain_end]

        if not joint_list:
            logger.warning(f'No joints match lookup {region}, {side}. Verify your lookups.')
            return []
        return joint_list
