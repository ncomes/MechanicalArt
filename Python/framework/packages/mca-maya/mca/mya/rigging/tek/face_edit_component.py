#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""
# System global imports
# software specific imports
import pymel.core as pm
# mca python imports
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging.flags import tek_flag
from mca.common import log
from mca.common.utils import lists

# Internal module imports
from mca.mya.rigging.tek import tek_base, face_parameters, tek_rig

logger = log.MCA_LOGGER


def get_face_edit_node(rig_node, skip_dialog=False):
	"""
	Returns the FaceEditComponent.
	
	:param pm.nt.Dagnode rig_node: a node that is connected to the rig.
	:param bool skip_dialog: If True, no warnings will be printed in the script editor.
	:return: Returns the FaceEditComponent.
	:rtype: FaceEditComponent
	"""
	
	tek_rig_node = tek_rig.get_tek_rig(rig_node)
	if not tek_rig_node:
		if not skip_dialog:
			logger.warning('The node given is not connected to a rig or there is not TEKRig node in the scene.')
		return
	edit_node = tek_rig_node.get_tek_children(of_type=FaceEditComponent)
	if not edit_node:
		if not skip_dialog:
			logger.warning('No Staging Edit Node exists in scene')
		return
	return edit_node[0]


class FaceEditComponent(tek_base.TEKNode):
	VERSION = 1.0
	
	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(tek_parent):
		"""
		Creates a Face Edit Component that connects and tracks meshes.
		
		:param tek_parent: TEK Skeletal Mesh TEKNode
		:return: Returns an instance of FaceEditNode
		:rtype: FaceEditComponent
		"""
		
		# Set Namespace
		root_namespace = tek_parent.namespace().split(':')[0]
		pm.namespace(set=':')
		if root_namespace != '':
			pm.namespace(set=f'{root_namespace}:')
		
		node = tek_base.TEKNode.create(tek_parent=tek_parent,
											tek_type=FaceEditComponent.__name__,
											version=FaceEditComponent.VERSION)
		
		node.addAttr('isStagingEditNode', at='bool', dv=1)
		
		node.addAttr('flag', dt='string')
		node.addAttr('flagAttribute', dt='string')
		node.addAttr('flagValue', at='float3')
		node.addAttr('flagX', at='float', parent='flagValue')
		node.addAttr('flagY', at='float', parent='flagValue')
		node.addAttr('flagZ', at='float', parent='flagValue')
		node.addAttr('maxValue', at='float')
		node.addAttr('poseName', dt='string')
		node.addAttr('poseSide', dt='string')
		node.addAttr('flagComponent', dt='string')
		
		node.addAttr('parameterNode', at='message')
		node.addAttr('parallelBlendnode', at='message')
		
		node.addAttr('mesh', dt='string')
		node.addAttr('parameterNodePose', dt='string')
		node.addAttr('diffMeshHidden', at='message')  # parallel diff
		node.addAttr('liveEditMesh', at='message')    # parallel Live
		node.addAttr('dupPosesMesh', at='message')    # extra dup mesh
		
		node.addAttr('poseMesh', at='message')
		node.addAttr('oldPose', at='message')
		node.addAttr('neutralPose', at='message')
		node.addAttr('editMode', at='bool', dv=0)
		node.addAttr('paintNeutral', at='bool', dv=0)
		node.addAttr('multiPoseMode', at='bool', dv=0)
		node.addAttr('singlePoseMode', at='bool', dv=0)
		node.addAttr('baseEditMode', at='bool', dv=0)
		node.addAttr('replaceEditMode', at='bool', dv=0)
		node.addAttr('duplicatedMeshes', dt='string')
		
		return node
	
	def set_flags_info(self, main_pose=None):
		"""
		Creates compound attributes (blocks) with flag information.
		
		:param str main_flag: if given, it will skip that flag in the pose data.
		"""
		
		# set the compound attribute
		self.pynode.addAttr('activeFlags', numberOfChildren=6, attributeType='compound', multi=True)
		self.pynode.addAttr('activeFlag', attributeType='message', parent='activeFlags')
		self.pynode.addAttr('activeFlagAttribute', dt='string', parent='activeFlags')
		self.pynode.addAttr('activeFlagValue', at='float3', parent='activeFlags')
		self.pynode.addAttr('activeX', at='float', parent='activeFlagValue')
		self.pynode.addAttr('activeY', at='float', parent='activeFlagValue')
		self.pynode.addAttr('activeZ', at='float', parent='activeFlagValue')
		
		self.pynode.addAttr('activeFlagMaxValue', at='float', parent='activeFlags')
		self.pynode.addAttr('activePoseName', dt='string', parent='activeFlags')
		self.pynode.addAttr('activeComponent', dt='string', parent='activeFlags')
		
		# Get the parameter node component so we can see what flags are being used.
		tek_parent = self.get_tek_parent()
		parameter_node = tek_parent.get_tek_children(of_type=face_parameters.FragFaceParameters)
		if not parameter_node:
			return
		# Get the flag names that are being used.
		active_flags = FaceFlagsData.create_active(parameter_node[0])
		if not active_flags:
			logger.warning('No flags are active.')
			return
		flags_dict = active_flags.get_flags_dict()
		
		# Enumerate doesn't work here.  If it needs to skip, it will set the compound attribute index incorrectly.
		#  Keeping it safe...
		i = 0
		for pose_name in list(flags_dict.keys()):
			# We have to set the compound attributes using the pose names, since they are unique.
			# go through every pose and collect the data to stamp on to the compound attributes
			# If we find the "Main" flag (The flag we care about) We do not include it in the compound attribute.
			
			flag_name = flags_dict[pose_name].get('activeFlag', None)
			if pose_name == main_pose:
				continue
			attr = self.pynode.activeFlags[i]
			flag_pynode = pm.ls(flag_name, type=pm.nt.Transform)[0]
			flag_pynode.message >> attr.activeFlag
			
			# Make sure we account whether the value is a vector or a float.
			# All compound attributes have 3 floats to represent a Vector.  if it is a single value we just use the
			# 1st Value.  ValueX
			value = flags_dict[pose_name].get('activeFlagValue', None)
			if value and isinstance(value, list):
				value = list(map(lambda x: float(x), value))
				attr.activeFlagValue.activeX.set(float(value[0]))
				attr.activeFlagValue.activeY.set(float(value[1]))
				attr.activeFlagValue.activeZ.set(float(value[2]))
			else:
				attr.activeFlagValue.activeX.set(float(value))
			
			flag_attr = flags_dict[pose_name].get('activeFlagAttribute', None)
			max_value = float(flags_dict[pose_name].get('activeFlagMaxValue', None))
			flag_component = str(flags_dict[pose_name].get('activeComponent', None))
			
			# Set the Compound attribute
			attr.activeFlagAttribute.set(flag_attr)
			attr.activeFlagMaxValue.set(max_value)
			attr.activePoseName.set(pose_name)
			attr.activeComponent.set(flag_component)
			attr.setAlias(pose_name)
			i+=1
	
	def set_main_flag_info(self, main_pose=None):
		"""
		Sets the data for the the flag you are focusing on.  This is the main flag.

		:param str main_pose: The pose that will be recorded.
		"""
		
		# Get the Parameter Node Componented and Run through all the flags in use and find the one we care about.
		#  The "Main" flag.  That data gets stamped outside the counpound attributes.
		tek_parent = self.get_tek_parent()
		parameter_node = tek_parent.get_tek_children(of_type=face_parameters.FragFaceParameters)
		if not parameter_node:
			return
		parameter_node = parameter_node[0]
		self.pynode.parameterNode >> parameter_node.faceEditNode
		
		active_flags = FaceFlagsData.create_active(parameter_node)
		if not active_flags:
			return
		flags_dict = active_flags.get_flags_dict()
		
		# Go through all the flags and find the "Main" flag.  Then stamp the data.
		for pose_name in list(flags_dict.keys()):
			flag_name = flags_dict[pose_name].get('activeFlag', None)
			if pose_name == main_pose:
				
				self.pynode.flag.set(flag_name)
				value = flags_dict[pose_name].get('activeFlagValue', None)
				if value and isinstance(value, list):
					value = list(map(lambda x: float(x), value))
					self.pynode.flagValue.flagX.set(float(value[0]))
					self.pynode.flagValue.flagY.set(float(value[1]))
					self.pynode.flagValue.flagZ.set(float(value[2]))
				else:
					self.pynode.flagValue.flagX.set(float(value))
				
				flag_attr = flags_dict[pose_name].get('activeFlagAttribute', None)
				max_value = float(flags_dict[pose_name].get('activeFlagMaxValue', None))
				flag_component = str(flags_dict[pose_name].get('activeComponent', None))
				
				# Set the attibute data
				self.pynode.flagAttribute.set(flag_attr)
				self.pynode.maxValue.set(max_value)
				self.pynode.parameterNodePose.set(pose_name)
				self.pynode.flagComponent.set(flag_component)
				break
		
	
	@property
	def single_pose(self):
		return self.pynode.singlePoseMode.get()
	
	@single_pose.setter
	def single_pose(self, value=True):
		self.pynode.singlePoseMode.set(value)
	
	@property
	def multi_pose(self):
		return self.pynode.multiPoseMode.get()
	
	@multi_pose.setter
	def multi_pose(self, value=True):
		self.pynode.multiPoseMode.set(value)
	
	@property
	def base_edit(self):
		return self.pynode.baseEditMode.get()
	
	@base_edit.setter
	def base_edit(self, value=True):
		self.pynode.baseEditMode.set(value)
	
	@property
	def paint_neutral(self):
		return self.pynode.paintNeutral.get()
	
	@paint_neutral.setter
	def paint_neutral(self, value=True):
		self.pynode.paintNeutral.set(value)
	
	@property
	def main_flag_value(self):
		"""
		Returns the flag value that was recorded.  If it is translate or rotate it will return a list.
		
		:return: Returns the flag value that was recorded.
		:rtype: list(float) or float
		"""
		
		if self.pynode.flagAttribute.get() == 'translate' or self.pynode.flagAttribute.get() == 'rotate':
			return [self.pynode.flagValue.flagX.get(), self.pynode.flagValue.flagY.get(), self.pynode.flagValue.flagZ.get()]
		else: return self.pynode.flagValue.flagX.get()
	
	def set_main_flag(self):
		"""
		Sets the flag data for the main flag.  This is the data outside of the compound attributes
		"""
		
		flag_name = self.pynode.flag.get()
		value = self.main_flag_value
		flag_attr = self.pynode.flagAttribute.get()
		
		flag_list = pm.ls(flag_name, type=pm.nt.Transform)
		if not flag_list:
			return
		main_flag = pm.PyNode(flag_list[0])
		pm.setAttr(main_flag.attr(flag_attr), value)
	
	def get_flag_block_value(self, pose_name):
		"""
		Returns the flag value that was recorded.  If it is translate or rotate it will return a list.
		
		:param str pose_name: The pose name is used for the compound attribute name.
		:return: Returns the flag value that was recorded.
		:rtype: list(float) or float
		"""
		
		flag_block = self.get_pose_block(pose_name)
		if not flag_block:
			return
		
		if flag_block.activeFlagAttribute.get() == 'translate' or flag_block.activeFlagAttribute.get() == 'rotate':
			value = [flag_block.activeFlagValue.activeX.get(),
						flag_block.activeFlagValue.activeY.get(),
						flag_block.activeFlagValue.activeZ.get()]
		else:
			value = flag_block.activeFlagValue.activeX.get()
		return value
	
	def get_pose_block(self, pose_name):
		"""
		Returns the pymel attribute for the compound attribute.
		
		:param str pose_name: The pose name is used for the compound attribute name.
		:return: Returns the pymel attribute for the compound attribute.
		:rtype: pm.nt.general.Attribute
		"""
		
		return self.pynode.attr(pose_name)
	
	def get_flag_block(self, flag_name):
		"""
		Gets a compound attribute block that matches the flag name
		
		:param str pose_name: The pose name is used for the compound attribute name.
		:return: Gets the name of the compound attribute
		:rtype: pm.nt.general.Attribute
		"""
		
		block_num = self.pynode.activeFlags.numElements()
		for x in range(block_num):
			_flag = self.pynode.activeFlags[x].activeFlag.get()
			block_flag = pm.PyNode(_flag).nodeName()
			if block_flag == flag_name:
				return self.pynode.activeFlags[x]
		
		logger.warning(f'"{flag_name}" does not have a compound attribute.')
		return

	def set_all_flag_block_values(self):
		"""
		Set all the flag values in the compound attributes
		"""
		
		block_num = self.pynode.activeFlags.numElements()
		
		pose_names = []
		for x in range(block_num):
			pose_name = self.pynode.activeFlags[x].activePoseName.get()
			pose_names.append(pose_name)
		
		for pose_name in pose_names:
			self.set_flag_block_value(pose_name)
	
	def set_flag_block_value(self, pose_name):
		"""
		Sets a flag value from a compound attribute
		
		:param str pose_name: The pose name is used for the compound attribute name.
		"""
		
		block_data = self.get_data_block(pose_name)

		value = block_data.get('activeFlagValue', None)
		flag_attr = block_data.get('activeFlagAttribute', None)
		flag_name = block_data.get('activeFlag', None)
		component = block_data.get('activeComponent', None)
		component = tek_base.TEKNode(component)
		
		flag_list = pm.ls(flag_name, type=pm.nt.Transform)
		if not flag_list:
			return
		active_flag = pm.PyNode(flag_list[0])
		if component.get_type() == 'EyeComponent':
			pm.xform(active_flag, t=value, ws=True)
			return
		pm.setAttr(active_flag.attr(flag_attr), value)
	
	def get_data_block(self, pose_name):
		"""
		Gets all of the data from a compound attribute. (block)
		
		:param string pose_name: Name of the flag or compound attribute.
		:return: dictionary of all the flag information.
		:rtype: Dictionary
		"""
		
		flag_block = self.get_pose_block(pose_name)
		if not flag_block:
			return
		
		value = self.get_flag_block_value(pose_name)
		
		block_dict = {}
		block_dict['activeFlag'] = flag_block.activeFlag.get()
		block_dict['activeFlagAttribute'] = flag_block.activeFlagAttribute.get()
		block_dict['activeFlagValue'] = value
		block_dict['activeFlagMaxValue'] = float(flag_block.activeFlagMaxValue.get())
		block_dict['activePoseName'] = flag_block.activePoseName.get()
		block_dict['activeComponent'] = flag_block.activeComponent.get()
		return block_dict

	def get_pose_from_block(self, flag_name):
		"""
		Returns the pose name from a flag compound attribute. (block)
		
		:param string flag_name: Name of the flag or compound attribute.
		:return: returns the pose name from a stored flag.
		:rtype: str
		"""
		
		flag_block = self.get_flag_block(flag_name)
		if not flag_block:
			return
		return flag_block.activePoseName.get()
	
	def get_flag_attr_from_block(self, flag_name):
		"""
		Returns the flag attribute from a compound attribute. (block)
		
		:param string flag_name: Name of the flag or compound attribute.
		:return: Returns the flag attribute from a compound attribute. (block)
		:rtype: str
		"""
		
		flag_block = self.get_flag_block(flag_name)
		if not flag_block:
			return
		return flag_block.activeFlagAttribute.get()
	
	def get_flag_value_from_block(self, flag_name):
		"""
		Returns the flag value from a compound attribute. (block)
		
		:param string flag_name: Name of the flag or compound attribute.
		:return: Returns the flag value from a compound attribute. (block)
		:rtype: str
		"""
		
		flag_block = self.get_flag_block(flag_name)
		if not flag_block:
			return
		return float(flag_block.activeFlagValue.get())
	
	def get_flag_max_value_from_block(self, flag_name):
		"""
		Returns the flag value from a compound attribute. (block)
		
		:param string flag_name: Name of the flag or compound attribute.
		:return: Returns the flag value from a compound attribute. (block)
		:rtype: str
		"""
		
		flag_block = self.get_flag_block(flag_name)
		if not flag_block:
			return
		return float(flag_block.activeFlagMaxValue.get())
	
	def get_flag_component_from_block(self, flag_name):
		"""
		Returns the flag component from a compound attribute. (block)
		
		:param string flag_name: Name of the flag or compound attribute.
		:return: Returns the flag component from a compound attribute. (block)
		:rtype: str
		"""
		
		flag_block = self.get_flag_block(flag_name)
		if not flag_block:
			return
		return tek_base.TEKNode(flag_block.activeComponent.get())
	
	
class FaceFlagsData:
	def __init__(self, flag_data_list):
		self.flag_data_list = flag_data_list
	
	@classmethod
	def create_active(cls, parameter_node):
		"""
		Returns an instance of the FlagData class.  It holds setting information about the flags.

		:return:  Return the list of transform information.
		:rtype: FlagData
		"""
		
		pose_list = parameter_node.get_all_active_poses()
		if not pose_list:
			logger.warning('No active poses have been found.  No poses with a value other than 0')
			return
		return FaceFlagsData.create(pose_list, parameter_node)
	
	@classmethod
	def create(cls, pose_list, parameter_node):
		"""
		Returns an instance of the FlagData class.  It holds setting information about the flags.

		:return:  Return the list of transform information.
		:rtype: FlagData
		"""
		
		# Goes through all the poses in the parameter node component and finds the ones in use.
		flag_data = []
		for pose in pose_list:
			range_node = parameter_node.get_range_node(pose)
			component = tek_base.TEKNode(parameter_node.attr(pose).input.get())
			rig_flag = component.get_flag()
			parameter_value = parameter_node.attr(pose).value.get()
			value = round(range_node.valueX.get(), 4)
			flag_attr_max = range_node.oldMaxX.get()
			flag_attr = lists.get_first_in_list(range_node.valueX.listConnections(p=True, scn=True))
			
			# The eye component is handled differently than any of the other components since we need to
			# convert rotation into translation.
			if component.get_type() == 'EyeComponent':
				value = pm.xform(rig_flag, q=True, t=True, ws=True)
				flag_attr = rig_flag.translate
			
			flag_data.append(FlagAttrData(rig_flag=rig_flag,
											flag_attr=flag_attr,
											value=value,
											pose=pose,
											flag_attr_max=flag_attr_max,
											parameter_value=parameter_value,
											component=component))
		
		return cls(flag_data)
	
	def get_fully_active_flags(self):
		"""
		Returns flags that are at the max value

		:return: Returns flags that are at the max value
		:rtype: list(FlagAttrData)
		"""
		
		active_flags = []
		for flag_data in self.flag_data_list:
			if flag_data.value == 1:
				active_flags.append(flag_data)
		return active_flags
	
	def get_partial_active_flags(self):
		"""
		Returns flags that are at not at the max value but due have a parameter value higher than zero

		:return:Returns flags that are at not at the max value but due have a parameter value higher than zero
		:rtype: list(FlagAttrData)
		"""
		
		active_flags = []
		for flag_data in self.flag_data_list:
			if 1 > flag_data.value > 0:
				active_flags.append(flag_data)
		return active_flags
	
	def get_flags_dict(self):
		"""
		Returns a dictionary with all of the flags that are in use.
		
		:return:  Returns a dictionary with all of the flags that are in use.
		:rtype: Dictionary
		"""
		
		flags_dict = {}
		for _flag in self.flag_data_list:
			pose_name = _flag.pose
			flags_dict[pose_name] = {}
			flags_dict[pose_name]['activeFlag'] = _flag.flag_as_string()
			flags_dict[pose_name]['activeFlagAttribute'] = _flag.flag_attr_as_string()
			flags_dict[pose_name]['activeFlagValue'] = _flag.value
			flags_dict[pose_name]['activeFlagMaxValue'] = _flag.flag_attr_max
			flags_dict[pose_name]['activePoseName'] = pose_name
			flags_dict[pose_name]['activeParameterValue'] = _flag.parameter_value
			flags_dict[pose_name]['activeComponent'] = _flag.component
		return flags_dict


class FlagAttrData(object):
	def __init__(self, rig_flag, flag_attr, value, pose, flag_attr_max, parameter_value, component):
		self.rig_flag = tek_flag.Flag(rig_flag)
		self.flag_attr = flag_attr
		self.value = value
		self.pose = pose
		self.flag_attr_max = flag_attr_max
		self.parameter_value = parameter_value
		self.component = component
	
	@property
	def percent(self):
		"""
		Get the percent value of the flag attribute value with a min and max.

		:return: percent value of the flag attribute value with a min and max.
		:rtype: float
		"""
		
		percent = abs(self.value / self.flag_attr_max) * 100
		return percent
	
	def flag_as_string(self, include_namespace=True):
		"""
		Returns the name of the flag as a string.

		:param bool include_namespace: If True, it will return the flag with the namespace.
		:return: Returns the name of the flag as a string.
		:rtype: str
		"""
		
		if not include_namespace and ':' in self.rig_flag.nodeName():
			string_flag = (self.rig_flag.nodeName()).split(':')[-1]
			return string_flag

		return self.rig_flag.nodeName()

	def flag_attr_as_string(self):
		"""
		Returns the flag attribute as a string.
		
		:return: Returns the flag attribute as a string.
		:rtype: str
		"""
		
		return self.flag_attr.split('.')[-1]

