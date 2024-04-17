#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a camera component for a camera rig.
"""

# system global imports
from __future__ import print_function, division, absolute_import
# Software specific imports

# mca Python imports
from mca.mya.modifiers import ma_decorators
from mca.common import log
from mca.mya.utils import constraint, namespace
from mca.mya.rigging.tek import fk_component

logger = log.MCA_LOGGER


class CameraComponent(fk_component.FKComponent):
	LATEST_VERSION = 1

	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(tek_parent,
	           joint,
	           side,
	           region,
	           cam):
		"""
		Creates a Camera Component

		:param tek_parent: TEK Rig TEKNode.
		:param pm.nt.Joint joint: joint which will be controlled
		:param str side: component side
		:param str region: component region
		:param pm.nt.Transform cam: Camera to rig.
		:return: Returns an instance of CameraComponent
		:rtype: CameraComponent
		"""

		# Set Namespace
		root_namespace = tek_parent.namespace().split(':')[0]
		namespace.set_namespace(root_namespace, check_existing=False)
		node = fk_component.FKComponent.create(tek_parent=tek_parent,
		                                       start_joint=joint,
		                                       end_joint=joint,
		                                       side=side,
		                                       region=region,
		                                       lock_child_translate_axes=(),
		                                       lock_root_translate_axes=())
		new_name = '{0}_{1}_{2}'.format(CameraComponent.__name__, side, region)
		node.rename(new_name)
		node.set_version(CameraComponent.LATEST_VERSION)
		node.tekType.set(CameraComponent.__name__)

		# Get flags
		flag = node.get_start_flag()
		cam_con = constraint.parent_constraint_safe(flag, cam, mo=True)

		node.connect_node(cam, 'cam', 'tekParent')
		node.connect_node(cam_con, 'constraints', 'tekParent')

		return node

	def get_cam_flag(self):
		"""
		Returns the camera flag for the camera component.

		:return: Returns the camera flag for the camera component.
		:rtype: pm.nt.Transform
		"""
		cam_flag = self.get_flags()
		if not cam_flag:
			return None
		return cam_flag[0]

	def get_cam(self):
		"""
		Returns the camera for the camera component.

		:return: Returns the camera for the camera component.
		:rtype: pm.nt.Transform

		"""

		cam = self.pynode.cam.listConnections()
		if not cam:
			return None
		return cam[0]
