#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to base FRAGNodes and their usage.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.common.assetlist import assetlist
from mca.common.utils import list_utils

from mca.mya.utils import dag_utils, namespace_utils
from mca.mya.modifiers import ma_decorators

from mca.mya.rigging import skin_utils
from mca.mya.rigging.frag import frag_base


class FRAGRoot(frag_base.FRAGNode):
    _version = 1.0

    @classmethod
    @ma_decorators.keep_namespace_decorator
    def create(cls, root_joint, asset_id, **kwargs):
        if root_joint:
            root_namespace = root_joint.namespace().split(':')[0]
            namespace_utils.set_namespace(root_namespace, check_existing=False)

        new_frag_node = super().create(**kwargs)

        new_frag_node.asset_id = asset_id
        asset_entry = assetlist.get_asset_by_id(asset_id)
        if asset_entry:
            new_frag_node.asset_name = asset_entry.asset_name

        new_frag_node.root_joint = root_joint

        return new_frag_node

    def remove(self):
        asset_group = self.asset_group
        if self.frag_mesh:
            self.frag_mesh.remove()
        if self.frag_display:
            self.frag_display.remove()
        if self.frag_rig:
            self.frag_rig._remove()

        if asset_group:
            pm.delete(asset_group)
        try:
            pm.delete(self.pynode)
        except:
            pass

    @property
    def asset_id(self):
        if self.pynode.hasAttr('asset_id'):
            return self.pynode.getAttr('asset_id')

    @asset_id.setter
    def asset_id(self, val):
        if not self.pynode.hasAttr('asset_id'):
            self.pynode.addAttr('asset_id', dt='string')
        self.pynode.setAttr('asset_id', val)

    @property
    def asset_name(self):
        asset_name = 'unnamed_asset'
        if self.pynode.hasAttr('asset_name'):
            asset_name = self.pynode.getAttr('asset_name')
        return asset_name

    @asset_name.setter
    def asset_name(self, val):
        if not self.pynode.hasAttr('asset_name'):
            self.pynode.addAttr('asset_name', dt='string')
        self.pynode.setAttr('asset_name', val)

    @property
    def root_joint(self):
        if self.pynode.hasAttr('root_joint'):
            return self.pynode.getAttr('root_joint')

    @root_joint.setter
    def root_joint(self, root_joint):
        if root_joint and isinstance(root_joint, pm.nt.Joint):
            if root_joint.getParent() != self.add_asset_group():
                root_joint.setParent(self.asset_group)
            self.connect_node(root_joint, 'root_joint')

            self.organize_content()

    @property
    def frag_rig(self):
        return list_utils.get_first_in_list(self.get_frag_children(frag_type='FRAGRig'))

    @property
    def frag_mesh(self):
        return list_utils.get_first_in_list(self.get_frag_children(frag_type='FRAGMesh'))

    @property
    def frag_display(self):
        return list_utils.get_first_in_list(self.get_frag_children(frag_type='FRAGDisplay'))

    @property
    def asset_group(self):
        if self.pynode.hasAttr('asset_group'):
            return self.pynode.getAttr('asset_group')

    @asset_group.setter
    def asset_group(self, asset_group):
        self.connect_node(asset_group, 'asset_group', 'frag_parent')

    def add_asset_group(self):
        asset_group = self.asset_group
        asset_name = self.asset_name
        if not self.asset_group:
            asset_group = self._create_managed_group(f'{asset_name}_all')
            self.asset_group = asset_group

        if asset_group:
            frag_display_node = self.frag_display
            if frag_display_node:
                display_layer_name = f'{asset_name}_dl'
                frag_display_node.add_display_layer(display_layer_name)
                frag_display_node.add_objects_to_layer(display_layer_name, asset_group)
        return asset_group
    
    def organize_content(self):
        frag_display_node = self.frag_display
        if frag_display_node:
            asset_name = self.asset_name
            layer_name = f'{asset_name}_skeleton_dl'
            frag_display_node.add_display_layer(layer_name)
            frag_display_node.add_objects_to_layer(layer_name, self.root_joint, True)

        frag_mesh_node = self.frag_mesh
        if frag_mesh_node:
            bound_node_list = skin_utils.get_skeleton_meshes(self.root_joint)
            if bound_node_list:
                skins_group = frag_mesh_node.add_skins_group()
                mesh_group = frag_mesh_node.mesh_group
                for node in bound_node_list:
                    parent_list = dag_utils.get_all_parents(node)
                    if parent_list:
                        if skins_group not in parent_list and mesh_group not in parent_list:
                            parent_list[0].setParent(skins_group)
                    else:
                        node.setParent(skins_group)


class FRAGRootSingle(frag_base.FRAGNode):
    """
    FRAG nodes that must be parented to a frag root, and may only have one instance in a hierarchy.

    """
    _version = 1.0

    @classmethod
    def create(cls, frag_parent, **kwargs):
        if not isinstance(frag_parent, FRAGRoot):
            (f'{frag_parent}, FRAGNode parent must be a FRAGRoot')
            return

        found_frag_node = list_utils.get_first_in_list(frag_parent.get_frag_children(frag_type=cls))
        if found_frag_node:
            return found_frag_node

        new_frag_node = super().create(frag_parent=frag_parent, **kwargs)
        return new_frag_node


def get_frag_root(node):
    """
    From a given object try and find the FRAGRoot node. These are used to represent the rig cores.

    :param PyNode node: The node we want to find a FRAGRoot from.
    :return: The found FRAGRoot
    :rtype: FRAGRoot
    """
    if isinstance(node, frag_base.FRAGNode):
        # If we just have a FRAGNode return the root.
        return node.get_frag_root()

    frag_node = frag_base.is_frag_node(node)
    if frag_node:
        # If we have the pynode of a FRAGNode return the root
        return frag_node.get_frag_root()

    if isinstance(node, pm.Attribute):
        # If we have an attr convert it into the base PyNode
        node = node.node()

    dag_parent = dag_utils.get_absolute_parent(node)
    if dag_parent.hasAttr('frag_parent'):
        # If the absolute parent of the PyNode has a connection to a FRAGNode
        frag_node = frag_base.FRAGNode(dag_parent.getAttr('frag_parent'))
        if frag_node:
            return frag_node.get_frag_root()

def get_all_frag_roots(asset_id=None):
    """
    Return all FRAGRoots, optionally limited to those with a matching asset_id

    :param str asset_id: An asset ID to match by
    :return: A list of all FRAGRoots
    :rtype: list[FRAGRoot]
    """
    return_list = []
    for network_node in pm.ls('*.frag_type', r=True, o=True):
        if network_node.getAttr('frag_type') == 'FRAGRoot':
            frag_node = frag_base.FRAGNode(network_node)
            if asset_id and frag_node.asset_id != asset_id:
                continue
            return_list.append(frag_node)
    return return_list
