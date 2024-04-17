#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.modifiers import ma_decorators
# Internal module imports
from mca.mya.rigging.tek import tek_base


class SingleSDKComponent(tek_base.TEKNode):
	VERSION = 1
	
	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(tek_parent,
				drive_attr,
				driven_obj,
				side,
				region,
				driven_attrs=None,
				drive_attr_values=(0,0)):
		"""
		Creates an Single Set Driven Key Component.

		:param TEKNode tek_parent: A TEK Component.
		:param pm.nt.Attribute drive_attr: Object and attribute that will drive another object.
		:param pm.nt.PyNode driven_obj: Object that will be driven by another object.
		:param str side: The side in which the component is on the body.
		:param str region: The name of the region.  EX: "Arm"
		:param dict driven_attrs: driven_attrs['start']={'tx': value}, driven_attrs['end']={'tx': value}
		:return: Returns an instance of SingleSDKComponent.
		:rtype: SingleSDKComponent
		"""
		
		# Set Namespace
		root_namespace = tek_parent.namespace().split(':')[0]
		pm.namespace(set=f'{root_namespace}:')
		
		node = tek_base.TEKNode.create(tek_parent,
											SingleSDKComponent.__name__,
											SingleSDKComponent.VERSION)
		node.rename('{0}_{1}_{2}'.format(node, side, region))
		
		ori_driven_value = drive_attr.get()
		anim_curves = []
		drive_attr.set(drive_attr_values[0])
		for attr, value in driven_attrs['start'].items():
			driven_attr = pm.PyNode(driven_obj.attr(attr))
			driven_attr.set(round(value, 3))
			pm.setDrivenKeyframe(driven_attr, currentDriver=drive_attr)
			anim_curve = driven_attr.listConnections()
			if anim_curve:
				anim_curves.append(anim_curve[0])
		
		drive_attr.set(drive_attr_values[1])
		for attr, value in driven_attrs['end'].items():
			driven_attr = pm.PyNode(driven_obj.attr(attr))
			driven_attr.set(round(value, 3))
			pm.setDrivenKeyframe(driven_attr, currentDriver=drive_attr)
			anim_curve = driven_attr.listConnections()
			if anim_curve:
				anim_curves.append(anim_curve[0])
		
		drive_attr.set(ori_driven_value)
		
		# Add Attributes
		start_driven_len = len(driven_attrs['start'].keys())
		node.addAttr('drivenStartAttrs', numberOfChildren=start_driven_len, attributeType='compound', multi=False)
		for attr, value in driven_attrs['start'].items():
			node.addAttr('drivenStartAttr_{0}'.format(attr), dt='string', parent='drivenStartAttrs')
		for attr, value in driven_attrs['start'].items():
			node.drivenStartAttrs.attr('drivenStartAttr_{0}'.format(attr)).set('{0}'.format(value))
		
		end_driven_len = len(driven_attrs['end'].keys())
		node.addAttr('drivenEndAttrs', numberOfChildren=end_driven_len, attributeType='compound', multi=False)
		for attr, value in driven_attrs['end'].items():
			node.addAttr('drivenEndAttr_{0}'.format(attr), dt='string', parent='drivenEndAttrs')
		for attr, value in driven_attrs['end'].items():
			node.drivenEndAttrs.attr('drivenEndAttr_{0}'.format(attr)).set('{0}'.format(value))
		
		# Connect Nodes
		node.addAttr('driver', dt='string')
		node.driver.set(drive_attr.nodeName().split(':')[-1])
		node.connect_node(driven_obj, 'driven', parent_attr='SDK_Parent')
		if anim_curves:
			anim_curves = list(set(anim_curves))
			node.connect_nodes(anim_curves, 'animCurves', 'tekParent')
		
		return node
	
	


