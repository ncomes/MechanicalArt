#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Component that tracks different types of meshes and their uses
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.mya.modifiers import ma_decorators
from mca.mya.utils import attr_utils
# Internal module imports
from mca.mya.rigging.tek import tek_base

logger = log.MCA_LOGGER


class MeshComponent(tek_base.TEKNode):
	VERSION = 1
	
	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(tek_parent,
				meshes_dict):
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
		
		node = tek_base.TEKNode.create(tek_parent=tek_parent,
											tek_type=MeshComponent.__name__,
											version=MeshComponent.VERSION)
		
		# Set the Attributes
		
		for category in meshes_dict.keys():
			attr_utils.set_compound_attribute_groups(node, category, meshes_dict[category])
		
		blendshape_meshes = node.get_all_category_meshes('blendshape_mesh')
		if not blendshape_meshes:
			return node
		
		# Get all blend shape meshes and parent them under the grp_blendshapes
		blendshape_grp = tek_parent.get_grp_blendshapes()
		if blendshape_grp:
			pm.parent(blendshape_meshes, blendshape_grp)
		
		return node
	
	def get_all_category_meshes(self, category):
		"""
		Returns all the meshes in a compound attribute
		
		:param str category: Name of the compound attribute
		:return: Returns all the meshes in a compound attribute
		:rtype: list(pm.nt.Transform)
		"""
		
		return attr_utils.get_compound_attr_connections(self.pynode, compound_attr_name=category)
	
	def get_all_attrs_from_category(self, category):
		"""
		Returns all the attributes from a compound attr.
		
		:param str category: Name of the compound attribute
		:return: :return: Returns all the meshes in a compound attribute
		:rtype: list(str)
		"""
		
		return attr_utils.get_all_attributes_from_compound_attr(self.pynode, compound_attr_name=category)
	
	def get_all_categories(self):
		"""
		Returns all the compound attribute names.
		:return: Returns all the compound attribute names.
		:rtype: list(str)
		"""
		
		return attr_utils.get_compound_attr_names(self.pynode)
	
	def remove_category(self, category):
		"""
		Removes a compound attribute
		
		:param str category: Name of the compound attribute
		"""
		
		attr_utils.disconnect_and_delete_compound_attr(self.pynode, category)
	
	def reconnect_mesh(self, mesh, attr_name, compound_attr_name):
		"""
		Reconnects a mesh back to the node.
		
		:param pm.nt.Transform mesh: The mesh that is getting reconnected.
		:param str attr_name: The name of the attribute that is connected to the compound attributes.
		:param str compound_attr_name: the compound attribute in which the mesh is connected to.
		"""
		
		attr_name = f'{compound_attr_name}_{attr_name}'
		if not pm.hasAttr(self.pynode.attr(compound_attr_name), attr_name):
			logger.warning(f'{attr_name}: Attribute does not exist or is not connected to {self.pynode}.')
			return
		mesh.message >> self.pynode.attr(attr_name)
	
	def get_mesh(self, attr_name, compound_attr_name):
		"""
		Returns a specific mesh associated with compound attributes.
		
		:param str attr_name: The name of the attribute that is connected to the compound attributes.
		:param str compound_attr_name: the compound attribute in which the mesh is connected to.
		:return: Returns a specific mesh associated with compound attributes.
		:rtype: list(pm.nt.Transform)
		"""
		
		attr_name = f'{compound_attr_name}_{attr_name}'
		
		if not pm.hasAttr(self.pynode.attr(compound_attr_name), attr_name):
			logger.warning(f'{attr_name}: Attribute does not exist or is not connected to {self.pynode}.')
			return
		compound_attr = self.pynode.attr(compound_attr_name)
		if pm.objExists(compound_attr.attr(attr_name)):
			mesh_attr = compound_attr.attr(attr_name)
			if mesh_attr.get():
				return mesh_attr.get()
		return
	
	def get_mesh_list(self, attr_name, compound_attr_name):
		"""
		Returns a list of specific meshes associated with the rig.
		
		:param str attr_name: The name of the attribute that is connected to the compound attribute
		:param str compound_attr_name: the compound attribute in which the mesh is connected to.
		:return: Returns a list of specific meshes associated with the rig.
		:rtype: list(pm.nt.Transform)
		"""
		
		attr_name = f'{compound_attr_name}_{attr_name}'
		
		if not self.hasAttr(compound_attr_name):
			logger.warning(f'{compound_attr_name}: Compound attribute does not exist on {self.pynode}.')
			return
		if not pm.hasAttr(self.pynode.attr(compound_attr_name), attr_name):
			logger.warning(f'{attr_name}: attribute does not exist or is not connected to {self.pynode}.')
			return
		compound_attr = self.pynode.attr(compound_attr_name)
		if pm.objExists(compound_attr.attr(attr_name)):
			mesh_attr = compound_attr.attr(attr_name)
			if mesh_attr.listConnections():
				meshes = mesh_attr.listConnections()
				return meshes
		return
	
	def get_connections_as_dict(self):
		"""
		Returns a dictionary of all the compound attributes, meshes, and there associated attr names.
		
		:return: Returns a dictionary of all the compound attributes, meshes, and there associated attr names.
		:rtype: dictionary
		"""
		
		_dict = {}
		categories = self.get_all_categories()
		for block in categories:
			meshes = self.get_all_category_meshes(block)
			attrs = self.get_all_attrs_from_category(block)
			for x, mesh in enumerate(meshes):
				# remove the block name out of the attribute
				attr = attrs[x+1].split('.')[-1]
				attr = attr.replace(f'{block}_', '')
				# Make sure the category exists
				_dict.setdefault(block, {})
				_dict[block].update({attr: mesh})
		return _dict

