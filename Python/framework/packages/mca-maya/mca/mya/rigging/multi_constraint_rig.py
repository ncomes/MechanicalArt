#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Tracks Joint data for face meshes.
"""

from __future__ import print_function, division, absolute_import

import pymel.core as pm

from mca.mya.utils import naming
from mca.mya.rigging import matrix_nodes


def multi_constraint(target_list,
						source_object,
						switch_obj=None,
						translate=True,
						rotate=True,
						scale=True,
						switch_attr='follow',
						**kwargs):
	
	if not isinstance(target_list, list):
		target_list = [target_list]
	
	t = kwargs.get('t', translate)
	r = kwargs.get('r', rotate)
	s = kwargs.get('s', scale)
	
	default_name = kwargs.get('default_name', None)
	
	if not switch_obj:
		switch_obj = source_object
	
	switch_obj.addAttr('__', k=True, at='bool')
	switch_obj.setAttr('__', e=True, cb=True, l=True)
	
	target_list_names = list(map(lambda x: naming.get_basename(x), target_list))
	if default_name != None:
		target_list_names[0] = default_name
	
	enum_names = ':'.join(target_list_names)
	switch_obj.addAttr(switch_attr, at='enum', en=enum_names, k=True)
	
	## Set up the Matrix constraint nodes
	m_constraint = matrix_nodes.matrix_constraint(target_list[0], source_object, mo=True)
	parent_grp = m_constraint['parent_constraint_group']
	source_grp = m_constraint['constraint_group']
	m_matrix = m_constraint['multi_matrix']
	d_matrix = m_constraint['decomp_matrix']
	
	# Create Choice Nodes
	source_object_name = naming.get_basename(source_object)
	choice_offset = pm.createNode(pm.nt.Choice, n='choice_{0}_offset'.format(source_object_name))
	choice_space = pm.createNode(pm.nt.Choice, n='choice_{0}_space'.format(source_object_name))
	
	# Add Attrs top the switch and connect the selects
	switch_obj.attr(switch_attr) >> choice_offset.selector
	switch_obj.attr(switch_attr) >> choice_space.selector
	
	# Connect the choice inputs.  THESE MUST ALL BE IN ORDER.
	for x in range(len(target_list)):
		target_list[x].worldMatrix >> choice_space.input[x]
	
	# Add the attributes for the offests to the parent node
	for x in range(len(target_list)):
		parent_grp.addAttr('{0}_offset'.format(naming.get_basename(target_list[x])), at='matrix')
	
	### Temp Matrix
	for x in range(len(target_list)):
		temp_matrix = pm.createNode(pm.nt.MultMatrix)
		source_grp.worldMatrix >> temp_matrix.matrixIn[0]
		target_list[x].worldInverseMatrix >> temp_matrix.matrixIn[1]
		matrix_offset = temp_matrix.matrixSum.get()
		
		parent_grp.attr('{0}_offset'.format(naming.get_basename(target_list[x]))).set(matrix_offset)
		parent_grp.attr('{0}_offset'.format(naming.get_basename(target_list[x]))) >> choice_offset.input[x]
		
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
