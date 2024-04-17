#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# python imports

# software specific imports
import pymel.core as pm
#  python imports
from mca.common import log
from mca.mya.utils import naming

logger = log.MCA_LOGGER


DEFAULT_NAMESPACES = ["UI", "shared", ':' + "UI", ':' + "shared"]


def set_namespace(namespace_name, check_existing=True):
    """
    Create/set the current namespace to a given value.

    :param str namespace_name: The namespace we wish to set as current.
    :param bool check_existing: Whether to check to see if the namespace already exists.

    """

    pm.namespace(set=':')
    if namespace_name == ':':
        return

    if not namespace_name or not isinstance(namespace_name, str):
        if namespace_name != '':
            logger.warning(f'{namespace_name} is not a valid name for a namespace.')
        return
    if check_existing:
        # Checks to see if namespace already exists, increments if so
        if pm.namespace(exists=namespace_name):
            new_name = find_unique_namespace(namespace_name)
            namespace_name = naming.make_maya_safe_name(new_name)
    if not pm.namespace(exists=namespace_name):
        pm.namespace(addNamespace=namespace_name)
    pm.namespace(set=namespace_name)


def get_all_namespaces(exclude_list=None):
    """
    Returns all the available namespaces in current scene.

    :return: list of namespaces in current scene.
    :rtype: list(str)
    """

    if not exclude_list:
        exclude_list = DEFAULT_NAMESPACES[:]
    else:
        exclude_list.extend(DEFAULT_NAMESPACES)

    namespaces = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    namespaces = list(set(namespaces) - set(exclude_list))
    namespaces = sorted(namespaces)

    return namespaces


def find_unique_namespace(namespace, increment_fn=None):
    """
    Returns a unique namespace based on the given namespace which does not exists in current scene.

    :param str namespace: namespace to find unique name of.
    :param callable(str, int) increment_fn: function that returns a unique name generated from the namespace and the
        index representing current iterator. If not specified a new namespace will be generated based on an index
        at the end of the namespace.
    :return: unique namespace that is guaranteed not to exists below the current namespace.
    :rtype: str
    """

    def _increment(b, i):
        return "%s%02i" % (b, i)

    # if given namespace does not exist, we use it
    if not pm.namespace(exists=namespace):
        return namespace

    if namespace.endswith(':'):
        namespace = namespace[:-1]

    if not increment_fn:
        increment_fn = _increment

    index = 1
    while True:
        test_namespace = increment_fn(namespace, index)
        index += 1
        if not pm.namespace(exists=test_namespace):
            return test_namespace


def get_namespace(name, check_node=True, top_only=True):
    """
    Returns the namespace of the given Maya node name (short name or full name).

    :param str name: str, node to get namespace from.
    :param bool check_node: whether if object exist should be check or not.
    :param bool top_only: whether to return top level namespace only or not.
    :return: namespace of the given node.
    :rtype: str
    """

    namespace = ''

    if not name.endswith(':'):
        name = name+':'

    if check_node:
        if not pm.namespace(exists=name):
            logger.debug('Impossible to retrieve namespace because object "{}" does not exist!'.format(name))
            return namespace

    if not name.count(':'):
        return namespace

    namespace = name.split(':')[0] if top_only else name.replace(':' + name.split(':')[-1], '')

    return namespace


def get_all_nodes_in_namespace(namespace_name, recursive=False):
    """
    Returns all the dependency nodes contained in the given namespace.

    :param str namespace_name: name of the namespace we want to retrieve all nodes of.
    :param bool recursive: If child namespaces should be searched as well.
    :return: list of dependency Maya nodes assigned to the give namespace.
    :rtype: list(str)
    """

    try:
        # try to wrap a namespace by name. If it fails it doesn't exist. It's like doing the exist check and assignment
        # all at once.
        search_namespace = pm.Namespace(namespace_name)
    except:
        logger.warning(f'Namespace "{namespace_name}" does not exist!')
        return list()

    return_list = search_namespace.ls()
    if recursive:
        for child_namespace in search_namespace.listNamespaces(recursive=True):
            return_list += child_namespace.ls()

    return return_list


def delete_empty_namespaces():
    """
    Removes all namespaces in current scene that are empty recursively starting from the bottom namespaces
    until the top one.

    :return: list of deleted namespaces.
    :rtype: list(str)
    """

    delete_namespaces = list()

    def _namespace_children_count(ns):
        return ns.count(':')

    # retrieve namespaces and sort them in a way that namespaces with more children are located at the front
    namespace_list = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    namespace_list.sort(key=_namespace_children_count, reverse=True)

    for namespace in namespace_list:
        try:
            pm.namespace(removeNamespace=namespace)
            delete_namespaces.append(namespace)
        except RuntimeError:
            pass

    if delete_namespaces:
        logger.debug('Namespaces removed: {}'.format(delete_namespaces))

    return delete_namespaces


def move_node_to_namespace(node, namespace_name):
    """
    Rename a given object to place it under a given namespace.

    :param PyNode node: A given object we want to place under a namespace.
    :param str namespace_name: The namespace we want to attempt to the object under.
    """

    try:
        node_name = naming.get_basename(node)
        node.rename(f':{namespace_name}:{node_name}') if namespace_name else node.rename(f'{node_name}')
    except:
        pass


def purge_namespace(namespace_name):
    """
    Deletes the named namespace and everything in it.

    :param str namespace_name: Name of a namespace
    :return:
    """

    pm.namespace(set=':')
    # don't purge root namespace
    if not namespace_name or namespace_name == ':':
        logger.warning('Can\'t purge root namespace.')
        return

    try:
        # try to wrap a namespace by name. If it fails it doesn't exist. It's like doing the exist check and assignment
        # all at once.
        search_namespace = pm.Namespace(namespace_name)

        for child_namespace in search_namespace.listNamespaces():
            purge_namespace(child_namespace)

        search_namespace.clean()
        # delete all the nodes in the namespace before purging, in case there's something in the namespace
        # that cannot be deleted
        objects = get_all_nodes_in_namespace(search_namespace, recursive=True)
        for obj in objects:
            if pm.objExists(obj):
                pm.lockNode(obj, lock=False)
        pm.delete(objects)

        pm.namespace(force=True, removeNamespace=search_namespace)
    except:
        logger.warning(f'Namespace "{namespace_name}" does not exist!')
        return

