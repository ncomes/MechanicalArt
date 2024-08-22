#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A way to interact with joint chains in rigs.
"""
# System global imports
import json
# Software specific imports
import pymel.core as pm
# CPG python imports
from mca.common import log
from mca.mya.utils import namespace_utils


logger = log.MCA_LOGGER


CPG_MESH_MARKUP = 'cpgMeshMarkup'


class MeshMarkup:
	def __init__(self, mesh):
		self._mesh = mesh
	
	@classmethod
	def create(cls,
				mesh,
				type_name,
				category,
				side,
				**kwargs):
		"""
		Creates the "cpgMeshMarkup" attribute on a mesh and adds the markup.
		
		:param pm.nt.Transform mesh: A mesh that will be tagged with data.
		:param str type_name: a key word on what type of meshes are in this region.  Examples: head_mesh, jaw_mesh, etc...
		:param str category: a key word on what type of category the meshes belong to in this region.
		Examples: skin_mesh, blendshape_mesh, etc...
		:param str side: side the mesh is on.
		:param str kwargs: Any added data that needs to be tagged.
		:return: Returns an instance of MeshMarkup.
		:rtype: MeshMarkup
		"""
		
		if not mesh.hasAttr(CPG_MESH_MARKUP):
			mesh.addAttr(CPG_MESH_MARKUP, dt='string')
		mesh.attr(CPG_MESH_MARKUP).set('')
		
		mesh_dict = {}
		mesh_dict.update({'type_name': type_name})
		mesh_dict.update({'category': category})
		mesh_dict.update({'side': side})
		mesh_dict.update(kwargs)
		
		mesh = cls(mesh)
		mesh.set_dict(mesh_dict)
		return mesh
	
	@property
	def mesh(self):
		"""
		Returns the pm.nt.Transform mesh.
		
		:return: Returns the pm.nt.Transform mesh.
		:rtype: pm.nt.Transform
		"""
		
		return self._mesh
	
	@property
	def region(self):
		"""
		Returns the type of mesh.  Example: head_mesh, left_eye_mesh

		:return: Returns the type of mesh.
		:rtype: str
		"""
		return self.get_mesh_entry('region')
	
	@region.setter
	def region(self, value):
		"""
		Adds or sets the type of mesh.  Example: head_mesh, left_eye_mesh

		:param str value: Adds or sets the type of mesh.
		"""
		
		self.update_entry('region', value)
	
	@property
	def type_name(self):
		"""
		Returns the type of mesh.  Example: head_mesh, left_eye_mesh

		:return: Returns the type of mesh.
		:rtype: str
		"""
		return self.get_mesh_entry('type_name')
	
	@type_name.setter
	def type_name(self, value):
		"""
		Adds or sets the type of mesh.  Example: head_mesh, left_eye_mesh

		:param str value: Adds or sets the type of mesh.
		"""
		
		self.update_entry('type_name', value)
	
	@property
	def category(self):
		"""
		Returns the mesh category.  Example: skin_mesh, blendshape_mesh

		:return: Returns what side the mesh is on.
		:rtype: str
		"""
		
		return self.get_mesh_entry('category')
	
	@category.setter
	def category(self, value):
		"""
		Adds or sets the mesh category.  Example: skin_mesh, blendshape_mesh

		:param str value: Adds or sets the mesh category.
		"""
		
		self.update_entry('category', value)
	
	@property
	def side(self):
		"""
		Returns what side the mesh is on.
		
		:return: Returns what side the mesh is on.
		:rtype: str
		"""
		
		return self.get_mesh_entry('side')
	
	@side.setter
	def side(self, value):
		"""
		Adds or sets the side for a mesh.
		
		:param str value: Adds or sets the side for a mesh.
		"""
		
		self.update_entry('side', value)
	
	@property
	def mirror_type(self):
		"""
		Either mirror_self or mirror_dup.
		MirrorSelf == Mirror the same mesh
		MirrorDup == Duplicate the mesh and then Mirror that mesh
		
		:return: Returns the mirror type
		:rtype: str
		"""
		
		return self.get_mesh_entry('mirror_type')
	
	@mirror_type.setter
	def mirror_type(self, value):
		"""
		Either mirror_self or mirror_dup.
		MirrorSelf == Mirror the same mesh
		MirrorDup == Duplicate the mesh and then Mirror that mesh

		:param str value: Adds or sets the mirror type for a mesh.
		"""
		
		self.update_entry('mirror_type', value)
	
	@property
	def race(self):
		"""
		Returns the race of the character associated to this mesh.

		:return: Returns the race of the character associated to this mesh.
		:rtype: str
		"""
		return self.get_mesh_entry('race')
	
	@race.setter
	def race(self, value):
		"""
		Adds or sets the race of the character associated to this mesh.

		:param str value: Adds or sets the race of the character associated to this mesh.
		"""
		
		self.update_entry('race', value)
	
	@property
	def skeleton(self):
		"""
		Returns the skeleton name associated to this mesh.

		:return: Returns the skeleton name associated to this mesh.
		:rtype: str
		"""
		
		return self.get_mesh_entry('skeleton')
	
	@skeleton.setter
	def skeleton(self, value):
		"""
		Adds or sets skeleton name associated to this mesh.

		:param str value: Adds or sets skeleton name associated to this mesh.
		"""
		
		self.update_entry('skeleton', value)
	
	@property
	def skin_type(self):
		"""
		Returns the a name associated with how the mesh will be skinned.
		Ex: linear Skinning Decomp, one button skinning, copy mesh, etc

		:return: Returns the a name associated with how the mesh will be skinned.
		:rtype: str
		"""
		
		return self.get_mesh_entry('skin_type')
	
	@skin_type.setter
	def skin_type(self, value):
		"""
		Adds or sets the a name associated with how the mesh will be skinned.
		Ex: linear Skinning Decomp, one button skinning, copy mesh, etc

		:param str value: Adds or sets the a name associated with how the mesh will be skinned.
		"""
		
		self.update_entry('skin_type', value)
	
	@property
	def source_mesh(self):
		"""
		Returns a name if the mesh has data associated from another mesh.

		:return: Returns a name if the mesh has data associated from another mesh.
		:rtype: str
		"""
		
		return self.get_mesh_entry('source_mesh')
	
	@source_mesh.setter
	def source_mesh(self, value):
		"""
		Adds or sets a name the mesh has data associated from another mesh.

		:param str value: Adds or sets a name the mesh has data associated from another mesh.
		"""
		
		self.update_entry('source_mesh', value)
	
	@property
	def joint_connection_type(self):
		"""
		Returns a name if the joints are connected to the mesh, or how the joints are set.

		:return: Returns a name if the joints are connected to the mesh, or how the joints are set.
		:rtype: str
		"""
		
		return self.get_mesh_entry('joint_connection_type')
	
	@joint_connection_type.setter
	def joint_connection_type(self, value):
		"""
		Adds or sets a name if the joints are connected to the mesh, or how the joints are set.

		:param str value: Adds or sets a name if the joints are connected to the mesh, or how the joints are set.
		"""
		
		self.update_entry('joint_connection_type', value)
	
	def set_dict(self, mesh_dict):
		"""
		Sets the string attribute with a dictionary.
		
		:param dict mesh_dict: Sets the string attribute with a dictionary.
		"""
		
		if mesh_dict:
			mesh_dump = json.dumps(mesh_dict)
			self.mesh.attr(CPG_MESH_MARKUP).set(mesh_dump)
			
	def update_entry(self, entry, value):
		"""
		Adds or sets an entry in the dictionary.
		
		:param str entry: A Key of the dictionary
		:param str value: A value of the dictionary
		"""
		
		mesh_dict = self.get_dict()
		mesh_dict.update({entry : value})
		self.set_dict(mesh_dict)
	
	def get_dict(self):
		"""
		Returns the dictionary from the string attribute.
		
		:return: Returns the dictionary from the string attribute.
		:rtype: dict
		"""
		
		return eval(self.mesh.attr(CPG_MESH_MARKUP).get())
	
	def get_mesh_entry(self, entry):
		"""
		Returns a specific entry from the dictionary from the string attribute.
		
		:param str entry: A Key of the dictionary
		:return: Returns a specific entry from the dictionary from the string attribute.
		:rtype: str
		"""
		
		mesh_dict = self.get_dict()
		return mesh_dict.get(entry, None)
	
	def remove_markup(self):
		"""
		Removes the markup and the attribute.
		"""
		
		if self.mesh.hasAttr(CPG_MESH_MARKUP):
			pm.deleteAttr(CPG_MESH_MARKUP)
	
	def clear_markup(self):
		"""
		Keeps the attribute, but clears the data.
		"""
		
		if self.mesh.hasAttr(CPG_MESH_MARKUP):
			self.mesh.attr(CPG_MESH_MARKUP).set('')
			

class RigMeshMarkup:
	def __init__(self, mesh_list):
		if not mesh_list:
			self.mesh_list = []
		else:
			self.mesh_list = self.get_mesh_markups(mesh_list)
	
	@classmethod
	def create(cls, ns=''):
		"""
		Gets all the meshes from a namespace with mesh markup and returns an instance of RigMeshMarkup.
		
		:param str ns: namespace to search through meshes.
		:return: Returns an instance of RigMeshMarkup
		:rtype: RigMeshMarkup
		"""
		
		all_nodes = namespace_utils.get_all_nodes_in_namespace(ns)
		mesh_shapes = pm.ls(all_nodes, geometry=True)
		mesh_list = list(set([x.getParent() for x in mesh_shapes if x.getParent().hasAttr(CPG_MESH_MARKUP)]))
		return cls(mesh_list)
		
	def get_mesh_markups(self, mesh_list=None):
		"""
		Returns the list of meshes as instances of MeshMarkups
		
		:param list(pm.nt.Transform) mesh_list: List of meshes
		:return: Returns the list of meshes as instances of MeshMarkup
		:rtype: list(MeshMarkup)
		"""
		
		if not mesh_list:
			mesh_list = self.mesh_list
		return list(map(lambda x: MeshMarkup(x), mesh_list))
	
	def get_dict(self):
		"""
		Returns a dictionary of all the compound attributes, meshes, and there associated attr names.
		
		:return: Returns a dictionary of all the compound attributes, meshes, and there associated attr names.
		:rtype: dictionary
		"""
		
		mesh_dict = {}
		for mesh in self.mesh_list:
			mesh_dict.setdefault(mesh.category, {})
			mesh_dict[mesh.category].update({mesh.type_name: pm.PyNode(mesh.mesh)})
		return mesh_dict
	
	def get_region_dict(self):
		"""
		Returns a dictionary of all the regions and mesh names.

		:return: Returns a dictionary of all the regions and mesh names.
		:rtype: dictionary
		"""
		
		mesh_dict = {}
		for mesh in self.mesh_list:
			mesh_dict.setdefault(mesh.region, {})
			mesh_dict[mesh.region].update({mesh.type_name: mesh.category})
		return mesh_dict
	
	def get_blendshape_region_dict(self):
		"""
		Returns a dictionary of all the regions and mesh names.

		:return: Returns a dictionary of all the regions and mesh names.
		:rtype: dictionary
		"""
		
		mesh_dict = {}
		for mesh in self.mesh_list:
			if not mesh.category == 'blendshape_mesh':
				continue
			mesh_dict.setdefault(mesh.region, {})
			mesh_dict[mesh.region].update({mesh.type_name: mesh.category})
		return mesh_dict
	
	def get_mesh_list_in_region(self, mesh_region, as_string=False):
		"""
		Returns a list of meshes with in the region
		
		:param str mesh_region: region name
		:param bool as_string: If True, the list will be returned as a string list.
		:return: Returns a list of meshes with in the region
		:rtype: list(pm.nt.Transform)
		"""
		
		meshes = []
		for mesh in self.mesh_list:
			if mesh.region == mesh_region:
				meshes.append(mesh.mesh)
		if as_string and meshes:
			meshes = list(map(lambda x: str(x), meshes))
		return meshes
	
	def get_mesh_dict_list_in_region(self, mesh_region, as_string=False):
		"""
		Returns a dictionary with all the meshes and it's markup in a region.
		
		:param str mesh_region: region name
		:param bool as_string: If True, the list will be returned as a string list.
		:return: Returns a dictionary with all the meshes and it's markup in a region.
		:rtype: dictionary
		"""
		
		meshes = {}
		for mesh in self.mesh_list:
			if mesh.region == mesh_region:
				meshes[mesh.mesh] = mesh
		if as_string and meshes:
			meshes = list(map(lambda x: str(x), meshes))
		return meshes
	
	def get_mesh_list_in_category(self, category, as_string=False):
		"""
		Returns a list of meshes with in a category

		:param str category: THe category of a mesh.  "blendshape_mesh", "skin_mesh"
		:param bool as_string: If True, the list will be returned as a string list.
		:return: Returns a list of meshes with in a category
		:rtype: list(pm.nt.Transform)
		"""
		
		meshes = []
		head_mesh = None
		for mesh in self.mesh_list:
			if mesh.category == category:
				if mesh.type_name == 'head_mesh':
					head_mesh = mesh.mesh
				else:
					meshes.append(mesh.mesh)
		if head_mesh:
			meshes.insert(0, head_mesh)
		if as_string and meshes:
			meshes = list(map(lambda x: str(x), meshes))
		return meshes
	
