# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains utilities for getting the time ranges of a scene and its animation.
"""

# system global imports
# python imports
# software specific imports
import pymel.core as pm
#  python imports
from mca.common import log
from mca.mya.utils import attr_utils

logger = log.MCA_LOGGER


def add_overlay_textures(obj_list, overlay_texture_path):
	"""
	Add an overlay texture onto a mesh.
	:param obj: mesh you are adding texture to.
	:param overlay_texture_path: The path to the png texture
	"""
	for obj in obj_list:
		if isinstance(obj, str):
			obj = pm.PyNode(obj)
		
		shape = obj.getShape()
		shading_engines = [x for x in shape.listConnections(s=1, d=1) if isinstance(x, pm.nt.ShadingEngine)]
		if shading_engines:
			# Find shaders
			for shading_engine in shading_engines:
				# blinn or phong
				shaders = shading_engine.surfaceShader.listConnections(s=1, d=0)
				# Find color textures
				for shader in shaders:
					color_node = shader.color.listConnections(s=True, d=False)
					if not color_node:
						color = shader.color.get()
						base_color_node = pm.createNode("checker")
						base_color_node.addAttr("isOverlayBase")
						base_color_node.color1.set(color)
						base_color_node.color2.set(color)
						base_color_node.outColor >> shader.color
						color_node = pm.PyNode(base_color_node)
					else:
						color_node = color_node[0]
					if not color_node.hasAttr("isOverlayLayeredTexture"):
						# Create new overlay graph
						layered_texture = pm.createNode("layeredTexture")
						layered_texture.addAttr("isOverlayLayeredTexture")
						texture_node = pm.createNode("file")
						texture_node.fileTextureName.set(overlay_texture_path)
						color_node.outColor >> layered_texture.attr("inputs")[1].color
						texture_node.outColor >> layered_texture.attr("inputs")[2].color
						pm.removeMultiInstance(layered_texture.attr("inputs")[0])
						layered_texture.attr("inputs")[1].alpha.set(.75)
						layered_texture.outColor >> shader.color


def remove_overlay_textures():
	"""
	Removes the Overlay Texture on all listed objects

	:param obj_list: List of objs that have a overlay texture.
	"""
	layered_textures = attr_utils.get_all_objects_with_attr("isOverlayLayeredTexture")
	
	for layered_texture in layered_textures:
		# Get connected textures
		shader_attrs = layered_texture.outColor.listConnections(s=0, d=1, plugs=True)
		main_color_attr = layered_texture.attr("inputs")[1].color.listConnections(s=True, d=False, plugs=True)[0]
		overlay_texture = layered_texture.attr("inputs")[2].color.listConnections(s=True, d=False)
		# Connect original texture back up
		for shader_attr in shader_attrs:
			main_color_attr >> shader_attr
			if main_color_attr.node().hasAttr("isOverlayBase"):
				pm.delete(main_color_attr.node())
		# Delete extra nodes
		pm.delete(overlay_texture, layered_texture)

