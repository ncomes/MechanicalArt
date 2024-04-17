#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Tracks Joint data for face meshes.
"""
# System global imports
# Software specific imports
import pymel.core as pm
#  python imports


def space_switch(target_list,
						source_object,
						switch_obj=None,
						translate=True,
						rotate=True,
						switch_attr='follow',
						**kwargs):

	if not isinstance(target_list, list):
		target_list = [target_list]
	
	t = kwargs.get('t', translate)
	r = kwargs.get('r', rotate)
	
	default_name = kwargs.get('default_name', None)
	
	if not switch_obj:
		switch_obj = source_object
	
	switch_obj.addAttr('__', k=True, at='bool')
	switch_obj.setAttr('__', e=True, cb=True, l=True)
	
	target_list_names = list(map(lambda x: str(x), target_list))
	if default_name != None:
		target_list_names[0] = default_name
	
	# Create switch attribute
	enum_names = ':'.join(target_list_names)
	switch_obj.addAttr(switch_attr, at='enum', en=enum_names, k=True)
	
	switch_offset_grp = pm.group(em=True, n='{0}_space'.format(source_object))
	pm.delete(pm.parentConstraint(source_object, switch_offset_grp, w=True, mo=False))
	
	pm.parent(switch_offset_grp, source_object.getParent())
	pm.parent(source_object, switch_offset_grp)
	switch_offset_grp.translate.set(0, 0, 0)
	switch_offset_grp.rotate.set(0, 0, 0)
	
	point_constraints = []
	orient_constraints = []
	conditions = []
	for x, target in enumerate(target_list):
		
		condition = pm.createNode(pm.nt.Condition, n='cond_{0}_space_{1}'.format(target, source_object))
		condition.secondTerm.set(x)
		condition.colorIfTrueR.set(1.0)
		condition.colorIfFalseR.set(0.0)
		conditions.append(condition)
		switch_obj.attr(switch_attr) >> condition.firstTerm
		
		if t:
			constraint = (pm.pointConstraint(target, switch_offset_grp, w=True, mo=True,
												n='point_const_{0}_space_{1}'.format(target, source_object)))
			
			point_constraints.append(constraint)
			condition.outColorR >> constraint.attr('{0}W{1}'.format(target, x))
		
		if r:
			constraint = (pm.orientConstraint(target,
												switch_offset_grp,
												w=True,
												mo=True,
												n='ori_const_{0}_space_{1}'.format(target, source_object)))
			orient_constraints.append(constraint)
			condition.outColorR >> constraint.attr('{0}W{1}'.format(target, x))
	
	result_dictionary = {}
	result_dictionary['point_constraints'] = point_constraints
	result_dictionary['orient_constraints'] = orient_constraints
	result_dictionary['conditions'] = conditions
	result_dictionary['switch_offset_grp'] = switch_offset_grp
	
	return result_dictionary

