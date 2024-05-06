#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
FRAG Node for handling cinematic sequences
"""

# mca python imports

# PySide2 imports

# software specific imports
import pymel.core as pm

# mca python imports
from mca.mya.rigging import frag
from mca.common import log

logger = log.MCA_LOGGER

class CineSequenceComponent(frag.FRAGNode):
	VERSION = 1
	# python class for the mya node that lives in scene and holds information
	# -----------------------------------------------------------------------()
	@staticmethod
	def create(seq_data):
		"""
		Creates a new CineSequenceComponent node and returns it.

		:param dict seq_data: Dictionary with data about the cinematic sequence. Should use CineSequenceData.data
		:return: Returns the created FRAGNode
		:rtype: CineSequenceComponent

		"""

		seq_name = seq_data.get('seq_name')
		stage = seq_data.get('stage')
		scene_name = seq_data.get('scene_name')
		version_num = seq_data.get('version_num')
		shots = seq_data.get('shots')

		node = (frag.FRAGNode.create(frag_parent=None,
											frag_type=CineSequenceComponent.__name__,
											version=CineSequenceComponent.VERSION))
		maya_node = node.pynode

		maya_node.addAttr('sequenceName', dt='string')
		maya_node.sequenceName.set(seq_name)
		maya_node.addAttr('stage', dt='string')
		maya_node.stage.set(stage)
		maya_node.addAttr('sceneName', dt='string')
		maya_node.sceneName.set(scene_name)
		maya_node.addAttr('versionNumber', dt='string')
		maya_node.versionNumber.set(str(version_num))
		maya_node.addAttr('shots', at='message')
		if shots:
			for shot_num, shot_data in shots.items():
				shot_name = shot_data.get('shot_name')
				shot_pynode = [x for x in pm.ls(type=pm.nt.Shot) if x.shotName.get() == shot_name]
				if shot_pynode:
					shot_pynode = shot_pynode[0]
					shot_pynode.setLocked(False)
				else:
					continue
				if not shot_pynode.hasAttr('sequenceNode'):
					shot_pynode.addAttr('sequenceNode', at='message')
				maya_node.shots >> shot_pynode.sequenceNode

		frag_node = CineSequenceComponent(maya_node)
		return frag_node

	def seq_name(self):
		return self.pynode.sequenceName.get()

	def scene_name(self):
		return self.pynode.sceneName.get()

	def version_num(self):
		return self.pynode.versionNumber.get()

	def stage(self):
		return self.pynode.stage.get()

	def shots(self):
		return self.pynode.shots.listConnections()

	def add_shot(self, shot):
		if not shot.hasAttr('sequenceNode'):
			shot.addAttr('sequenceNode', at='message')
		self.pynode.shots >> shot.sequenceNode

	def remove_shot(self, shot):
		if shot.hasAttr('sequenceNode'):
			self.pynode.shots // shot.sequenceNode


def find_cine_seq_component():
	scene_network_nodes = pm.ls(type=pm.nt.Network)
	for network_node in scene_network_nodes:
		try:
			frag_node = frag.FRAGNode(network_node)
			if isinstance(frag_node, (frag.CineSequenceComponent)):
				return frag_node
		except Exception:
			logger.info(f'{network_node} cannot be a FRAGNode')
			pass
	return None