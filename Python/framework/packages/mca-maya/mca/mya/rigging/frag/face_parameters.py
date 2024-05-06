#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# mca python imports
import logging
import os
# software specific imports
import pymel.core as pm
# mca python imports
from mca.common.utils import lists
from mca.common import log
from mca.common.textio import jsonio
from mca.mya.modifiers import ma_decorators

from mca.mya.rigging.frag import frag_base

logger = log.MCA_LOGGER


class SingleParameterData:
	def __init__(self, parameter_name,
						region,
						frame,
						multiplier,
						opposite,
						mirror,
						side,
						connection):
		self.parameter_name = parameter_name
		self.frame = frame
		self.multiplier = multiplier
		self.opposite = opposite
		self.mirror = mirror
		self.side = side
		self.connection = connection
		self.region = region


class ParameterData:   # This is from dictionary data not the Node.
	def __init__(self, data):
		self.data = data
	
	@property
	def regions(self):
		"""
		Returns a list of regions.

		:return: Returns a list of regions.
		:rtype: list[str]
		"""
		
		return list(self.data.keys())
	
	@classmethod
	def load(cls, file_path):
		"""
		Loads the parameter data from a json file.

		:param str file_path: The full path of the json file.
		:return: Returns the class instance.
		:rtype: ParameterData
		"""
		
		if '.json' not in file_path:
			file_path = os.path.join(file_path + '.json')
		if not os.path.exists(file_path):
			return
		data = jsonio.read_json_file(file_path)
		return cls(data)
	
	def export(self, file_path):
		"""
		Exports the data to a json file.

		:param str file_path: Full path to the file.
		"""
		
		jsonio.write_to_json_file(data=self.data, filename=file_path)
	
	def add_pose(self, region, pose, frame, opposite, mirror, side, connection, multiplier=1.0):
		"""
		Adds a pose to the parameter data.

		:param str region: The region of the face the pose is affecting.  Ex: Nose, Mouth, Eyes.
		:param str pose: Name of the pose.
		:param float frame: The frame number that represents that pose.
		:param str opposite: The pose that is the opposite.  Meaning up and down.  Not mirror.
		:param str mirror: The pose that is mirrored.  Not up and down.  Mirrored on the x axis.
		:param str side: The side of the face the pose is on.  Ex: left, right, center
		:param str connection: The name of the attribute that the pose gets connected to on the parameter node.
		:param float multiplier: An extra attribute that can be used to multiply a parameter.
		"""
		
		added_pose = SingleParameterData(parameter_name=pose,
									region=region,
									frame=frame,
									multiplier=multiplier,
									opposite=opposite,
									mirror=mirror,
									side=side,
									connection=connection)
		
		parameter_list = self.get_parameters_list()
		parameter_list.insert(added_pose.frame - 1, added_pose)

		for x, parameter in enumerate(parameter_list):
			parameter.frame = x + 1
		self.convert_parameter_list_to_dict(parameter_list)
	
	def remove_pose(self, pose, region=None):
		"""
		Removes a pose from the parameter data.

		:param str pose: Name of the pose.
		:param str region: The region of the face the pose is affecting.  Ex: Nose, Mouth, Eyes.
		"""
		
		if not region:
			for reg in self.regions:
				if pose in self.data[reg]:
					region = reg
					break
		if not region:
			logger.WARNING('Please provide a region.  Unable to find the pose data.')
			return
		
		self.data[region].pop(pose, '{0}: Pose was not found,'.format(pose))
		parameter_list = self.get_parameters_list()
		for x, parameter in enumerate(parameter_list):
			parameter.frame = x + 1
		self.convert_parameter_list_to_dict(parameter_list)
		
	def get_parameters_list(self, sort_by_frame=False, sort_by_name=False):
		"""
		Returns a list of pose parameters without the regions.

		:return: Returns a list of pose parameters without the regions.
		:rtype: list[SingleParameterData]
		"""
		
		parameter_data = []
		for region in self.regions:
			for pose in list(self.data[region].keys()):
				parameter_data.append(self.get_single_pose_data(region, pose))
		if sort_by_frame:
			frame_list = sorted([x.frame for x in parameter_data])
			sorted_parameters = []
			for frame in frame_list:
				for param in parameter_data:
					if param.frame == frame:
						sorted_parameters.append(param)
						break
			return sorted_parameters
		
		if sort_by_name:
			pose_list = sorted([x.parameter_name for x in parameter_data])
			sorted_parameters = []
			for name in pose_list:
				for param in parameter_data:
					if param.parameter_name == name:
						sorted_parameters.append(param)
						break
			return sorted_parameters
		
		return parameter_data
	
	def get_parameter(self, pose):
		parameter = None
		for region in self.regions:
			for pose_name in list(self.data[region].keys()):
				if pose_name == pose:
					parameter = self.get_single_pose_data(region, pose)
					break
		return parameter
	
	def get_parameter_by_connection(self, connection_name):
		parameters = self.get_parameters_list()
		for parameter in parameters:
			if parameter.connection == connection_name:
				return parameter
	
	def get_parameters(self, sort_by_frame=False, sort_by_name=False):
		"""
		Returns a Dictionary of the pose name as the key and the parameters wrapped in a the ParameterData class
		as the value.

		:return: Returns a Dictionary of the pose name as the key and the parameters wrapped in a the
			ParameterData class as the value.
		:rtype: Dictionary{Pose Name : SingleParameterData Class}
		"""
		
		parameter_data = []
		parameter_list = self.get_parameters_list(sort_by_frame=sort_by_frame, sort_by_name=sort_by_name)
		for parameter in parameter_list:
			parameter_data.append({parameter.parameter_name: parameter})
		return parameter_data
	
	def get_pose_list(self):
		"""
		Returns all the parameter names.
		
		:return: Returns all the parameter names.
		:rtype: list(str)
		"""
		
		parameter_list = self.get_parameters_list()
		return [x.parameter_name for x in parameter_list]
		
	def get_region_list(self, region):
		"""
		Returns a list of all the poses in a region.

		:param str region: The region of the face the pose is affecting.  Ex: Nose, Mouth, Eyes.
		:return: Returns a list of all the poses in a region.
		:rtype: list[Dictionary]
		"""
		
		parameter_data = []
		for pose in list(self.data[region].keys()):
			parameter_data.append(self.get_single_pose_data(region, pose))
		return parameter_data

	def convert_parameter_list_to_dict(self, parameter_list):
		pose_data = {}
		for parameter in parameter_list:
			pose_data.setdefault(parameter.region, {})
			pose_data[parameter.region].setdefault(parameter.parameter_name, {})
			pose_data[parameter.region][parameter.parameter_name].update({'frame': parameter.frame})
			pose_data[parameter.region][parameter.parameter_name].update({'multiplier': parameter.multiplier})
			pose_data[parameter.region][parameter.parameter_name].update({'opposite': parameter.opposite})
			pose_data[parameter.region][parameter.parameter_name].update({'mirror': parameter.mirror})
			pose_data[parameter.region][parameter.parameter_name].update({'side': parameter.side})
			pose_data[parameter.region][parameter.parameter_name].update({'connection': parameter.connection})
		self.data = {}
		self.data.update(pose_data)
	
	def get_single_pose_data(self, region, pose):
		"""
		Returns an instance of SingleParameterData.

		:param str region: The region of the face the pose is affecting.  Ex: Nose, Mouth, Eyes.
		:param str pose: Name of the pose.
		:return: Returns an instance of SingleParameterData.
		:rtype: SingleParameterData
		"""
		
		pose_name = pose
		frame = self.data[region][pose]['frame']
		multiplier = self.data[region][pose]['multiplier']
		opposite = self.data[region][pose]['opposite']
		mirror = self.data[region][pose]['mirror']
		side = self.data[region][pose]['side']
		connection = self.data[region][pose]['connection']
		
		return SingleParameterData(parameter_name=pose_name,
									region=region,
									frame=frame,
									multiplier=multiplier,
									opposite=opposite,
									mirror=mirror,
									side=side,
									connection=connection)

	
class FragFaceParameters(frag_base.FRAGNode):
	VERSION = 1.0
	
	@staticmethod
	@ma_decorators.keep_selection_decorator
	@ma_decorators.keep_namespace_decorator
	def create(frag_parent, parameters_list, usage=''):
		"""
		Creates a parameters node that connects a face rig to it's blend shapes.

		param FRAGNode frag_parent: FRAG Rig FRAGNode.
		:param list(ParameterData) parameters_list: List of parameter/pose data.
		:param str usage: Keyword description of the parameter node.
		:return: Returns a node wrapped in a FragFaceParameters instance.
		:rtype: FragFaceParameters
		"""
		
		# Set namespaces
		root_namespace = frag_parent.namespace().split(':')[0]
		pm.namespace(set=':')
		if root_namespace != '':
			pm.namespace(set=f'{root_namespace}:')
		
		node = (frag_base.FRAGNode.create(frag_parent=frag_parent,
											frag_type=FragFaceParameters.__name__,
											version=FragFaceParameters.VERSION))
		node = node.pynode
		
		node.addAttr('usage', dt='string')
		node.usage.set(usage)
		node.addAttr('isFragFace', at='bool', dv=True)
		# node.setAttr("parameter_set", 'expressions', force=True)
		node.addAttr('parameters', numberOfChildren=4, attributeType='compound', multi=True)
		node.addAttr('parameter', dt='string', parent='parameters')
		node.addAttr('value', at='float', parent='parameters', k=True)
		node.addAttr('input', attributeType='message', parent='parameters')
		node.addAttr('pose_data', dt='string', parent='parameters')
		
		node.addAttr('faceEditNode', attributeType='message')
		if not node.hasAttr('message'):
			node.addAttr('message', attributeType='message')
		
		frag_node = FragFaceParameters(node)
		
		# Create variables for each parameter
		for x in range(len(parameters_list)):
			attr = frag_node.parameters[x]
			# Set the compound attribute name
			attr.parameter.set(parameters_list[x].parameter_name)
			attr.setAlias(parameters_list[x].parameter_name)
			# Add parameter info
			pose_data_dict = frag_node.create_pose_data_dict(parameters_list[x])
			pose_data_dict = jsonio.convert_dict_to_string(pose_data_dict)
			attr.pose_data.set(pose_data_dict)
		return frag_node
	
	@staticmethod
	def create_pose_data_dict(parameter):
		"""
		Gathers the parameter information.

		:param ParameterData parameter: The parameter data about a specific pose.
		:return: Returns a string with information about a pose.
		:rtype: str
		"""
		
		tags = {'mirror': str(parameter.mirror),
				'region': str(parameter.region),
				'frame': str(parameter.frame),
				'multiplier': str(parameter.multiplier),
				'opposite': str(parameter.opposite),
				'side': str(parameter.side)}
		return tags
	
	def get_pose_data(self, parameter_name):
		"""
		Returns the pose data for a pose.
		Mirror type, region, frame, multiplier, opposite, side

		:param parameter_name:
		:return: Returns the pose data for a pose.
		:rtype: dictionary
		"""
		
		compound_attribute = self.get_compound_attribute(parameter_name)
		pose_data = eval(compound_attribute.pose_data.get())
		for pose in pose_data:
			try:
				pose_data[pose] = eval(pose_data[pose])
			except:
				pass
		return pose_data
	
	def get_compound_attribute(self, attr_name):
		"""
		Get the compound attribute that is associated with the pose name.

		:param string attr_name: The name of the compound attribute or pose.
		:return: Returns the compound attribute.
		:rtype: pm.nt.general.Attribute
		"""
		
		result = None
		if self.pynode.hasAttr(attr_name):
			result = self.pynode.attr(attr_name)
		return result
	
	def get_parameter_names(self):
		"""
		Returns all the parameter names, or "Pose" names.
		
		:return: Returns all the parameter names.
		:rtype: list(str)
		"""
		
		parameter_names = []
		for x in range(self.pynode.parameters.numElements()):
			parameter_attr = self.pynode.parameters[x]
			parameter_names.append(parameter_attr.parameter.get())
		return parameter_names
	
	def get_side(self, parameter_name):
		"""
		Returns the side the pose is on.

		:param string parameter_name: The name of the compound attribute or pose.
		:return: Returns the side the pose is on.
		:rtype: str
		"""
		
		pose_data = self.get_pose_data(parameter_name)
		return pose_data['side']
	
	def get_mirror(self, parameter_name):
		"""
		Returns the Mirror Type.  Mirror the pose or duplicate and flip.

		:param string parameter_name: The name of the compound attribute or pose.
		:return: Returns the Mirror Type.
		:rtype: str
		"""
		
		pose_data = self.get_pose_data(parameter_name)
		return pose_data.get('mirror', None)
	
	def get_frame(self, parameter_name):
		"""
		Returns the the frame number the pose is stored on.

		:param string parameter_name: The name of the compound attribute or pose.
		:return: Returns the the frame number the pose is stored on.
		:rtype: str
		"""
		
		pose_data = self.get_pose_data(parameter_name)
		return pose_data['frame']
	
	def get_region(self, parameter_name):
		"""
		Returns the the region.

		:param string parameter_name: The name of the compound attribute or pose.
		:return: Returns the the region.
		:rtype: str
		"""
		
		pose_data = self.get_pose_data(parameter_name)
		return pose_data['region']
	
	def get_opposite(self, parameter_name):
		"""
		Returns the the opposite pose.

		:param string parameter_name: The name of the compound attribute or pose.
		:return: Returns the the opposite pose.
		:rtype: str
		"""
		
		pose_data = self.get_pose_data(parameter_name)
		return pose_data.get('opposite', None)
	
	def get_multiplier(self, parameter_name):
		"""
		Returns the the multiplier.  An extra value to multiple any values for this pose.

		:param string parameter_name: The name of the compound attribute or pose.
		:return: Returns the the multiplier.  An extra value to multiple any values for this pose.
		:rtype: str
		"""
		
		pose_data = self.get_pose_data(parameter_name)
		return pose_data['multiplier']
	
	def config_input(self, obj, attribute_name, start_value, end_value, parameter_name):
		"""
		This creates a network of range nodes to connect the parameter node to the animation controls.

		:param nt.PyNode obj: object that will have an attribute added to.
		Must be connected to a Frag node or be a FRAG node.
		:param string attribute_name: name of the attribute that is getting added.
		:param float start_value: Start value of the pose on the animation control.
		:param float end_value: End value of the pose on the animation control.
		:param str parameter_name: Name of the pose.
		"""
		
		compound_attribute = self.get_compound_attribute(parameter_name)
		if not compound_attribute:
			message = "Attribute name given, {0} , isn't a registered face parameter".format(parameter_name)
			logging.warning(message)
			return
		
		obj = pm.PyNode(obj)
		
		if frag_base.is_frag_node(obj):
			frag_parent = frag_base.FRAGNode(obj)
		else:
			frag_parent = frag_base.get_frag_parent(obj)
			
		if not frag_parent:
			raise ValueError("object given isn't connected to a FRAG node")

		# Check to see if the attribute exists
		if not obj.hasAttr(attribute_name):
			obj.addAttr(attribute_name, dv=start_value, min=start_value, max=end_value, keyable=True)
		obj_attr = obj.attr(attribute_name)
		
		# Check attribute limits
		self.check_attribute_limits(obj_attr, start_value, end_value)
		
		# create the range nodes
		range_node = self.create_and_set_range_node(prefix=attribute_name,
													start_value=start_value,
													end_value=end_value)
		obj_attr >> range_node.valueX
		out_attr = range_node.outValueX
		
		# Connect to compound attribute
		in_attr = compound_attribute.value
		out_attr >> in_attr
		
		# Call config_input on the frag_parent
		frag_parent.config_input(obj,
									attribute_name,
									start_value,
									end_value,
									parameter_name,
									self.pynode,
									int(self.get_frame(parameter_name)))
		unit_conv_node = range_node.listConnections(type=pm.nt.UnitConversion)
		if unit_conv_node:
			self.connect_nodes(unit_conv_node, 'unitConvNodes', 'fragParent')
		frag_parent.message >> compound_attribute.input
	
	@staticmethod
	def create_and_set_range_node(prefix, start_value, end_value):
		"""
		Creates a nt.SetRange node to connect to the parameter node.

		:param str prefix: Prefix name fot the nt.SetRange node.
		:param float start_value: Start value of the pose on the animation control.
		:param float end_value: End value of the pose on the animation control.
		:return: Returns a nt.SetRange node to connect to the parameter node.
		:rtype: nt.SetRange
		"""
		
		range_node = pm.createNode(pm.nt.SetRange, n=prefix + '_set_range')
		
		# Set the ranges for negative values
		if end_value < start_value:
			range_node.minX.set(1)
			range_node.maxX.set(0)
			range_node.oldMinX.set(end_value)
			range_node.oldMaxX.set(start_value)
		# Set the ranges for Positive values
		else:
			range_node.minX.set(0)
			range_node.maxX.set(1)
			range_node.oldMinX.set(start_value)
			range_node.oldMaxX.set(end_value)
		return range_node
	
	@staticmethod
	def check_attribute_limits(py_attr, start_value, end_value):
		"""
		Check the limits of an attribute.

		:param pm.nt.general.Attribute py_attr:
		:param float start_value: Start value of the attribute.
		:param float end_value: End value of an attribute.
		"""
		
		if not isinstance(py_attr, pm.nt.general.Attribute):
			message = "{0}: Attribute is not an instance of a PyNode Attribute".format(py_attr)
			logging.warning(message)
			return
		
		attr_max = py_attr.getMax()
		attr_min = py_attr.getMin()
		# accounting for negative range
		if not attr_max is None:
			if end_value < start_value:
				if start_value > attr_max:
					py_attr.setMax(start_value)
			else:
				if end_value > attr_max:
					py_attr.setMax(end_value)
		if not attr_min is None:
			if end_value < start_value:
				if end_value < attr_min:
					py_attr.setMin(end_value)
			else:
				if start_value < attr_min:
					py_attr.setMin(start_value)
	
	def config_output_blendnode(self, blendnode_attr, parameter_name):
		"""
		Connects an attribute on a blend node to an attribute on the parameter node.
		This is the destination side of the connections.

		:param nt.general.Attribute blendnode_attr:  The blend shape attribute that will connect to the parameter node.
		:param str parameter_name: Name of the pose.
		"""
		
		# Connect to compound attribute
		compound_attribute = self.get_compound_attribute(parameter_name)
		out_attr = compound_attribute.value
		out_attr >> blendnode_attr
	
	def is_pose_activated(self, parameter):
		"""
		Checks to see if a pose is not set to it's default looking at the set range nodes.
		
		:param pm.nt.general.Attribute parameter: pose in the parameter node.  Ex: self.pynode.parameters[0]
		:return: returns whether the flag is being used or not.
		:rtype: bool
		"""
		
		if round(parameter.value.get(), 3) != 0:
			return True
		return False
	
	def get_all_active_poses(self):
		"""
		Returns a list of all the poses that have a positive value.
		
		:return: Returns a list of all the poses that have a positive value.
		:rtype: list(str)
		"""
		active_poses = []
		for x in range(self.pynode.parameters.numElements()):
			parameter_attr = self.pynode.parameters[x]
			if self.is_pose_activated(parameter_attr):
				pose_name = parameter_attr.parameter.get()
				active_poses.append(pose_name)
		return active_poses
	
	def get_all_active_poses_and_value(self):
		"""
		Returns a Dictionary of all the poses that have a positive value.

		:return: Returns a Dictionary of all the poses that have a positive value.
		:rtype: Dictionary
		"""
		active_poses = {}
		for x in range(self.pynode.parameters.numElements()):
			parameter_attr = self.pynode.parameters[x]
			if self.is_pose_activated(parameter_attr):
				pose_name = parameter_attr.parameter.get()
				component = frag_base.FRAGNode(parameter_attr.input.get())
				active_poses[pose_name] = {}
				active_poses[pose_name]['value'] = parameter_attr.value.get()
				active_poses[pose_name]['flag'] = component.get_flag()
		return active_poses
	
	def get_all_components(self, active=False):
		"""
		Returns all the components on the parameter node.
		
		:param bool active: If there are only active
		:return: Returns all the components on the parameter node.
		:rtype: list(FRAGNode)
		"""
		
		active_component = []
		for pose in self.node.parameters:
			if self.is_pose_activated(pose) and active:
				active_component.append(pose.input.get())
			else:
				active_component.append(pose.input.get())
		return active_component
	
	def get_range_node(self, parameter_name):
		"""
		Returns the range node connected the parameters node.  The range node holds all the
		values for the flag.
		
		:param string parameter_name: name of the parameter block
		:return: Returns a range network node
		:rtype: pm.nt.SetRange
		"""
		
		compound_attr = self.pynode.attr(str(parameter_name))
		block_connections = compound_attr.value.listConnections(d=True, type=pm.nt.SetRange)
		range = lists.get_first_in_list(block_connections)
		return range
	
	def keyframe_flags_max_values(self):
		"""
		Sets a keyframe for the pose on the max value on the correct pose frame.
		This is needed, since it is a Frag Face Component.
		"""
		
		return None
	
	def reanimate(self,other_root):
		pass
	
	