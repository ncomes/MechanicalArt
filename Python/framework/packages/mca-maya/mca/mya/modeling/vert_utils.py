#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mesh vertices
"""

# System global imports

# software specific imports
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
# mca python imports
from mca.common import log
from mca.common.utils import list_utils, string_utils
from mca.mya.utils import maya_utils

logger = log.MCA_LOGGER


def get_vertices_as_numbers(vertices, as_string=False):
	"""
	Strips off everything except the vertex number.
	:param string list vertices: either a list of vertices or a single vertex.
	:param bool as_string: True returns as a string.  False returns as an int.
	:return: Returns a list of vertex numbers.
	:rtype: list[int] or list[str]
	"""
	
	verts = []
	if not isinstance(vertices, list):
		vertices = [vertices]
	for vert in vertices:
		if '.' in vert:
			vert = vert.split('.')[-1]
		vert_string = string_utils.get_numbers_from_string(vert, as_string=True)
		vert_num = ''.join(vert_string)
		if not as_string:
			vert_num = int(vert_num)
		verts.append(vert_num)
	return verts


def get_closest_vertex_to_object(mesh, obj):
	"""
	Returns the closest vertex to an object.

	:param PyNode mesh: mesh object name
	:param PyNode obj: object near a mesh
	:return: vertex closest to an object
	:return: str
	"""
	
	mesh_shape = mesh.getShape()
	closest_node = pm.createNode('closestPointOnMesh', n=str(obj) + '_closest_point_node')
	mesh_shape.outMesh >> closest_node.inMesh
	mesh_shape.worldMatrix[0] >> closest_node.inputMatrix
	obj = pm.xform(obj, q=True, ws=True, t=True)
	
	closest_node.inPositionX.set(obj[0])
	closest_node.inPositionY.set(obj[1])
	closest_node.inPositionZ.set(obj[2])
	
	closest_point_vertex = closest_node.closestVertexIndex.get()
	pm.delete(closest_node)
	return closest_point_vertex


def get_opposite_vertices(vertex_list):
	opposite_list = []
	if not vertex_list:
		return
	
	temp_locator = pm.spaceLocator()
	for vert in vertex_list:
		vert_position = pm.xform(vert, q=True, ws=True, t=True)
		temp_locator.translate.set((vert_position[0] * -1), vert_position[1], vert_position[2])
		mesh = pm.ls(vert, o=True)[0].getParent()
		mirrored_vert = get_closest_vertex_to_object(mesh, temp_locator)
		opposite_list.append(mirrored_vert)
	pm.delete(temp_locator)
	return opposite_list


def mirror_vertices(mesh, vertex_mapping, vertices=None, axis=(-1, 1, 1), world=False):
	"""
	Import a json file that has a dictionary of selected vertices on an object and it's mirror.
	The key is the +x and the value is the -x.
	In the future it would be great to not have to specify vertices and just mirror left to right or opposite.

	>>> Example Dictionary {[left Vert Number : Right Vert Number], [Right Vert Number, left Vert Number], etc...}

	:param string mesh: mesh name
	:param dict vertex_mapping: dict of vertices
	:param list vertices: List of string vertices
	:param str axis: Which axis to mirror on. x, y, or z.
	:param bool world: If True, the coordinates will be world space.  If False the coordinates will be local space.
	"""
	
	if not vertex_mapping or not isinstance(vertex_mapping, dict):
		logger.warning('Must provide a dictionary mapping value.')
		return
	
	mesh_name = str(mesh)
	if not vertices:
		vertices = vertex_mapping.keys()
	elif any('.vtx' in str(string) for string in vertices):
		vertices = list(map(lambda x: str(x), vertices))
		vertices = get_vertices_as_numbers(vertices, as_string=True)
	else:
		vertices = list(map(lambda x: str(x), vertices))
	
	for vert in vertices:
		if vert in vertex_mapping.keys():
			vertex = mesh_name + '.vtx[' + vert + ']'
			inverse_index = vertex_mapping[vert]
			inverse_vert = mesh_name + '.vtx[' + inverse_index + ']'
			mirror_vertex(vertex=vertex, opposite_vertex=inverse_vert, axis=axis, world=world)


def mirror_mesh(left_vertices, right_vertices, middle_vertices, mesh_name, axis=(-1, 1, 1), world=False):
	"""
	Mirrors a a fully mapped mesh.
	The key is the +x and the value is the -x.
	In the future it would be great to not have to specify vertices and just mirror left to right or opposite.
	>>> Example Dictionary {[left Vert Number : Right Vert Number], [Right Vert Number, left Vert Number], etc...}
	:param list(str) left_vertices: List of left vertices.
	:param list(str) right_vertices: List of right vertices.
	:param list(str) middle_vertices: List of middle vertices.
	:param string mesh_name: mesh name
	:param str axis: Which axis to mirror on. x, y, or z.
	:param bool world: If True, the coordinates will be world space.  If False the coordinates will be local space.
	"""
	
	mesh_name = str(mesh_name)
	# Mirror the left and right vertices
	if any('.vtx' in str(x) for x in left_vertices):
		vertices = list(map(lambda x: str(x), left_vertices))
		left_vertices = get_vertices_as_numbers(vertices, as_string=True)
	
	if any('.vtx' in str(x) for x in right_vertices):
		vertices = list(map(lambda x: str(x), right_vertices))
		right_vertices = get_vertices_as_numbers(vertices, as_string=True)
	
	for x, vert in enumerate(left_vertices):
		vertex = mesh_name + '.vtx[' + str(vert) + ']'
		inverse_vert = mesh_name + '.vtx[' + str(right_vertices[x]) + ']'
		
		pos = cmds.xform(vertex, q=True, t=True, ws=world)
		inv_pos = cmds.xform(inverse_vert, q=True, t=True, ws=world)
		pm.xform(vertex, t=(inv_pos[0] * axis[0], inv_pos[1] * axis[1], inv_pos[2] * axis[2]), ws=world)
		pm.xform(inverse_vert, t=(pos[0] * axis[0], pos[1] * axis[1], pos[2] * axis[2]), ws=world)
	
	# Mirror the middle vertices
	if any('.vtx' in str(x) for x in middle_vertices):
		mid_vertices = list(map(lambda x: str(x), middle_vertices))
		middle_vertices = get_vertices_as_numbers(mid_vertices, as_string=True)
	
	for vert in middle_vertices:
		vertex = mesh_name + '.vtx[' + str(vert) + ']'
		pos = pm.xform(vertex, q=True, t=True, ws=world)
		pm.xform(vertex, t=(pos[0] * axis[0], pos[1] * axis[1], pos[2] * axis[2]))


def mirror_vertex(vertex, opposite_vertex, axis=(-1, 1, 1), world=False):
	"""
	Mirrors a vertex from one side of an object to the other.  Assumes mirroring on X axis.

	:param str vertex: source vertex full name.  The vertex that the position will be used to mirror.
	:param str opposite_vertex: target vertex full name.  The vertex that will be moved to a mirroring position with
		the source vertex.
	:param str axis: Which axis to mirror on. x, y, or z.
	:param bool world: If True, the coordinates will be world space.  If False the coordinates will be local space.
	"""
	
	pos = pm.xform(vertex, q=True, t=True, ws=world)
	pm.xform(opposite_vertex, t=(pos[0] * axis[0], pos[1] * axis[1], pos[2] * axis[2]))


def get_inverse_vertex_selection(vertices):
	'''
	Returns a list of vertices of the inverse selection.
	:param list(str) vertices: list of vertices
	:return: vertex closest to an object
	:rtype: list(str)
	'''
	
	soft_select_mode = pm.softSelect(q=True, sse=True)
	pm.softSelect(sse=False)
	
	mesh = cmds.listRelatives(cmds.ls(vertices[0], o=True)[0], p=True)[0]
	all_verts = cmds.polyEvaluate(mesh, vertex=True)
	cmds.select(mesh + '.vtx [0:' + str(all_verts - 1) + ']')
	cmds.select(vertices, tgl=True)
	
	pm.softSelect(sse=soft_select_mode)
	inverse_vertices = cmds.ls(sl=True, fl=True)
	return inverse_vertices


def get_uv_coordinates(obj, mesh):
	"""
	Returns uv coordinates from a mesh using an objects position.
	:param nt.Transform obj: The object is used to get the uv coordinates using is position near a mesh.
	:param nt.Transform mesh: Mesh Transform that that has uv setup.
	:return: Returns uv coordinates from a mesh using an objects position.
	:rtype: list(float)
	"""
	
	closest_node = pm.createNode('closestPointOnMesh', n='cpm_' + str(obj))
	mesh.getShape().outMesh >> closest_node.inMesh
	mesh.getShape().worldMatrix[0] >> closest_node.inputMatrix
	
	obj_position = pm.xform(obj, q=True, ws=True, t=True)
	closest_node.inPositionX.set(obj_position[0])
	closest_node.inPositionY.set(obj_position[1])
	closest_node.inPositionZ.set(obj_position[2])
	uv = [closest_node.parameterU.get(), closest_node.parameterV.get()]
	pm.delete(closest_node)
	return uv


def convert_to_vertices(obj):
	"""
	Converts every poly selection to vertices
	:param obj: variant, can be the mesh transform, the mesh shape or component based selection
	"""
	
	check_object = list_utils.get_first_in_list(list_utils.force_list(obj))
	
	obj_type = pm.objectType(check_object)
	check_type = check_object
	if obj_type == 'transform':
		shapes = list_utils.force_list(obj.getShapes())
		check_type = list_utils.get_first_in_list(shapes) if shapes else obj
	
	obj_type = pm.objectType(check_type)
	if obj_type == 'mesh':
		converted_vertices = pm.polyListComponentConversion(obj, toVertex=True)
		return pm.filterExpand(converted_vertices, selectionMask=maya_utils.SelectionMasks.PolygonVertices)
	
	if obj_type == 'nurbsCurve' or obj_type == 'nurbsSurface':
		if isinstance(obj, list) and '.cv' in obj[0]:
			return pm.filterExpand(object, selectionMask=maya_utils.SelectionMasks.CVs)
		elif '.cv' in obj:
			return pm.filterExpand(obj, selectionMask=maya_utils.SelectionMasks.CVs)
		else:
			return pm.filterExpand('{}cv[*]'.format(obj[0], selectionMask=maya_utils.SelectionMasks.CVs))
	
	if obj_type == 'lattice':
		if isinstance(obj, list) and '.pt' in obj[0]:
			return pm.filterExpand(obj, selectionMask=maya_utils.SelectionMasks.LatticePoints)
		elif '.pt' in obj:
			return pm.filterExpand(obj, selectionMask=maya_utils.SelectionMasks.LatticePoints)
		else:
			return pm.filterExpand(obj, selectionMask=maya_utils.SelectionMasks.LatticePoints)


def fix_mesh_components_selection_visualization(mesh):
	"""
	Cleanup selection details in Maya so given mesh selection components visualization is correct.

	:param pm.Transform or pm.Shapes mesh: mesh (shape or transform) components we want to visualize.
	"""

	object_type = pm.objectType(mesh)
	if object_type == 'transform':
		shape = list_utils.get_first_in_list(pm.listRelatives(mesh, children=True, shapes=True))
		object_type = pm.objectType(shape)

	mel.eval('if( !`exists doMenuComponentSelection` ) eval( "source dagMenuProc" );')
	if object_type == "nurbsSurface" or object_type == "nurbsCurve":
		mel.eval('doMenuNURBComponentSelection("%s", "controlVertex");' % mesh)
	elif object_type == "lattice":
		mel.eval('doMenuLatticeComponentSelection("%s", "latticePoint");' % mesh)
	elif object_type == "mesh":
		mel.eval('doMenuComponentSelection("%s", "vertex");' % mesh)


def set_vertex_symmetry(side=None, symmetry=True):
	"""
	Set Maya's Vertex Symmetry
	:param string side: the side the pose is on.
	:param bool symmetry: Turn on/off vertex symmetry.
	"""
	
	if symmetry:
		if side == 'center':
			pm.symmetricModelling(symmetry=True)
		else:
			pm.symmetricModelling(symmetry=False)
	else:
		pm.symmetricModelling(symmetry=False)

