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
from mca.mya.rigging import space_switch_rig
# Internal module imports
from mca.mya.rigging.tek import tek_base


class SpaceSwitchComponent(tek_base.TEKNode):
	VERSION = 1
	
	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(tek_parent,
				side,
				region,
				source_object,
				target_list,
				switch_obj=None,
				translate=True,
				rotate=True,
				switch_attr='follow',
				**kwargs):
		
		"""
		Creates a Multi Constraint Component.  Allows an object to switch constraints between multiple objects.

		:param TEKNode tek_parent: TEK Rig TEKNode.
		:param str side: The side in which the component is on the body.
		:param str region: The name of the region.  EX: "Arm"
		:param pm.nt.transform source_object: The object that will be driven.
		:param list(pm.nt.transform) target_list: The objects that will be driving the source object.
		:param bool translate: Allows the source object to be driven by translate.
		:param bool rotate: Allows the source object to be driven by rotate.
		:param str switch_attr: Name of the switch attribute.
		:return: Returns the MultiConstraint component.
		:rtype: SpaceSwitchComponent
		"""
		
		t = kwargs.get('t', translate)
		r = kwargs.get('r', rotate)
		
		# Set Namespace
		root_namespace = tek_parent.namespace().split(':')[0]
		pm.namespace(set=f'{root_namespace}:')
		
		node = tek_base.TEKNode.create(tek_parent,
											SpaceSwitchComponent.__name__,
											version=SpaceSwitchComponent.VERSION)
		node.rename('{0}_{1}_{2}'.format(SpaceSwitchComponent.__name__, side, region))
		
		if not switch_obj:
			switch_obj = source_object
		
		# Create the multiconstraint.
		result_space = space_switch_rig.space_switch(target_list=target_list,
														source_object=source_object,
														switch_obj=switch_obj,
														translate=t,
														rotate=r,
														switch_attr=switch_attr,
														default_name=kwargs.get('default_name', None))
		# Add attrs
		if not node.has_attribute('switchAttrName'):
			node.addAttr('switchAttrName', dt='string')
		node.switchAttrName.set(switch_attr)
		
		# Set results
		point_constraints = result_space['point_constraints']
		orient_constraints = result_space['orient_constraints']
		conditions = result_space['conditions']
		switch_offset_grp = result_space['switch_offset_grp']
		
		# Connect all the nodes
		node.connect_node(switch_offset_grp, "switchGroup", 'tekParent')
		node.connect_node(source_object, 'sourceObject', parent_attr="sourceSpaceConstraint")
		node.connect_node(switch_obj, 'switchObject', parent_attr="switchObject")
		
		node.connect_nodes(point_constraints, 'pointConstraints', 'tekParent')
		node.connect_nodes(orient_constraints, 'orientConstraints', 'tekParent')
		node.connect_nodes(conditions, 'conditions', 'tekParent')
		
		return node
	
	@property
	def point_constraints(self):
		"""
		Returns the point constraints.

		:return: Returns the point constraints.
		:rtype: list(pm.nt.pointConstraint)
		"""
		
		return self.pointConstraints.get()
	
	@property
	def orient_constraints(self):
		"""
		Returns the orient constraints.

		:return: Returns the orient constraints.
		:rtype: list(pm.nt.orientConstraint)
		"""
		
		return self.orient_constraints.get()
	
	@property
	def switch_attr(self):
		"""
		Returns switch attr.

		:return: Returns switch attr.
		:rtype: str
		"""
		
		return self.switchAttrName.get()
	
	@property
	def conditions(self):
		"""
		Returns the condition nodes.

		:return: Returns the condition nodes.
		:rtype: list(pm.nt.Condition)
		"""
		
		return self.conditions.get()
	
	@property
	def source_object(self):
		"""
		Returns the source object.  The object being driven.

		:return: Returns the source object.  The object being driven.
		:rtype: pm.nt.Transform
		"""
		
		return self.sourceObject.get()
	
	@property
	def switch_object(self):
		"""
		Returns the switch object.  The object that has the attributes applied.

		:return: Returns the switch object.  The object that has the attributes applied.
		:rtype: pm.nt.Transform
		"""
		
		return self.switchObject.get()
