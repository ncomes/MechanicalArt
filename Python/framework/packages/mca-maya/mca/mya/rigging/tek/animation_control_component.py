#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

from __future__ import print_function, division, absolute_import

import pymel.core as pm

from mca.mya.rigging.tek import rig_component
from mca.mya.utils import attr_utils


class animationControlComponent(rig_component.RigComponent):
	
	@staticmethod
	def create(tek_parent, tek_type, version, side, region, align_component=None):
		"""

		:param tek_parent:
		:param tek_type:
		:param version:
		:param side:
		:param region:
		:param align_component:
		:return:
		"""
		node = rig_component.RigComponent.create(tek_parent,
													tek_type,
													version,
													side=side.lower(),
													region=region,
													align_component=align_component)
		flag_group = pm.group(empty=1, n="flags_{0}_{1}".format(side, region))
		if align_component:
			pm.delete(pm.parentConstraint(align_component, flag_group))
		pm.makeIdentity(flag_group, apply=1, t=1, r=1, s=1)
		# Add Attributes and connect attributes
		node.connect_node(flag_group, 'flagGroup', 'tekParent')
		if tek_parent.get_type() == "TEKRig":
			flag_group.setParent(tek_parent.flagsAll.get())
		return node
	
	@property
	def flag_group(self):
		return self.flagGroup.get()
	
	def attach_to_skeleton(self):
		# should return [flag(s), constraints]
		raise NotImplementedError()
	
	def attach_component(self, other_component, parent_object, point=True, orient=True):
		# Get local level groups
		flag_grp = self.flagGroup.get()
		nt_grp = self.noTouch.get()
		
		_attrs = nt_grp.translate.children() + nt_grp.rotate.children()
		attr_utils.unlock_and_show_attrs(_attrs)
		
		if point:
			pm.parentConstraint(parent_object, flag_grp, w=1, mo=1, skipRotate = ["x","y","z"])
			pm.parentConstraint(parent_object, nt_grp, w=1, mo=1, skipRotate = ["x","y","z"])
			
			other_component.attachedComponents >> self.pointAttachComponent
			self.pointAttachLocation.set(parent_object)
		
		if orient:
			pm.parentConstraint(parent_object, flag_grp, w=1, mo=1, skipTranslate = ["x","y","z"])
			pm.parentConstraint(parent_object, nt_grp, w=1, mo=1, skipTranslate = ["x","y","z"])
			
			other_component.attachedComponents >> self.orientAttachComponent
			self.pointAttachLocation.set(parent_object)
		attr_utils.lock_and_hide_object_attrs(_attrs)
