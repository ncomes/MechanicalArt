#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to base FRAGNodes and their usage.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import flags
from mca.mya.utils import attr_utils, namespace_utils


class FRAGNodeRegister(type):
    """
    Metaclass for tracking all FRAGNode classes in the import path.
    """

    _FRAGNODE_TYPES = dict()

    def __init__(cls, *args, **kwargs):
        super(FRAGNodeRegister, cls).__init__(*args, **kwargs)
        # Check for clashing class names on FRAGNodes. New FRAGNodes require unique class names!
        if cls.__name__ in cls._FRAGNODE_TYPES:
            clash_path = cls.__module__ + '.' + cls.__name__
            existing_class = cls._FRAGNODE_TYPES[cls.__name__]
            existing_path = existing_class.__module__ + '.' + existing_class.__name__
            # If we reload() and the exact same class is registered things are fine, but if a clashing class name is
            # registered from a different module raise an exception.
            if clash_path != existing_path:
                raise LookupError(f"FRAG Node {clash_path} name clashes with existing FRAG Node {existing_path}.")
        else:
            cls._FRAGNODE_TYPES[cls.__name__] = cls


class FRAGNode(object, metaclass=FRAGNodeRegister):
    """
    Rough breakdown for class inheritance.

    FRAGNode - Base node everything inherits from.

	FRAGRoot - Represents a whole asset.

	FRAGROOTSingle
		FRAGMesh - Handles mesh groups. (including blendshapes)
		FRAGDisplay - Handles managing display layers
		FRAGRig - Core of the rig, contains a link to all rig components.

	FRAGComponent - Must be children of a FRAGRig
		FRAGAnimatedfComponent
				Bake from a skeleton
			CogComponent - Limit 1
			RootComponent - Limit 1

			<<RIG>>Component

		TwistComponent

    FragSequencer

    """
    _version = 1.0
    pynode = None
    def __new__(cls, node=None):
        if isinstance(node, FRAGNode):
            return node
        if node:
            frag_node_type = None
            if not isinstance(node, pm.nt.Network):
                raise TypeError(f'{node} is not a network node and can\'t be a FRAG Node.')
            elif node.hasAttr('frag_type'):
                frag_node_type = node.getAttr('frag_type')
            else:
                raise TypeError(f'{node} is not a valid FRAG Node')
            if frag_node_type in cls._FRAGNODE_TYPES:
                frag_class = cls._FRAGNODE_TYPES.get(frag_node_type)
                return frag_class.__new__(frag_class)
            raise TypeError(f'FRAGNode {frag_node_type} does not exist in register.')

        else:
            return super(FRAGNode, cls).__new__(cls)

    def __init__(self, node):
        # Inititalize a FRAGNode off an existing network node.
        if not isinstance(node, pm.nt.Network):
            return
        self.pynode = node

    # These two class overrides are important as it lets us look up the wrapper in lists or dicts.
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.pynode == other.pynode
        return False
    
    def __hash__(self):
        return hash(self.pynode)

    @classmethod
    @ma_decorators.keep_namespace_decorator
    def create(cls, **kwargs):
        """
        Some universal things this handles.
        If there is a frag_parent it'll build the nodes under the parent namespace.
        Sets the frag_type
        Connects to a frag_parent if provided.

        :param FRAGNode frag_parent: Parent FRAGNode for the newly created FRAGNode
        :return: The newly created FRAGNode
        :rtype: FRAGNode
        """
        frag_parent = kwargs.get('frag_parent')
        if frag_parent:
            root_namespace = frag_parent.namespace
            namespace_utils.set_namespace(root_namespace, check_existing=False)

        network_node = pm.createNode(pm.nt.Network, n=cls.__name__)
        network_node.addAttr('frag_type', dt='string')
        network_node.setAttr('frag_type', cls.__name__)

        new_frag_node = FRAGNode(network_node)

        new_frag_node.version = cls._version
        if frag_parent:
            new_frag_node.frag_parent = frag_parent
        return new_frag_node

    @ma_decorators.keep_namespace_decorator
    def _create_managed_group(self, group_name):
        """
        Singular spot to setup groups in the same namespace as this FRAGNode.

        :param str group_name: Name for the new managed group.
        :return: The Transform that represents the new empty group.
        :rtype: Transform
        """
        root_namespace = self.namespace
        namespace_utils.set_namespace(root_namespace, check_existing=False)

        new_group = pm.group(n=group_name, em=True, w=True)
        return new_group

    def remove(self):
        try:
            pm.delete(self.pynode)
        except:
            pass

    @property
    def version(self):
        if self.pynode.hasAttr('frag_version'):
            return self.pynode.getAttr('frag_version')

    @version.setter
    def version(self, val):
        if not self.pynode.hasAttr('frag_version'):
            self.pynode.addAttr('frag_version', at='float')
        self.pynode.setAttr('frag_version', val)

    @property
    def frag_type(self):
        if self.pynode.hasAttr('frag_type'):
            return self.pynode.getAttr('frag_type')

    @frag_type.setter
    def frag_type(self, val):
        if not self.pynode.hasAttr('frag_type'):
            self.pynode.addAttr('frag_type', dt='string')
        self.pynode.setAttr('frag_type', val)

    @property
    def frag_parent(self):
        if self.pynode.hasAttr('frag_parent'):
            return FRAGNode(self.pynode.getAttr('frag_parent'))

    @frag_parent.setter
    def frag_parent(self, frag_node):
        if isinstance(frag_node, FRAGNode):
            self.connect_node(frag_node, 'frag_parent')
            frag_node.frag_children += [self.pynode]
        else:
            raise TypeError('FRAG Parent must be a FRAGNode')

    @property
    def frag_children(self):
        if self.pynode.hasAttr('frag_children'):
            return [FRAGNode(x) for x in self.pynode.getAttr('frag_children')]
        return []

    @frag_children.setter
    def frag_children(self, node_list):
        # Just some logic to convert the call to frag_children back into pynodes to handle the connect.
        nodes_to_connect = []
        for node in node_list:
            if isinstance(node, FRAGNode):
                nodes_to_connect.append(node.pynode)
            elif isinstance(node, pm.PyNode):
                nodes_to_connect.append(node)
        self.connect_nodes(nodes_to_connect, attr_name='frag_children')

    @property
    def asset_id(self):
        """
        From the FRAGRoot return the asset_id registered

        :return: The guid representative of this FRAGRoot
        :rtype: str
        """
        frag_root = self.get_frag_root()

        if frag_root and hasattr(frag_root, 'asset_id'):
            return frag_root.asset_id

        else:
            ('Failed to find a root with asset_id markup.')
            return
        
    @property
    def asset_name(self):
        """
        From the FRAGRoot return the asset_name registered

        :return: The asset name representative of this FRAGRoot
        :rtype: str
        """
        frag_root = self.get_frag_root()

        if frag_root and hasattr(frag_root, 'asset_name'):
            return frag_root.asset_name

        else:
            ('Failed to find a root with asset_name markup.')
            return


    def connect_node(self, node, attr_name, parent_attr=None):
        """
        Connect from a node or attribute to this network node via a message connection to a new attribute
        of attr_name.

        :param PyNode node: A PyNode instance, often transforms, or attributes.
        :param str attr_name: The name of the attribute the passed object should be connected to.
        :param str parent_attr: If the passed object should use a specific attribute to connect with.
        """
        if not node:
            return
        if not attr_name:
            return

        node_to_connect = node
        if isinstance(node, (FRAGNode, flags.Flag)):
            node_to_connect = node.pynode
        elif not isinstance(node, pm.PyNode):
            if hasattr(node, 'node'):
                node_to_connect = node.node
            else:
                node_to_connect = pm.PyNode(node)

        if parent_attr:
            if not node_to_connect.hasAttr(parent_attr):
                node_to_connect.addAttr(parent_attr, at='message')
            node_to_connect = node_to_connect.attr(parent_attr)
        attr_utils.set_attribute(self.pynode, {attr_name: node_to_connect})


    def connect_nodes(self, node_list, attr_name, parent_attr=None, merge_values=False):
        """
        Connect from a list of nodes or attributes to this FRAG node via a message connection to a new multi
        attribute of attr_name.

        :param list[PyNode] node_list: A list of PyNodes, often transforms, or attributes.
        :param str attr_name: The name of the attribute the passed objects should be connected to.
        :param str parent_attr: If the passed objects should use a specific attribute to connect with.
        :param bool merge_values: If the values on this FRAG node should be kept when adding the new connections.
        """
        if not isinstance(node_list, (list, tuple)):
            node_list = [node_list]

        pynode_list = []
        for node in node_list:
            if isinstance(node, (FRAGNode, flags.Flag)):
                pynode_list.append(node.pynode)
                continue
            elif not isinstance(node, pm.PyNode):
                if hasattr(node, 'node'):
                    pynode_list.append(node.node)
                    continue
                pynode_list.append(pm.PyNode(node))
                continue
            else:
                pynode_list.append(node)

        nodes_to_connect = []
        if parent_attr:
            for node in pynode_list:
                if not node.hasAttr(parent_attr):
                    node.addAttr(parent_attr, at='message')
                nodes_to_connect.append(node.attr(parent_attr))
        else:
            nodes_to_connect = pynode_list

        attr_utils.set_attribute(self.pynode, {attr_name: nodes_to_connect}, merge_values=merge_values)

    @property
    def namespace(self):
        frag_root = self.get_frag_root()
        return frag_root.pynode.namespace().split(':')[0]

    def get_frag_root(self):
        """
        Recursively check each FRAGNode for a parent connection and return it.

        :return: The highest FRAGNode in this hierarchy.
        :rtype: FRAGNode
        """
        frag_root = self

        while frag_root.frag_parent:
            if frag_root.frag_type == 'FRAGRoot':
                # If we find a FRAGRoot immediately return it.
                return frag_root
            frag_root = frag_root.frag_parent

        return frag_root


    def get_frag_children(self, frag_type=None, side=None, region=None, **kwargs):
        recursive = (kwargs.get('r') or kwargs.get('recursive')) or False

        return_list = []
        for frag_child in self.frag_children:
            if isinstance(frag_type, str):
                if frag_child.frag_type != frag_type:
                    continue
            elif frag_type and not isinstance(frag_child, frag_type):
                continue
            if side and side != frag_child.side:
                continue
            if region and region != frag_child.region:
                continue
            return_list.append(frag_child)
            if recursive:
                return_list += frag_child.frag_children(frag_type, side, region)
        return return_list


def is_frag_node(node):
    """
    Return the FRAGNode of a given object if it is one. Combined is/get fnc.

    :param PyNode node: The node we want to check if it is a FRAGNode
    :return: The object's FRAGNode class representation
    :rtype: FRAGNode
    """
    frag_node = None
    if isinstance(node, FRAGNode):
        frag_node = node
    else:
        if isinstance(node, pm.nt.Network):
            if pm.objExists(node) and node.hasAttr('frag_type'):
                frag_node = FRAGNode(node)
    return frag_node

def get_all_frag_nodes(frag_type=None):
    network_node_list = pm.ls('*.frag_type', r=True, o=True)
    return_list = []
    for network_node in network_node_list:
        frag_node = FRAGNode(network_node)
        if frag_type:
            if isinstance(frag_type, str) and frag_node.frag_type != frag_type:
                continue
            elif not isinstance(frag_node, frag_type):
                continue
        return_list.append(frag_node)
    return return_list
