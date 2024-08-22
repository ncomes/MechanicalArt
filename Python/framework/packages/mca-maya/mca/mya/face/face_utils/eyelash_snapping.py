#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules that do eyelash snapping to the face model.
"""

# System global imports
import os
# python imports
import pymel.core as pm
# mca python imports
from mca.mya.modeling import rivets
from mca.common.project import paths
from mca.common import log
from mca.mya.modifiers import ma_decorators
from mca.mya.face import source_data
from mca.mya.rigging import mesh_markup_rig
from mca.mya.rigging import skin_utils

logger = log.MCA_LOGGER


def setup_jnts(main_mesh,
               snap_mesh,
               eyelash_coords,
               side):
	"""
	Set up joints and locators based on UV coords.

	:param nt.Transform main_mesh: Head mesh
	:param nt.Transform snap_mesh: Mesh to snap
	:param dict eyelash_coords: A dictionary containing UV information
	:param int side: Side to identify correct coords to use, 1 is left and 2 is right
	:return: Returns a dictionary of created joints and locators
	:rtype: dictionary
	"""

	created_locs = []
	created_jnts = []

	for x, item in enumerate(eyelash_coords):
		# Get coords for mesh that will snap and coords for where on head mesh it should connect
		coord = eyelash_coords[item].get('coord', None)
		connect = eyelash_coords[item].get('connection_point', None)

		# Create UV pin on snap mesh to pull position data from it
		pin = rivets.connect_uv_pin(snap_mesh, coord)
		loc = pm.ls(pin)
		x, y, z = pm.pointPosition(loc, w=True)
		pm.delete(pin)

		# Create joint and move to where locator was
		jnt = pm.joint(rad=0.1, n=item)
		pm.parent(jnt, world=True)
		pm.setAttr(f'{jnt}.translateX', x)
		pm.setAttr(f'{jnt}.translateY', y)
		pm.setAttr(f'{jnt}.translateZ', z)

		# Mark UV and side info on joint so it can be connected with correct counterpart later
		pm.addAttr(jnt, ln='uv1', at='float')
		pm.addAttr(jnt, ln='uv2', at='float')
		pm.addAttr(jnt, ln='uvCon1', at='float')
		pm.addAttr(jnt, ln='uvCon2', at='float')

		pm.setAttr(f'{jnt}.uv1', coord[0])
		pm.setAttr(f'{jnt}.uv2', coord[1])
		pm.setAttr(f'{jnt}.uvCon1', connect[0])
		pm.setAttr(f'{jnt}.uvCon2', connect[1])
		pm.setAttr(f'{jnt}.side', side)
		created_jnts.append(jnt)

		# Create locator on main mesh and add attrs with UV and side info
		pin2 = rivets.connect_uv_pin(main_mesh, connect)
		loc2 = pm.ls(pin2)

		pm.addAttr(loc2, ln='uv1', at='float')
		pm.addAttr(loc2, ln='uv2', at='float')
		pm.addAttr(loc2, ln='side', at='double')

		pm.setAttr(f'{loc2[0]}.uv1', connect[0])
		pm.setAttr(f'{loc2[0]}.uv2', connect[1])

		pm.setAttr(f'{loc2[0]}.side', side)

		created_locs.append(loc2)

	return_dictionary = {}
	return_dictionary['jnts'] = created_jnts
	return_dictionary['locs'] = created_locs

	return return_dictionary


def snap_eyelash_mesh(main_mesh,
                      snap_mesh,
                      snap_region,
                      eyelash_coords,
                      skin_data_path):
	"""
	Snaps eyelash/shadow/tear mesh onto eyelids based on UV coords.

	:param nt.Transform main_mesh: Head mesh
	:param nt.Transform snap_mesh: Mesh to snap
	:param str snap_region: The name of the region to identify which coords to use
	:param dict eyelash_coords: A dictionary containing UV information
	:param str skin_data_path: Path to common skin data to use for snapping meshes
	"""
	# Duplicate mesh to separate mirrored mesh without messing up vert order
	dup_mesh = pm.duplicate(snap_mesh)[0]
	sep = pm.polySeparate(dup_mesh)
	created_jnts = []
	created_locs = []
	xform_group = pm.listRelatives(sep[0], p=True)
	# Lash is separated from AO/tear as it splits into four meshes with upper/lower rather than just two (left/right)
	if snap_region == 'eye_lash':
		mesh_sides = ['right_upper', 'right_lower', 'left_upper', 'left_lower']
	else:
		mesh_sides = ['right', 'left']

	for mesh_side, separated_mesh in list(zip(mesh_sides, sep)):
		mesh_side_info = eyelash_coords.get(f'{mesh_side}_{snap_region}')
		if mesh_side[0] == 'r':
			jnts_side = 2
		else:
			jnts_side = 1

		# Create joints on snap mesh, locators on main mesh
		mesh_side_setup = setup_jnts(main_mesh,
		                             separated_mesh,
		                             mesh_side_info,
		                             jnts_side)

		mesh_side_jnts = mesh_side_setup.get('jnts')
		for jnt in mesh_side_jnts:
			created_jnts.append(jnt)
		mesh_side_locs = mesh_side_setup.get('locs')
		for loc in mesh_side_locs:
			created_locs.append(loc)

	skin_utils.apply_skinning_to_mesh([snap_mesh], skin_data_path, name_override=snap_region)

	# Match up UV connect attr on joints with UV attr on loc
	for jnt in created_jnts:
		jnt_side = pm.getAttr(f'{jnt}.side')
		val1 = pm.getAttr(f'{jnt}.uvCon1')
		val2 = pm.getAttr(f'{jnt}.uvCon2')
		for each in created_locs:
			val3 = pm.getAttr(f'{each[0]}.uv1')
			val4 = pm.getAttr(f'{each[0]}.uv2')
			loc_side = pm.getAttr(f'{each[0]}.side')
			if val1 != val3:
				pass
			elif val2 != val4:
				pass
			elif jnt_side != loc_side:
				pass
			else:
				pm.pointConstraint(each, jnt, mo=False)

	# Delete construction history so mesh stays, plus delete any objects just created
	pm.delete(snap_mesh, ch=True)
	pm.makeIdentity(snap_mesh, a=True)
	pm.delete(sep)
	pm.delete(xform_group)
	pm.delete(created_jnts)
	pm.delete(created_locs)


@ma_decorators.undo_decorator
def eyelash_snap_action():
	"""
	Snaps mesh onto eyelids using mesh markup and coordinate data in face_source_data file.

	"""

	source_data_path = os.path.join(paths.get_common_face(), 'rig_source_data.json')
	skin_data_path = os.path.join(paths.get_common_face(), 'BaseSkinning')
	rig_markup = mesh_markup_rig.RigMeshMarkup.create()
	meshes_dict = rig_markup.get_dict()
	skin_meshes = meshes_dict.get('skin_mesh', None)
	if not skin_meshes:
		logger.warning('No meshes with correct markup found.')
		return

	head_mesh = skin_meshes.get('head_mesh', None)
	selection_list = pm.selected()
	if not selection_list:
		mesh_types = ['eye_shadow', 'eye_lash', 'eye_tear']

	else:
		mesh_types = []
		for mesh in selection_list:
			if mesh == head_mesh:
				pass
			else:
				for region_type, type_mesh in skin_meshes.items():
					if type_mesh == mesh:
						mesh_types.append(region_type)

	for mesh_type in mesh_types:
		mesh_type_data = source_data.FaceMeshRegionData.load(source_data_path, f'{mesh_type}_mesh')
		mesh_type_coords = mesh_type_data.eye_card_uv_data
		mesh_type_mesh = skin_meshes.get(mesh_type, None)

		if mesh_type_mesh and head_mesh != mesh_type_mesh:
			snap_eyelash_mesh(head_mesh,
			                  mesh_type_mesh,
			                  mesh_type,
			                  mesh_type_coords,
			                  skin_data_path)
