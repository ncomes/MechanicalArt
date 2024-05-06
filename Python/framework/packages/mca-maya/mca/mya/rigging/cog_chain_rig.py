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


def cog_chain(start_joint, end_joint, scale=1.0, orientation=(-90,0,0)):
	"""
	Creates a Cog.
	
	:param pm.nt.Joint start_joint: The start joint of the chain.
	:param pm.nt.Joint end_joint: The end joint of the chain.
	:param float scale: Scale size of the flag.
	:param list(float) orientation: Orientation of the flag.
	:return: Returns a dictionary of the chain data.
	:rtype: Dictionary
	"""
	
	chain = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)
	
	# Create flags
	flags = []
	constraints = []
	for jnt in chain:
		flag_node = frag_flag.Flag.create(jnt, label='cog', orientation=orientation, scale=scale)
		
		flag_node.setAttr('rotateOrder', 2)
		constraint = pm.parentConstraint(flag_node, jnt, w=1, mo=1)
		flags.append(flag_node)
		constraints.append(constraint)
	
	# create dictionary
	return_dictionary = {}
	return_dictionary['chain'] = chain
	return_dictionary['start_joint'] = start_joint
	return_dictionary['end_joint'] = end_joint
	return_dictionary['flags'] = flags
	return_dictionary['constraints'] = constraints
	return return_dictionary

