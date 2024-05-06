#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
import string

# software specific imports
import pymel.core as pm
from mca.common.utils import strings
#  python imports


def get_basename(node, remove_namespace=True, remove_attribute=False):
    """
    Get the base name in a hierarchy name (a|b|c -> returns c).

    :param str or pm.PyNode or FRAGNode node: name to get base name from.
    :param bool remove_namespace: whether to remove or not namespace from the base name.
    :param bool remove_attribute: whether to remove or not attribute from the base name.
    :return: base name of the given node name.
    :rtype: str
    """

    node_name = node if isinstance(node, str) else node.longName()
    split_name = node_name.split('|')
    base_name = split_name[-1]

    if remove_attribute:
        base_name_split = base_name.split('.')
        base_name = base_name_split[0]

    if remove_namespace:
        split_base_name = base_name.split(':')
        return split_base_name[-1]

    return base_name


def get_unique_dagname(node_name):
    """Returns passed name if unique otherwise appends numerals until it is.

    :param str node_name: Potential base name.
    :return: Base name if unique otherwise append numerals.
    :rtype: str
    """
    
    if not node_name:
        raise ValueError(f'{node_name} is None or empty.')
    if not pm.objExists(node_name):
        return node_name

    counter = strings.get_trailing_numbers(node_name) or 0

    while pm.objExists(node_name):
        counter += 1
        node_name = f'{node_name.rstrip(string.digits)}{counter}'
    return node_name


def remove_illegal_characters(node_name):
    """
    Converts a given string to match Maya's naming conventions.

    :param str node_name: String name.
    :return: str A string that meets Maya's requirement.
    :rtype: str
    """
    
    if len(node_name) >= 1 and node_name != " ":
        if node_name[0] == ' ':
            node_name = node_name[1:len(node_name)]
            remove_illegal_characters(node_name)
        elif node_name[-1] == ' ':
            node_name = node_name[0:-1]
            remove_illegal_characters(node_name)
        else:
            node_name = node_name.replace(' ', '_')
            return node_name
    return ''


def make_maya_safe_name(node_name, make_unique=False):
    """
    Makes a string a mya safe name for objects.

    :param str node_name: Desired name of the object.
    :param bool make_unique: If the end result should have no conflicts with the existing objects in the scene. This will be done by adding numerals as a suffix.
    :return: A mya safe name.
    :rtype: str
    """

    if node_name and node_name[0].isdigit():
        # If name starts with a digit add an alpha character to the head.
        node_name = 'a'+node_name

    node_name = remove_illegal_characters(node_name)
    if make_unique:
        node_name = get_unique_dagname(node_name)

    return node_name


def get_node_name_parts(node_name):
    """
    Breaks different Maya node name parts and returns them in a tuple:
        - node_name: a:a:grpA|a:a:grpB|a:b:pSphere1
        - long_prefix: a:a:grpA|a:a:grpB
        - namespace: 'a:b
        - basename': 'pSphere1'

    :param str node_name: name of Maya node to retrieve name parts of.
    :return: tuple with long_prefix, namespace and basename.
    :rtype: tuple(str, str, str)
    """

    if '|' in node_name:
        obj_name = str(node_name)
        long_name_parts = obj_name.split('|')
        long_prefix = ''.join(long_name_parts[:-1])
        short_name = long_name_parts[-1]
    else:
        short_name = node_name
        long_prefix = ''

    if ':' in short_name:
        namespace_parts = short_name.split(':')
        base_name = namespace_parts[-1]
        namespace = ':'.join(namespace_parts[:-1])
    else:
        base_name = short_name
        namespace = ''

    return long_prefix, namespace, base_name
