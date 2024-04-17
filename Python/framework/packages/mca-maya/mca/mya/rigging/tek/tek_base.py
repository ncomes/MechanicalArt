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

TEK_TYPE_ATTR = 'tekType'


def is_tek_node(node):
    result = False
    if isinstance(node, TEKNode):
        result = True
    else:
        if not isinstance(node, pm.PyNode):
            if pm.objExists(node):
                node = pm.PyNode(node)
            else:
                print('Type filter found that node does not exist in the scene. Skipping - "{0}"'.format(node))
    if isinstance(node, pm.nt.Network):
        result = attr_utils.has_attribute(node, 'teksType') or attr_utils.has_attribute(node, TEK_TYPE_ATTR)

    return result


def get_tek_parent(node):
    node = pm.PyNode(node)
    result = None

    if isinstance(node, pm.nt.DependNode):
        if attr_utils.has_attribute(node, 'tekParent'):
            conn = cmds.listConnections(str(node) + '.tekParent')
            if conn:
                result = TEKNode(conn[0])
    return result


def _import_external_tek_node_package(tek_node_type):
    """
    Import TEKNode package locations that were registered at startup then check to see if the given TEKNode type
    exists in any of them. This utility assumes that the TEKNode type was not found within this base package.
    The very act of importing registers TEKNode classes to a dictionary of known types so this just returns True
    to indicate that our TEKNode type was found. Then whatever is calling this utility can sort out the rest.

    :param str tek_node_type: tek node class name from TEKNode's get_type()
    :return bool: True if a package was found and imported with the given TEKNode type
    """

    for node_package_path in ma_consts.TEK_NODE_PACKAGE_PATHS:
        # If the package path is THIS package then we can skip it since if the
        # TEK Node lived here it would have been imported and found already
        if __package__ == node_package_path:
            continue

        # Make sure the external package is imported. These packages were registered at
        # startup and will be different depending on the project context.
        package = importlib.import_module(node_package_path)
        if hasattr(package, tek_node_type):
            tek_class = getattr(package, tek_node_type)
            if issubclass(tek_class, TEKNode):
                # We imported the package, found the class, and verified it inherited from TEKNode
                return True

    return False


class TEKNodeRegister(type):
    """
    Metaclass for tracking all TEKNode classes in the import path.
    """

    __tek_node_types__ = dict()

    def __init__(cls, *args, **kwargs):
        super(TEKNodeRegister, cls).__init__(*args, **kwargs)
        # Check for clashing class names on TEKNodes. New TEKNodes require unique class names!
        if cls.__name__ in cls.__tek_node_types__:
            clash_path = cls.__module__ + '.' + cls.__name__
            existing_class = cls.__tek_node_types__[cls.__name__]
            existing_path = existing_class.__module__ + '.' + existing_class.__name__
            # If we reload() and the exact same class is registered things are fine, but if a clashing class name is
            # registered from a different module raise an exception.
            if clash_path != existing_path:
                raise LookupError(
                    "TEK Node {} name clashes with existing TEK Node {}.".format(clash_path, existing_path))
        else:
            cls.__tek_node_types__[cls.__name__] = cls


class TEKNode(object, metaclass=TEKNodeRegister):

    VERSION = 1

    # Overwrite of __new__ allows wrapping any TEKNode in the base TEKNode class and getting the correct subclass
    # returned
    def __new__(cls, node=None):
        if node:
            if not isinstance(node, pm.PyNode):
                node = pm.PyNode(node)
            # Check if node is a network.
            if not isinstance(node, pm.nt.Network):
                raise TypeError("Node {0} is not a network node and can't be a TEK Node.".format(node))
            elif attr_utils.has_attribute(node, TEK_TYPE_ATTR):
                class_string = attr_utils.get_attribute(node, TEK_TYPE_ATTR, attr_type='string')
            else:
                raise TypeError("Node {0} is not a TEK Node.".format(node))

            if class_string in cls.__tek_node_types__:
                tek_class = cls.__tek_node_types__[class_string]
                return tek_class.__new__(tek_class)
            elif _import_external_tek_node_package(class_string):
                tek_class = cls.__tek_node_types__[class_string]
                return tek_class.__new__(tek_class)
            raise TypeError("TEKNode {0} does not exist in register.".format(class_string))
        else:
            return super(TEKNode, cls).__new__(cls)

    def __init__(self, node):
        if not isinstance(node, pm.PyNode):
            node = pm.PyNode(node)
        self.pynode = node

    @staticmethod
    def create(tek_parent, tek_type, version):
        """
        Creates a TEKNode of given tek_type.

        :param tek_parent:
        :param tek_type:
        :param version:
        :return:
        """

        if tek_parent:
            tek_parent = TEKNode(tek_parent)
        # Create node
        node = pm.createNode("network", n=str(tek_type))

        # Add attributes
        node.addAttr("version", at='double')
        node.version.set(version)
        node.addAttr(TEK_TYPE_ATTR, dt='string')
        node.attr(TEK_TYPE_ATTR).set(tek_type)
        node.addAttr("tekChildren", at='message')
        node.addAttr("tekParent", at='message')
        node = TEKNode(node)
        if tek_parent:
            node.set_tek_parent(tek_parent)
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
        Connects the node to tek node at given attr.

        :param list[PyNode] connect_nodes: A list of pynodes to connect to this TEKNode
        :param str attr: Attr on this TEKNode to connect with.
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

    def get_tek_parent(self):
        result = None
        if self.has_attribute('tekParent'):
            conn = cmds.listConnections(str(self.pynode) + '.tekParent')
            if conn:
                result = TEKNode(conn[0])
        return result

    def get_tek_children(self, of_type=None, side=None, region=None):
        """
        From a list of all TEKNode children return a list of them that match search criteria.

        :param TEKNode of_type: The specific class of TEKNode to filter by.
        :param str side: Side identifier of the TEKNode
        :param str region: Region identifier of the TEKNode
        :return: A list of TEKNodes that match the search.
        :rtype: list[TEKNode]
        """

        return_list = []
        if self.hasAttr('tekChildren'):
            tek_children = self.tekChildren.listConnections()
            for child_node in tek_children:
                wrapped_node = TEKNode(child_node)

                if side and wrapped_node.side != side:
                    continue

                if side and wrapped_node.region != region:
                    continue

                if of_type and not isinstance(wrapped_node, of_type):
                    continue
                return_list.append(wrapped_node)
        return return_list

    def get_type(self):
        if self.has_attribute(TEK_TYPE_ATTR):
            return attr_utils.get_attribute(self.pynode, TEK_TYPE_ATTR, attr_type='string')
        else:
            return None

    def set_tek_parent(self, tek_parent):
        if not is_tek_node(tek_parent):
            raise TypeError("tek node parent given, {0}, isn't a TEKNode")
        parent_attr = tek_parent.tekChildren
        child_attr = self.tekParent
        parent_attr >> child_attr

    def add_tek_child(self, child):
        child.set_tek_parent(self)

    def get_tek_child(self, of_type=None):
        results = self.get_tek_children(of_type=of_type)
        return lists.get_first_in_list(results)

    def get_pynode(self):
        return self.pynode

    def get_version(self):
        return self.version.get()

    def set_version(self, version):
        self.version.set(version)
    
    def get_tek_root(self, input_node):
        if not is_tek_node(input_node):
            return None
    
        if not isinstance(input_node, TEKNode):
            input_node = TEKNode(input_node)
    
        found_root = input_node if input_node.has_attribute('isFragRoot') else None
        tek_parent_node = input_node.get_tek_parent()
        while not found_root and tek_parent_node:
            if tek_parent_node.has_attribute('isFragRoot'):
                found_root = tek_parent_node
            else:
                input_node = tek_parent_node
            tek_parent_node = input_node.get_tek_parent()
        return found_root
    
    def get_asset_id(self, input_node):
        root = self.get_tek_root(input_node=input_node)
        if not root:
            logging.warning('No root was found.  Cannot access the Asset ID.')
            return
        return root.asset_id

    def get_flags(self):
        return[]
    
    @property
    def side(self):
        """
        Returns the side markup on this TEKNode.

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
        Returns the region markup on this TEKNode.

        :return: Returns the region markup on this node.
        :rtype: str
        """

        if self.pynode.hasAttr('region'):
            return self.pynode.getAttr('region')
        return ''

    @region.setter
    def region(self, val):
        """
        Sets the TEKNode's region markup

        :param str val: An identifier for the TEKNode
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
        Efficient way of checking if this TEK node's PyNode has a particular attribute.

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


def get_tek_node_parents(node, of_type=TEKNode):
    node = pm.PyNode(node)
    result = []
    tek_parent = get_tek_parent(node)
    if tek_parent:
        to_add = []
        if isinstance(tek_parent, of_type):
            to_add = [tek_parent]
        result = to_add + get_tek_node_parents(tek_parent, of_type=of_type)  # direct parent first
    return result


def get_tek_node_descendants(node, of_type=TEKNode):
    result = []
    if is_tek_node(node):
        node = TEKNode(node)
        all_children = node.get_tek_children()
        matching_children = [x for x in all_children if isinstance(x, of_type)]
        children_descendants = []
        for child in all_children:
            children_descendants += get_tek_node_descendants(child, of_type=of_type)
        result = matching_children + children_descendants
    return result


def get_all_tek_nodes(of_type=TEKNode):
    all_networks = cmds.ls(type='network') or []
    all_tek_nodes = [TEKNode(x) for x in all_networks if is_tek_node(x)]
    matching_tek_nodes = [x for x in all_tek_nodes if isinstance(x, of_type)]
    return matching_tek_nodes


def list_tek_node_connections(object, of_type=TEKNode):
    # get connected network nodes
    network_nodes = cmds.listConnections(str(object), type='network') or []
    network_nodes = [TEKNode(x) for x in network_nodes if is_tek_node(x) and isinstance(TEKNode(x), of_type)]
    return network_nodes


def update_all_tek_nodes():
    all_networks = cmds.ls(type='network') or []
    all_tek_nodes = [TEKNode(x) for x in all_networks if is_tek_node(x)]
    for x in all_tek_nodes:
        x.update()
