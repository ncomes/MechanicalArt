#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to matrix manipulation in Maya.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.utils import dag_utils, naming


def _create_matrix_constraint_base():
    """
    Creates the matrix nodes for the matrix constraint.

    :return: Returns the base matrix nodes for the matrix constraint.
    :rtype: list(pm.nt.MultMatrix, pm.nt.DecomposeMatrix)
    """

    m_matrix = pm.createNode(pm.nt.MultMatrix)
    d_matrix = pm.createNode(pm.nt.DecomposeMatrix)

    m_matrix.addAttr('is_matrix_constraint', at='bool', dv=True)
    d_matrix.addAttr('is_matrix_constraint', at='bool', dv=True)

    m_matrix.matrixSum >> d_matrix.inputMatrix

    return [m_matrix, d_matrix]


def matrix_constraint(parent_node, child_node, mo=True, t=True, r=True, s=True, **kwargs):
    """
    Builds a matrix constraint.

    :param Transform parent_node: The parent object.
    :param Transform child_node: The child object that will be driven.
    :param bool mo: If True, Maintains the offset.
    :param bool t: If True, will follow in translation.
    :param bool r: If True, will follow rotation.
    :param bool s: If True, will follow Scale.
    :return: Returns a dictionary with all the created nodes.
    :rtype: Dictionary
    """
    
    t = kwargs.get('translate') or t
    r = kwargs.get('rotate') or r
    s = kwargs.get('scale') or s

    matrix_grp = dag_utils.create_aligned_parent_group(child_node,
                                                       suffix='matrix_constraint',
                                                       attr_name='matrix_constraint',
                                                       group_attr='matrix_constraint')

    matrix_parent_grp = dag_utils.create_aligned_parent_group(matrix_grp,
                                                              suffix='matrix_constraint',
                                                              attr_name='matrix_constraint',
                                                              group_attr='matrix_constraint')

    pm.rename(matrix_parent_grp, '{0}_constraint_parent_grp'.format(naming.get_basename(child_node)))
    matrix_parent_grp = matrix_grp.getParent()
    m_matrix, d_matrix = _create_matrix_constraint_base()

    parent_name = naming.get_basename(parent_node)
    m_matrix.rename(f'{parent_name}_multi_matrix')
    d_matrix.rename(f'{parent_name}_decomp_matrix')

    parent_node.worldMatrix >> m_matrix.matrixIn[1]
    matrix_parent_grp.worldInverseMatrix >> m_matrix.matrixIn[2]

    if mo:
        temp_matrix = pm.createNode(pm.nt.MultMatrix)
        matrix_grp.worldMatrix >> temp_matrix.matrixIn[0]
        parent_node.worldInverseMatrix >> temp_matrix.matrixIn[1]
        matrix_offset = temp_matrix.matrixSum.get()

        m_matrix.matrixIn[0].set(matrix_offset)

        pm.delete(temp_matrix)

    if t:
        d_matrix.outputTranslate >> matrix_grp.translate
    if r:
        d_matrix.outputRotate >> matrix_grp.rotate
    if s:
        d_matrix.outputScale >> matrix_grp.scale

    if not child_node.hasAttr('parent_matrix_constraint'):
        child_node.addAttr('parent_matrix_constraint', at='message')
    if not child_node.hasAttr('parent_constraint_node'):
        child_node.addAttr('parent_constraint_node', at='message')

    matrix_parent_grp.matrix_constraint >> child_node.parent_matrix_constraint
    matrix_parent_grp.message >> child_node.parent_constraint_node

    result_dictionary = {}
    result_dictionary['multi_matrix'] = m_matrix
    result_dictionary['decomp_matrix'] = d_matrix
    result_dictionary['constraint_group'] = matrix_grp
    result_dictionary['parent_constraint_group'] = matrix_parent_grp

    return result_dictionary


def remove_matrix_constraint(child_obj):
    """
    Removes a matrix constraint.

    :param pm.nt.Transform child_obj: The child object that is being driven.
    """

    constraint_grp = child_obj.parent_matrix_constraint.get()
    parent_grp = constraint_grp.getParent()

    pm.parent(child_obj, w=True)
    if parent_grp:
        pm.parent(child_obj, parent_grp)

    pm.delete(constraint_grp)
    pm.select(cl=True)
