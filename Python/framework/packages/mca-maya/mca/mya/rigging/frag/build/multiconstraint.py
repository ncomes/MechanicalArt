#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to building a multiconstraint.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.rigging import matrix_utils
from mca.mya.utils import naming


def build_multi_constraint(target_list, source_node,  switch_node=None, translate=True, rotate=True, scale=True, switch_attr=None, **kwargs):
    if not isinstance(target_list, list):
        target_list = [target_list]

    if not switch_attr:
        switch_attr = 'follow'

    t = kwargs.get('t', translate)
    r = kwargs.get('r', rotate)
    s = kwargs.get('s', scale)

    default_name = kwargs.get('default_name', None)

    if not switch_node:
        switch_node = source_node

    switch_node.addAttr('__', k=True, at='bool')
    switch_node.setAttr('__', e=True, cb=True, l=True)

    target_list_names = list([naming.get_basename(x) for x in target_list])
    if default_name != None:
        target_list_names[0] = default_name

    enum_names = ':'.join(target_list_names)
    switch_node.addAttr(switch_attr, at='enum', en=enum_names, k=True)

    ## Set up the Matrix constraint nodes
    m_constraint = matrix_utils.matrix_constraint(target_list[0], source_node, mo=True)
    parent_grp = m_constraint['parent_constraint_group']
    source_grp = m_constraint['constraint_group']
    m_matrix = m_constraint['multi_matrix']
    d_matrix = m_constraint['decomp_matrix']

    # Create Choice Nodes
    source_node_name = naming.get_basename(source_node)
    choice_offset = pm.createNode(pm.nt.Choice, n=f'choice_{source_node_name}_offset')
    choice_space = pm.createNode(pm.nt.Choice, n=f'choice_{source_node_name}_space')

    # Add Attrs top the switch and connect the selects
    switch_node.attr(switch_attr) >> choice_offset.selector
    switch_node.attr(switch_attr) >> choice_space.selector

    # Connect the choice inputs. THESE MUST ALL BE IN ORDER.
    for i, target_node in enumerate(target_list):
        target_node.worldMatrix >> choice_space.input[i]

    for i, target_node in enumerate(target_list):
        # Add the attributes for the offests to the parent node
        parent_grp.addAttr(f'{naming.get_basename(target_node)}_offset', at='matrix')
    
    for i, target_node in enumerate(target_list):
        # Temp Matrix
        temp_matrix = pm.createNode(pm.nt.MultMatrix)
        source_grp.worldMatrix >> temp_matrix.matrixIn[0]
        target_node.worldInverseMatrix >> temp_matrix.matrixIn[1]
        matrix_offset = temp_matrix.matrixSum.get()

        parent_grp.attr(f'{naming.get_basename(target_node)}_offset').set(matrix_offset)
        parent_grp.attr(f'{naming.get_basename(target_node)}_offset') >> choice_offset.input[i]

        pm.delete(temp_matrix)

    # Connect the mult matrix back up
    pm.disconnectAttr(m_matrix.matrixIn)
    choice_offset.output >> m_matrix.matrixIn[0]
    choice_space.output >> m_matrix.matrixIn[1]
    parent_grp.worldInverseMatrix >> m_matrix.matrixIn[2]

    # Todo ncomes: Add attributes to the switch to toggle t,r,s.
    if not t:
        pm.disconnectAttr(d_matrix.outputTranslate)

    if not r:
        pm.disconnectAttr(d_matrix.outputRotate)

    if not s:
        pm.disconnectAttr(d_matrix.outputScale)

    result_dictionary = {}
    result_dictionary['multi_matrix'] = m_matrix
    result_dictionary['decomp_matrix'] = d_matrix
    result_dictionary['constraint_group'] = source_grp
    result_dictionary['parent_constraint_group'] = parent_grp
    result_dictionary['choice_offset'] = choice_offset
    result_dictionary['choice_space'] = choice_space

    return result_dictionary