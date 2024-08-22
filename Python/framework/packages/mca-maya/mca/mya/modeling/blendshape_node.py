#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Face: Utility Functions. """

# system global imports
from __future__ import print_function, division, absolute_import

# software specific imports
import pymel.core as pm

# mca python imports
from mca.mya.utils import attr_utils
from mca.mya.modeling import blendshape_model
from mca.mya.animation import time_utils
#from mca.mya.rigging.flags import flag_utils


class BlendShapeNode(object):
	def __init__(self, blendnode=None):
		self.blendnode = self.get_blendnode(blendnode)
	
	@classmethod
	def create(cls, shapes, mesh, label=None, suffix='blendnode', blendnode_type='main'):
		"""
		Returns an instance of the class BlendShapeNode

		:param list(str) shapes: list of meshes that are used to create blend shapes.
		:param pm.nt.Transform mesh: The mesh to connect the blend shapes to.
		:param str label: name of the blend node.
		:param str suffix: name of the blend node.
		:return: Returns an instance of the class BlendShapeNode
		:rtype: BlendShapeNode
		"""
		
		if not label:
			label = str(mesh)
		blendnode = pm.blendShape(shapes, mesh, n=f'{label}_{suffix}')[0]
		blendnode.addAttr('blendNodeType', dt='string')
		blendnode.blendNodeType.set(blendnode_type)
		
		return cls(blendnode)
	
	def disconnect_from_rig(self):
		"""
		Disconnects all of the blend shapes from a rig.
		"""
		
		shapes = self.shapes
		for shape in shapes:
			blendnode_attr = self.blendnode.attr(shape)
			pm.disconnectAttr(blendnode_attr)
	
	def reconnect_to_rig(self, parameters, parameter_node):
		"""
		Reconnects the blendnode to the FragFaceParameters rig node.

		:param list parameters: list of parameters with pose names and information.
		:param face_parameters.FragFaceParameters parameter_node: FragFaceParameters rig node.
		"""
		
		# zero controllers
		flag_utils.zero_flags([parameter_node])
		
		for parameter in parameters:
			param_name = parameter.parameter_name
			param_connection = parameter.connection
			if pm.objExists(param_name) and self.blendnode.hasAttr(param_name) and parameter.connection:
				face_param = parameter_node.pynode.attr(param_connection)
				blendshape_parameter = self.blendnode.attr(param_name)
				face_param.value >> blendshape_parameter
	
	def set_parameterized_keyframes(self, parameters, set_time_range=True):
		"""
		Sets keyframes for each blend shape on the blend node.

		:param list(ParameterData) parameters: a list of parameter data for each pose.
		:param bool set_time_range: If true, it will set the time range.
		:return: Returns the timeline
		:rtype: list(float)
		"""
		
		for parameter in parameters:
			if self.blendnode.hasAttr(parameter.parameter_name):
				pm.setKeyframe(self.blendnode.attr(parameter.parameter_name), t=parameter.pose_frame - 1, v=0)
				pm.setKeyframe(self.blendnode.attr(parameter.parameter_name), t=parameter.pose_frame, v=1.0)
				pm.setKeyframe(self.blendnode.attr(parameter.parameter_name), t=parameter.pose_frame + 1, v=0)
		time_range = [time_utils.get_scene_first_keyframe(), time_utils.get_scene_last_keyframe()]
		if set_time_range and time_range:
			pm.playbackOptions(min=time_range[0], max=time_range[1])
		return time_range
	
	def get_blendnode_mesh_name(self):
		"""
		Returns the name of the mesh the blend node is attached to.

		:return: Returns the name of the mesh the blend node is attached to.
		:rtype: str
		"""
		object_set = self.blendnode.message.listConnections(type=pm.nt.ObjectSet)
		if not object_set:
			return
		object_set = object_set[0]
		all_connections = object_set.listConnections()
		if not all_connections:
			return
		for node in all_connections:
			if isinstance(node, pm.nt.Transform) and pm.listRelatives(node, s=True):
				return node
		return
	
	@property
	def shapes(self):
		"""
		Gets a list of all the shapes connected to the blend node.

		:return: Gets a list of all the shapes connected to the blend node.
		:rtype: list[str]
		"""
		
		return blendshape_model.get_blendnode_shapes(self.blendnode)
	
	def get_all_blendnodes(self, mesh):
		"""
		Returns all the blendnodes associated with a mesh.

		:param pm.nt.transform mesh: Mesh that has blendnodes associated with a it.
		:return: List of all the blendnodes associated with a mesh.
		:rtype: list[pm.nt.Blendnode]
		"""
		
		return blendshape_model.get_all_blendnodes(mesh=mesh)
	
	def delete_blendshapes(self):
		"""
		Deletes all blend shape in a scene that are attached to the blendnode.
		"""
		
		blendshape_model.delete_blendshapes(self.blendnode)
	
	def set_blendshape_weights(self, weight=0):
		"""
		Sets the vertex weight of the blend shape.  Think of painting weights.
		"""
		
		blendshape_model.set_blendshape_weights(blendnode=self.blendnode, weight=weight)
	
	def get_blendnode(self, blendnode=None):
		"""
		Returns a blend node.  If you pass in a mesh it will grab the 1st blend node.

		:param pm.nt blend blendnode: This can be a blend shape node or a mesh that has a blend shape connected to it.
		:return pm.nt.Blendnode: Returns a blend node.
		"""
		
		if not blendnode:
			blendnode = self.blendnode
		
		first_blendnode = blendshape_model.get_first_blendnode(blendnode)
		if not first_blendnode:
			# raising error, it can get confusing if this returns none.
			raise RuntimeError('The object is not a blend shape or an object with a blend shape attached.')
		return first_blendnode
	
	def get_blendnode_index_as_dict(self):
		"""
		Returns the name of the shape as the key and the index as the value.

		:return: Returns the name of the shape as the key and the index as the value.
		:rtype: dictionary{string:int}
		"""
		
		return blendshape_model.get_blendnode_index_as_dict(self.blendnode)
	
	def get_mesh(self):
		"""
		Returns the original connected mesh.

		:return: Returns the original connected mesh.
		:rtype: pm.nt.Transform
		"""
		
		mesh = self.blendnode.originalGeometry.listConnections()
		if not mesh:
			return
		return mesh[0]
	
	def generate_face_shapes(self, mesh=None):
		"""
		Returns a list of generated face shapes.

		:return: Returns a list of generated face shapes.
		:rtype: list(pm.nt.Transform)
		"""
		
		blendnode_dict = self.get_blendnode_index_as_dict()
		if not mesh:
			mesh = self.get_mesh()
		shapes = []
		for pose, index in blendnode_dict.items():
			self.blendnode.attr(pose).set(1)
			new_mesh = pm.duplicate(mesh)[0]
			pm.rename(new_mesh, pose)
			self.blendnode.attr(pose).set(0)
			shapes.append(new_mesh)
		shapes = [pm.PyNode(x) for x in shapes]
		attr_utils.purge_user_defined_attrs(shapes)
		return shapes

