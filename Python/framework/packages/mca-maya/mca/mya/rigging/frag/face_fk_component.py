#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
purpose: single fk component. Single joint with translate and rotation options available
"""

# system global imports
from __future__ import print_function, division, absolute_import
# Software specific imports
import pymel.core as pm

# mca Python imports
from mca.mya.utils import attr_utils, groups
from mca.mya.modifiers import ma_decorators
from mca.mya.modeling import vert_utils, rivets
from mca.mya.animation import anim_curves
from mca.mya.animation import time_utils
from mca.common import log

# internal module imports
from mca.mya.rigging.frag import fk_component

logger = log.MCA_LOGGER


class FaceFKComponent(fk_component.FKComponent):
	LATEST_VERSION = 1
	
	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(frag_parent,
				joint,
				side,
				region,
				flag_scale=1,
				limit_point=((None, None), (None, None), (None, None)),
				limit_orient=((None, None), (None, None), (None, None)),
				translate_scale=(10, 10, 10),
				*args,
				**kwargs):
		"""
		Creates a Face FK Component

		:param frag_parent: FRAG Rig FRAGNode.
		:param pm.nt.Joint joint: joint which will be controlled
		:param str side: component side
		:param str region: component region
		:param flag_scale: Scale factor for flag shapes
		:param limit_point:  [(tx_min, tx_max), (ty_min, ty_max), (tz_min, tz_max)], control for setting up limits when rigged
		:param limit_orient: [(rx_min, rx_max), (ry_min, ry_max), (rz_min, rz_max)], control for setting up limits when rigged
		:param translate_scale: [tx_scale, ty_scale, tz_scale]  scale the translate amount to appear different, example if [10,10,10] translate 0-10 appears to move only from 0-1
		:return: Returns an instance of FaceFKComponent
		:rtype: FaceFKComponent
		"""
		
		# Set Namespace
		root_namespace = frag_parent.namespace().split(':')[0]
		pm.namespace(set=':')
		if root_namespace != '':
			pm.namespace(set=f'{root_namespace}:')
		
		node = fk_component.FKComponent.create(frag_parent=frag_parent,
												start_joint=joint,
												end_joint=joint,
												side=side,
												region=region,
												scale=flag_scale,
												lock_child_translate_axes=(),
												lock_root_translate_axes=(),
												*args,
												**kwargs)
		new_name = '{0}_{1}_{2}'.format(FaceFKComponent.__name__, side, region)
		node.rename(new_name)
		node.set_version(FaceFKComponent.LATEST_VERSION)
		node.fragType.set(FaceFKComponent.__name__)
		
		# Get flag
		face_flag = node.get_start_flag()
		align_grp = face_flag.alignTransform.get()
		
		flag = node.get_start_flag()
		if flag:
			flag.addAttr('flag_follow', at='message')
			align_transform = flag.get_align_transform()
			follow_grp = pm.group(em=True, n=flag.nodeName() + '_flag_follow')
			follow_grp.addAttr('flag_follow', at='message')
			follow_grp.flag_follow >> flag.flag_follow
			pm.parent(follow_grp, align_transform)
			follow_grp.translate.set(0, 0, 0)
			follow_grp.rotate.set(0, 0, 0)
			pm.parent(flag, follow_grp)
		
		attr_utils.set_limits(rig_flag=face_flag,
									rig_node=node,
									limit_point=limit_point,
									limit_orient=limit_orient)
		
		groups.transform_scale(align_grp=align_grp,
								flag_node=face_flag,
								translate_scale=translate_scale)
		
		# add face parameter info
		node.addAttr('parameters', numberOfChildren=6, attributeType='compound', multi=True)
		node.addAttr('parameter', dt='string', parent='parameters')
		node.addAttr('controlStart', at='float', parent='parameters')
		node.addAttr('controlEnd', at='float', parent='parameters')
		node.addAttr('controlAttr', attributeType='message', parent='parameters')
		node.addAttr('faceParameters', attributeType='message', parent='parameters')
		node.addAttr('poseFrame', at='float', parent='parameters')
		node.addAttr('isFragFace', at='bool', dv=True)
		
		if not node.hasAttr('message'):
			node.addAttr('message', attributeType='message')
		
		return FaceFKComponent(node)
	
	def get_flag_attr(self, pose_name):
		"""
		
		:param str pose_name: name of the pose.
		:return: Returns the flag attribute the pose is connected.
		:rtype: pm.nt.general.Attribute
		"""
		
		flag_attr = self.attr(pose_name).controlAttr.listConnections(plugs=True)
		if not flag_attr:
			return
		return flag_attr[0]
		
	
	def get_min_pose_value(self, pose_name):
		"""
		Returns the min rotation value of a pose.
		
		:param str pose_name: name of the pose.
		:return: Returns the min rotation value of a pose.
		:rtype: float
		"""
		
		min_val = None
		if self.pynode.hasAttr(pose_name):
			block = self.pynode.attr(pose_name)
			min_val = block.controlStart.get()
		return min_val

	def get_max_pose_value(self, pose_name):
		"""
		Returns the max rotation value of a pose.
		
		:param string pose_name: name of the pose.
		:return: Returns the max rotation value of a pose.
		:rtype: float
		"""
		
		max_val = None
		if self.pynode.hasAttr(pose_name):
			block = self.pynode.attr(pose_name)
			max_val = block.controlEnd.get()
		return max_val
	
	def keyframe_flags_max_values(self):
		"""
		Sets a keyframe for the pose on the max value on the correct pose frame.
		"""
		
		num_elements = self.pynode.parameters.numElements()
		for x in range(num_elements):
			pose_name = self.pynode.parameters[x].parameter.get()
			max_value = self.get_max_pose_value(pose_name)
			attr_control = self.pynode.parameters[x].controlAttr.listConnections(p=True)[0]
			pose_frame = self.pynode.parameters[x].poseFrame.get()
			
			time_utils.set_padded_keys(obj_attr=attr_control, frame=pose_frame, value=max_value)
			
	def get_parameters_node(self, pose_name):
		"""
		Returns the parameters node that has all the pose values.
		
		:param str pose_name: name of the pose.
		:return: Returns the parameters node that has all the pose values.
		:rtype: FRAGFaceParameters
		"""
		
		parameters_node = None
		if self.pynode.hasAttr(pose_name):
			block = self.pynode.attr(pose_name)
			parameters_node = block.input.get()
		return parameters_node

	def _get_parameter(self, parameter_name):
		result = None
		if self.pynode.hasAttr(parameter_name):
			result = self.pynode.attr(parameter_name)
		return result

	def set_parameter(self, parameter_name, value, key=False):
		"""
		if possible sets the face_parameter to specified value,
		return None if not possible
		return value if possible.
		
		:param str parameter_name: Name of the pose.
		:param float value: value of the animated property
		:param bool key: if True, keys the parameter
		:return: Returns the value
		:rtype: float
		"""
		
		result = None

		matching_parameter = self._get_parameter(parameter_name)
		if matching_parameter:
			min = float(matching_parameter.controlStart.get())
			max = float(matching_parameter.controlEnd.get())
			remapped_value = ((max -min)+min)*value
			con  = matching_parameter.controlAttr.listConnections(s=1, d=0, p=1)
			if con:
				con[0].set(remapped_value)
				result = value
				if key:
					pm.setKeyframe(con[0])

		return result

	def get_range_values_from_flag(self):
		"""
		If there is a setRange node, this returns the min and max ranges.
		Example: {'translateX':[-10, 10]}
		
		:return: If there is a setRange node, this returns the min and max ranges.
		:rtype: dictionary
		"""
		
		flag = self.get_flags()[0]
		attributes = pm.listAnimatable(flag)
		ranges = {}
		for attr in attributes:
			attr_range = self.get_range_value(attr)
			if attr_range:
				attr = str(attr).split('.')[-1]
				ranges[str(attr)] = attr_range
		return ranges

	def get_range_value(self, attribute):
		"""
		Returns the min and max range of range nodes associated with an attribute.
		Example: [-10, 10]
		
		:param pm.nt.Attribute attribute: The attribute used to look for the ranges.
		:return: Returns the min and max range of range nodes associated with an attribute.
		:rtype: list(float)
		"""
		
		set_range = attribute.listConnections(type=pm.nt.SetRange, scn=True)
		if not set_range:
			return
		attr_range = [0, 0]
		for range_node in set_range:
			if range_node.oldMin.get()[0]:
				attr_range[0] = range_node.oldMin.get()[0]
			if range_node.oldMax.get()[0]:
				attr_range[1] = range_node.oldMax.get()[0]
		if not attr_range[0] and not attr_range[1]:
			return
		return attr_range

	def config_input(self, obj, attr_name, min_value, max_value, parameter_name, face_parameters_node, pose_frame):
		"""
		Gives information which should be stored for correct information later, info needed for set_parameter
		
		:param nt.PyNode obj: object that will have an attribute added to.
		Must be connected to a Frag node or be a FRAG node.
		:param str attr_name: Attribute name to that connects to the blend shape
		:param float min_value: min value
		:param float max_value: Max value
		:param str parameter_name: Name of the pose
		:param float pose_frame: frame number to set keyframe
		:param FRAGFaceParameters face_parameters_node: The parameter node.
		:return: Returns the obj
		:rtype: nt.PyNode
		"""
		
		result = self
		if not obj in self.get_flags():
			result = None
		if result:
			compound_attribute = self.parameters[self.parameters.numElements()]
			compound_attribute.parameter.set(parameter_name)
			compound_attribute.controlStart.set(min_value)
			compound_attribute.controlEnd.set(max_value)
			compound_attribute.poseFrame.set(pose_frame)
			obj.attr(attr_name) >> compound_attribute.controlAttr
			compound_attribute.setAlias(parameter_name)
			face_parameters_node.message >> compound_attribute.faceParameters
		return result
	
	def flag_follow_mesh(self, mesh):
		"""
		Sets the flag to follow a mesh.
		
		:param pm.nt.Transform mesh: The mesh the flag will follow.
		"""
		
		face_flag = self.get_flag()
		uv = vert_utils.get_uv_coordinates(face_flag, mesh)
		rivet_result = rivets.connect_uv_pin(mesh=mesh, uv=uv, uv_pin_name=f'{face_flag}_rivet')
		follow_grp = face_flag.flag_follow.get()

		if not follow_grp:
			logger.warning(f'The {face_flag} is not setup to follow a mesh.  Please check to see if it '
							f'has a follow grp parent')
			return

		rivet_loc = pm.PyNode(list(rivet_result.keys())[0])
		uv_pin = pm.PyNode(list(rivet_result.values())[0])
		pm.pointConstraint(rivet_loc, follow_grp, mo=True, w=True)
		rivet_loc.addAttr('isFaceUvPin', at='bool', dv=1)

		dnt_grp = self.get_frag_parent().do_not_touch
		dnt_grp_children = dnt_grp.getChildren()

		rivet_grp = [x for x in dnt_grp_children if x.hasAttr('isRivetGrp')]
		if rivet_grp:
			pm.parent(rivet_loc, rivet_grp)

		self.connect_nodes([rivet_loc, uv_pin], 'flagFollowNodes', 'fragParent')


	def attach_to_skeleton(self, attach_skeleton_root=None, mo=True):
		"""
		Drive the component with a given skeleton.

		:param Joint attach_skeleton_root: Top level joint of the hierarchy to drive the component.
		:param bool mo: If object offsets should be maintained.
		:return: A list of all created constraints.
		:rtype list[Constraint]:
		"""
		
		logger.warning(f'{self}: Face components currently do not support attaching to skeleton.')
		return []
	
	def reanimate(self, other_root, start_time=None, end_time=None):
		"""
		Transfers animation from a skeleton back onto a face rig.

		:param pm.nt.Joint other_root: The root joint that has all the animation curves
		"""
		
		pose_dict = {}
		for x in range(self.pynode.parameters.numElements()):
			pose_attr = self.pynode.parameters[x].parameter.get()
		
			# Check the root for the same pose
			if not other_root.hasAttr(pose_attr):
				continue
			
			root_anim_curve = other_root.attr(pose_attr).listConnections(type=pm.nt.AnimCurve)
			if not root_anim_curve:
				continue
			flag_attr = self.pynode.attr(pose_attr).controlAttr.listConnections(plugs=True)[0]
			end_value = self.get_max_pose_value(pose_attr)
			
			root_anim_curve = root_anim_curve[0]
			anim_exists = pose_dict.get(flag_attr, None)
			
			new_anim_curve = pm.duplicate(root_anim_curve)[0]
			anim_curves.multiply_curve_values(new_anim_curve, end_value)
			if not anim_exists:
				pose_dict.setdefault(flag_attr, new_anim_curve)
			else:
				merged_curve = anim_curves.merge_curves(new_anim_curve, anim_exists, delete_curves=True)
				pose_dict.update({flag_attr: merged_curve})
		
		for flag_attr, anim_curve in pose_dict.items():
			# Attach or merge anim curve to flag attribute
			anim_curves.reanimate_from_anim_curves(anim_curve=anim_curve,
			                                       object_attribute=flag_attr,
			                                       start_time=start_time,
			                                       end_time=end_time)
			
	def get_flag(self):
		"""
		Returns the face flag.
		
		:return: Returns the face flag.
		:rtype: flag.Flag()
		"""
		
		return self.get_start_flag()

