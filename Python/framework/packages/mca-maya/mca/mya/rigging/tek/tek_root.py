#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""
# System global imports
import os
# mca python imports
import pymel.core as pm
# mca python imports
from mca.common.assetlist import assetlist
# Internal module imports
from mca.mya.modifiers import ma_decorators
# Internal module imports
from mca.mya.rigging.tek import tek_base, tek_rig, skeletal_mesh
from mca.mya.utils import namespace


class TEKRoot(tek_base.TEKNode):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(root_joint, asset_type, asset_id):
        # Set Namespace
        root_namespace = root_joint.namespace().split(':')[0]
        namespace.set_namespace(root_namespace, check_existing=False)

        node = tek_base.TEKNode.create(None, TEKRoot.__name__, TEKRoot.VERSION)

        node.addAttr('assetType', dt='string')
        node.addAttr('assetID', dt='string')
        node.addAttr('assetName', dt='string')
        node.addAttr('isFragRoot', at='bool', dv=True)
        node.assetType.set(asset_type)
        node.assetID.set(asset_id)
        mca_asset = assetlist.get_asset_by_id(asset_id)
        if mca_asset:
            node.assetName.set(mca_asset.asset_name.lower())
        else:
            node.assetName.set('missing_name')

        # Connect the root joint to the root component
        node.connect_node(root_joint, 'rootJoint', parent_attr='tekRootJoint')

        return node

    @property
    def root_joint(self):
        """
        Returns the root joint.

        :return: Returns the root joint.
        :rtype: pm.nt.Joint
        """

        return self.pynode.rootJoint.get()

    @property
    def asset_id(self):
        """
        Returns the asset id.

        :return: Returns the asset id.
        :rtype: str
        """

        return self.pynode.assetID.get()

    @asset_id.setter
    def asset_id(self, value):
        """
        Sets the asset id.

        :param str value: Sets the asset id.
        """

        self.pynode.assetID.set(value)

    def get_rig(self):
        """
        Returns the TEKRig if this root has one.

        :return: The attached TEKRig
        :rtype: TEKRig
        """

        return self.get_tek_child(tek_rig.TEKRig)

    def get_skeletal_mesh(self):
        """
        Returns the TEKRig if this root has one.

        :return: The attached TEKRig
        :rtype: TEKRig
        """

        return self.get_tek_child(skeletal_mesh.SkeletalMesh)


def is_tek_root(node):
    """
    Checks if node is a TEKRoot.

    :param TEKNode node: Any TEKNode to check.
    :return: Returns whether or not the node is a TEKRoot.
    :rtype: bool
    """

    if not tek_base.is_tek_node(node):
        return False

    if not isinstance(node, tek_base.TEKNode):
        node = tek_base.TEKNode(node)

    return isinstance(node, TEKRoot)


def get_tek_root(input_node):
    """
    Get the associated TEKRoot from a passed TEKNode.

    :param TEKNode input_node: A given tek node within a hierarchy.
    :return: TEK root node.
    :rtype: TEKRoot
    """

    if not tek_base.is_tek_node(input_node):
        return None

    if not isinstance(input_node, tek_base.TEKNode):
        input_node = tek_base.TEKNode(input_node)

    found_root = input_node if is_tek_root(input_node) else None
    tek_parent_node = input_node.get_tek_parent()
    while not found_root and tek_parent_node:
        if is_tek_root(tek_parent_node):
            found_root = tek_parent_node
        else:
            input_node = tek_parent_node
        tek_parent_node = input_node.get_tek_parent()
    return found_root


def get_all_tek_roots():
    """
    Get all TEKRoots in the scene.

    :return: A list of all TEKRoots
    :rtype: list[TEKRoot]
    """

    return_list = []
    for is_tek_root_attr in pm.ls('*.isFragRoot', r=True):
        if is_tek_root_attr.get():
            return_list.append(tek_base.TEKNode(is_tek_root_attr.node()))
    return return_list


def get_tek_root_by_assetid(assetid):
    """
    Find a TEKRoot by matching asset id.

    :param str assetid: String identifier for a particular rig
    :return: First found TEKRoot by matching assetid
    :rtype: TEKRoot
    """

    for is_tek_root_attr in pm.ls('*.isFragRoot', r=True):
        if isinstance(is_tek_root_attr, pm.Attribute) and is_tek_root_attr.get():
            root_node = is_tek_root_attr.node()
            if root_node.assetID.get() == assetid:
                return tek_base.TEKNode(root_node)


def get_root_joint(rig_node):
    """
    Returns the root joint of the rig.

    :param pm.nt.transform rig_node: A node connected to the rig.
    :return: Returns the root joint of the rig.
    :rtype: pm.nt.joint
    """

    tek_root = get_tek_root(rig_node)
    return tek_root.root_joint

