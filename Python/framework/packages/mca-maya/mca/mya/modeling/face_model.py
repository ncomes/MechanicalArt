#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Face: Utility Functions. """

# system global imports
from __future__ import print_function, division, absolute_import

# software specific imports
import pymel.core as pm
import maya.cmds as cmds

# mca python imports
from mca.mya.rigging import tek
from mca.common.utils import lists
from mca.mya.rigging import mesh_markup_rig
from mca.mya.face.face_utils import face_util, face_import_export
from mca.mya.modeling import blendshape_model, blendshape_node
from mca.mya.utils import attr_utils, naming, display_layers
from mca.common import log

logger = log.MCA_LOGGER


class FaceModel:
	def __init__(self, mesh):
		if isinstance(mesh, str):
			mesh = pm.PyNode(mesh)
		self._mesh = mesh
	
	@property
	def mesh(self):
		return self._mesh
	
	@classmethod
	def create(cls, mesh):
		"""
		Creates an instance of the class using either the base mesh or the source mesh.

		:param pm.nt.Transform mesh: Whether to search for the base mesh or the source mesh.  By default it will search for the base mesh.
		:return class instance:
		:rtype:
		"""
		
		return cls(mesh)
	
	def get_string_name(self, include_namespace=False):
		"""
		Returns the string name of the mesh

		:param bool include_namespace: include the namespace
		:return: mesh name
		:rtype: str
		"""
		
		if not include_namespace and ':' in self.mesh.nodeName():
			string_mesh = str(naming.get_basename(self.mesh))
		else:
			return self.mesh.nodeName()
		return string_mesh
	
	@property
	def mesh_markup(self):
		return mesh_markup_rig.MeshMarkup(self.mesh)
	
	@property
	def region(self):
		return self.mesh_markup.region
	
	@property
	def type_name(self):
		return self.mesh_markup.type_name
	
	@property
	def category(self):
		return self.mesh_markup.category
	
	@category.setter
	def category(self, value):
		self.mesh_markup.category = value
		new_dict = self.mesh_markup.get_dict()
		self.mesh_markup.set_dict(new_dict)
	
	@property
	def side(self):
		return self.mesh_markup.side
	
	@property
	def mirror_type(self):
		return self.mesh_markup.mirror_type
	
	@property
	def race(self):
		return self.mesh_markup.race
	
	@property
	def source_mesh(self):
		return self.mesh_markup.source_mesh
	
	@source_mesh.setter
	def source_mesh(self, value):
		self.mesh_markup.source_mesh = value
		new_dict = self.mesh_markup.get_dict()
		self.mesh_markup.set_dict(new_dict)
	
	def mirror_self(self):
		return self.mirror_type == 'mirror_self'
	
	@property
	def part_type_name(self):
		"""
		Returns the 1st part of the name

		:return: Returns the 1st part of the name
		:rtype: str
		"""
		
		name = self.type_name.split('_')[0]
		if name == 'left' or name == 'right' or name == 'center':
			name = self.type_name.split('_')[1]
		return name
	
	def set_markup(self, type_name, category, side, **kwargs):
		"""
		Creates the "matMeshMarkup" attribute on the mesh and adds the markup.

		:param str type_name: a key word on what type of meshes are in this region.  Examples: head_mesh, jaw_mesh, etc...
		:param str category: a key word on what type of category the meshes belong to in this region.
		Examples: skin_mesh, blendshape_mesh, etc...
		:param str side: side the mesh is on.
		:param str kwargs: Any added data that needs to be tagged.
		"""
		
		self.mesh_markup.create(self.mesh, type_name, category, side, **kwargs)
	
	def delete(self):
		"""
		Deletes it's self and any blendshapes connected to it.
		"""
		
		blendnodes = self.mesh.getShape().listConnections(type=pm.nt.BlendShape)
		if blendnodes:
			pm.delete(blendnodes)
		pm.delete(self.mesh)
	
	def connect_joints(self,
	                   asset_id=None,
	                   delete_rivets=False,
	                   delete_old_rivet_grp=True):
		"""
		Connects joints to the blend shape model using rivets.

		:param str asset_id: ID of the asset we want to retrieve path of.
		:param bool delete_rivets: Deletes the rivets when the task is complete.
		:param bool delete_old_rivet_grp: Checks for and deletes old rivet group.
		:return: Returns a list of the created rivets
		:rtype: list[str]
		"""
		try:
			mesh_data = self.get_region_data(asset_id)
		except FileNotFoundError:
			logger.info(f'No source data found for {asset_id}, using common')
			mesh_data = face_util.get_common_face_region_data(self.region)
		
		# may not need to unlock skeleton
		self.unlock_skeleton_display_layer()
		
		# Get the UV data.  This is positions and names.
		uv_positions = mesh_data.get_joints_uv()
		
		# See if the rivets exist.  If they do, remove them.
		ns = self.mesh.namespace()
		rivet_names = uv_positions.rivet_names
		rivet_names = list(map(lambda x: f'{ns}{x}', rivet_names))
		[pm.delete(x) for x in rivet_names if pm.objExists(x)]
		# See if the rivet group exists and delete if desired. If not, old rivet group is used.
		check_for_grp = pm.objExists(f'{ns}rivet_grp')
		if check_for_grp and delete_old_rivet_grp:
			pm.delete(f'{ns}rivet_grp')
		
		rivets = uv_positions.connect_all_rivets_joints(self.mesh)
		if check_for_grp and not delete_old_rivet_grp:
			rivet_grp = pm.PyNode(f'{ns}rivet_grp')
		else:
			rivet_grp = pm.group(em=True, n='rivet_grp')
			rivet_grp.addAttr('isRivetGrp', at='bool', k=True)
		
		pm.parent(rivet_names, rivet_grp)
		rivet_grp.v.set(0)
		if delete_rivets:
			pm.delete(rivet_grp)
		
		return rivets
	
	def reconnect_to_mesh_component(self, asset_id=None):
		"""
		Reconnects a mesh to the mesh_component

		:param str asset_id: ID of the asset we want to retrieve path of.
		"""
		
		if not asset_id:
			tek_rig = tek.get_tek_rig(self.mesh)
			tek_root = tek_rig.get_tek_parent()
			asset_id = tek_root.assetID.get()
		
		all_roots = tek.get_all_tek_roots()
		tek_root = [x for x in all_roots if x.asset_id == asset_id]
		if not tek_root:
			return
		tek_root = tek_root[0]
		skeletal_mesh = tek_root.get_skeletal_mesh()
		face_components = skeletal_mesh.get_tek_children(of_type=tek.FaceMeshComponent)
		if not face_components:
			return
		face_component = face_components[0]
		face_component.reconnect_mesh(self.mesh, self.type_name, self.category)
	
	def reconnect_shapes_to_rig(self, asset_id, parameter_node=None):
		"""
		Reconnects blend shapes back to the rig.

		:param str asset_id: ID of the asset we want to retrieve path of.
		:param tek.FragFaceParameters parameter_node: The node that connects the blend shapes to the rig.
		:return: If True, The shapes were successfully connected.
		:rtype: Bool
		"""
		
		if not parameter_node:
			tek_rig = tek.get_tek_rig(self.mesh)
			if not tek_rig:
				return False
			parameter_node = tek_rig.get_tek_children(of_type=tek.FragFaceParameters)
			if not parameter_node:
				return False
			parameter_node = parameter_node[0]
		
		blendnode = self.get_main_blendnode()
		if blendnode:
			pm.delete(blendnode.blendnode)
		parameters_inst = self.get_parameters(asset_id)
		parameter_list = parameters_inst.get_parameters_list()
		shapes = parameters_inst.get_pose_list()
		shapes = [x for x in shapes if cmds.objExists(x)]
		
		new_blendnode = blendshape_node.BlendShapeNode.create(shapes=shapes,
		                                                      mesh=self.mesh,
		                                                      label=self.part_type_name)
		
		new_blendnode.reconnect_to_rig(parameter_list, parameter_node)
		return True
	
	def get_face_mesh_component(self):
		"""
		Returns the FaceMeshComponent that is attached to the mesh.

		:return: Returns the FaceMeshComponent that is attached to the mesh.
		:rtype: FaceMeshComponent
		"""
		
		comp_list = [x for x in self.mesh.message.listConnections() if
		             x.hasAttr('tekType') and x.tekType.get() == 'FaceMeshComponent']
		if not comp_list:
			return
		face_component = comp_list[0]
		return tek.TEKNode(face_component)
	
	def get_parameters(self, asset_id=None):
		"""
		Returns an instanced of ParameterData.  This is has all the data about the poses.

		:param str asset_id: ID of the asset we want to retrieve path of.
		:return: Returns an instanced of ParameterData.
		:rtype: ParameterData
		"""
		
		if not asset_id:
			tek_rig = tek.get_tek_rig(self.mesh)
			tek_root = tek_rig.get_tek_parent()
			asset_id = tek_root.assetID.get()
		
		# returns the tek.face_parameters.ParameterData instance
		parameters = face_util.get_parameters_region_instance(asset_id=asset_id, region_name=self.region)
		return parameters
	
	def get_region_data(self, asset_id=None):
		"""
		Returns an instance of the FaceMeshRegionData.

		:param str asset_id: ID of the asset we want to retrieve path of.
		:return:Returns an instance of the FaceMeshRegionData.
		:rtype: FaceMeshRegionData
		"""
		
		if not asset_id:
			tek_rig = tek.get_tek_rig(self.mesh)
			tek_root = tek_rig.get_tek_parent()
			asset_id = tek_root.assetID.get()
		mesh_data = face_util.get_face_region_data(asset_id=asset_id, region_name=self.region)
		return mesh_data
	
	def unlock_skeleton_display_layer(self):
		"""
		Unlocks the skins layer so all the head meshes can be edited.
		"""
		
		control_rig = tek.get_tek_rig(self.mesh)
		if control_rig:
			world_root = tek.get_root_joint(control_rig)
			joint = lists.get_first_in_list(world_root.listRelatives(c=True))
			display_layer = lists.get_first_in_list(display_layers.get_display_layers([joint]))
			if display_layer:
				if display_layer.displayType.get() == 1 or display_layer.displayType.get() == 2:
					display_layer.displayType.set(0)
				else:
					display_layer.displayType.set(2)
	
	def clean_up_mesh(self, remove_user_attrs=True,
	                  remove_poly_blind=True,
	                  remove_deform_shapes=True,
	                  unlock_normals=True,
	                  remove_layer=True,
	                  delete_history=True):
		"""
		Cleans up a blend shape mesh and strips it down to the core so the file is small.

		:param bool remove_poly_blind: Searches for PolyBlindData nodes and deletes them
		:param bool remove_deform_shapes: Deletes extra deformable shapes that are not used.
		:param bool unlock_normals: Unlocks the poly normals on the mesh.
		:param bool remove_layer: Removes from the display layer.
		"""
		
		# Removes User Defined Attributes
		if remove_user_attrs:
			attr_utils.purge_user_defined_attrs(self.mesh)
		
		# delete PolyBlindData since we are not using skinning info and will keep file size down.
		if remove_poly_blind:
			poly_blind_data = self.mesh.getShape().listConnections(type=pm.nt.PolyBlindData)
			pm.delete(poly_blind_data)
		
		# delete any unwanted deformers to keep file size down
		if remove_deform_shapes:
			deformable_shapes = self.mesh.listRelatives()
			[pm.delete(x) for x in deformable_shapes if str(self.mesh) not in str(x)]
		
		# unlock the normals
		if unlock_normals:
			pm.polyNormalPerVertex(self.mesh, ufn=True)
			pm.polySoftEdge(self.mesh, a=180, ch=1)
			pm.select(cl=True)
		
		if remove_layer:
			display_layers.remove_objects_from_layers(self.mesh)
		
		if delete_history:
			pm.delete(self.mesh, ch=True)
	
	def import_blendshapes(self, asset_id=None, ext='.obj', exist_check=False):
		"""
		Imports all the blend shapes associated with the mesh.
		:param str asset_id: Asset Identifier.
		:param str ext: The file extension.
		:param bool exist_check: If True, will check to see if the mesh is already in the scene.
		:return: Returns a list of all the shapes that were imported.
		:rtype: list(str)
		"""
		
		if not asset_id:
			tek_rig = tek.get_tek_rig(self.mesh)
			tek_root = tek_rig.get_tek_parent()
			asset_id = tek_root.assetID.get()
		shape_result = face_import_export.import_all_blendshapes(asset_id=asset_id,
		                                                         region=self.region,
		                                                         ext=ext,
		                                                         exist_check=exist_check)
		return shape_result
	
	def get_blendnode(self):
		"""
		Returns a blend node.  If you pass in a mesh it will grab the 1st blend node.

		:return: Returns a blend node.
		:rtype: pm.nt.Blendnode
		"""
		
		first_blendnode = blendshape_model.get_first_blendnode(self.mesh)
		if not first_blendnode:
			# raising error, it can get confusing if this returns none.
			raise RuntimeError('The object is not a blend shape or an object with a blend shape attached.')
		return blendshape_node.BlendShapeNode(first_blendnode)
	
	def get_main_blendnode(self):
		"""
		Returns a blend node.  Gets the blend node with the "main" type.

		:return: Returns a blend node.
		:rtype: pm.nt.Blendnode
		"""
		
		all_blendnodes = blendshape_model.get_all_blendnodes(self.mesh)
		for blendnode in all_blendnodes:
			if not blendnode.hasAttr('blendNodeType'):
				continue
			if blendnode.blendNodeType.get() == 'main':
				return blendshape_node.BlendShapeNode(blendnode)
		return
	
	def duplicate(self, label=None, remove_attrs=(), remove_user_attrs=False):
		"""
		Duplicates a mesh.

		:param list remove_attrs: Removes listed attributes from the mesh.
		:param string label:  The name of the newly created mesh.
		:param bool remove_user_attrs: Removes all attributes that were added by a user.
		:return: Returns an instance of FaceModel.
		:rtype: FaceModel
		"""
		
		new_mesh = blendshape_model.duplicate_mesh(mesh=self.mesh,
		                                           label=label,
		                                           remove_attrs=remove_attrs,
		                                           remove_user_attrs=remove_user_attrs)
		return FaceModel(new_mesh)
	
	def dup_and_delete(self, label=None, remove_attrs=(), remove_user_attrs=False):
		"""
		Duplicates its a mesh and deletes the old copy. A way to generate a clean mesh/pose.

		:param list remove_attrs: Removes listed attributes from the mesh.
		:param string label:  The name of the newly created mesh.
		:param bool remove_user_attrs: Removes all attributes that were added by a user.
		:return: Returns an instance of FaceModel.
		:rtype: FaceModel
		"""
		
		new_mesh = blendshape_model.dup_and_delete_mesh(mesh=self.mesh,
		                                                label=label,
		                                                remove_attrs=remove_attrs,
		                                                remove_user_attrs=remove_user_attrs)
		return FaceModel(new_mesh)

