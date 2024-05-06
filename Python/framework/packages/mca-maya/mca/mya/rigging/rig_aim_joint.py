#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Tracks Joint data for face meshes.
"""

# System global imports
# python imports
import pymel.core as pm
#  python imports
from mca.mya.rigging import rig_utils
from mca.mya.rigging.flags import frag_flag


def rig_aim_joint(bind_joint,
					flag_distance=20,
					aim_axis=(1, 0, 0),
					up_axis=(0, 0, 1),
					proxy=False):
	"""
	Builds an aim constraint for a single joint.
	
	:param pm.nt.Joint bind_joint: Joint that will be the aim joint.
	:param float flag_distance: distance between start_joint and the flag
	:param vector aim_axis: which direction in local space is up.
	:param vector up_axis: which axis + or negative will be pointing down the joint in local space.
	:param bool proxy: if True then it won't affect the bind joints.
	:return: a dictionary with following keys: bind_joint, flag, rotate_locator, rotate_locator_zero_grp, up_locator.
	:rtype: dictionary
	"""

	# Rig flags prep
	direction = map(lambda x: x * flag_distance, aim_axis)
	up_direction = map(lambda x: x * flag_distance, up_axis)

	# Rig aim flag ###
	# Create
	rotate_loc = rig_utils.create_locator_at_object(bind_joint)

	up_loc = rig_utils.create_locator_at_object(rotate_loc)
	up_loc.rename(up_loc.nodeName().replace('_loc_loc', '_up_loc'))

	pm.move(up_loc, up_direction, os=True, r=True)
	rotate_loc_align_grp = rig_utils.create_align_transform(rotate_loc)
	object_to_match = rig_utils.create_locator_at_object(bind_joint)
	pm.move(object_to_match, direction, os=True, r=True)
	aim_flag = frag_flag.Flag.create(object_to_match, label=(bind_joint.name() + '_aim'))

	pm.delete(object_to_match)
	pm.aimConstraint(aim_flag,
						rotate_loc,
						mo=False,
						aimVector=aim_axis,
						upVector=up_axis,
						worldUpType='object',
						worldUpObject=up_loc)

	# Lock and hide attributes
	aim_flag.lock_and_hide_attrs(['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])

	# Move aim joints to the NoTouch group
	if not proxy:
		pm.parentConstraint(rotate_loc, bind_joint, mo=False)

	# create dictionary
	return_dictionary = {}
	return_dictionary['bind_joint'] = bind_joint
	return_dictionary['flag'] = aim_flag
	return_dictionary['rotate_locator'] = rotate_loc
	return_dictionary['rotate_loc_align_grp'] = rotate_loc_align_grp
	return_dictionary['up_locator'] = up_loc

	return return_dictionary

