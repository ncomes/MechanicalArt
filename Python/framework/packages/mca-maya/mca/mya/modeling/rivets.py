# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
purpose: Creating and Manipulating Matrix Rivets
"""

from __future__ import print_function, division, absolute_import

# System global imports
import logging

import pymel.core as pm

# software specific imports
# mca python imports
from mca.mya.modeling import vert_utils, surface


class MatrixRivet:
	"""
	Example on how to use:
	mesh = pm.PyNode('head_mesh')
	obj = pm.PyNode('locator30')
	usable_edges = model.get_two_edges_from_close_object(mesh=mesh, obj=obj)
	rivet = MatrixRivet(edges=usable_edges, rivet_name='test_rivet')
	test_rivet = rivet.create(obj=obj)
	"""
	
	def __init__(self, edges, rivet_name='rivet'):
		self.rivet_name = rivet_name
		if (len(edges) == 2 and isinstance(edges[0], pm.MeshEdge) and isinstance(edges[1], pm.MeshEdge)):
			
			self.main = {
				'meshObject': edges[0].node().getParent(),
				'edgeIndex1': edges[0].indices()[0],
				'edgeIndex2': edges[1].indices()[0]
			}
		else:
			pm.warning('Please make sure input a total of two edges.')
	
	def create(self, obj=None, uv=()):
		"""
		Creates all the nodes and connects them
		:param nt.Transform obj: An object that is used to get its world coordinates.
		:param list(float) uv: 2 float values that represent the uv values
		:return:  The final result that is displayed connected to the mesh.
		:rtype: nt.Transform
		"""
		self.create_nodes()
		self.create_connections()
		self.set_attributes()
		self.set_uv(obj, uv)
		return self.node['locator']
	
	def create_nodes(self):
		"""
		Creates the nodes needed for the rivet system.
		"""
		self.node = {
			'meshEdgeNode1': pm.createNode('curveFromMeshEdge', n=self.rivet_name + '_curveFromMeshEdge_01'),
			'meshEdgeNode2': pm.createNode('curveFromMeshEdge', n=self.rivet_name + '_curveFromMeshEdge_02'),
			'ptOnSurfaceInfo': pm.createNode('pointOnSurfaceInfo', n=self.rivet_name + '_pointOnSurfaceInfo'),
			'matrixNode': pm.createNode('fourByFourMatrix', n=self.rivet_name + '_fourByFourMatrix'),
			'decomposeMatrix': pm.createNode('decomposeMatrix', n=self.rivet_name + '_decomposeMatrix'),
			'loftNode': pm.createNode('loft', n=self.rivet_name + '_loft'),
			'locator': pm.createNode('locator')
		}
		self.node['locator'] = self.node['locator'].getParent()
		pm.rename(self.node['locator'], self.rivet_name)
	
	def set_attributes(self):
		"""
		Sets the attributes needed for the rivet system.
		"""
		# Set attributes on MeshEdgeNodes
		self.node['meshEdgeNode1'].isHistoricallyInteresting.set(1)
		self.node['meshEdgeNode2'].isHistoricallyInteresting.set(1)
		self.node['meshEdgeNode1'].edgeIndex[0].set(self.main['edgeIndex1'])
		self.node['meshEdgeNode2'].edgeIndex[0].set(self.main['edgeIndex2'])
		
		# Setup loft node
		self.node['loftNode'].reverseSurfaceNormals.set(1)
		self.node['loftNode'].inputCurve.set(size=2)
		self.node['loftNode'].uniform.set(True)
		self.node['loftNode'].sectionSpans.set(3)
		self.node['loftNode'].caching.set(True)
		
		# position the surfaceInfoNode in the absolute center position.
		self.node['ptOnSurfaceInfo'].turnOnPercentage.set(True)
		self.node['ptOnSurfaceInfo'].caching.set(True)
		
		self.node['locator'].addAttr('parameterU', at='double', dv=0)
		self.node['locator'].addAttr('parameterV', at='double', dv=0)
	
	def set_uv(self, obj=None, uv=()):
		"""
		Sets the uv position of the locator on the loft node.
		"""
		
		if obj:
			obj_pos = pm.xform(obj, q=True, ws=True, t=True)
			closest_node = pm.createNode('closestPointOnSurface', n=self.rivet_name)
			closest_node.inPositionX.set(obj_pos[0])
			closest_node.inPositionY.set(obj_pos[1])
			closest_node.inPositionZ.set(obj_pos[2])
			
			self.node['loftNode'].outputSurface >> closest_node.inputSurface
			u = closest_node.parameterU.get()
			if u >= 1:
				u = u - 1
			v = closest_node.parameterV.get()
			
			self.node['ptOnSurfaceInfo'].parameterU.set(u)
			self.node['ptOnSurfaceInfo'].parameterV.set(v)
			self.node['ptOnSurfaceInfo'].parameterU >> self.node['locator'].parameterU
			self.node['ptOnSurfaceInfo'].parameterV >> self.node['locator'].parameterV
			
			pm.delete(closest_node)
		
		elif not obj and uv:
			self.node['ptOnSurfaceInfo'].parameterU.set(uv[0])
			self.node['ptOnSurfaceInfo'].parameterV.set(uv[1])
			self.node['ptOnSurfaceInfo'].parameterU >> self.node['locator'].parameterU
			self.node['ptOnSurfaceInfo'].parameterV >> self.node['locator'].parameterV
		
		else:
			self.node['ptOnSurfaceInfo'].parameterU.set(0.5)
			self.node['ptOnSurfaceInfo'].parameterV.set(0.5)
			self.node['ptOnSurfaceInfo'].parameterU >> self.node['locator'].parameterU
			self.node['ptOnSurfaceInfo'].parameterV >> self.node['locator'].parameterV
	
	def create_connections(self):
		"""
		Connects all the nodes.
		"""
		# Connect main object's world mesh information
		self.main['meshObject'].worldMesh >> self.node['meshEdgeNode1'].inputMesh
		self.main['meshObject'].worldMesh >> self.node['meshEdgeNode2'].inputMesh
		# Connect both meshEdgeNodes to the loftNode
		self.node['meshEdgeNode1'].outputCurve >> self.node['loftNode'].inputCurve[0]
		self.node['meshEdgeNode2'].outputCurve >> self.node['loftNode'].inputCurve[1]
		# Connect the loftNode Output Surface information to our ptOnSurface nodes input
		self.node['loftNode'].outputSurface >> self.node['ptOnSurfaceInfo'].inputSurface
		# Connect the Normalized Normals (X,Y,Z) to the first row of the 4x4 Matrix Node
		self.node['ptOnSurfaceInfo'].normalizedNormalX >> self.node['matrixNode'].in00
		self.node['ptOnSurfaceInfo'].normalizedNormalY >> self.node['matrixNode'].in01
		self.node['ptOnSurfaceInfo'].normalizedNormalZ >> self.node['matrixNode'].in02
		# Connect the Normalized TangentU (X,Y,Z) to the second row of the 4x4 Matrix Node
		self.node['ptOnSurfaceInfo'].normalizedTangentUX >> self.node['matrixNode'].in10
		self.node['ptOnSurfaceInfo'].normalizedTangentUY >> self.node['matrixNode'].in11
		self.node['ptOnSurfaceInfo'].normalizedTangentUZ >> self.node['matrixNode'].in12
		# Connect the Normalized TangentV (X,Y,Z) to the third row of the 4x4 Matrix Node
		self.node['ptOnSurfaceInfo'].normalizedTangentVX >> self.node['matrixNode'].in20
		self.node['ptOnSurfaceInfo'].normalizedTangentVY >> self.node['matrixNode'].in21
		self.node['ptOnSurfaceInfo'].normalizedTangentVZ >> self.node['matrixNode'].in22
		# Connect the surface positions (X,Y,Z) to the fourth row of the 4x4 Matrix Node
		self.node['ptOnSurfaceInfo'].positionX >> self.node['matrixNode'].in30
		self.node['ptOnSurfaceInfo'].positionY >> self.node['matrixNode'].in31
		self.node['ptOnSurfaceInfo'].positionZ >> self.node['matrixNode'].in32
		# All of the above will be processed by the decomposed matrix node to output what we need.
		# Connect the 4x4 Matrix output to the decompose matrix Input
		self.node['matrixNode'].output >> self.node['decomposeMatrix'].inputMatrix
		
		self.node['decomposeMatrix'].outputTranslate >> self.node['locator'].translate
		self.node['decomposeMatrix'].outputRotate >> self.node['locator'].rotate


def create_uv_pin(mesh, obj, uv=None, name=None):
	"""
	Creates a UvPin to pin geometry onto a mesh.
	:param nt.Transform mesh: Mesh with a UV map.
	:param nt.Transform obj: Object that will be pinned to the geometry.
	:param list(float) uv: UV coordinates.
	:param str name: Name of the UvPin.
	:return: Returns a UvPin to pin geometry onto a mesh.
	:rtype: nt.UvPin
	"""
	if not mesh.getShape():
		logging.warning('Must be a transform with a mesh shape.')
		return
	
	if not isinstance(obj, pm.nt.Transform):
		obj = pm.PyNode(obj)
	
	uv_pin = pm.createNode(pm.nt.UvPin)
	uv_pin.addAttr('isUvPin', at='bool', dv=1)
	if name:
		pm.rename(uv_pin, f'{name}_uvpin')
	if not uv:
		uv = vert_utils.get_uv_coordinates(obj, mesh)
	obj.inheritsTransform.set(0)
	
	mesh.getShape().worldMesh[0] >> uv_pin.deformedGeometry
	uv_pin.outputMatrix[0] >> obj.offsetParentMatrix
	
	# Set the UV position
	uv_pin.coordinate[0].coordinateU.set(uv[0])
	uv_pin.coordinate[0].coordinateV.set(uv[1])
	
	# Need to set the transforms back to zero.  The offset matrix will have the coordinates.
	obj.translate.set((0, 0, 0))
	obj.rotate.set((0, 0, 0))
	obj.scale.set((1, 1, 1))
	
	return uv_pin


def connect_uv_pin(mesh, uv, uv_pin_name=None, locator_scale=0.2):
	"""
	Creates a nt.UvPin and connects a rivet/locator to a mesh.

	:param nt.Transform mesh: The mesh that will have the rivet connected to.
	:param list(float) uv: UV Coordinates.
	:param str uv_pin_name: Name of the UvPin.
	:param float locator_scale: Local scale of the locator that gets connected to the UV pin.
	:return: Returns the name of the locator and the UvPin.
	:rtype: Dictionary
	"""
	
	if not uv_pin_name:
		uv_pin_name = 'loc_rivet'
	loc = pm.spaceLocator(n=uv_pin_name)
	# Scale down the locator.
	pm.setAttr(str(loc) + '.localScaleX', locator_scale)
	pm.setAttr(str(loc) + '.localScaleY', locator_scale)
	pm.setAttr(str(loc) + '.localScaleZ', locator_scale)
	
	# Create the name for the UvPin.
	name_list = loc.split('_')
	if uv_pin_name == 'loc_rivet':
		name_list[0] = 'uvpin'
		uv_pin_name = '_'.join(name_list)
	uv_pin = create_uv_pin(mesh=mesh,
						   obj=loc,
						   uv=uv,
						   name=uv_pin_name)
	# Add a tag for later use.
	return {str(loc): str(uv_pin)}


class BasicRivet(object):
	"""
	Helpers class that allows to create Rivets using vanilla Maya functionality.
	"""
	
	def __init__(self, transform):
		self._surface = None
		self._edges = list()
		self._rivet = transform or None
		self._aim_constraint = None
		self._uv = [0.5, 0.5]
		self._create_joint = False
		self._surface_created = False
		self._percent_on = True
		self._local = False
		self._point_on_surface = None
	
	@classmethod
	def attach_to_surface(cls, transform, surface_to_attach, u=None, v=None, constraint=True):
		"""
		Attach the transform to the surface using a rivet.

		:param pm.PyNode transform: transform node to attach to surface.
		:param pm.PyNode surface_to_attach: surface to attach transform to.
		:param float u: float, U value to attach to.
		:param float v: float, V value to attach to.
		:param bool constraint: whether to create a new locator constrained to given transform.
		:return: Rivet object instance.
		:rtype: pm.PyNode
		"""
		
		position = pm.xform(transform, query=True, ws=True, t=True)
		uv = [u, v]
		if u is None or v is None:
			uv = surface.get_closest_parameter_on_surface(surface_to_attach, position)
		
		rivet = BasicRivet(transform)
		rivet.set_surface(surface_to_attach, uv[0], uv[1])
		rivet.set_create_joint(False)
		rivet.create()
		
		if constraint:
			loc = pm.spaceLocator(n='locator_{}'.format(rivet.rivet))
			pm.parent(loc, rivet.rivet)
			pm.matchTransform(loc, transform, pos=True, rot=True)
			pm.parentConstraint(loc, transform, mo=True)
		else:
			if transform != rivet.rivet:
				pm.parent(transform, rivet.rivet)
		
		return rivet
	
	@property
	def rivet(self):
		return self._rivet
	
	@property
	def aim_constraint(self):
		return self._aim_constraint
	
	@property
	def point_on_surface(self):
		return self._point_on_surface
	
	def set_surface(self, surface_to_attach, u, v):
		self._surface = surface_to_attach
		self._uv = [u, v]
	
	def set_create_joint(self, flag):
		self._create_joint = flag
	
	def set_edges(self, edges):
		self._edges = edges
	
	def set_percent_on(self, flag):
		self._percent_on = flag
	
	def set_local(self, flag):
		self._local = flag
	
	def create(self):
		self._create_rivet()
		self._create_point_on_surface()
		self._create_aim_constraint()
		self._connect()
		
		pm.parent(self._aim_constraint, self._rivet)
		
		return self._rivet
	
	def _create_rivet(self):
		if not self._rivet or not pm.objExists(self._rivet):
			if self._create_joint:
				pm.select(clear=True)
				self._rivet = pm.joint(name='rivetJoint')
			else:
				self._rivet = pm.spaceLocator(name='rivet')
	
	def _create_point_on_surface(self):
		surface_name = self._surface.name(stripNamespace=True)
		self._point_on_surface = pm.createNode('pointOnSurfaceInfo', n='pointOnSurface_{}'.format(surface_name))
		self._point_on_surface.turnOnPercentage.set(self._percent_on)
		self._point_on_surface.parameterU.set(self._uv[0])
		self._point_on_surface.parameterV.set(self._uv[1])
	
	def _create_aim_constraint(self):
		surface_name = self._surface.name(stripNamespace=True)
		self._aim_constraint = pm.createNode('aimConstraint', n='aimConstraint_{}'.format(surface_name))
		self._aim_constraint.aimVector.set((0, 1, 0))
		self._aim_constraint.upVector.set((0, 0, 1))
	
	def _connect(self):
		if pm.objExists('{}.worldSpace'.format(self._surface)):
			if self._local:
				pm.connectAttr(
					'{}.local'.format(self._surface), '{}.inputSurface'.format(self._point_on_surface))
			else:
				pm.connectAttr(
					'{}.worldSpace'.format(self._surface), '{}.inputSurface'.format(self._point_on_surface))
		
		if pm.objExists('{}.outputSurface'.format(self._surface)):
			pm.connectAttr(
				'{}.outputSurface'.format(self._surface), '{}.inputSurface'.format(self._point_on_surface))
		
		pm.connectAttr('{}.position'.format(self._point_on_surface), '{}.translate'.format(self._rivet))
		pm.connectAttr(
			'{}.normal'.format(self._point_on_surface), '{}.target[0].targetTranslate'.format(self._aim_constraint))
		pm.connectAttr(
			'{}.tangentV'.format(self._point_on_surface), '{}.worldUpVector'.format(self._aim_constraint))
		pm.connectAttr('{}.constraintRotateX'.format(self._aim_constraint), '{}.rotateX'.format(self._rivet))
		pm.connectAttr('{}.constraintRotateY'.format(self._aim_constraint), '{}.rotateY'.format(self._rivet))
		pm.connectAttr('{}.constraintRotateZ'.format(self._aim_constraint), '{}.rotateZ'.format(self._rivet))
