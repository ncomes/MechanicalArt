#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
purpose: Saves animated curves.  Disconnects them from objects and connects them to compound attributes.
THIS IS MEANT TO BE A FAST WAY TO TRANSFER ANIMATION.  IT SHOULD NOT HAVE TOO MANY CHECKS OR ACCOUNT FOR EVERY VARIABLE.
"""

# system global imports
# software specific imports
import pymel.core as pm
import maya.cmds as cmds

# mca python imports
from mca.common import log
from mca.common.utils import lists
from mca.mya.utils import attr_utils, naming
from mca.mya.animation import anim_curves, anim_layers
from mca.mya.modifiers import ma_decorators

# internal module imports
from mca.mya.rigging.frag import frag_base

logger = log.MCA_LOGGER


class AnimatedCurvesComponent(frag_base.FRAGNode):
	VERSION = 1

	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(frag_parent):
		"""
		Creates the animatedCurveData Frag Node.
		
		:param frag_rig.FragRig frag_parent: The Frag Node that this node will be connected to.
		:return Returns an instance AnimatedCurvesComponent:
		"""
		
		# Set Namespace
		root_namespace = frag_parent.namespace().split(':')[0]
		pm.namespace(set=f'{root_namespace}:')

		node = frag_base.FRAGNode.create(frag_parent,
											frag_type=AnimatedCurvesComponent.__name__,
											version=AnimatedCurvesComponent.VERSION)

		node.addAttr('animatedCurveData', at="message")
		node.addAttr('animationLayers', dt="string")
		node.addAttr('startFrame', at='float', dv=0.0)
		node.addAttr('endFrame', at='float', dv=0.0)

		return node

	def restore_curves_from_skeleton(self, flags,
											force_unlock=True,
											keep_curves=True,
											delete_old_curves=True,
											start_time=None):
		"""
		Restores curves connected to joints back to flags on another rig.
		
		:param bool force_unlock: If True it will unlock attributes and add the connect the animation curve.
		:param bool keep_curves: If True the animation curves will be duplicated stay connected.
		"""
		
		if not self.is_connected_to_skeleton():
			logger.warning('There is no animatedCurveData node connected to the world root joint.')
			return

		if not isinstance(flags, list):
			flags = [flags]

		self.restore_all_animation_curves(obj_list=flags,
											force_unlock=force_unlock,
											keep_curves=keep_curves,
											delete_old_curves=delete_old_curves,
											start_time=start_time)

	def restore_all_animation_curves(self, obj_list,
							force_unlock=True,
							keep_curves=False,
							delete_old_curves=True,
							start_time=None):
		"""
		Transfers curves connected to the node to an objects with the same attributes.
		
		:param list[pm.nt.transform] obj_list: List of objects that will receive animation curves.
		:param bool force_unlock: If True it will unlock attributes and add the connect the animation curve.
		:param bool keep_curves: If True the animation curves will be duplicated stay connected.
		:param bool delete_old_curves: If True, The curves on the object being transferred to will be deleted.
		:param float start_time: The time the animation should start.
		"""
		
		if not isinstance(obj_list, list):
			obj_list = [obj_list]

		for obj in obj_list:
			self.restore_animation_curves(obj=obj,
											force_unlock=force_unlock,
											keep_curves=keep_curves,
											delete_old_curves=delete_old_curves,
											start_time=start_time)

		if isinstance(start_time, int) and start_time != self.startFrame.get():
			self.startFrame.set(start_time)

	def restore_animation_curves(self, obj,
							force_unlock=True,
							keep_curves=False,
							delete_old_curves=True,
							start_time=None):
		"""
		Transfers animation curves back to an object.
		
		:param pm.nt.transform obj: An obj that animation curves will be transferred to.
		:param bool force_unlock: If True it will unlock attributes and add the connect the animation curve.
		:param bool keep_curves: If True the animation curves will be duplicated stay connected.
		:param bool delete_old_curves: If True, The curves on the object being transferred to will be deleted.
		:param float start_time: The time the animation should start.
		"""
		
		# Find the compound attribute associated with that object.
		sub_attrs = self._get_compound_attributes(obj)
		if not sub_attrs:
			return

		obj_name = naming.get_basename(obj)

		# get the corrected/true names from the compound attribute.  This is the original attribute from the
		# original object.  EX: was - f_nose_null_translateX and is now - f_nose_null.translateX
		sub_attr_names = self._correct_attribute_names(obj_name=obj_name, attributes=sub_attrs)

		# Get the name of all the attributes from the node that have animation curves attached.
		node_attributes = sorted(self.get_attributes_with_curves(obj, sub_attr_names))
		# get a list of all the object/flag attributes that we need to attach curves to.
		object_attributes = sorted(obj.attr(x) for x in sub_attr_names.values() if obj.hasAttr(x))

		# Unlock object attributes if they are locked.
		if force_unlock:
			attr_utils.unlock_and_show_attrs(object_attributes)

		if not object_attributes:
			logger.warning('The are no object attributes that can have animation curves.')
			return
		for x, node_attr in enumerate(node_attributes):
			# Make sure we do not get out of sync.
			if x == len(object_attributes):
				logger.warning('The attribute list is at the same length as the number of object attributes.')
				break
			# Get the curve for that animatedcurvedata(self) node compound attribute.
			anim_curve = node_attr.listConnections(s=True, d=False)
			if not anim_curve:
				continue
			anim_curve = lists.get_first_in_list(list(set(anim_curve)))
			if isinstance(start_time, int) and float(self.pynode.getAttr('startFrame')) != float(start_time):
				start_time = self.get_start_time_diff(start_time=start_time)
			end_frame = None
			if isinstance(anim_curve, pm.nt.AnimCurve):
				end_frame = anim_curves.restore_from_anim_curves(anim_curve=anim_curve,
														object_attribute=object_attributes[x],
														keep_curves=keep_curves,
														delete_old_curves=delete_old_curves,
														start_time=start_time)
				if not keep_curves:
					pm.disconnectAttr(node_attr)

			elif isinstance(anim_curve, pm.nt.AnimBlendNodeBase) or isinstance(anim_curve, list):
				end_frame = anim_layers.restore_for_anim_layers(anim_blend=anim_curve,
																	object_attribute=object_attributes[x],
																	keep_curves=keep_curves,
																	delete_old_curves=delete_old_curves,
																	start_time=start_time)
				anim_layer_list = self.pynode.animationLayers.listConnections()
				[pm.disconnectAttr(x.animatedCurveData) for x in anim_layer_list]
				pm.disconnectAttr(node_attr)
			if end_frame and end_frame > self.endFrame.get():
				self.endFrame.set(end_frame)

	def get_start_time_diff(self, start_time):
		"""
		Updates the time range on an animation curve.
		
		:param float start_time: where the timeline should start.
		"""
		
		anim_start_time = self.pynode.getAttr('startFrame')
		if float(anim_start_time) == float(start_time):
			logger.warning("Start Time and the Curve's start is the same.  Nothing to change.")
			return
		start_diff = start_time - anim_start_time
		return start_diff

	def get_attributes_with_curves(self, obj, sub_attr_names):
		"""
		Returns a list of attributes that have animation curves attached.
		
		:param obj: The object that animation curves will be transferred to.
		:param dict sub_attr_names: dictionary of attribute names that are on the node and the correct name
		that is used to reconnect to the object.
		:return: Returns a list of attributes that have animation curves attached.
		:rtype: List[pm.nt.transform]
		"""
		
		compound_attr = []
		for node_attr, obj_attr in sub_attr_names.items():
			if obj.hasAttr(obj_attr):
				compound_attr.append(node_attr)
		node_attributes = []
		for attr in compound_attr:
			attr = self.pynode.attr(attr)
			anim_curve = attr.listConnections()
			if anim_curve and isinstance(anim_curve[0], (pm.nt.AnimCurve, pm.nt.AnimBlendNodeBase)):
				node_attributes.append(attr)
		return node_attributes

	def _correct_attribute_names(self, obj_name, attributes):
		"""
		Removes the object name that gets prefixed onto the attributes.  This from the default process from creating
		the compound attributes.
		
		:param string obj_name: name of the object.
		:param list[string] attributes: list of attributes on the node.
		:return: Returns a dictionary of the old attribute names and the corrected ones.
		:rtype: dict{string:string}
		"""
		attribute_names = {}
		for attr in attributes:
			if obj_name in attr:
				attr_name = attr.replace(obj_name+'_', '')
				attribute_names[attr] = attr_name
		return attribute_names

	def _get_compound_attributes(self, obj):
		"""
		Returns the sub attributes in the compound attribute that the restore curves process needs.
		
		:param pm.nt.transform obj: The object that animation curves will be transferred to.
		:return: Returns the sub attributes in the compound attribute that the restore curves process needs.
		:rtype: list[pm.nt.Attribute]
		"""
		
		obj_name = naming.get_basename(obj)
		if not self.hasAttr(obj_name):
			return
		compound_attr = self.attr(obj_name)
		sub_attrs = [x for x in pm.listAttr(compound_attr) if 'hidden' not in str(x).split('_')[-1]]
		compound_attributes = [x for x in sub_attrs if not str(x) == obj_name]
		return compound_attributes

	@ma_decorators.undo_decorator
	def store_curves_on_skeleton(self, skeleton_root, keep_animation=True):
		"""
		Connects the node to a skeleton root.
		
		:param pm.nt.Joint skeleton_root:  The root_joint to a skeleton.
		:param bool keep_animation: If True, the animation curves are duplicated before adding to the node.
		"""
		
		control_rig = frag_base.get_frag_parent(self)
		if not control_rig:
			raise RuntimeError('No Control Rig was found connected to the AnimatedCurve node.')

		skeleton_root = pm.PyNode(skeleton_root)
		# Move the node to the same namespace as the skeleton root.
		nsp = skeleton_root.namespace()
		ns = self.namespace()
		new_name = self.replace(ns, nsp)
		pm.rename(self, new_name)

		# Go through each flag as create compound attrs and attach animated curves to them.
		flags = control_rig.get_flags()
		all_flags = []
		for flag in flags:
			flag_count = self.store_animation_curves(flag, keep_animation)
			if flag_count:
				all_flags.append(flag_count)
		if all_flags:
			# Connect node to the skeleton_root.
			if not skeleton_root.hasAttr('animatedCurveData'):
				skeleton_root.addAttr('animatedCurveData', at="message")
			if not self.pynode.hasAttr('animatedCurveData'):
				self.pynode.addAttr('animatedCurveData', at="message")
			# disconnect the node from the control rig and anything else it is connected to so we can connect it
			# to the skeleton root.
			pm.disconnectAttr(self.pynode.animatedCurveData)
			pm.disconnectAttr(self.pynode.fragParent)
			# Connecting node on both side so when you delete the skeleton, it deletes this node.
			# Also prevents the re-animator process from deleting the node.
			self.animatedCurveData >> skeleton_root.animatedCurveData
			skeleton_root.animatedCurveData >> self.animatedCurveData
		else:
			self.remove()

	@ma_decorators.undo_decorator
	def store_all_animation_curves(self, obj_list,
									keep_animation=True,
									min_time_range=None,
									max_time_range=None,
									merge_layers=False,
									start_time=None):
		"""
		Runs through all the objects on a rig and transfers the animation curves.
		
		:param list[pm.nt.transsform] obj_list: List of objects that have animation curves.
		:param bool keep_animation: If True, the animation curves are duplicated before adding to the node.
		:param int min_time_range: Any key before this number will be deleted.
		:param int max_time_range: Any key after this number will be deleted.
		"""
		
		all_objs = []
		# Go through each object as create compound attrs and attach animated curves to them.
		for obj in obj_list:
			obj_count = self.store_animation_curves(obj=obj,
											keep_animation=keep_animation,
											min_time_range=min_time_range,
											max_time_range=max_time_range,
											merge_layers=merge_layers,
											start_time=start_time)
			if obj_count:
				all_objs.append(obj_count)
		# if there were not animation curves on any of the objects.  Delete the node.
		if not all_objs:
			self.remove()

	def store_animation_curves(self,
								obj,
								keep_animation=True,
								min_time_range=None,
								max_time_range=None,
								merge_layers=False,
								start_time=None):
		"""
		Creates compound attributes associated with the objects and animation curves.
		This will disconnect the animation curve and connect them to the associated compound attribute.
		
		:param pm.nt.transform obj: An object that has animation curves.
		:param bool keep_animation: If True, the animation curves are duplicated before adding to the node.
		:param int min_time_range: Any key before this number will be deleted.
		:param int max_time_range: Any key after this number will be deleted.
		:return: The object that animation curves were transferred to.
		:rtype: pm.nt.transform
		"""
		
		# get the string name which is used for the compound attribute
		obj_name = naming.get_basename(obj)
		component = frag_base.get_frag_parent(obj)

		attr_curves = anim_layers.store_object_animation(obj,
														keep_animation=keep_animation,
														min_time_range=min_time_range,
														max_time_range=max_time_range,
														merge_layers=merge_layers,
														start_time=start_time)

		anim_layer_list = self.animationLayers.listConnections()
		animation_layers = [x for x in pm.ls(type=pm.nt.AnimLayer) if x.hasAttr('original_anim_layer')]
		for anim_layer in animation_layers:
			if anim_layer not in anim_layer_list:
				if not anim_layer.hasAttr('animatedCurveData'):
					anim_layer.addAttr('animatedCurveData', at="message")
				self.animationLayers >> anim_layer.animatedCurveData

		if not attr_curves:
			return

		for key_attr in attr_curves.keys():
			attr_curves[key_attr.replace('.', '_')] = attr_curves.pop(key_attr)

		for value_attr in attr_curves.values():
			if isinstance(value_attr, list):
				[self.set_start_frame(x.node(), min_time_range) for x in value_attr]
				[self.set_end_frame(x.node()) for x in value_attr]
			else:
				self.set_start_frame(value_attr.node(), min_time_range)
				self.set_end_frame(value_attr.node())

		# Record the component name.
		if component and attr_curves:
			attr_curves['component'] = naming.get_basename(component)

		# Creates the compound attribute and transfers the animation curves.
		attr_utils.set_compound_attribute_groups(self, obj_name, attr_curves)
		return obj

	def set_start_frame(self, anim_curve, min_time_range=None):
		"""
		Checks and sets the start value if needed.
		
		:param pm.nt.AnimCurve anim_curve: The animation curve to evaluate.
		:param int min_time_range: Any key before this number will be deleted.
		:return: Returns the 1st key in the animation curve.
		:rtype: int
		"""
		
		key_time = pm.keyframe(anim_curve, q=True)
		if not key_time:
			return
		if key_time[0] < self.startFrame.get() or (min_time_range and self.startFrame.get() < min_time_range):
			self.startFrame.set(key_time[0])
		return key_time[0]

	def set_end_frame(self, anim_curve):
		"""
		Checks and sets the end value if needed.
		
		:param pm.nt.AnimCurve anim_curve: The animation curve to evaluate.
		:return: Returns the last key in the animation curve.
		:rtype: int
		"""
		
		key_time = pm.keyframe(anim_curve, q=True)
		if not key_time:
			return
		if key_time[-1] > self.endFrame.get():
			self.endFrame.set(key_time[-1])
		return key_time[-1]

	def is_connected_to_skeleton(self):
		"""
		Checks if the node is connected to the skeleton.
		"""
		
		if self.animatedCurveData.listConnections():
			return True
		return False

	def remove(self):
		"""
		Deletes the AnimatedCurveNode.
		"""
		
		pm.delete(self.pynode)

	@classmethod
	def import_animated_curve_data(cls, full_path):
		"""
		Imports a file with the exported curves and returns the animatedCurveData node.
		
		:param string full_path: File directory.
		:return: Returns the animatedCurveData node
		:rtype: animatedCurveData
		"""
		
		# import the file and find the animatedCurveData node.
		import_files = pm.importFile(full_path, returnNewNodes=True)
		curve_data = [x for x in import_files if x.hasAttr('animatedCurveData')]
		if not curve_data:
			return
		return cls(curve_data[0])

	def export(self, full_path):
		"""
		Export the animation curves.
		
		:param string full_path: folder path to export
		"""
		
		if not '.mb' in full_path and not '.ma' in full_path:
			raise ValueError('File type must be a .mb, .ma')

		# remove any namespaces
		ns = self.namespace()
		if ns:
			new_name = self.replace(ns, ':')
			pm.rename(self, new_name)
		if self.pynode.fragParent.listConnections():
			pm.disconnectAttr(self.pynode.fragParent)
		pm.parent(self, w=True)
		scene_name = pm.sceneName()
		# select the node and export
		pm.select(self)
		if '.ma' in full_path:
			cmds.file(rename=full_path)
			cmds.file(force=True, exportSelected=True, type="mayaAscii")
		else:
			cmds.file(rename=full_path)
			cmds.file(force=True, exportSelected=True, type="mayaBinary")

		cmds.file(rename=scene_name)

