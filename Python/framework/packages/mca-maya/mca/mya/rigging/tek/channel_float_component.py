#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Adds a custom channel to export into engine.
"""

# system global imports
from __future__ import print_function, division, absolute_import

# software specific imports
import pymel.core as pm

# mca python imports
from mca.common import log
from mca.mya.utils import attr_utils
from mca.mya.modifiers import ma_decorators
# internal module imports
from mca.mya.rigging.tek import keyable_component


logger = log.MCA_LOGGER


class ChannelFloatComponent(keyable_component.KeyableComponent):
	"""
	Channel component base
	"""
	
	VERSION = 1
	
	# Future request!
	# Need to add an add_attr and remove attr function for this component.
	
	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(tek_parent,
				obj,
				joint,
				channel_dict_list,  # See create_channel_dict() function below.
				component_name):
		"""
		Creates an animatable channel component that allows custom components to be exported in engine.
		
		:param TEKRig tek_parent: The TEKRig.
		:param pm.nt.DagNode obj: the object that the channel gets added too.
		:param pm.nt.Joint joint: A duplicated attribute added to a joint to be exported into engine.
		:param string component_name: the name that gets attached to the component
		:param list(dict) channel_dict_list: list of dictionaries that has the information that pertains to the attribute
		and animation channel
		:return: Returns an instance of ChannelComponent
		:rtype: ChannelFloatComponent
		"""
		
		if isinstance(channel_dict_list, dict):
			channel_dict_list = [channel_dict_list]
			
		# Set Namespace
		root_namespace = tek_parent.namespace().split(':')[0]
		pm.namespace(set=f'{root_namespace}:')
		
		# create channel node
		channel_node = keyable_component.KeyableComponent.create(tek_parent,
																	tek_type=ChannelFloatComponent.__name__,
																	version=ChannelFloatComponent.VERSION,
																	side='center',
																	region=component_name)
		kwargs_dict = {}
		kwargs_dict['obj'] = obj
		kwargs_dict['joint'] = joint
		#kwargs_dict['channel_dict_list'] = channel_dict_list  # ToDo ncomes - need to find a way to work with re-animator
		kwargs_dict['component_name'] = component_name
		
		# set serialized kwargs onto our network node we'll use this for serializing the exact build params.
		attr_utils.set_compound_attribute_groups(channel_node, 'buildKwargs', kwargs_dict)
		
		for channel in channel_dict_list:
			obj_attr_name = channel.pop('obj_attr_name')
			joint_attr_name = channel.pop('joint_attr_name')
			attr_min = channel.pop('min')
			attr_max = channel.pop('max')
			default_value = channel.pop('default_value')
			keyable = channel.pop('keyable')
			
			if isinstance(obj_attr_name, pm.nt.general.Attribute):
				obj_attr = obj_attr_name
			
			elif not obj.hasAttr(obj_attr_name):
				# add channel attrs
				obj.addAttr(obj_attr_name,
							at='float',
							defaultValue=default_value,
							min=attr_min,
							max=attr_max,
							k=keyable)
				obj_attr = obj.attr(obj_attr_name)
			else:
				obj_attr = obj.attr(obj_attr_name)
			
			if isinstance(joint_attr_name, pm.nt.general.Attribute):
				joint_attr = joint_attr_name
			
			elif not joint.hasAttr(joint_attr_name):
				# add channel attrs
				joint.addAttr(joint_attr_name,
							at='float',
							defaultValue=default_value,
							usedAsProxy=True,
							min=attr_min,
							max=attr_max,
							k=keyable)
				joint_attr = joint.attr(joint_attr_name)
			else:
				joint_attr = joint.attr(joint_attr_name)
			
			obj_attr >> joint_attr
			
		channel_node.connect_node(obj, 'FragChannelFloat', 'FragChannelFloat')
		channel_node.connect_node(joint, 'FragChannelFloatJnt', 'FragChannelFloatJnt')
		
		
		
		
		return channel_node


def create_channel_float_dict(obj_attr_name,
								joint_attr_name,
								attr_min=0.0,
								attr_max=1.0,
								default_value=0.0,
								keyable=True):
	"""
	Set up the dictionary for plug into the ChannelComponent.
	
	:param str obj_attr_name: the name of the attribute for the channel component
	:param str joint_attr_name: the name of the attribute that gets applied to the joint.
	:param float attr_min: minimum value of the attribute
	:param float attr_max: maximum value of the attribute
	:param float default_value: the value the attribute in Maya will start at.
	:param bool keyable: sets whether the attribute in Maya is keyable and hidden.
	:return: Returns a dictionary for the channel component
	:rtype: Dictionary
	"""
	
	channel = dict()
	channel['obj_attr_name'] = obj_attr_name
	channel['joint_attr_name'] = joint_attr_name
	channel['min'] = attr_min
	channel['max'] = attr_max
	channel['default_value'] = default_value
	channel['keyable'] = keyable
	return channel

