#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Creates an ik chain
"""

from __future__ import print_function, division, absolute_import

import pymel.core as pm


def twist_fixup_chain(start_joint,
						end_joint,
						side,
						region):
	"""
	Builds the twist fix up joint chain. This supports a maximum of 3 twist joints.

	:param list[Joint] joint_list: The list of twist joints which will be driven by this twist drive system.
	:param pm.nt.Joint end_joint: End joint (ex: toe)
	:param str side: Which side the foot is on.
	:param str region: A unique name for the region.  (ex: foot)
	:return: Returns a dictionary with all of the built nodes.
	:rtype: dictionary
	"""
	
	# Chain
	twist_joints = sorted([x for x in start_joint.getChildren(type=pm.nt.Joint) if end_joint != x])
	
	# Nodes needed
	m_matrix = pm.createNode(pm.nt.MultMatrix, name='twist_multimatrix_{0}_{1}'.format(side, region))
	d_matrix = pm.createNode(pm.nt.DecomposeMatrix, name='twist_decompmatrix_{0}_{1}'.format(side, region))
	euler = pm.createNode(pm.nt.QuatToEuler, name='twist_euler_{0}_{1}'.format(side, region))
	
	# Add connections
	end_grp = pm.group(em=True, name='twist_end_grp_{0}_{1}'.format(side, region))
	pm.delete(pm.pointConstraint(end_joint, end_grp, w=True, mo=False))
	pm.delete(pm.orientConstraint(twist_joints[0], end_grp, w=True, mo=False))
	pm.parentConstraint(end_joint, end_grp, w=True, mo=True)
	
	end_grp.worldMatrix[0] >> m_matrix.matrixIn[0]
	start_joint.worldInverseMatrix[0] >> m_matrix.matrixIn[1]
	m_matrix.matrixSum >> d_matrix.inputMatrix
	d_matrix.outputQuatX >> euler.inputQuatX
	d_matrix.outputQuatW >> euler.inputQuatW
	
	multi_list = []
	twist_grps = []
	
	twist_sub = (len(twist_joints) / (1 + len(twist_joints))) - 1
	twist_range = 1
	for x in range(len(twist_joints)):
		twist_grp = pm.group(em=True, name='twist_grp_{0}_{1}_{2}'.format(side, region, x))
		pm.delete(pm.parentConstraint(twist_joints[x], twist_grp, w=True, mo=False))
		pm.parent(twist_grp, start_joint)
		twist_grp.rotate.set(0,0,0)
		
		multi = pm.createNode(pm.nt.MultiplyDivide, name='twist_multi_{0}_{1}_{2}'.format(side, region, x))
		euler.outputRotateX >> multi.input1X
		multi.outputX >> twist_grp.rotateX
		
		twist_range += twist_sub
		multi.input2X.set(twist_range)
		
		pm.orientConstraint(twist_grp, twist_joints[x], w=True, mo=True)
		
		multi_list.append(multi)
		twist_grps.append(twist_grp)
		
	# create dictionary
	return_dictionary = {}
	return_dictionary['twist_joints'] = twist_joints
	return_dictionary['m_matrix'] = m_matrix
	return_dictionary['d_matrix'] = d_matrix
	return_dictionary['euler'] = euler
	return_dictionary['multi_nodes'] = multi_list
	return_dictionary['twist_grps'] = twist_grps
	return_dictionary['end_grp'] = end_grp
	return return_dictionary


def reverse_twist_fixup_chain(start_joint,
								end_joint,
								side,
								region):
	"""
	Builds a reverse twist fix up joint chain.  Usually used from the shoulder to the elbow.

	:param pm.nt.Joint start_joint: Start joint (ex: ankle)
	:param pm.nt.Joint end_joint: End joint (ex: toe)
	:param str side: Which side the foot is on.
	:param str region: A unique name for the region.  (ex: foot)
	:return: Returns a dictionary with all of the built nodes.
	:rtype: dictionary
	"""
	
	# Chain
	twist_joints = sorted([x for x in start_joint.getChildren(type=pm.nt.Joint) if end_joint != x])
	
	m_matrix = pm.createNode(pm.nt.MultMatrix, name='twist_multimatrix_{0}_{1}'.format(side, region))
	d_matrix = pm.createNode(pm.nt.DecomposeMatrix, name='twist_decompmatrix_{0}_{1}'.format(side, region))
	euler = pm.createNode(pm.nt.QuatToEuler, name='twist_euler_{0}_{1}'.format(side, region))
	
	end_grp = pm.group(em=True, name='twist_end_grp_{0}_{1}'.format(side, region))
	pm.delete(pm.pointConstraint(start_joint, end_grp, w=True, mo=False))
	pm.delete(pm.orientConstraint(twist_joints[0], end_grp, w=True, mo=False))
	pm.parentConstraint(start_joint, end_grp, w=True, mo=True)
	
	end_grp.parentInverseMatrix[0] >> m_matrix.matrixIn[0]
	end_grp.worldMatrix[0] >> m_matrix.matrixIn[1]
	m_matrix.matrixSum >> d_matrix.inputMatrix
	d_matrix.outputQuatX >> euler.inputQuatX
	d_matrix.outputQuatW >> euler.inputQuatW
	
	multi_list = []
	twist_grps = []
	
	twist_sub = (len(twist_joints) / (1 + len(twist_joints))) - 1
	twist_range = 1
	for x in range(len(twist_joints)):
		twist_grp = pm.group(em=True, name='twist_grp_{0}_{1}_{2}'.format(side, region, x))
		pm.delete(pm.parentConstraint(twist_joints[x], twist_grp, w=True, mo=False))
		pm.parent(twist_grp, start_joint)
		twist_grp.rotate.set(0, 0, 0)
		
		multi = pm.createNode(pm.nt.MultiplyDivide, name='twist_multi_{0}_{1}_{2}'.format(side, region, x))
		euler.outputRotateX >> multi.input1X
		multi.outputX >> twist_grp.rotateX
		
		twist_range += twist_sub
		multi.input2X.set(twist_range * -1)
		
		pm.orientConstraint(twist_grp, twist_joints[x], w=True, mo=True)
		
		multi_list.append(multi)
		twist_grps.append(twist_grp)
	
	# create dictionary
	return_dictionary = {}
	return_dictionary['twist_joints'] = twist_joints
	return_dictionary['m_matrix'] = m_matrix
	return_dictionary['d_matrix'] = d_matrix
	return_dictionary['euler'] = euler
	return_dictionary['multi_nodes'] = multi_list
	return_dictionary['twist_grps'] = twist_grps
	return_dictionary['end_grp'] = end_grp
	return return_dictionary

