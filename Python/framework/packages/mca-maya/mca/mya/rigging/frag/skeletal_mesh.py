#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""
# System global imports
# Software specific imports
import pymel.core as pm
# mca python imports
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import mesh_markup_rig
from mca.mya.utils import dag
from mca.common import log
# Internal module imports
from mca.mya.rigging.frag import frag_base, frag_root

logger = log.MCA_LOGGER


def get_frag_skeletal_mesh(node):
	"""
	From any node within the rig dag hierarchy find the all grp and return the fragParent connection. This should be the
	rig in all cases.

	:param Transform node:
	:return: The FRAGRig driving this hierarchy.
	:rtype: FRAGRig
	"""
	
	# If it is a frag child, get parent FRAGNode, root, then rig.
	if node.hasAttr('fragParent'):
		wrapped_frag_node = frag_base.FRAGNode(node.getAttr('fragParent'))
		wrapped_frag_root = frag_root.get_frag_root(wrapped_frag_node)
		return wrapped_frag_root.get_skeletal_mesh()
	
	# if it is in the hierarchy but not a frag node, search for the frag root.
	all_grp = dag.get_absolute_parent(node)
	grp_skins = [x for x in all_grp.getChildren() if x.hasAttr('fragParent') and x.fragParent.get().fragType.get() == 'SkeletalMesh']
	if not grp_skins:
		logger.warning(f'Cannot find a connection to the FRAG SkeletalMesh Node from {node}.')
		return

	return grp_skins[0].getAttr('fragParent')


class SkeletalMesh(frag_base.FRAGNode):
	VERSION = 1
	
	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(frag_parent, variant='default', variant_version=1):
		
		# Set Namespace
		root_namespace = frag_parent.namespace().split(':')[0]
		pm.namespace(set=f'{root_namespace}:')
		
		if not frag_parent.hasAttr('isFragRoot'):
			raise AttributeError('{0}: FRAG parent is not the Frag Root Component')
		
		# Create the Control Rig Network Node
		node = frag_base.FRAGNode.create(frag_parent, SkeletalMesh.__name__, SkeletalMesh.VERSION)
		
		#node.set_frag_parent(frag_parent)
		
		# Set the Attributes
		node.addAttr('grpSkins', at='message')
		node.addAttr('grpBlendshapes', at='message')
		node.addAttr('variant', dt='string')
		node.addAttr('variantVersion', at='double')
		node.variantVersion.set(1)
		
		grp_skins = pm.group(empty=1, n='grp_skins')
		grp_skins.inheritsTransform.set(0)
		grp_skins.addAttr('isGrpSkins', at='bool', dv=1)
		node.connect_node(grp_skins, 'grpSkins', 'fragParent')
		
		#adding
		grp_blendshapes = pm.group(empty=1, n='grp_blendshapes')
		grp_blendshapes.addAttr('isGrpBlendshapes', at='bool', dv=1)
		grp_blendshapes.inheritsTransform.set(0)
		node.connect_node(grp_blendshapes, 'grpBlendshapes', 'fragParent')
		
		# Get all meshes and parent them under the grp_skins
		meshes = node.get_meshes_w_grps()
		pm.parent(meshes, grp_skins)
		
		blendshape_meshes = node.get_blendshapes_from_scene()
		pm.parent(blendshape_meshes, grp_blendshapes)

		return node
	
	def get_all_meshes_from_scene(self):
		"""
		Returns all the meshes in a scene.
		
		:return: Returns all the meshes in a scene.
		:rtype: list(pm.nt.Transform)
		"""
		transforms = list(set([x.getParent() for x in pm.ls(type=pm.nt.Mesh)]))
		meshes = [x for x in transforms if isinstance(x, pm.nt.Transform) and not isinstance(x, pm.nt.Joint)]
		return meshes
	
	def get_blendshapes_from_scene(self):
		"""
		Returns all the blend shape meshes in the scene within the namespace.
		
		:return: Returns all the blend shape meshes in the scene within the namespace.
		:rtype: list(pm.nt.Transform)
		"""
		markups = mesh_markup_rig.RigMeshMarkup.create(self.pynode.namespace())
		return markups.get_mesh_list_in_region('blendshape_mesh')
	
	def get_meshes_w_grps(self):
		"""
		Returns all the meshes from the rig, skinned meshes and meshes that are children of the skeleton.

		:return: Returns all the meshes from the rig, skinned meshes and meshes that are children of the skeleton.
		:rtype: list(pm.nt.Transform)
		"""
		
		meshes = self.get_all_meshes_from_scene()
		grps = []
		for mesh in meshes:
			parents = mesh.getAllParents()
			if parents:
				grps.append(parents[-1])
			else:
				grps.append(mesh)
				
		grps = list(set(grps))
		return grps
	
	def get_grp_skins(self):
		"""
		Returns the skins group.
		:return: Returns the skins group.
		:rtype: pm.nt.Group
		"""
		skins_grp = self.has_attribute('grpSkins')
		if not skins_grp:
			logger.warning(f'There is no skins grp connected to the {self.pynode}')
			return
		return self.pynode.grpSkins.get()
	
	def get_grp_blendshapes(self):
		"""
		Returns the skins group.
		:return: Returns the skins group.
		:rtype: pm.nt.Group
		"""
		blend_grp = self.has_attribute('grpBlendshapes')
		if not blend_grp:
			logger.warning(f'There is no blend shape grp connected to the {self.pynode}')
			return
		return self.pynode.grpBlendshapes.get()


def get_group_skins(node):
	"""
	Returns the grp parent of meshes given a node
	
	:param pm.nt.Transform node: A node connected to the rig
	:return: Returns the grp parent of meshes given a node
	:rtype: pm.nt.Transform
	"""
	
	result = None
	root_node = frag_root.get_frag_root(node)
	skel_node = root_node.get_frag_child(of_type=SkeletalMesh)
	if skel_node:
		result = skel_node.get_grp_skins()
	return result


def get_group_blendshapes(node):
	"""
	Returns the grp parent of meshes given a node
	
	:param pm.nt.Transform node: A node connected to the rig
	:return: Returns the grp parent of meshes given a node
	:rtype: pm.nt.Transform
	"""
	
	result = None
	root_node = frag_root.get_frag_root(node)
	skel_node = root_node.get_frag_child(of_type=SkeletalMesh)
	if skel_node:
		result = skel_node.get_grp_blendshapes()
	return result

