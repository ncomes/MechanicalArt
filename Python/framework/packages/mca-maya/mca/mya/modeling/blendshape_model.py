#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper functions for Blend nodes and shapes
"""

from __future__ import print_function, division, absolute_import

# python imports

# software specific imports
import pymel.core as pm

# mca python imports
from mca.common import log
from mca.common.utils import lists
from mca.mya.utils import attr_utils

logger = log.MCA_LOGGER


def delete_blendshapes(blendnode):
	"""
	Deletes the all the blend shape connected to the blend shape node in the scene.
	"""
	
	shapes = get_blendnode_shapes(blendnode)
	[pm.delete(x) for x in shapes if pm.objExists(x)]


def set_blendshape_weights_from_mesh(mesh, blendnode=None, weight=0):
	"""
	Set the Blendshape weight on each vert.

	:param nt.Mesh mesh: Mesh that is being set.
	:param nt.BlendShape blendnode: Blend node that has shapes attached.
	:param float weight: the blend shape weight value a blend shape should have on a base mesh.
	"""
	
	if not blendnode:
		blendnode = get_first_blendnode(mesh)
	if not blendnode:
		logger.warning('{0}: No blend node was connected to the mesh.  No Weights were set.'.format(mesh))
		return
	verts = pm.polyEvaluate(mesh, v=True)
	for x in range(verts):
		blendnode.inputTarget[0].inputTargetGroup[0].targetWeights[x].set(weight)


def set_blendshape_weights(blendnode, weight=0):
	"""
	Set the Blendshape weight on each vert.

	:param nt.BlendShape blendnode: Blend node that has shapes attached.
	:param float weight: the blend shape weight value a blend shape should have on a base mesh.
	"""
	
	mesh = blendnode.outputGeometry[0].listConnections()
	if not mesh:
		logger.warning('{0}: No mesh was connected to the blend node.  No Weights were set.'.format(blendnode))
		return
	mesh = mesh[0]
	verts = pm.polyEvaluate(mesh, v=True)
	for x in range(verts):
		blendnode.inputTarget[0].inputTargetGroup[0].targetWeights[x].set(weight)


def get_blendnode_index(blendnode):
	"""
	Returns an index list of the blend shapes as ints.

	:param nt.BlendShape blendnode: Blend node that has shapes attached.
	:return: Returns an index list of the blend shapes as ints.
	:rtype: list[int]
	"""
	
	return blendnode.weightIndexList()


def get_blendnode_index_as_dict(blendnode):
	"""
	Returns the name of the shape as the key and the index as the value.

	:param nt.BlendShape blendnode: Blend node that has shapes attached.
	:return: Returns the name of the shape as the key and the index as the value.
	:rtype: dictionary{string:int}
	"""
	
	shapes = get_blendnode_shapes(blendnode)
	index = get_blendnode_index(blendnode)
	return dict(zip([x.split(':')[-1] for x in shapes], index))


def get_blendnode_shapes(blendnode):
	"""
	Gets a list of all the shapes connected to the blend node.

	:param nt.BlendShape blendnode: Blend node that has shapes attached.
	:return: Gets a list of all the shapes connected to the blend node.
	:rtype: list[string]
	"""
	
	history = pm.listHistory(blendnode)
	blendnode_history = pm.ls(history, type='blendShape')[0]
	shapes = pm.listAttr(blendnode_history + ".w", m=True)
	return shapes


def get_active_attribute(blendnode):
	"""
	Returns a list of blend shapes that are fully activated.

	:param nt.BlendShape blendnode: Blend node that has shapes attached.
	:return: Returns a list of blend shapes that are fully activated.
	:rtype: list[string]
	"""
	
	shapes = get_blendnode_shapes(blendnode)
	active = []
	for shape in shapes:
		if pm.PyNode(str(blendnode) + '.' + str(shape)).get() == 1:
			active.append(shape)
	return active


def get_all_blendnodes(mesh):
	"""
	Returns all the blend nodes on a mesh.

	:param nt.Mesh mesh: A poly Mesh.
	:return: Returns all the blend nodes on a mesh.
	:rtype: list[pm.nt.BlendShape]
	"""
	
	all_blendnodes = []
	mesh_shapes = mesh.getShapes()
	blendnodes = [x.listConnections(type=(pm.nt.BlendShape)) for x in mesh_shapes]
	
	blendnodes = list(set(lists.flatten_list(blendnodes)))
	for blendnode in blendnodes:
		if not blendnode.hasAttr('blendNodeType'):
			other_blendnodes = blendnode.listConnections(type=pm.nt.BlendShape)
			if other_blendnodes:
				for blend in other_blendnodes:
					if blend.hasAttr('blendNodeType'):
						all_blendnodes.append(blend)
		else:
			all_blendnodes.append(blendnode)
	return all_blendnodes


def get_first_blendnode(mesh):
	"""
	Returns the first blend node.

	:param nt.transform mesh: A mesh that has a blend node attached.
	:return: Returns a blend node.
	:rtype: pm.nt.BlendShape
	"""
	
	if isinstance(mesh, pm.nt.BlendShape):
		return mesh
	# if a mesh is passed in, return the 1st blend node.
	blendnode = lists.get_first_in_list(get_all_blendnodes(mesh))
	if not blendnode:
		logger.warning('No blend node was found connected to {0}.'.format(mesh))
		return
	return blendnode


def create_parallel_blendnode(diff_mesh, pose_mesh, last_mesh, name='parallel_blendshape'):
	"""
	Creates a parallel blend shape node.

	:param nt.Mesh last_mesh: Mesh that is the shape you want to blend.
	:param nt.Mesh pose_mesh: Source mesh that is the shape you want to blend.
	:param nt.Mesh diff_mesh: A neutral posed mesh.
	:param string name: name of the blend node.
	:return: Returns the parallel blend node.
	:rtype: pm.nt.BlendShape
	"""
	
	parallel_node = lists.get_first_in_list(pm.blendShape(diff_mesh, pose_mesh, last_mesh, parallel=True, n=name))
	parallel_node.weight[0].set(1)
	parallel_node.weight[1].set(1)
	return parallel_node


def duplicate_mesh(mesh, label=None, remove_attrs=(), remove_user_attrs=False):
	"""
	Duplicates a mesh.

	:param pm.nt.transform mesh:  Mesh that will be duplicated.
	:param string label:  The name of the newly created mesh.
	:param list[string] remove_attrs: Removes a list attributes from the mesh.
	:param bool remove_user_attrs: Removes all attributes that were added by a user.
	:return:  Returns the duplicated mesh.
	:rtype: pm.nt.transform
	"""
	
	if not label:
		label = str(mesh)
	dup_mesh = pm.duplicate(mesh, n=label)[0]
	attr_utils.unlock_all_attrs(dup_mesh)
	if remove_user_attrs:
		attr_utils.purge_user_defined_attrs([dup_mesh])
	
	for attr in remove_attrs:
		if dup_mesh.hasAttr(attr):
			dup_mesh.deleteAttr(attr)
	return dup_mesh


def dup_and_delete_mesh(mesh, label=None, remove_attrs=(), remove_user_attrs=False):
	"""
	Duplicates its a mesh and deletes the old copy. A way to generate a clean mesh/pose.

	:param pm.nt.transform mesh:  Mesh that will be duplicated.
	:param string label:  The name of the newly created mesh.
	:param list[string] remove_attrs: Removes a list attributes from the mesh.
	:param bool remove_user_attrs: Removes all attributes that were added by a user.
	:return:  Returns the duplicated mesh.
	:rtype: pm.nt.transform
	"""
	
	if not label:
		label = str(mesh)
	pm.rename(mesh, 'temp_mesh_DELETE')
	
	dup_mesh = duplicate_mesh(mesh=mesh,
	                          label=label,
	                          remove_attrs=remove_attrs,
	                          remove_user_attrs=remove_user_attrs)
	pm.delete(mesh)
	return dup_mesh


def set_blendshape_weight_symmetry(side=None, symmetry=True):
	"""
	Set Maya's blend shape weight symmetry.
	:param string side: the side the pose is on.
	:param bool symmetry: Turn on/off blend shape weight symmetry.
	"""
	if symmetry:
		if side == 'center':
			pm.artAttrCtx('artAttrBlendShapeContext', e=1, reflection=True)
		else:
			pm.artAttrCtx('artAttrBlendShapeContext', e=1, reflection=False)
	else:
		pm.artAttrCtx('artAttrBlendShapeContext', e=1, reflection=False)


