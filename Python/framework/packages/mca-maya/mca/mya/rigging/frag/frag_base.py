#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generic Meta Node class
"""

import importlib
import logging

import pymel.core as pm
import maya.cmds as cmds

from mca.common.utils import lists
from mca.mya.utils import attr_utils
from mca.mya.startup.configs import ma_consts

FRAG_TYPE_ATTR = 'fragType'


def is_frag_node(node):
    result = False
    if isinstance(node, FRAGNode):
        result = True
    else:
        if not isinstance(node, pm.PyNode):
            if pm.objExists(node):
                node = pm.PyNode(node)
            else:
                print('Type filter found that node does not exist in the scene. Skipping - "{0}"'.format(node))
    if isinstance(node, pm.nt.Network):
        result = attr_utils.has_attribute(node, 'xrigType') or attr_utils.has_attribute(node, FRAG_TYPE_ATTR)

    return result


def get_frag_parent(node):
    node = pm.PyNode(node)
    result = None

    if isinstance(node, pm.nt.DependNode):
        if attr_utils.has_attribute(node, 'fragParent'):
            conn = cmds.listConnections(str(node) + '.fragParent')
            if conn:
                result = FRAGNode(conn[0])
    return result


def _import_external_frag_node_package(frag_node_type):
    """
    Import FRAGNode package locations that were registered at startup then check to see if the given FRAGNode type
    exists in any of them. This utility assumes that the FRAGNode type was not found within this base package.
    The very act of importing registers FRAGNode classes to a dictionary of known types so this just returns True
    to indicate that our FRAGNode type was found. Then whatever is calling this utility can sort out the rest.

    :param str frag_node_type: frag node class name from FRAGNode's get_type()
    :return bool: True if a package was found and imported with the given FRAGNode type
    """

    for node_package_path in ma_consts.FRAG_NODE_PACKAGE_PATHS:
        # If the package path is THIS package then we can skip it since if the
        # FRAG Node lived here it would have been imported and found already
        if __package__ == node_package_path:
            continue

        # Make sure the external package is imported. These packages were registered at
        # startup and will be different depending on the project context.
        package = importlib.import_module(node_package_path)
        if hasattr(package, frag_node_type):
            frag_class = getattr(package, frag_node_type)
            if issubclass(frag_class, FRAGNode):
                # We imported the package, found the class, and verified it inherited from FRAGNode
                return True

    return False


class FRAGNodeRegister(type):
    """
    Metaclass for tracking all FRAGNode classes in the import path.
    """

    __frag_node_types__ = dict()

    def __init__(cls, *args, **kwargs):
        super(FRAGNodeRegister, cls).__init__(*args, **kwargs)
        # Check for clashing class names on FRAGNodes. New FRAGNodes require unique class names!
        if cls.__name__ in cls.__frag_node_types__:
            clash_path = cls.__module__ + '.' + cls.__name__
            existing_class = cls.__frag_node_types__[cls.__name__]
            existing_path = existing_class.__module__ + '.' + existing_class.__name__
            # If we reload() and the exact same class is registered things are fine, but if a clashing class name is
            # registered from a different module raise an exception.
            if clash_path != existing_path:
                raise LookupError(
                    "FRAG Node {} name clashes with existing FRAG Node {}.".format(clash_path, existing_path))
        else:
            cls.__frag_node_types__[cls.__name__] = cls


class FRAGNode(object, metaclass=FRAGNodeRegister):

    VERSION = 1

    # Overwrite of __new__ allows wrapping any FRAGNode in the base FRAGNode class and getting the correct subclass
    # returned
    def __new__(cls, node=None):
        if node:
            if not isinstance(node, pm.PyNode):
                node = pm.PyNode(node)
            # Check if node is a network.
            if not isinstance(node, pm.nt.Network):
                raise TypeError("Node {0} is not a network node and can't be a FRAG Node.".format(node))
            elif attr_utils.has_attribute(node, FRAG_TYPE_ATTR):
                class_string = attr_utils.get_attribute(node, FRAG_TYPE_ATTR, attr_type='string')
            else:
                raise TypeError("Node {0} is not a FRAG Node.".format(node))

            if class_string in cls.__frag_node_types__:
                frag_class = cls.__frag_node_types__[class_string]
                return frag_class.__new__(frag_class)
            elif _import_external_frag_node_package(class_string):
                frag_class = cls.__frag_node_types__[class_string]
                return frag_class.__new__(frag_class)
            raise TypeError("FRAGNode {0} does not exist in register.".format(class_string))
        else:
            return super(FRAGNode, cls).__new__(cls)

    def __init__(self, node):
        if not isinstance(node, pm.PyNode):
            node = pm.PyNode(node)
        self.pynode = node

    @staticmethod
    def create(frag_parent, frag_type, version):
        """
        Creates a FRAGNode of given frag_type.

        :param frag_parent:
        :param frag_type:
        :param version:
        :return:
        """

        if frag_parent:
            frag_parent = FRAGNode(frag_parent)
        # Create node
        node = pm.createNode("network", n=str(frag_type))

        # Add attributes
        node.addAttr("version", at='double')
        node.version.set(version)
        node.addAttr(FRAG_TYPE_ATTR, dt='string')
        node.attr(FRAG_TYPE_ATTR).set(frag_type)
        node.addAttr("fragChildren", at='message')
        node.addAttr("fragParent", at='message')
        node = FRAGNode(node)
        if frag_parent:
            node.set_frag_parent(frag_parent)
        return node

    def connect_node(self, node, attr, parent_attr=None):
        node_to_connect = node
        if not isinstance(node, pm.PyNode):
            if hasattr(node, 'node'):
                node_to_connect = node.node
            else:
                node_to_connect = pm.PyNode(node)

        if parent_attr:
            if not node.hasAttr(parent_attr):
                node.addAttr(parent_attr, at='message')
            node_to_connect = node.attr(parent_attr)
        attr_utils.set_attribute(self.pynode, {attr: node_to_connect})

    def connect_nodes(self, connect_nodes, attr, parent_attr=None, merge_values=False):
        """
        Connects the node to frag node at given attr.

        :param list[PyNode] connect_nodes: A list of pynodes to connect to this FRAGNode
        :param str attr: Attr on this FRAGNode to connect with.
        :param str parent_attr: The name of the parent attr on the connected nodes that should be used to form the connection
            NOTE this will override the connection when used so last connected will be the final value.
        :param bool merge_values: If values already connected should be kept.
        :return:
        """

        if not isinstance(connect_nodes, (list, tuple)):
            connect_nodes = [connect_nodes]

        pynode_list = []
        for node in connect_nodes:
            if not isinstance(node, pm.PyNode):
                if hasattr(node, 'node'):
                    pynode_list.append(node.node)
                    continue
                pynode_list.append(pm.PyNode(node))
                continue
            pynode_list.append(node)

        objs_to_connect = []
        if parent_attr:
            for node in pynode_list:
                if not node.hasAttr(parent_attr):
                    node.addAttr(parent_attr, at='message')
                objs_to_connect.append(node.attr(parent_attr))
        else:
            objs_to_connect = pynode_list

        attr_utils.set_attribute(self.pynode, {attr: objs_to_connect}, merge_values=merge_values)

    def get_frag_parent(self):
        result = None
        if self.has_attribute('fragParent'):
            conn = cmds.listConnections(str(self.pynode) + '.fragParent')
            if conn:
                result = FRAGNode(conn[0])
        return result

    def get_frag_children(self, of_type=None, side=None, region=None):
        """
        From a list of all FRAGNode children return a list of them that match search criteria.

        :param FRAGNode of_type: The specific class of FRAGNode to filter by.
        :param str side: Side identifier of the FRAGNode
        :param str region: Region identifier of the FRAGNode
        :return: A list of FRAGNodes that match the search.
        :rtype: list[FRAGNode]
        """

        return_list = []
        if self.hasAttr('fragChildren'):
            frag_children = self.fragChildren.listConnections()
            for child_node in frag_children:
                wrapped_node = FRAGNode(child_node)

                if side and wrapped_node.side != side:
                    continue

                if side and wrapped_node.region != region:
                    continue

                if of_type and not isinstance(wrapped_node, of_type):
                    continue
                return_list.append(wrapped_node)
        return return_list

    def get_type(self):
        if self.has_attribute(FRAG_TYPE_ATTR):
            return attr_utils.get_attribute(self.pynode, FRAG_TYPE_ATTR, attr_type='string')
        else:
            return None

    def set_frag_parent(self, frag_parent):
        if not is_frag_node(frag_parent):
            raise TypeError("frag node parent given, {0}, isn't a FRAGNode")
        parent_attr = frag_parent.fragChildren
        child_attr = self.fragParent
        parent_attr >> child_attr

    def add_frag_child(self, child):
        child.set_frag_parent(self)

    def get_frag_child(self, of_type=None):
        results = self.get_frag_children(of_type=of_type)
        return lists.get_first_in_list(results)

    def get_pynode(self):
        return self.pynode

    def get_version(self):
        return self.version.get()

    def set_version(self, version):
        self.version.set(version)
    
    def get_frag_root(self, input_node):
        if not is_frag_node(input_node):
            return None
    
        if not isinstance(input_node, FRAGNode):
            input_node = FRAGNode(input_node)
    
        found_root = input_node if input_node.has_attribute('isFragRoot') else None
        frag_parent_node = input_node.get_frag_parent()
        while not found_root and frag_parent_node:
            if frag_parent_node.has_attribute('isFragRoot'):
                found_root = frag_parent_node
            else:
                input_node = frag_parent_node
            frag_parent_node = input_node.get_frag_parent()
        return found_root
    
    def get_asset_id(self, input_node):
        root = self.get_frag_root(input_node=input_node)
        if not root:
            logging.warning('No root was found.  Cannot access the Asset ID.')
            return
        return root.asset_id

    def get_flags(self):
        return[]
    
    @property
    def side(self):
        """
        Returns the side markup on this FRAGNode.

        :return: Returns the side markup on this node.
        :rtype: str
        """

        if self.pynode.hasAttr('side'):
            return self.pynode.getAttr('side')
        return ''

    @side.setter
    def side(self, val):
        """
        Sets the joint as is_start and adds the region.

        :param str val: A name used to define a joint chain.
        """

        if not self.pynode.hasAttr('side'):
            self.pynode.addAttr('side', dt='string')
        self.pynode.setAttr('side', val)

    @property
    def region(self):
        """
        Returns the region markup on this FRAGNode.

        :return: Returns the region markup on this node.
        :rtype: str
        """

        if self.pynode.hasAttr('region'):
            return self.pynode.getAttr('region')
        return ''

    @region.setter
    def region(self, val):
        """
        Sets the FRAGNode's region markup

        :param str val: An identifier for the FRAGNode
        """

        if not self.pynode.hasAttr('region'):
            self.pynode.addAttr('region', dt='string')
        self.pynode.setAttr('region', val)

    def update(self):
        current_version = self.get_version()
        latest_version = self.VERSION
        while current_version < latest_version:
            update_method_name = "_update_version_{0}_to_version_{1}".format(current_version, current_version + 1)
            update_method = getattr(self, update_method_name)
            update_method()
            later_version = self.get_version()
            if later_version == current_version:
                raise AttributeError("Please set the version in your update script: {0}".format(update_method))
            current_version = later_version

    def has_attribute(self, attr_name):
        """
        Efficient way of checking if this FRAG node's PyNode has a particular attribute.

        :param str attr_name: Name of attribute to check for
        :return: True if the attribute exists on the internally stored PyNode
        """

        return attr_utils.has_attribute(self.pynode, attr_name)

    def __str__(self):
        return self.pynode.__str__()

    def __getattr__(self, attrname):
        if attrname == 'pynode':
            raise AttributeError("this instance of {0} has no pynode".format(self.__class__.__name__))
        return getattr(self.pynode, attrname)

    def __melobject__(self):
        return self.pynode.__melobject__()

    def __apimfn__(self):
        return self.pynode.__apimfn__()

    def __repr__(self):
        return self.pynode.__repr__()

    def __radd__(self, other):
        return self.pynode.__radd__(other)

    def __reduce__(self):
        return self.pynode.__reduce__()

    def __eq__(self, other):
        if hasattr(other, "pynode"):
            return self.pynode.__eq__(other.pynode)
        return self.pynode.__eq__(other)

    def __hash__(self):
        return self.pynode.__hash__()

    def __ne__(self, other):
        return self.pynode.__ne__(other)

    def __nonzero__(self):
        return self.pynode.__nonzero__()

    def __lt__(self, other):
        return self.pynode.__lt__(other)

    def __gt__(self, other):
        return self.pynode.__gt__(other)

    def __le__(self, other):
        return self.pynode.__le__(other)

    def __ge__(self, other):
        return self.pynode.__ge__(other)


def get_frag_node_parents(node, of_type=FRAGNode):
    node = pm.PyNode(node)
    result = []
    frag_parent = get_frag_parent(node)
    if frag_parent:
        to_add = []
        if isinstance(frag_parent, of_type):
            to_add = [frag_parent]
        result = to_add + get_frag_node_parents(frag_parent, of_type=of_type)  # direct parent first
    return result


def get_frag_node_descendants(node, of_type=FRAGNode):
    result = []
    if is_frag_node(node):
        node = FRAGNode(node)
        all_children = node.get_frag_children()
        matching_children = [x for x in all_children if isinstance(x, of_type)]
        children_descendants = []
        for child in all_children:
            children_descendants += get_frag_node_descendants(child, of_type=of_type)
        result = matching_children + children_descendants
    return result


def get_all_frag_nodes(of_type=FRAGNode):
    all_networks = cmds.ls(type='network') or []
    all_frag_nodes = [FRAGNode(x) for x in all_networks if is_frag_node(x)]
    matching_frag_nodes = [x for x in all_frag_nodes if isinstance(x, of_type)]
    return matching_frag_nodes


def list_frag_node_connections(object, of_type=FRAGNode):
    # get connected network nodes
    network_nodes = cmds.listConnections(str(object), type='network') or []
    network_nodes = [FRAGNode(x) for x in network_nodes if is_frag_node(x) and isinstance(FRAGNode(x), of_type)]
    return network_nodes


def update_all_frag_nodes():
    all_networks = cmds.ls(type='network') or []
    all_frag_nodes = [FRAGNode(x) for x in all_networks if is_frag_node(x)]
    for x in all_frag_nodes:
        x.update()
