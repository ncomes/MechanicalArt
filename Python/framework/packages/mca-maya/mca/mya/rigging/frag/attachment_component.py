#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""
# System global imports
from __future__ import print_function, division, absolute_import
# Software specific imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.mya.utils import groups

# Internal module imports
from mca.mya.rigging.frag import frag_base, frag_rig

logger = log.MCA_LOGGER


class AttachmentComponent(frag_base.FRAGNode):
	VERSION = 1
	
	@staticmethod
	def create(frag_parent,
				side,
				region,
				source_component,
				attachment_point,
				target_frag_root,
				translate=True,
				rotate=True,
				snap=True,
				**kwargs):
		"""
		Creates an Attachment Component.  Connects a rig to another rig at a given node.

		:param FRAGNode frag_parent: FRAG Rig FRAGNode.
		:param str side: The side in which the component is on the body.
		:param str region: The name of the region.  EX: "Arm"
		:param FRAGNode source_component: A Frag Component.
		:param FRAGNode attachment_point: The node where the rig gets attached.
		:param frag_base.FRAGRoot target_frag_root: The rig root that gets driven.
		:param bool translate: Allows the target object to be driven by translate.
		:param bool rotate: Allows the target object to be driven by rotate.
		:return: Returns the AttachmentComponent component.
		:rtype: AttachmentComponent
		"""
		
		t = kwargs.get('t', translate)
		r = kwargs.get('r', rotate)
		
		target_frag_root = frag_base.FRAGNode(target_frag_root)
		
		node = frag_base.FRAGNode.create(frag_parent,
											AttachmentComponent.__name__,
											version=AttachmentComponent.VERSION)
		node.rename('{0}_{1}_{2}'.format(AttachmentComponent.__name__, side, region))
		
		target_frag_rig = target_frag_root.get_frag_children(of_type=frag_rig.FRAGRig)
		if not target_frag_rig:
			logger.warning('The source rig has no Frag Rig Component.')
			return
		target_frag_rig = target_frag_rig[0]
		
		target_flags_all = target_frag_rig.flags_all
		
		# Add a attachment group above the flags_all grp
		target_parent = groups.create_aligned_parent_group(target_flags_all,
															suffix='attachment_transform',
															attr_name='attachmentTransform',
															obj_attr='attachmentTransform',
															orient_obj=None)
		
		# Attach to the grp
		if t:
			pm.pointConstraint(attachment_point, target_parent, w=True, mo=not snap)
		if r:
			pm.orientConstraint(attachment_point, target_parent, w=True, mo=not snap)
		# Connect components
		node.connect_node(target_parent, 'targetParent', 'fragParent')
		node.connect_nodes(target_flags_all, 'targetFlagsAll', parent_attr='attachementComponent')
		node.connect_node(source_component, 'sourceComponent', parent_attr='sourceAttachement')
	
		return node
	
	