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
from mca.mya.rigging.frag import frag_base, frag_rig, skeletal_mesh
from mca.mya.utils import namespace


class FRAGRoot(frag_base.FRAGNode):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(root_joint, asset_type, asset_id):
        # Set Namespace
        root_namespace = root_joint.namespace().split(':')[0]
        namespace.set_namespace(root_namespace, check_existing=False)

        node = frag_base.FRAGNode.create(None, FRAGRoot.__name__, FRAGRoot.VERSION)

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
        node.connect_node(root_joint, 'rootJoint', parent_attr='fragRootJoint')

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
        Returns the FRAGRig if this root has one.

        :return: The attached FRAGRig
        :rtype: FRAGRig
        """

        return self.get_frag_child(frag_rig.FRAGRig)

    def get_skeletal_mesh(self):
        """
        Returns the FRAGRig if this root has one.

        :return: The attached FRAGRig
        :rtype: FRAGRig
        """

        return self.get_frag_child(skeletal_mesh.SkeletalMesh)


def is_frag_root(node):
    """
    Checks if node is a FRAGRoot.

    :param FRAGNode node: Any FRAGNode to check.
    :return: Returns whether or not the node is a FRAGRoot.
    :rtype: bool
    """

    if not frag_base.is_frag_node(node):
        return False

    if not isinstance(node, frag_base.FRAGNode):
        node = frag_base.FRAGNode(node)

    return isinstance(node, FRAGRoot)


def get_frag_root(input_node):
    """
    Get the associated FRAGRoot from a passed FRAGNode.

    :param FRAGNode input_node: A given frag node within a hierarchy.
    :return: FRAG root node.
    :rtype: FRAGRoot
    """

    if not frag_base.is_frag_node(input_node):
        return None

    if not isinstance(input_node, frag_base.FRAGNode):
        input_node = frag_base.FRAGNode(input_node)

    found_root = input_node if is_frag_root(input_node) else None
    frag_parent_node = input_node.get_frag_parent()
    while not found_root and frag_parent_node:
        if is_frag_root(frag_parent_node):
            found_root = frag_parent_node
        else:
            input_node = frag_parent_node
        frag_parent_node = input_node.get_frag_parent()
    return found_root


def get_all_frag_roots():
    """
    Get all FRAGRoots in the scene.

    :return: A list of all FRAGRoots
    :rtype: list[FRAGRoot]
    """

    return_list = []
    for is_frag_root_attr in pm.ls('*.isFragRoot', r=True):
        if is_frag_root_attr.get():
            return_list.append(frag_base.FRAGNode(is_frag_root_attr.node()))
    return return_list


def get_frag_root_by_assetid(assetid):
    """
    Find a FRAGRoot by matching asset id.

    :param str assetid: String identifier for a particular rig
    :return: First found FRAGRoot by matching assetid
    :rtype: FRAGRoot
    """

    for is_frag_root_attr in pm.ls('*.isFragRoot', r=True):
        if isinstance(is_frag_root_attr, pm.Attribute) and is_frag_root_attr.get():
            root_node = is_frag_root_attr.node()
            if root_node.assetID.get() == assetid:
                return frag_base.FRAGNode(root_node)


def get_root_joint(rig_node):
    """
    Returns the root joint of the rig.

    :param pm.nt.transform rig_node: A node connected to the rig.
    :return: Returns the root joint of the rig.
    :rtype: pm.nt.joint
    """

    frag_root = get_frag_root(rig_node)
    return frag_root.root_joint

