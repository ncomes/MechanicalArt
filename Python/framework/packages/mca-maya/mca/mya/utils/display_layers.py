#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules that interact with mya display layers
"""

# python imports
# software specific imports
import pymel.core as pm

# mca python imports


def get_display_layers(objs):
	"""
	Finds and returns display layers for specified objects.

	:param list objs: list of objects that may or may not be connected to a display layer
	:return: list of display layers (nt.DisplayLayer)
	:rtype: list[nt.DisplayLayer]
	"""
	
	display_layers = []
	if not isinstance(objs, (list, tuple)):
		objs = [objs]
	
	for obj in objs:
		layer = obj.listConnections(type=pm.nt.DisplayLayer)
		if layer:
			display_layers.append(layer[0])
	
	return display_layers


def remove_objects_from_layers(objs):
	"""
	Removes an object from whatever layers it's under.

	:param list objs: list of objects to remove from all layers.
	"""
	
	if not isinstance(objs, (list, tuple)):
		objs = [objs]
	for obj in objs:
		display_layer = obj.drawOverride.listConnections(type=pm.nt.DisplayLayer)
		obj_shape = obj.getShape()
		display_layer_shape = None
		if obj_shape:
			display_layer_shape = obj_shape.drawOverride.listConnections(type=pm.nt.DisplayLayer)

		if display_layer:
			for layer in display_layer:
				layer.drawInfo // obj.drawOverride
		if display_layer_shape:
			for layer in display_layer_shape:
				layer.drawInfo // obj.getShape().drawOverride


def delete_empty_display_layers():
	"""
	Deletes empty display layers
	"""
	
	for layer in pm.ls(type="displayLayer"):
		if layer.identification.get() > 0 and not pm.editDisplayLayerMembers(layer, q=True):
			pm.delete(layer)


