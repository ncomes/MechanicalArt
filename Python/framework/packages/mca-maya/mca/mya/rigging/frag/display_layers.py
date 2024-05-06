#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display Layers Component
"""

# System global imports
# software specific imports
import pymel.core as pm
# mca python imports
from mca.mya.modifiers import ma_decorators
# internal module imports
from mca.mya.rigging.frag import frag_base
from mca.mya.utils import namespace


SKEL_LYR = 'skel_lyr'
SKIN_LYR = 'skins_lyr'
FLAGS_LYR = 'flags_lyr'
FLAGS_CONTACT_LYR = 'flags_contact_lyr'
FLAGS_DETAIL_LYR = 'flags_detail_lyr'


class DisplayLayers(frag_base.FRAGNode):
	VERSION = 1
	
	@staticmethod
	@ma_decorators.keep_namespace_decorator
	def create(frag_parent):
		"""
		Creates a Frag node to connect rig display layers.
		
		:param FRAGNode frag_parent: parent frag node.
		:return: Returns the display layers frag node.
		:rtype: FRAGNode
		"""
		
		display_children = frag_parent.get_frag_children(of_type=DisplayLayers)
		if display_children:
			return display_children[0]
		
		# Set Namespace
		root_namespace = frag_parent.namespace().split(':')[0]
		namespace.set_namespace(root_namespace, check_existing=False)
		
		# Create the FRAG Rig Network Node
		node = frag_base.FRAGNode.create(frag_parent, DisplayLayers.__name__, DisplayLayers.VERSION)
		node.addAttr("layers", dt="string", m=True)  # ToDo ncomes: need to change to a compound attribute

		return node

	@ma_decorators.keep_namespace_decorator
	def add_objects(self, obj_list, layer_name):
		"""
		Add the objects to the layer, if layer doesn't exist will create one.

		:param pm.nt.dagNodes obj_list: Objects to add to display layer.
		:param str layer_name: string name of the display layer.
		:return: Returns the layer the objects were added to.
		:rtype: DisplayLayers
		"""
		
		# namespace switch
		root_namespace = self.namespace().split(':')[0]
		namespace.set_namespace(root_namespace, check_existing=False)
		
		obj_list = list(map(lambda x: pm.PyNode(x), obj_list))
		
		if self.has_layer(layer_name):
			layer = self._get_layer_from_layer_name(layer_name)
		else:
			pm.select(clear=1)
			layer = pm.createDisplayLayer(empty=True, name=layer_name)
			self.connect_nodes([layer], 'layers', merge_values=True)
		
		# skip objects that are already added to layers
		for obj in obj_list:
			if not len(obj.drawOverride.connections()):
				layer.addMembers(obj)

		return layer
	
	def show_layer(self, layer_name):
		"""
		Makes the layer visible
		
		:param str layer_name: Name of the display layer.
		"""
		
		layer = self._get_layer_from_layer_name(layer_name)
		if layer:
			layer.v.set(1)
	
	def hide_layer(self, layer_name):
		"""
		Makes the layer invisible.
		
		:param str layer_name: Name of the display layer.
		"""
		
		layer = self._get_layer_from_layer_name(layer_name)
		if layer:
			layer.v.set(0)
	
	def set_layer_to_template(self, layer_name):
		"""
		Sets state of layer to template.
		
		:param str layer_name: Name of the display layer.
		"""
		
		layer = self._get_layer_from_layer_name(layer_name)
		if layer:
			layer.displayType.set(1)
	
	def set_layer_to_reference(self, layer_name):
		"""
		Sets state of layer to reference.
		
		:param str layer_name: Name of the display layer.
		"""
		
		layer = self._get_layer_from_layer_name(layer_name)
		if layer:
			layer.displayType.set(2)
	
	def remove_state_on_layer(self, layer_name):
		"""
		Makes layer not templated and not reference.
		
		:param layer_name:
		"""
		
		layer = self._get_layer_from_layer_name(layer_name)
		if layer:
			layer.displayType.set(0)
	
	def get_layers(self):
		"""
		Returns all connected layers.
		
		:return: Returns all connected layers.
		:rtype: list(pm.nt.displayLayer)
		"""
		
		return self.layers.listConnections()
	
	def get_layer(self, name):
		"""
		Returns a layer by searching for the name.
		
		:param str name: name of a layer.
		:return: Returns a layer by searching for the name.
		:rtype: pm.nt.displayLayer
		"""
		
		result = None
		if self.has_layer(name):
			layer = self._get_layer_from_layer_name(name)
			result = layer
		return result
	
	def remove_layer(self, layer_name):
		"""
		Removes the layer from the scene.
		
		:param str layer_name: name of a layer.
		"""
		
		layer = self._get_layer_from_layer_name(layer_name)
		if layer:
			pm.delete(layer)
	
	def get_members(self, layer_name):
		"""
		Returns the members of the given layer.
		
		:param str layer_name: name of a layer.
		:return: Returns the members of the given layer.
		:rtype: members
		"""
		
		layer = self._get_layer_from_layer_name(layer_name)
		result = None
		if layer:
			result = layer.listMembers()
		return result
	
	def has_layer(self, layer_name):
		"""
		Returns true if this rig has a layer of that name.
		
		:param str layer_name: Name of a layer.
		:return: Returns true if this rig has a layer of that name.
		:rtype: bool
		"""
		
		all_layer_names = self.list_layer_names()
		result = False
		if layer_name in all_layer_names:
			return True
		return result
	
	def remove_objects(self, obj_list, layer_name):
		"""
		Remove the objects from the layer.
		
		:param list(pm.nt.PyNode) obj_list:
		:param str layer_name: Name of a layer.
		"""
		
		obj_list = list(map(lambda x: pm.PyNode(x), obj_list))
		layer = self._get_layer_from_layer_name(layer_name)
		if layer:
			pm.editDisplayLayerMembers("defaultLayer", obj_list, noRecurse=True)
	
	def remove(self):
		"""
		Removes this node and all the layers associated with it.
		
		"""
		
		layers = self.get_layers()
		for layer in layers:
			try:
				pm.delete(layer)
			except:
				pass
		try:
			pm.delete(self)
		except:
			pass
	
	def list_layer_names(self):
		"""
		Returns a list of all the layer names associated with this node without the namespace.
		
		:return: Returns a list of all the layer names associated with this node without the namespace.
		:rtype: list(str)
		"""
		
		layers = self.get_layers()
		return [self._get_layer_absolute_name_from_layer(layer) for layer in layers]
	
	def _get_layer_absolute_name_from_layer(self, layer):
		"""
		Returns the name of a layer without the namespace.
		
		:param pm.nt.displayLayer layer: The layer to get the name.
		:return: Returns the name of a layer without the namespace.
		:rtype: str
		"""
		
		return layer.name().split(":")[-1]
	
	def _get_layer_from_layer_name(self, layer_name):
		"""
		If layer of same absolute name exists return that layer, else None
		
		:param str layer_name: Name of a layer.
		:return: Returns a layer.
		:rtype: pm.nt.displayLayer
		"""
		
		layers = self.get_layers()
		layerName_layer = dict([(self._get_layer_absolute_name_from_layer(layer), layer) for layer in layers])
		result = None
		if layer_name in layerName_layer.keys():
			result = layerName_layer[layer_name]
		return result

