#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
modules that interact with matrix nodes
"""

# System global imports
# python imports
import pymel.core as pm
#  python imports
from mca.mya.utils import groups, naming


def _create_matrix_constraint_base():
	"""
	Creates the matrix nodes for the matrix constraint.

	:return: Returns the base matrix nodes for the matrix constraint.
	:rtype: list(pm.nt.MultMatrix, pm.nt.DecomposeMatrix)
	"""
	
	m_matrix = pm.createNode(pm.nt.MultMatrix)
	d_matrix = pm.createNode(pm.nt.DecomposeMatrix)
	
	m_matrix.addAttr('isMatrixConstraint', at='bool', dv=True)
	d_matrix.addAttr('isMatrixConstraint', at='bool', dv=True)
	
	m_matrix.matrixSum >> d_matrix.inputMatrix
	
	return [m_matrix, d_matrix]


def matrix_constraint(parent_obj, child_obj, mo=True, t=True, r=True, s=True):
	"""
	Builds a matrix constraint.

	:param pm.nt.Transform parent_obj: The parent object.
	:param pm.nt.Transform child_obj: The child object that will be driven.
	:param bool mo: If True, Maintains the offset.
	:param bool t: If True, will follow in translation.
	:param bool r: If True, will follow rotation.
	:param bool s: If True, will follow Scale.
	:return: Returns a dictionary with all the created nodes.
	:rtype: Dictionary
	"""
	
	matrix_grp = groups.create_aligned_parent_group(child_obj,
													suffix='matrix_constraint',
													attr_name='matrixConstraint',
													obj_attr='matrixConstraintObject')
	
	matrix_parent_grp = groups.create_aligned_parent_group(matrix_grp,
															suffix='matrix_constraint',
															attr_name='matrixConstraint',
															obj_attr='matrixConstraintObject')
	
	pm.rename(matrix_parent_grp, '{0}_constraint_parent_grp'.format(naming.get_basename(child_obj)))
	matrix_parent_grp = matrix_grp.getParent()
	m_matrix, d_matrix = _create_matrix_constraint_base()
	
	parent_name = naming.get_basename(parent_obj)
	m_matrix.rename(f'{parent_name}_multi_matrix')
	d_matrix.rename(f'{parent_name}_decomp_matrix')
	
	parent_obj.worldMatrix >> m_matrix.matrixIn[1]
	matrix_parent_grp.worldInverseMatrix >> m_matrix.matrixIn[2]
	
	if mo:
		temp_matrix = pm.createNode(pm.nt.MultMatrix)
		matrix_grp.worldMatrix >> temp_matrix.matrixIn[0]
		parent_obj.worldInverseMatrix >> temp_matrix.matrixIn[1]
		matrix_offset = temp_matrix.matrixSum.get()
		
		m_matrix.matrixIn[0].set(matrix_offset)
		
		pm.delete(temp_matrix)
	
	if t:
		d_matrix.outputTranslate >> matrix_grp.translate
	if r:
		d_matrix.outputRotate >> matrix_grp.rotate
	if s:
		d_matrix.outputScale >> matrix_grp.scale
	
	if not child_obj.hasAttr('parentMatrixConstraint'):
		child_obj.addAttr('parentMatrixConstraint', at='message')
	if not child_obj.hasAttr('parentConstraintObject'):
		child_obj.addAttr('parentConstraintObject', dt='string')
	
	matrix_parent_grp.matrixConstraintObject >> child_obj.parentMatrixConstraint
	child_obj.parentConstraintObject.set(str(matrix_parent_grp))
	
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
	
	constraint_grp = child_obj.parentMatrixConstraint.get()
	parent_grp = constraint_grp.getParent()
	
	pm.parent(child_obj, w=True)
	if parent_grp:
		pm.parent(child_obj, parent_grp)
	
	pm.delete(constraint_grp)
	pm.select(cl=True)
