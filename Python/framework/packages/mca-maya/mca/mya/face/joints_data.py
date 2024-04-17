#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Tracks Joint data for face meshes.
"""

# python imports
from __future__ import print_function, division, absolute_import

# software specific imports
import pymel.core as pm
import maya.cmds as cmds

#  python imports
from mca.common.utils import pyutils
from mca.common.textio import yamlio, jsonio
from mca.mya.modeling import rivets, vert_utils


UV_DATA = {'joints': {'rivet': {},
					'uv': {},
					'ws_position': {},
					'rotation': {},
					'orientation': {},
					'allow_translate': True,
					'allow_rotate': True,
					'allow_scale': False,
					'curve_name': None,
					'uuid': {}},
			'skinned_joints': {}}


class FaceJointData:
	def __init__(self, data):
		self.data = pyutils.ObjectDict(data)
		
	@classmethod
	def create(cls, mesh, joints, prefix='rivet_'):
		"""
		Creates the data structure to connect joints to the face mesh.
		
		:param nt.Transform mesh: The mesh the joints get attached to.
		:param list(nt.Joint) joints: List of joints.
		:param string prefix: adds a unique name to the rivet.
		:return: Returns an instance of UvPositionData
		:rtype: UvPositionData
		"""
		
		data = {'joints' : {}, 'skinned_joints': {}}
		#data = dict(list(UV_DATA.items()) + list(data.items()))
		for joint in joints:
			# Get the joint uv coordinates
			rivet_name = prefix + joint.nodeName()
			uv_pin = 'uvpin_' + joint.nodeName()
			ws_position = pm.xform(joint, q=True, ws=True, t=True)
			ws_rotation = joint.rotate.get()
			orientation = joint.jointOrient.get()
			uuid = cmds.ls(str(joint), uuid=True)[0]
			uv = vert_utils.get_uv_coordinates(mesh=mesh, obj=joint)
			
			data['joints'][str(joint)] = {}
			data['joints'][str(joint)]['rivet'] = rivet_name
			data['joints'][str(joint)]['uv_pin'] = uv_pin
			data['joints'][str(joint)]['uv'] = list(uv)
			data['joints'][str(joint)]['ws_position'] = list(ws_position)
			data['joints'][str(joint)]['rotation'] = list(ws_rotation)
			data['joints'][str(joint)]['orientation'] = list(orientation)
			data['joints'][str(joint)]['uuid'] = uuid
			data['joints'][str(joint)]['allow_translate'] = True
			data['joints'][str(joint)]['allow_rotate'] = True
			data['joints'][str(joint)]['allow_scale'] = False
			data['joints'][str(joint)]['curve_name'] = None
			
			joints = list(map(lambda x: str(x), joints))
			data['skinned_joints'] = joints
		return cls(data)
	
	@staticmethod
	def data_check(data):
		"""
		Checks to make sure the dictionary is setup correctly.
		
		:param dictionary data: dictionary with uv data.
		:return: Returns a dictionary with at least the basic data needed.
		:rtype: dictionary
		"""
		
		if not data:
			data = {}
		data = dict(list(UV_DATA.items()) + list(data.items()))
		return pyutils.ObjectDict(data)
	
	@property
	def joints(self):
		"""
		Returns all the joints listed in the data.
		
		:return: Returns all the joints listed in the data.
		:rtype: List(str)
		"""
		
		return list(self.data['joints'].keys())
	
	@property
	def joints_data(self):
		"""
		Returns a dictionary with all the joints and listed data.
		
		:return: Returns a dictionary with all the joints and listed data.
		:rtype: dictionary
		"""
		
		return self.data['joints']
	
	@joints_data.setter
	def joints_data(self, value):
		"""
		Sets joint data to attach to a mesh.
		
		:param dictionary value: Dictionary of joints data to attach to a mesh.
		"""
		
		self.data.update({'joints': value})
	
	@property
	def rivet_names(self):
		rivet_names = []
		for joint in self.joints:
			rivet_name = self.data['joints'][joint].get('rivet', None)
			if rivet_name:
				rivet_names.append(rivet_name)
		return rivet_names
	
	@property
	def skinned_joints(self):
		"""
		Returns a list of joints that get skinned to the mesh.
		
		:return: Returns a list of joints that get skinned to the mesh.
		:rtype: List(str)
		"""
		
		return self.data['skinned_joints']
	
	@skinned_joints.setter
	def skinned_joints(self, value):
		"""
		Sets the skinned joints list.
		
		:param list(str) value: List of joints that get skinned to a mesh.
		"""
		
		self.data.update({'skinned_joints': value})
		
	def set_anim_control_shape(self, joint, shape_name):
		"""
		Sets the name of the animation curve.
		
		:param str joint: name of the joint.
		:param str shape_name: name of the curve file.
		"""
		
		self.joints_data.update({str(joint): {'curve_name': shape_name}})
	
	def get_anim_control_shape(self, joint):
		"""
		Returns the name of the animation curve.
		
		:param str joint: name of the joint.
		:return: Returns the name of the curve file.
		:rtype: str
		"""

		return self.joints_data[str(joint)].get('curve_name', None)

	@staticmethod
	def connect_rivet(mesh, locator, uv, uv_pin_name=None, locator_scale=0.2):
		"""
		Creates a nt.UvPin and connects a rivet/locator to a mesh.
		
		:param nt.Transform mesh: The mesh that will have the rivet connected to.
		:param str locator: Name of the locator that will represent the rivet.
		:param list(float) uv: UV Coordinates.
		:param str uv_pin_name: Name of the UvPin.
		:param float locator_scale: Local scale of the locator that gets connected to the UV pin.
		:return: Returns the name of the locator and the UvPin.
		:rtype: Dictionary
		"""
		
		if not pm.objExists(locator):
			locator = pm.spaceLocator(n=locator)
		# Scale down the locator.
		pm.setAttr(str(locator) + '.localScaleX', locator_scale)
		pm.setAttr(str(locator) + '.localScaleY', locator_scale)
		pm.setAttr(str(locator) + '.localScaleZ', locator_scale)
		
		# Create the name for the UvPin.
		name_list = locator.split('_')
		if not uv_pin_name:
			name_list[0] = 'uvpin'
			uv_pin_name = '_'.join(name_list)
		uv_pin = rivets.create_uv_pin(mesh=mesh,
										obj=locator,
										uv=uv,
										name=uv_pin_name)
		# Add a tag for later use.
		uv_pin.addAttr('isFaceUvPin', at='bool', dv=1)
		return {str(locator): str(uv_pin)}

	def connect_joint_to_rivet(self, rivet, joint):
		"""
		Connects a joint to a rivet.
		
		:param str rivet: Name of the rivet.
		:param nt.Joint joint: The joint that will be connected to the rivet.
		"""
		
		if self.joints_data[str(joint)]['allow_translate']:
			pm.pointConstraint(rivet, joint, w=True)
		if self.joints_data[str(joint)]['allow_rotate']:
			pm.orientConstraint(rivet, joint, w=True, mo=True)
		if self.joints_data[str(joint)]['allow_scale']:
			pm.scaleComponents(rivet, joint, w=True)
		joint = pm.PyNode(joint)
		self.set_rotate(joint=joint)
		self.set_orientation(joint=joint)
	
	def connect_all_joints(self):
		"""
		Connects all the joints in the data to the rivets.
		"""
		
		for joint in self.joints:
			self.connect_joint_to_rivet(self.joints[str(joint)]['rivet'], joint)
	
	def connect_all_rivets_joints(self, mesh, joint_list=None):
		"""
		Connects all the rivets and joints in the data to a mesh using the uv coordinates.
		
		:param nt.Transform mesh: The mesh that will receive the rivets.
		"""
		
		rivet_names = []
		if not joint_list:
			joint_list = self.joints
		for joint in joint_list:
			rivet_name = self.joints_data[str(joint)].get('rivet')
			uv = self.joints_data[str(joint)]['uv']
			uv_pin_name = self.joints_data[str(joint)].get('uv_pin')
			rivet = self.connect_rivet(mesh=mesh,
										locator=rivet_name,
										uv=uv,
										uv_pin_name=uv_pin_name)
			self.connect_joint_to_rivet(rivet=list(rivet.keys())[0], joint=joint)
			rivet_names.append(rivet_name)
		return rivet_names
	
	def set_ws_positions(self, joints=None):
		"""
		Sets the world sppace position of a joint.
		
		:param list(nt.Joint) joints: The joint that will have the world space set.
		"""
		
		if not joints:
			joints = self.joints
		if not isinstance(joints, list):
			joints = [joints]
			
		for joint in joints:
			if not isinstance(joint, pm.nt.Joint):
				joint = pm.PyNode(joint)
			ws = self.joints_data[str(joint)].get('ws_position')
			pm.xform(joint, ws=True, t=ws)
			self.set_rotate(joint=joint)
			self.set_orientation(joint=joint)
				
	def set_rotate(self, joint):
		"""
		Sets the rotation of a joint.
		
		:param nt.Joint joint: The joint that will have the rotation set.
		"""
		
		if not isinstance(joint, pm.nt.Joint):
			joint = pm.PyNode(joint)
		value = self.joints_data[str(joint)].get('rotation')
		if value:
			joint.rotate.set(value)
			
	def set_orientation(self, joint):
		"""
		Sets the orientation of a joint.
		
		:param nt.Joint joint: The joint that will have the orientation set.
		"""
		
		if not isinstance(joint, pm.nt.Joint):
			joint = pm.PyNode(joint)
		value = self.joints_data[str(joint)].get('orientation')
		if value:
			joint.jointOrient.set(value)
		
	def delete_all_rivets(self, ns=''):
		"""
		Deletes all the rivets that are stored in the data.
		
		:param str ns: Namespace of the rivets and UvPins.
		"""
		
		for joint in self.joints:
			rivet = self.joints_data[str(joint)].get('rivet')
			if pm.objExists(rivet):
				pm.delete(ns+rivet)
			uv_pin = self.joints_data[str(joint)].get('uv_pin')
			if pm.objExists(uv_pin):
				pm.delete(ns+uv_pin)
	
	def export(self, file_path):
		"""
		Exports the data to a yaml file.
		
		:param str file_path: Full path to the file.
		"""
		
		jsonio.write_to_json_file(data=self.data, filename=file_path)
		
	@classmethod
	def load(cls, file_path):
		"""
		Loads a yaml file and Returns the instance of the class.
		
		:param str file_path: Full path to the file.
		:return: Returns the instance of the class UvPositionData.
		:rtype: UvPositionData
		"""
		
		data = jsonio.read_json_file(file_path)
		return cls(data)
	
	def export_yaml(self, file_path):
		"""
		Exports the data to a yaml file.
		
		:param str file_path: Full path to the file.
		"""
		
		yamlio.write_to_yaml_file(data=self.data, filename=file_path)
	
	@classmethod
	def load_yaml(cls, file_path):
		"""
		Loads a yaml file and Returns the instance of the class.
		
		:param str file_path: Full path to the file.
		:return: Returns the instance of the class UvPositionData.
		:rtype: UvPositionData
		"""
		
		data = yamlio.read_yaml_file(file_path)
		return cls(data)
