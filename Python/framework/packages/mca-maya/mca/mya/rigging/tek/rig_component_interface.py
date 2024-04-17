#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import abc
# Internal module imports
from mca.mya.rigging.tek import tek_base


class RigComponentInterface(tek_base.TEKNode):
	
	@abc.abstractmethod
	def remove(self, bake=False):
		"""
		remove everything about this rig implementation
		"""
		
		raise NotImplementedError()
	
	@abc.abstractmethod
	def bake(self):
		"""
		bake the rig down to its base joint structure
		"""
		
		raise NotImplementedError()
	
	@abc.abstractmethod
	def get_bind_joints(self):
		"""
		get the base joint structure
		"""
		
		raise NotImplementedError()
	
	@abc.abstractmethod
	def attach_to_skeleton(self, skeleton):
		raise NotImplementedError()
	
	@abc.abstractmethod
	def to_default_pose(self):
		"""
		moves the rig implementation back to the default pose
		"""
		
		raise NotImplementedError()
	
	@abc.abstractmethod
	def get_component(self, side, region):
		"""
		return the component that matches side and type
		"""
		
		raise NotImplementedError()