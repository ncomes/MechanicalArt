#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# software specific imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.mya.modifiers import ma_decorators
from mca.mya.utils import attr_utils
from mca.mya.modeling import face_model
# internal module imports
from mca.mya.rigging.tek import mesh_component, skeletal_mesh

logger = log.MCA_LOGGER

FACE_SKINNED_CATEGORY = 'skin_mesh'
FACE_BLENDSHAPE_CATEGORY = 'blendshape_mesh'
FACE_SOURCE_CATEGORY = 'source_mesh'


def get_face_mesh_component(rig_node):
	"""
	Returns an instance of the FaceMeshComponent
	
	:param pm.nt.DagNode rig_node: A node connected to the rig.
	:return: Returns an instance of the FaceMeshComponent
	:rtype: FaceMeshComponent
	"""
	
	sk_mesh = skeletal_mesh.get_tek_skeletal_mesh(rig_node)
	if not sk_mesh:
		logger.warning(f'There is no tek Skeletal Mesh connected to {rig_node}')
		return
	
	face_comp = sk_mesh.get_tek_children(of_type=FaceMeshComponent)
	if not face_comp:
		logger.warning(f'There is no face component connected to {rig_node}')
		return
	return face_comp[0]
	
	
class FaceMeshComponent(mesh_component.MeshComponent):
	VERSION = 1

	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(tek_parent, meshes_dict):
		"""
		Creates a Mesh Component that connects and tracks meshes.
	
		:param tek_parent: TEK Skeletal Mesh TEKNode.
		:param dict meshes_dict: {mesh_category: {mesh_type_names: pm.nt.PyNode}}
		:return: Returns an instance of MeshComponent
		:rtype: MeshComponent
		"""
		
		# Set Namespace
		root_namespace = tek_parent.namespace().split(':')[0]
		pm.namespace(set=':')
		if root_namespace != '':
			pm.namespace(set=f'{root_namespace}:')
		
		node = mesh_component.MeshComponent.create(tek_parent=tek_parent,
												meshes_dict=meshes_dict)
		
		new_name = f'{FaceMeshComponent.__name__}'
		node.rename(new_name)
		node.set_version(FaceMeshComponent.VERSION)
		node.tekType.set(FaceMeshComponent.__name__)
		
		for category in meshes_dict.keys():
			attr_utils.set_compound_attribute_groups(node, category, meshes_dict[category])

		return FaceMeshComponent(node)
	
	@property
	def head_mesh(self):
		"""
		Returns the mesh associated with the rig.
		
		:return Returns a mesh
		:rtype: FaceModel
		"""
		
		mesh = self.get_mesh(attr_name='head_mesh', compound_attr_name=FACE_SKINNED_CATEGORY)
		if not mesh:
			return
		return face_model.FaceModel(mesh=mesh)
	
	@property
	def head_blendshape(self):
		"""
		Returns the mesh associated with the rig.
		
		:return Returns a mesh
		:rtype: FaceModel
		"""
		
		mesh = self.get_mesh(attr_name='head_mesh', compound_attr_name=FACE_BLENDSHAPE_CATEGORY)
		if not mesh:
			return
		return face_model.FaceModel(mesh=mesh)
	
	@property
	def head_source(self):
		"""
		Returns the mesh associated with the rig.

		:return Returns a mesh
		:rtype: FaceModel
		"""
		
		mesh = self.get_mesh(attr_name='head_mesh', compound_attr_name=FACE_SOURCE_CATEGORY)
		if not mesh:
			return
		return face_model.FaceModel(mesh=mesh)
	
	@property
	def mouth_mesh(self):
		"""
		Returns the mesh associated with the rig.
		
		:return Returns a mesh
		:rtype: FaceModel
		"""
		
		mesh = self.get_mesh(attr_name='mouth_mesh', compound_attr_name=FACE_SKINNED_CATEGORY)
		if not mesh:
			return
		return face_model.FaceModel(mesh=mesh)
	
	@property
	def mouth_blendshape(self):
		"""
		Returns the mesh associated with the rig.
		
		:return Returns a mesh
		:rtype: FaceModel
		"""
		
		mesh = self.get_mesh(attr_name='mouth_mesh', compound_attr_name=FACE_BLENDSHAPE_CATEGORY)
		if not mesh:
			return
		return face_model.FaceModel(mesh=mesh)
	
	@property
	def l_eye_mesh(self):
		"""
		Returns the mesh associated with the rig.

		:return Returns a mesh
		:rtype: FaceModel
		"""
		
		mesh = self.get_mesh(attr_name='eye_left_mesh', compound_attr_name=FACE_SKINNED_CATEGORY)
		return face_model.FaceModel(mesh=mesh)
	
	@property
	def r_eye_mesh(self):
		"""
		Returns the mesh associated with the rig.

		:return Returns a mesh
		:rtype: FaceModel
		"""
		
		mesh = self.get_mesh(attr_name='eye_right_mesh', compound_attr_name=FACE_SKINNED_CATEGORY)
		if not mesh:
			return
		return face_model.FaceModel(mesh=mesh)
	
	@property
	def left_eye_cards(self):
		"""
		Returns the mesh associated with the rig.

		:return Returns a list of meshes
		:rtype: list(FaceModel)
		"""
		meshes = self.get_mesh_list('eye_cards_left', compound_attr_name=FACE_SKINNED_CATEGORY)
		if not meshes:
			return
		meshes = list(map(lambda x: face_model.FaceModel(x), meshes))
		return meshes
	
	@property
	def right_eye_cards(self):
		"""
		Returns the mesh associated with the rig.

		:return Returns a list of meshes
		:rtype: list(FaceModel)
		"""
		meshes = self.get_mesh_list('eye_cards_right', compound_attr_name=FACE_SKINNED_CATEGORY)
		if not meshes:
			return
		meshes = list(map(lambda x: face_model.FaceModel(x), meshes))
		return meshes

	def get_counterpart_mesh(self, mesh):
		"""
		Returns the opposite mesh, if Skinned mesh - returns a blend shape mesh of same type
		
		:param pm.nt.Transform mesh: The mesh that you are looking to get the opposite mesh.
		:return: Returns the opposite mesh, if Skinned mesh - returns a blend shape mesh of same type
		:rtype: face_model.FaceModel
		"""
		
		if not isinstance(mesh, face_model.FaceModel):
			mesh = face_model.FaceModel(mesh)
		category = mesh.category
		if category == FACE_BLENDSHAPE_CATEGORY:
			mesh_list = self.get_mesh_list(mesh.type_name, compound_attr_name=FACE_SKINNED_CATEGORY)
			if not mesh_list:
				return
			return face_model.FaceModel(mesh_list[0])
		if category == FACE_SKINNED_CATEGORY:
			mesh_list = self.get_mesh_list(mesh.type_name, compound_attr_name=FACE_BLENDSHAPE_CATEGORY)
			if not mesh_list:
				return
			return face_model.FaceModel(mesh_list[0])

