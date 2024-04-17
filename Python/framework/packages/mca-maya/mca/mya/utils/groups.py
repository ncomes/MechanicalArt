#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# Software specific imports
import pymel.core as pm
#  python imports
from mca.mya.utils import naming
from mca.mya.utils import attr_utils


def create_aligned_parent_group(obj, suffix='', attr_name='alignTransform', obj_attr='alignObject', orient_obj=None):
	"""
	Creates a transform at the given object's location then parents the object to that transform to effectively
	"zero out" all transformation attributes. If a align transform already exists for the object then return it.

	:param pm.nt.Transform obj: Transform to create the align group node.
	:param str suffix: added suffix to the group name.
	:param str attr_name: Name of the attribute to be added.
	:return: Newly created or existing align transform.
	:rtype: nt.Transform
	"""
	
	if suffix != '':
		suffix = '_' + suffix
	
	obj = pm.PyNode(obj)
	transform = pm.group(empty=True, n=naming.get_basename(obj) + suffix)
	if obj.hasAttr('rotateOrder'):
		transform.rotateOrder.set(obj.rotateOrder.get())
	pm.delete(pm.parentConstraint(obj, transform, w=1, mo=False))
	if orient_obj:
		pm.delete(pm.orientConstraint(orient_obj, transform, w=1, mo=False))
	object_parent = obj.getParent()
	if object_parent:
		transform.setParent(object_parent)
	obj.setParent(transform)
	if isinstance(obj, pm.nodetypes.Joint):
		obj.jointOrient.set([0, 0, 0])
	if not obj.hasAttr(attr_name):
		obj.addAttr(attr_name, at='message')
	transform.addAttr(obj_attr, dt='string')
	transform.attr(obj_attr) >> obj.attr(attr_name)
	
	return transform


def create_aligned_child_group(obj, suffix='', attr_name='childGrpTransform', obj_attr='childGrpObject'):
	obj = pm.PyNode(obj)
	if suffix != '':
		suffix = '_' + suffix
	
	transform = pm.group(empty=True, n=naming.get_basename(obj) + suffix)
	if obj.hasAttr('rotateOrder'):
		transform.rotateOrder.set(obj.rotateOrder.get())
	pm.delete(pm.parentConstraint(obj, transform, w=1, mo=False))
	pm.parent(transform, obj)
	if not obj.hasAttr(attr_name):
		obj.addAttr(attr_name, at='message')
	transform.addAttr(obj_attr, dt='string')
	transform.attr(obj_attr) >> obj.attr(attr_name)
	
	return transform


def transform_scale(align_grp, flag_node, translate_scale=(1, 1, 1)):
	"""
	Scales the group node above the flag so the movement is scaled.

	:param pm.nt.Group align_grp: Alignment group above the flag.
	:param flag.Flag flag_node:  The animation control.
	:param list(float) translate_scale: scale the group and flag by the number in x,y,z.
	"""
	
	attr_utils.unlock_and_show_attrs(flag_node.scale.children())
	
	align_grp.scaleX.set(1.0 / translate_scale[0])
	align_grp.scaleY.set(1.0 / translate_scale[1])
	align_grp.scaleZ.set(1.0 / translate_scale[2])
	flag_node.scaleX.set(translate_scale[0])
	flag_node.scaleY.set(translate_scale[1])
	flag_node.scaleZ.set(translate_scale[2])
	
	flag_node.sx.lock()
	flag_node.sx.set(keyable=False, channelBox=False)
	flag_node.sy.lock()
	flag_node.sy.set(keyable=False, channelBox=False)
	flag_node.sz.lock()
	flag_node.sz.set(keyable=False, channelBox=False)


