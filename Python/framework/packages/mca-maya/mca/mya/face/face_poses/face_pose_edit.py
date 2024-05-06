#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# python imports
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
# mca python imports
from mca.common.paths import paths
from mca.mya.rigging import frag
from mca.mya.pyqt import dialogs
from mca.mya.utils import display_layers, attr_utils
from mca.mya.modeling import vert_utils, blendshape_model, blendshape_node, face_model
from mca.mya.face.face_utils import face_util, face_import_export, face_skinning
from mca.mya.rigging.flags import flag_utils
from mca.common import log
# Internal module imports


logger = log.MCA_LOGGER


class FacePoseEdit:
	def __init__(self, edit_inst):
		self.edit_inst = edit_inst
		self.dsp_lyrs = self.get_display_layers()
	
	@classmethod
	def create(cls, mesh, main_pose=None, frag_node=None):
		"""
		This extends the face edit component and allows the user to edit face meshes.
		
		:param str/None main_pose: The pose that will be edited
		:param str mesh: Name of the blend shape mesh.  The one that has all the blend shapes attached.
		:param FRAGRig frag_node: The FRAGRig node
		:return: Returns an instance of FacePoseEdit.
		:rtype: FacePoseEdit
		"""
		
		if frag_node:
			frag_rig = frag.get_frag_rig(frag_node)
		else:
			all_frag_roots = frag.get_all_frag_roots()
			if not all_frag_roots:
				return
			frag_root = all_frag_roots[0]
			frag_rig = frag_root.get_rig()
		
		# Make sure the mesh is an instance of the FaceModel Module
		if not isinstance(mesh, face_model.FaceModel):
			mesh = face_model.FaceModel(mesh)
		
		# Check to see if the edit node exists.  If it does, bail.
		face_edit_component = frag_rig.get_frag_children(of_type=frag.FaceEditComponent)
		if face_edit_component:
			logger.warning(f'{face_edit_component} already exists.')
			return
		# Create the Face Edit Node
		edit_inst = frag.FaceEditComponent.create(frag_rig)
		# Create compound attributes with all of the poses activated, except the main pose.
		edit_inst.set_flags_info(main_pose=main_pose)
		edit_inst.set_main_flag_info(main_pose=main_pose)
		
		asset_id = frag_rig.get_asset_id(frag_rig)
		# get the parameter data so we can get the actual pose name from the mesh.
		# The parameter connection will give us the name.
		parameter_inst = face_util.get_parameters_region_instance(asset_id, mesh.region)
		parameters = parameter_inst.get_parameters_list()
		pose_name = None
		pose_side = None
		parameter_node_pose = edit_inst.pynode.parameterNodePose.get()
		for param in parameters:
			if param.connection == parameter_node_pose:
				pose_name = param.parameter_name
				pose_side = param.side
				break
		
		# Set the name of the pose that correlates with the mesh.
		if pose_name:
			edit_inst.pynode.poseName.set(pose_name)
			edit_inst.pynode.poseSide.set(pose_side)
		# Set the mesh name
		edit_inst.pynode.mesh.set(mesh.mesh.nodeName())
		
		return cls(edit_inst)
	
	def pose_edit_start(self, multi_edit=False, show_skel=False, symmetry=False, transfer_jnts=False):
		"""
		Puts the tool in a state where the artist can update a blend shape mesh.
		It duplicates the mesh, with the pose that is to be updated.
		
		:param bool multi_edit: If False it puts the user in a Single pose Edit.
								IF True, puts the user in a multi pose edit.
		:param bool show_skel: If True, it will unhide the skeleton.
		:param bool symmetry: If True, will turn on Maya's modeling Symmetry options.
		"""
		
		mesh = face_model.FaceModel(self.edit_inst.pynode.mesh.get())
		extra_head_mesh = None
		
		if not multi_edit:
			# Reset all the flags -  This is for Single pose edit.  We start with no poses and then add them with
			# the Flags.
			flag_utils.zero_flags([self.edit_inst])
			# Set the main flag
			self.edit_inst.single_pose = True
		self.edit_inst.set_main_flag()
		
		if not multi_edit:
			# Get the main blend shape mesh so we can duplicate it and edit it
			extra_head_mesh = self.duplicate_head_mesh_extra()
		
		# Duplicate the mesh.  This will be the mesh the artist will edit.
		pose_mesh = mesh.duplicate(label=f'{self.edit_inst.pynode.poseName.get()}_edit')
		pose_mesh.mesh.addAttr('poseMesh', at='message')
		pm.parent(pose_mesh.mesh, w=True)
		pose_mesh.mesh.v.set(1)
		
		self.edit_inst.pynode.poseMesh >> pose_mesh.mesh.poseMesh
		
		# Duplicate the mesh again.  This is the extra mesh the artist can view his changes one either
		# Multiple or Single pose.  This mesh does not get edited.
		if not multi_edit:
			flag_utils.zero_flags([self.edit_inst])
		live_mesh = mesh.duplicate(label='live_edit')
		live_mesh.mesh.addAttr('liveEditMesh', at='message')
		pm.parent(live_mesh.mesh, w=True)
		live_mesh.mesh.tx.set(25)
		live_mesh.mesh.v.set(1)
		
		self.edit_inst.pynode.liveEditMesh >> live_mesh.mesh.liveEditMesh
		
		# Make sure they are not under any layers
		display_layers.remove_objects_from_layers([live_mesh.mesh, pose_mesh.mesh])
		
		# Create a parallel blend shape
		self.edit_inst.set_all_flag_block_values()
		if multi_edit:
			# Get the main blend shape mesh so we can duplicate it and edit it
			extra_head_mesh = self.duplicate_head_mesh_extra()
			
		if extra_head_mesh and mesh.type_name == 'head_mesh':
			extra_head_mesh.v.set(0)
		
		parallel_blendnode = blendshape_model.create_parallel_blendnode(diff_mesh=mesh.mesh,
																		pose_mesh=pose_mesh.mesh,
																		last_mesh=live_mesh.mesh,
																		name='pose_edit_parallel_blendnode')
		parallel_blendnode.addAttr('parallelBlendnode', at='message')
		self.edit_inst.pynode.parallelBlendnode >> parallel_blendnode.parallelBlendnode
		
		if multi_edit:
			# Reset all the flags - If we are in Multi Edit mode.  We do the opposite of Single.
			# We duplicate the Meshes with all of the poses and then remove them with the flags.
			# The User will edit the mesh with all of the poses, but can see their changes on the single pose
			# On the extra duplicated mesh.
			flag_utils.zero_flags([self.edit_inst])
			# Set the main flag
			self.edit_inst.set_main_flag()
			self.edit_inst.multi_pose = True
		
		self.show_display_layers()
		if show_skel:
			self.hide_display_layers(skip_layers=[frag.SKEL_LYR])
		else:
			self.hide_display_layers()
		if transfer_jnts:
			self.transfer_joints(pose_mesh.mesh)
		side = self.edit_inst.pynode.poseSide.get()
		vert_utils.set_vertex_symmetry(side=side, symmetry=symmetry)
		
		pm.select(cl=True)
	
	def pose_edit_end(self, multi_edit=False, due_mirror=False, due_export=False, transfer_jnts=False):
		"""
		Ends the editing mode and updates the rig with the newly updated pose.
		
		:param bool multi_edit: If False it puts the user in a Single pose Edit.
								IF True, puts the user in a multi pose edit.
		:param bool due_mirror: IF True, will mirror the mesh and updated the mirrored mesh on the rig.
		:param bool due_export: If True, will export the meshes so they are saved in Plastic.
		"""
		
		pose_mesh = self.edit_inst.pynode.poseMesh.get()
		live_mesh = self.edit_inst.pynode.liveEditMesh.get()
		extra_head_mesh = self.edit_inst.pynode.dupPosesMesh.get()
		parallel_blendnode = self.edit_inst.pynode.parallelBlendnode.get()
		old_pose_mesh = pm.PyNode(self.edit_inst.pynode.poseName.get())
		mesh = face_model.FaceModel(self.edit_inst.pynode.mesh.get())
		parameter_node = frag.FragFaceParameters(self.edit_inst.pynode.parameterNode.get())
		frag_root = frag.get_frag_root(parameter_node)
		asset_id = frag_root.asset_id
		if transfer_jnts:
			mesh.connect_joints(asset_id=asset_id)
		# delete the extra head mesh
		if extra_head_mesh:
			pm.delete(extra_head_mesh)
		
		# Get old meshes placement
		old_mesh_pos = pm.xform(old_pose_mesh, q=True, t=True, ws=True)
		old_pose_parent = old_pose_mesh.getParent()
		pm.delete(old_pose_mesh)
		
		if not multi_edit:
			# replace the old mesh with the new one
			attr_utils.purge_user_defined_attrs([pose_mesh], skip_dialog=True)
			new_pose_mesh = pose_mesh
			pm.rename(new_pose_mesh, self.edit_inst.pynode.poseName.get())
			pm.xform(new_pose_mesh, t=old_mesh_pos, ws=True)
			pm.parent(new_pose_mesh, old_pose_parent)
		else:
			new_pose_mesh = blendshape_model.dup_and_delete_mesh(live_mesh, remove_user_attrs=True)
			pm.rename(new_pose_mesh, self.edit_inst.pynode.poseName.get())
			pm.xform(new_pose_mesh, t=old_mesh_pos, ws=True)
			pm.parent(new_pose_mesh, old_pose_parent)
			
		# Disconnect all blend shape from the rig.
		blendnode = mesh.get_main_blendnode()
		blendnode.disconnect_from_rig()
		pm.delete(blendnode.blendnode)
		
		# Mirror Pose
		parameters_inst = mesh.get_parameters()
		parameter = parameters_inst.get_parameter(str(new_pose_mesh))
		mirror_pose = parameter.mirror
		mirror_mesh = None
		if mirror_pose and due_mirror:
			if mesh.mirror_self:
				mirror_mesh = self.mirror_edited_mesh(pose_mesh=new_pose_mesh,
														mesh=mesh,
														mirror_pose_name=mirror_pose,
														asset_id=asset_id)
				attr_utils.purge_user_defined_attrs([mirror_mesh], skip_dialog=True)
				dialogs.display_view_message(text='Mirroring Successful!', header='Face Editing')
		
		# Get the parameters and reconnect the blend shapes to the rig
		#parameters_inst = mesh.get_parameters()
		shapes = parameters_inst.get_pose_list()
		shapes = [x for x in shapes if pm.objExists(x)]
		
		parameters = parameters_inst.get_parameters_list()
		
		new_blendnode = blendshape_node.BlendShapeNode.create(shapes=shapes,
																mesh=mesh.mesh,
																label=(mesh.type_name).split('_')[0])
		
		new_blendnode.reconnect_to_rig(parameters, parameter_node)
		
		# Export the meshes if necessary.
		if due_export:
			pose_list = [new_pose_mesh]
			if mirror_mesh:
				pose_list = [new_pose_mesh, mirror_mesh]
			for pose in pose_list:
				pose_parent = pose.getParent()
				pm.parent(pose, w=True)
				self.export_blendshape(str(pose), asset_id)
				pm.parent(pose, pose_parent)
		
		# Clean up
		if pm.objExists(parallel_blendnode):
			pm.delete(parallel_blendnode)
		if not multi_edit and pm.objExists(live_mesh):
			pm.delete(live_mesh)
		elif multi_edit and pm.objExists(pose_mesh):
			pm.delete(pose_mesh)
		vert_utils.set_vertex_symmetry(symmetry=False)
		self.hide_display_layers()
		self.show_display_layers([frag.FLAGS_CONTACT_LYR, frag.SKEL_LYR, frag.FLAGS_DETAIL_LYR])
		
		# Set the rig settings - put it back to the original flag settings before editing
		self.edit_inst.set_main_flag()
		self.edit_inst.set_all_flag_block_values()
		
		pm.delete(self.edit_inst.pynode)
		
		face_skinning.apply_face_skinning_from_file(asset_id, mesh.mesh)
		
		pm.select(cl=True)
	
	def pose_edit_cancel(self):
		"""
		Cancels the edit modes.
		"""
		
		pose_mesh = self.edit_inst.pynode.poseMesh.get()
		live_mesh = self.edit_inst.pynode.liveEditMesh.get()
		extra_head_mesh = self.edit_inst.pynode.dupPosesMesh.get()
		parallel_blendnode = self.edit_inst.pynode.parallelBlendnode.get()
		
		# delete the extra head mesh
		if extra_head_mesh:
			pm.delete(extra_head_mesh)
		
		# Clean up
		pm.delete(parallel_blendnode)
		pm.delete(live_mesh)
		pm.delete(pose_mesh)
		
		self.hide_display_layers()
		self.show_display_layers([frag.FLAGS_CONTACT_LYR, frag.SKEL_LYR, frag.FLAGS_DETAIL_LYR])
		
		# Set the rig settings - put it back to the original flag settings before editing
		self.edit_inst.set_main_flag()
		self.edit_inst.set_all_flag_block_values()
		pm.delete(self.edit_inst.pynode)
		vert_utils.set_vertex_symmetry(symmetry=False)
		pm.select(cl=True)
	
	def paint_neutral_start(self, symmetry=False):
		"""
		Puts the UI and scene in a state where the artist can paint back the neutral pose on a blend shape.
		Only available in Single Pose Edit.  Single pose edit will always be activated when using this tool.
		
		:param bool symmetry: Turn on/off Blend shape symmetry.
		"""
		
		self.edit_inst.paint_neutral = True
		# get the pose
		mesh = face_model.FaceModel(self.edit_inst.pynode.mesh.get())
		pose_mesh = self.edit_inst.pynode.poseMesh.get()
		# the mesh is posed.  Remove the pose, duplicate it and reset the pose.
		flag_utils.zero_flags([self.edit_inst])
		
		# Create the new neutral pose so we do not need to use the main mesh.
		neutral_pose = blendshape_model.duplicate_mesh(mesh.mesh, label=f'neutral_pose_edit')
		neutral_pose.addAttr('neutralPose', at='message')
		pm.parent(neutral_pose, w=True)
		neutral_pose.v.set(0)
		display_layers.remove_objects_from_layers([neutral_pose])
		
		self.edit_inst.pynode.neutralPose >> neutral_pose.neutralPose
		
		# Reset the main flags on the main mesh.
		#self.edit_inst.set_main_flag()
		
		# Create a blend shape, so we can paint back the neutral pose.
		blendnode = blendshape_node.BlendShapeNode.create(neutral_pose, pose_mesh)
		blendnode.blendnode.weight[0].set(1)
		blendnode.set_blendshape_weights()
		pm.select(pose_mesh)
		
		# Opens the Maya Blend Shape Paints Weights tool
		mel.eval('ArtPaintBlendShapeWeightsToolOptions')
		
		if symmetry:
			side = self.edit_inst.pynode.poseSide.get()
			blendshape_model.set_blendshape_weight_symmetry(side)
		pm.select(pose_mesh)
	
	def paint_neutral_end(self):
		"""
		Applies the neutral blend shape painting to the current pose being edited.
		"""
		
		self.edit_inst.paint_neutral = False
		# dup and delete pose_mesh
		mesh = face_model.FaceModel(self.edit_inst.pynode.mesh.get())
		pose_mesh = self.edit_inst.pynode.poseMesh.get()
		uv_pin_nodes = []
		pose_mesh_shape = pose_mesh.getShape()
		connected_nodes = pose_mesh_shape.listConnections(d=True, s=False)
		for node in connected_nodes:
			if isinstance(node, pm.nodetypes.UvPin):
				uv_pin_nodes.append(node)
		if uv_pin_nodes:
			rivet_group = next((xform for xform in pm.ls(type=pm.nt.Transform) if xform.hasAttr('isRivetGrp')), None)
			if rivet_group:
				pm.delete(rivet_group)

		pose_mesh = blendshape_model.dup_and_delete_mesh(pose_mesh)
		if uv_pin_nodes:
			self.transfer_joints(pose_mesh)

		self.edit_inst.pynode.poseMesh >> pose_mesh.poseMesh

		neutral_pose = self.edit_inst.pynode.neutralPose.get()
		pm.delete(neutral_pose)

		# Reconnect parallel_blend - Set the scene back up to the Single pose edit.
		parallel_blendnode = self.edit_inst.pynode.parallelBlendnode.get()
		if parallel_blendnode:
			pm.delete(parallel_blendnode)
		
		parallel_blendnode = blendshape_model.create_parallel_blendnode(diff_mesh=mesh.mesh,
																		pose_mesh=pose_mesh,
																		last_mesh=self.edit_inst.pynode.liveEditMesh.get(),
																		name='pose_edit_parallel_blendnode')
		parallel_blendnode.addAttr('parallelBlendnode', at='message')
		self.edit_inst.pynode.parallelBlendnode >> parallel_blendnode.parallelBlendnode

		blendshape_model.set_blendshape_weight_symmetry(symmetry=False)

		# set flags back to the selected poses
		#self.edit_inst.set_main_flag()
	
	def paint_neutral_cancel(self):
		"""
		Cancels out the the blend shape painting and returns the artist back to
		single pose edit mode without any changes from blend shape painting.
		"""
		
		self.edit_inst.paint_neutral = False
		
		neutral_pose = self.edit_inst.pynode.neutralPose.get()
		blendnode = blendshape_model.get_first_blendnode(neutral_pose)
		pm.delete(neutral_pose, blendnode)
		
		blendshape_model.set_blendshape_weight_symmetry(symmetry=False)
		# set flags back to the selected poses
		self.edit_inst.set_main_flag()
	
	def base_edit_start(self, symmetry=False, show_skel=False, replace_mesh=None):
		"""
		Puts the tool in a state where the artist can update a blend shape mesh.
		It duplicates the mesh, with the pose that is to be updated.

		:param bool show_skel: If True, it will unhide the skeleton.
		:param bool symmetry: If True, will turn on Maya's modeling Symmetry options.
		"""
		
		# Reset all the flags -  This is for Single pose edit.  We start with no poses and then add them with
		# the Flags.
		flag_utils.zero_flags([self.edit_inst])
		# # Set the main flag
		# self.edit_inst.set_main_flag()
		self.edit_inst.base_edit = True
		
		# Get the main blend shape mesh so we can duplicate it and edit it
		mesh = face_model.FaceModel(self.edit_inst.pynode.mesh.get())
		
		if not replace_mesh:
			# Duplicate the mesh.  This will be the mesh the artist will edit.
			pose_mesh = mesh.duplicate(label=f'{self.edit_inst.pynode.poseName.get()}_edit')
			pm.parent(pose_mesh.mesh, w=True)
			pose_mesh.mesh.tx.set(25)
			pose_mesh.mesh.v.set(1)
		else:
			pose_mesh = face_model.FaceModel(replace_mesh)
		
		pose_mesh.mesh.addAttr('poseMesh', at='message')
		
		self.edit_inst.pynode.poseMesh >> pose_mesh.mesh.poseMesh
		
		# Duplicate the mesh again.  This is the extra mesh the artist can view his changes one either
		# Multiple or Single pose.  This mesh does not get edited.

		live_mesh = mesh.duplicate(label='live_edit')
		live_mesh.mesh.addAttr('liveEditMesh', at='message')
		pm.parent(live_mesh.mesh, w=True)
		live_mesh.mesh.v.set(0)
		
		self.edit_inst.pynode.liveEditMesh >> live_mesh.mesh.liveEditMesh
		
		# Make sure they are not under any layers
		display_layers.remove_objects_from_layers([live_mesh.mesh, pose_mesh.mesh])
		
		# Create a parallel blend shape
		
		parallel_blendnode = blendshape_model.create_parallel_blendnode(diff_mesh=live_mesh.mesh,
																		pose_mesh=pose_mesh.mesh,
																		last_mesh=mesh.mesh,
																		name='pose_edit_parallel_blendnode')
		parallel_blendnode.addAttr('parallelBlendnode', at='message')
		self.edit_inst.pynode.parallelBlendnode >> parallel_blendnode.parallelBlendnode
	
		# Set the flags again
		self.edit_inst.set_all_flag_block_values()
		
		if show_skel:
			self.hide_display_layers()
			self.show_display_layers(skip_layers=[frag.FLAGS_CONTACT_LYR, frag.FLAGS_DETAIL_LYR])
		else:
			self.hide_display_layers()
			self.show_display_layers(skip_layers=[frag.FLAGS_CONTACT_LYR, frag.SKEL_LYR, frag.FLAGS_DETAIL_LYR])
		
		vert_utils.set_vertex_symmetry(side='center', symmetry=symmetry)
	
	def base_edit_end(self, due_export=False):
		"""
		Ends the editing mode and updates the rig with the newly updated pose.
		
		:param bool due_export: If True, will export the meshes so they are saved in Plastic.
		"""
		
		mesh = face_model.FaceModel(self.edit_inst.pynode.mesh.get())
		parameter_node = frag.FragFaceParameters(self.edit_inst.pynode.parameterNode.get())
		face_component = frag.get_face_mesh_component(parameter_node.pynode)
		frag_root = frag.get_frag_root(parameter_node)
		asset_id = frag_root.asset_id
		parameter_inst = face_util.get_parameters_region_instance(asset_id=asset_id, region_name=mesh.region)
		
		skin_mesh = face_component.get_mesh(mesh.type_name, frag.FACE_SKINNED_CATEGORY)
		skin_mesh = face_model.FaceModel(skin_mesh)
		
		# Disconnect all blend shape from the rig.
		blendnode = mesh.get_main_blendnode()
		shapes = blendnode.shapes
		blendnode.disconnect_from_rig()
		pose_grp = cmds.listRelatives(shapes[0], p=True)
		blendnode.delete_blendshapes()
		
		new_shapes = blendnode.generate_face_shapes()
		pm.delete(blendnode.blendnode)
		
		new_mesh = mesh.dup_and_delete()
		blendnode = blendshape_node.BlendShapeNode.create(shapes=new_shapes,
															mesh=new_mesh.mesh,
															label=new_mesh.part_type_name)
		
		if due_export:
			path = paths.get_face_blendshape_path(asset_id)
			blendshapes_meshes = list(map(lambda x: str(x), new_shapes))
			face_import_export.export_blendshapes(path=path, meshes=blendshapes_meshes, remove_mtls=True)
		
		if pose_grp:
			pm.parent(new_shapes, pose_grp[0])
		
		parameters = parameter_inst.get_parameters_list()
		blendnode.reconnect_to_rig(parameters=parameters, parameter_node=parameter_node)
		
		self.base_edit_cancel(set_block_values=False)
		face_util.sort_shapes(new_shapes)
		display_layers.remove_objects_from_layers(new_shapes)
		
		# clean up the meshes
		# Need to recreate the skinned mesh and connect both meshes back to the mesh component.
		new_mesh.reconnect_to_mesh_component(asset_id=asset_id)
		skin_mesh = self.swap_mesh_with_new_base(skin_mesh, new_mesh)
		skin_mesh.reconnect_to_mesh_component(asset_id=asset_id)

		face_skinning.apply_face_skinning_from_file(asset_id, new_mesh.mesh)
		face_skinning.apply_face_skinning_from_file(asset_id, skin_mesh.mesh)
		
	def base_edit_cancel(self, set_block_values=True):
		"""
		Cancels the edit mode.
		"""
		
		pose_mesh = self.edit_inst.pynode.poseMesh.get()
		live_mesh = self.edit_inst.pynode.liveEditMesh.get()
		parallel_blendnode = self.edit_inst.pynode.parallelBlendnode.get()
		
		# Clean up
		pm.delete(parallel_blendnode)
		pm.delete(live_mesh)
		pm.delete(pose_mesh)
		
		self.hide_display_layers()
		self.show_display_layers([frag.FLAGS_CONTACT_LYR, frag.SKEL_LYR, frag.FLAGS_DETAIL_LYR])
		
		# Set the rig settings - put it back to the original flag settings before editing
		if set_block_values:
			self.edit_inst.set_all_flag_block_values()
			pm.delete(self.edit_inst.pynode)
		vert_utils.set_vertex_symmetry(symmetry=False)
		pm.select(cl=True)
	
	def duplicate_head_mesh_extra(self):
		"""
		Returns an extra pose head mesh.
		
		:return: Returns an extra pose head mesh.
		:rtype: pm.nt.Transform
		"""
		
		parameter_node = frag.FragFaceParameters(self.edit_inst.pynode.parameterNode.get())
		face_component = frag.get_face_mesh_component(parameter_node.pynode)
		head_mesh = face_component.get_mesh('head_mesh', frag.FACE_BLENDSHAPE_CATEGORY)
		
		dup_mesh = blendshape_model.duplicate_mesh(mesh=head_mesh, label='DELETE_ME_DUP_MESH', remove_user_attrs=True)
		dup_mesh.addAttr('dupPosesMesh', at='message')
		pm.parent(dup_mesh, w=True)
		display_layers.remove_objects_from_layers(dup_mesh)
		self.edit_inst.pynode.dupPosesMesh >> dup_mesh.dupPosesMesh
		return dup_mesh
	
	def replace_base(self, replace_mesh, due_export=False):
		self.base_edit_start(replace_mesh=replace_mesh)
		self.base_edit_end(due_export=due_export)
	
	def swap_mesh_with_new_base(self, old_mesh, new_mesh):
		"""
		Swaps a new mesh with an old mesh and adding the markup data.
		
		:param face_model.FaceModel old_mesh: An instance of face_model.FaceModel that represents the unedited mesh.
		:param face_model.FaceModel new_mesh: An instance of face_model.FaceModel that represents the edited mesh.
		:return: Returns An instance of face_model.FaceModel that represents the edited mesh.
		:rtype: face_model.FaceModel
		"""
		
		mark_up = old_mesh.mesh.matMeshMarkup.get()
		old_parent = old_mesh.mesh.getParent()
		dup_mesh = pm.duplicate(new_mesh.mesh, n='TEMPFACEEDITMESH')[0]
		if not dup_mesh.hasAttr('matMeshMarkup'):
			dup_mesh.addAttr('matMeshMarkup', dt='string')
		old_mesh_name = str(old_mesh.mesh)
		pm.delete(old_mesh.mesh)
		dup_mesh.rename(old_mesh_name)
		dup_mesh.matMeshMarkup.set(mark_up)
		if old_parent:
			pm.parent(dup_mesh, old_parent)
		dup_mesh.v.set(0)
		return face_model.FaceModel(dup_mesh)
	
	def export_blendshape(self, pose_mesh, asset_id):
		"""
		Exports a blend shape pose.
		
		:param str pose_mesh: Pose mesh name.
		:param str asset_id: Asset identifier.
		"""
		
		path = paths.get_face_blendshape_path(asset_id)
		face_import_export.export_blendshapes(path, pose_mesh, remove_mtls=True)
		dialogs.display_view_message(text=f'{pose_mesh}: Exported Successfully', header='Face Editing')
	
	def mirror_edited_mesh(self, pose_mesh, mesh, mirror_pose_name, asset_id):
		"""
		Mirrors a mesh and renames it to the mirrored pose.
		
		:param str pose_mesh: Name of the original pose being edited.
		:param FaceModel mesh: Name of the blend shape that has all the blend shapes attached.
		:param str mirror_pose_name: name of the mirrored pose.
		:param str asset_id: Asset identifier.
		:return: Returns the mirrored mesh.
		:rtype: pm.nt.Transform
		"""
		
		if not isinstance(mesh, face_model.FaceModel):
			mesh = face_model.FaceModel(mesh)
		
		mirror_mesh = pm.PyNode(mirror_pose_name)
		
		region_data = mesh.get_region_data(asset_id)
		mirror_data = region_data.get_mirror_data()
		dup_mesh = pm.duplicate(pose_mesh, n=f'temp_mirror_pose')[0]
		mirror_data.mirror_mesh(mesh_name=dup_mesh)
		
		old_pose_parent = mirror_mesh.getParent()
		pos = pm.xform(mirror_mesh, q=True, t=True, ws=True)
		
		pm.delete(mirror_mesh)
		dup_mesh.rename(mirror_pose_name)
		pm.parent(dup_mesh, old_pose_parent)
		
		pm.xform(dup_mesh, t=pos, ws=True)
		return dup_mesh
	
	def get_display_layers(self):
		"""
		Gets all the display layers from frag.DisplayLayers
		"""
		
		# Hide the Display Layers
		frag_rig = frag.get_frag_rig(self.edit_inst.pynode)
		dsp_lyrs = frag_rig.get_frag_children(of_type=frag.DisplayLayers)
		if not dsp_lyrs:
			return
		self.dsp_lyrs = dsp_lyrs[0]
	
	def show_display_layers(self, skip_layers=()):
		"""
		Makes the Rig layers visible expected for what is in the skip list.
		
		:param list(str) skip_layers:  The layers to skip
		"""
		
		self.get_display_layers()
		# Hide the Display Layers
		layers = self.dsp_lyrs.get_layers()
		for lyr in layers:
			if skip_layers and lyr in skip_layers:
				continue
			self.dsp_lyrs.show_layer(str(lyr))
	
	def hide_display_layers(self, skip_layers=()):
		"""
		Makes the Rig layers not visible expected for what is in the skip list.

		:param list(str) skip_layers:  The layers to skip
		"""
		
		self.get_display_layers()
		# Hide the Display Layers
		layers = self.dsp_lyrs.get_layers()
		for lyr in layers:
			if skip_layers and lyr in skip_layers:
				continue
			self.dsp_lyrs.hide_layer(str(lyr))
		
	def lock_display_layers(self, skip_layers=()):
		"""
		Makes the Rig layers locked expected for what is in the skip list.

		:param list(str) skip_layers:  The layers to skip
		"""
		
		self.get_display_layers()
		# Lock the Display Layers
		layers = self.dsp_lyrs.get_layers()
		for lyr in layers:
			if skip_layers and lyr in skip_layers:
				continue
			self.dsp_lyrs.set_layer_to_reference(str(lyr))
	

	def transfer_joints(self, new_mesh):
		"""
		Connects joints through UV pins to a new mesh

		:param new_mesh: Mesh that will receive UV pins
		"""

		new_mesh_model = face_model.FaceModel(new_mesh)
		frag_rig_node = self.edit_inst.pynode.fragParent.listConnections()[0]
		frag_root = frag.get_frag_root(frag_rig_node)
		asset_id = frag_root.asset_id
		new_mesh_model.connect_joints(asset_id=asset_id)
