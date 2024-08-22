#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules that interact with transforms
"""

# System global imports
import json
import copy
# software specific imports
import pymel.core as pm

#  python imports
from mca.common.utils import list_utils
from mca.common import log

logger = log.MCA_LOGGER

def is_empty(node, no_user_attributes=True, no_connections=True):
    """
    Returns whether a given node is an empty one (is not referenced, has no child transforms, has no custom attributes
    and has no connections).

    :param pm.PyNode node: name of a Maya node we want to check.
    :param bool no_user_attributes: whether a node is considered empty if it contains user attributes.
    :param bool no_connections: whether a node is considered empty if it contains connections.
    :return: True if the given node is an empty node; False otherwise.
    :rtype: bool
    """

    if pm.referenceQuery(node, isNodeReferenced=True):
        return False

    if isinstance(node, pm.nt.Transform):
        relatives = pm.listRelatives(node)
        if relatives:
            return False

    if no_user_attributes:
        attrs = pm.listAttr(node, userDefined=True, keyable=True)
        if attrs:
            return False

    default_nodes = ['defaultLightSet', 'defaultObjectSet', 'initialShadingGroup', 'uiConfigurationScriptNode',
                     'sceneConfigurationScriptNode']
    if node in default_nodes:
        return False

    if no_connections:
        connections = pm.listConnections(node)
        if connections != ['defaultRenderGlobals']:
            if connections:
                return False

    return True


def create_or_find(name, node_type):
    """
    Find by name or create a new node of the given type.

    :param str name: The desired name of the new node.
    :param PyNode node_type: The PyNode class of the node type.
    :return: The created or found PyNode.
    :rtype: PyNode
    """

    node = lists.get_first_in_list(pm.ls(name, r=True, type=node_type))
    if not node:
        node = pm.createNode(node_type, n=name)
    return node