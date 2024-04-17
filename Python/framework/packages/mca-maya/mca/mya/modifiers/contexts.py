#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains custom contexts managers for Autodesk Maya
"""
# System global imports
from contextlib import contextmanager
# software specific imports
import pymel.core as pm
#  python imports
from mca.common import log

logger = log.MCA_LOGGER


@contextmanager
def undo_chunk_context(name=None):
    """
    Enables undo functionality during the context execution.
    """

    try:
        pm.undoInfo(openChunk=True, chunkName=name or '')
        yield
    finally:
        pm.undoInfo(closeChunk=True)


@contextmanager
def disable_undo_context():
    """
    Disable undo functionality during the context execution.
    """

    try:
        pm.undoInfo(stateWithoutFlush=False)
        yield
    finally:
        pm.undoInfo(stateWithoutFlush=True)


@contextmanager
def suspend_refresh_context():
    """
    Suspends viewport refresh during the context execution
    :return:
    """

    try:
        pm.refresh(suspend=True)
        yield
    finally:
        pm.refresh(suspend=False)


@contextmanager
def no_panel_refresh_context():
    """
    Disable all controlled panel refresh during the context execution
    """

    controls = list()
    for panel in pm.lsUI(panels=True, long=True):
        control = pm.panel(panel, query=True, control=True)
        if not control:
            continue
        if not pm.layout(control, query=True, visible=True):
            continue
        controls.append(control)

    try:
        for control in controls:
            pm.layout(control, edit=True, manage=False)
        yield
    finally:
        for control in controls:
            try:
                pm.layout(control, edit=True, manage=True)
            except RuntimeError:
                logger.warning('Cannot manage control {}'.format(control))


@contextmanager
def disable_cycle_check_warnings_context():
    """
    Disables Cycle Check warnings during the context execution

    ..note:: This only disables the main pain and will sometimes still trigger updates in torn of panls.
    """

    current_evaluation = pm.cycleCheck(evaluation=True, query=True)
    try:
        pm.cycleCheck(evaluation=False)
        yield
    finally:
        pm.cycleCheck(evaluation=current_evaluation)


@contextmanager
def namespace_context(namespace):
    """
    Python context that sets the given namespace as the active namespace and after yielding the function restores
    the previous namespace.

    :param str namespace: namespace name to set as active one.

    ..note:: if the give namespace does not exist, it will be created automatically.
    """

    # some characters are illegal for namespaces
    namespace = namespace.replace('.', '_')
    if namespace != ':' and namespace.endswith(':'):
        namespace = namespace[:-1]

    current_namespace = pm.namespaceInfo(currentNamespace=True, absoluteName=True)
    existing_namespaces = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True, absoluteName=True)
    if current_namespace != namespace and namespace not in existing_namespaces and namespace != ':':
        try:
            namespace = pm.namespace(add=namespace)
        except RuntimeError:
            logger.error('Failed to create namespace: {}, existing namespaces: {}'.format(
                namespace, existing_namespaces), exc_info=True)
            pm.namespace(setNamespace=current_namespace)
            raise
    pm.namespace(setNamespace=namespace)
    try:
        yield
    finally:
        pm.namespace(setNamespace=current_namespace)


@contextmanager
def unlock_attribute_context(attribute):
    """
    PyMEL Maya context that allows to force unlock of an attribute before executing a function and recover its
    original lock status after the function is executed.

    :param pm.Attribute attribute: attribute to unlock.
    """

    is_locked = attribute.isLocked()
    if is_locked:
        attribute.unlock()
    try:
        yield
    finally:
        if is_locked:
            attribute.lock()


@contextmanager
def unlock_node_context(node):
    """
    PyMEL Maya context that allows to force unlock of a node before executing a function and recover its original
    lock state after the function is executed.

    :param pm.PyNode node: node to unlock.
    """

    set_locked = False
    if node and pm.objExists(node):
        if node.isLocked():
            if node.isReferenced():
                raise ('Unable to unlock a referenced node: {}'.format(node.fullPathName()))
            node.unlock()
            set_locked = True
    try:
        yield
    finally:
        if node and pm.objExists(node) and set_locked:
            node.lock()


@contextmanager
def maintained_selection_context():
    """
    Maintain selection during context
    Example:
        >>> scene = pm.newFile(force=True)
        >>> node = pm.createNode('transform', name='newGroup')
        >>> pm.select('persp')
        >>> with maintained_selection_context():
        ...     pm.select(node, replace=True)
        >>> node in pm.ls(selection=True)
        False
    """

    previous_selection = pm.ls(selection=True)
    try:
        yield
    finally:
        if previous_selection:
            valid_selection = [node for node in previous_selection if node and pm.objExists(node)]
            if valid_selection:
                pm.select(valid_selection, replace=True, noExpand=True)
        else:
            pm.select(clear=True)


@contextmanager
def maintain_time_context():
    """
    Context manager that preserves the time after the context.
    """

    current_time = pm.currentTime(query=True)
    try:
        yield
    finally:
        pm.currentTime(current_time, edit=True)
