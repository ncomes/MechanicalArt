#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
Source data for working with the facial rigs.
"""

# system global imports
# python imports
import logging
import os
# software specific imports
import pymel.core as pm
# mca python imports
from mca.mya.animation import time_utils
from mca.mya.rigging import tek, rig_utils, chain_markup
from mca.mya.utils import fbx_utils
from mca.mya.face.face_utils import face_util
from mca.mya.modeling import face_model


POSE_FILE = 'FacePoses'


def create_face_pose_file(create_skeleton=True):
	"""
	Creates a mya animation file with a line up of poses.
	
	:param bool create_skeleton: Will duplicate the skeleton and bake the animation.
	:return: Returns the new root joint.
	:rtype: pm.nt.Joint
	"""
	
	all_components = tek.get_all_tek_nodes()
	face_components = [x for x in all_components if x.pynode.hasAttr('isFragFace')]
	[x.keyframe_flags_max_values() for x in face_components]
	time_utils.reframe_visible_range()
	if create_skeleton:
		tek_rig = tek.get_tek_rig(face_components[0])
		start_frame = pm.playbackOptions(q=True, min=True)
		end_frame = pm.playbackOptions(q=True, max=True)
		return rig_utils.bake_skeleton_from_rig(tek_rig=tek_rig,
												start_frame=start_frame,
												end_frame=end_frame)
	return


def export_face_pose_file(folder_path, delete_root=True):
	"""
	Exports the face pose file
	
	:param str folder_path: folder path to be saved
	:param bool delete_root: If True, the root joint will be deleted afterwards.
	"""
	# Make sure frame rate is correct or poses will be on the wrong frames
	frame_rate = pm.currentUnit(q=True, time=True)
	if frame_rate != 'ntsc':
		pm.currentUnit(time='ntsc')

	root_joint = create_face_pose_file(create_skeleton=True)
	if not root_joint:
		logging.warning('No Root Joint')
		return
	deletable_joints = [x for x in pm.listRelatives(root_joint, ad=True, type=pm.nt.Joint) if 'null' in x.name()]
	pm.delete(deletable_joints)
	# Get rid of eye flag curves, eye poses for pose file should be taken from root
	wrapped_root = chain_markup.ChainMarkup(root_joint)
	for side in ['left', 'right']:
		eye_jnt = wrapped_root.get_start('eye', side)
		eye_anim = eye_jnt.listConnections(type='animCurve')
		if eye_anim:
			flag_keys = [x for x in [str(x) for x in eye_anim] if 'flag' in x or 'Flag' in x]
			pm.delete(flag_keys)

	path = os.path.join(folder_path, f'{POSE_FILE}.fbx')

	fbx_utils.export_fbx(fbx_path=path,
					node_list=[root_joint],
					start_frame=pm.playbackOptions(q=True, min=True),
					end_frame=pm.playbackOptions(q=True, max=True))
	if delete_root:
		pm.delete(root_joint)
	# Set back the frame rate to whatever it was originally
	pm.currentUnit(frame_rate)


def create_blank_poses(mesh, asset_id, region):
	"""
	Creates blank poses with the name of the pose.
	
	:param pm.nt.Transform mesh: The blend shape mesh.
	:param str asset_id: id of the asset.
	:param str region: The name of the new region being added.
	:return: Returns the list of pose names
	:rtype: list(str)
	"""
	
	mesh = face_model.FaceModel(mesh)
	
	parameter_inst = face_util.get_parameters_region_instance(asset_id=asset_id, region_name=region)
	pose_list = parameter_inst.get_pose_list()
	for pose in pose_list:
		mesh.duplicate(label=pose, remove_user_attrs=True)
	
	return pose_list


def mirror_pose(pose_mesh, mesh, pose_connection=None, asset_id=None):
	"""
	Mirrors a pose using the parameter data.
	
	:param pm.nt.Transform pose_mesh: The mesh that will be mirrored.
	:param str pose_connection: Name of the attribute that the pose is connected to on the Parameter Node.
	:param str asset_id: id of the asset.
	:return: Returns the mirrored mesh.
	:rtype: pm.nt.Transform
	"""
	
	if not isinstance(mesh, face_model.FaceModel):
		mesh = face_model.FaceModel(mesh)
	
	if not pose_connection:
		pose_connection = str(pose_mesh)
	
	# Get the parameter data so we can get the name of the mirrored pose
	parameter_inst = mesh.get_parameters(asset_id=asset_id)
	pose_data = parameter_inst.get_parameter_by_connection(pose_connection)
	mirror_mesh = pose_data.mirror
	
	if not mirror_mesh:
		return
	mirror_mesh = pm.PyNode(mirror_mesh)
	pose_mesh = pm.PyNode(pose_data.parameter_name)
	
	# Get the region data so we can access the vertex data to mirror the mesh.
	region_data = mesh.get_region_data(asset_id)
	mirror_data = region_data.get_mirror_data()
	dup_mesh = pm.duplicate(pose_mesh, n=f'temp_mirror_pose')[0]
	mirror_data.mirror_mesh(mesh_name=dup_mesh)
	
	if pm.objExists(mirror_mesh):
		old_pose_parent = mirror_mesh.getParent()
		pos = pm.xform(mirror_mesh, q=True, t=True, ws=True)
		pm.delete(mirror_mesh)
		
		pm.xform(dup_mesh, t=pos, ws=True)
		pm.parent(dup_mesh, old_pose_parent)
	
	dup_mesh.rename(mirror_mesh)
	
	return [pose_mesh, mirror_mesh]

