#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Creates an cog rig
"""

# System global imports
# python imports
import pymel.core as pm
#  python imports
from mca.mya.utils import dag
from mca.mya.rigging.flags import frag_flag


def reverse_chain(start_joint, end_joint, suffix='', scale=1.0, orientation=(-90, 0, 0)):
	"""
	Creates a reverse chain.

	:param pm.nt.Joint start_joint: The start of the chain joint.
	:param pm.nt.Joint end_joint: The end of the chain joint.
	:param str suffix: Suffix to remove on the flag.
	:param float scale: Scale size of the flag.
	:param list(float) orientation: Orientation of the flag.
	:return: Returns a dictionary of the chain data.
	:rtype: Dictionary
	"""
	
	chain = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)
	
	if not len(chain) == 2:
		raise RuntimeError("There can be no joints between startJoint and endJoint")
		
	# rotate joint chain
	rotate_joint = pm.duplicate(end_joint, po=True)[0]
	end_rotate_joint = pm.duplicate(start_joint, po=True)[0]
	end_rotate_joint.setParent(rotate_joint)
	rotate_joint.setParent(None)
	rotate_joint.v.set(0)
	
	# create flags
	label = start_joint.nodeName().replace('_' + suffix, '')
	rotate_flag = frag_flag.Flag.create(rotate_joint, label=label, scale=scale, orientation=orientation)
	pm.parentConstraint(rotate_flag, rotate_joint, w=1, mo=True)
	pm.parentConstraint(end_rotate_joint, start_joint, w=1, mo=True)
	
	# create dictionary
	return_dictionary = dict()
	return_dictionary['chain'] = chain
	return_dictionary['start_joint'] = start_joint
	return_dictionary['end_joint'] = end_joint
	return_dictionary['rotate_joint'] = rotate_joint
	return_dictionary['align_group'] = rotate_flag.getParent()
	return_dictionary['flag'] = rotate_flag

	return return_dictionary

