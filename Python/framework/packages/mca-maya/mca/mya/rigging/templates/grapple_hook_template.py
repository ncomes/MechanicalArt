#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Template for human players and npcs
"""

# System global imports
# Software specific imports
import pymel.core as pm

# mca python imports
from mca.mya.rigging import frag
from mca.mya.rigging.templates import rig_templates
from mca.mya.rigging import chain_markup


# Internal module imports


class GrappleHook03(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = 'grapple_hook_03'
	ASSET_TYPE = 'weapon'
	
	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(GrappleHook03, self).__init__(asset_id, asset_type)
	
	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):
		
		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		world_root = pm.PyNode('root')
		
		frag_root = frag.FRAGRoot.create(world_root, self.asset_type, self.asset_id)
		frag.SkeletalMesh.create(frag_root)
		frag_rig = frag.FRAGRig.create(frag_root)
		
		root = pm.PyNode('root')
		chain = chain_markup.ChainMarkup(root)
		# world
		
		world_component = frag.WorldComponent.create(frag_rig,
															root,
															'center',
															'world',
															orientation=[-90, 0, 0])
		world_flag = world_component.world_flag
		root_flag = world_component.root_flag
		root_flag.set_as_sub()
		offset_flag = world_component.offset_flag
		offset_flag.set_as_detail()
		
		# Base
		base_chain = chain.get_start('base', 'center')
		base_component = frag.FKComponent.create(frag_rig,
															base_chain,
															base_chain,
															side='center',
															region='base',
															lock_child_translate_axes=[],
															lock_root_translate_axes=['v'])
		base_component.attach_component(world_component, root)
		base_flag = base_component.get_flags()[0]
		
		# Left Hook
		l_hook_chain = chain.get_chain('left_grap', 'left')
		l_hook_component = frag.FKComponent.create(frag_rig,
															l_hook_chain[0],
															l_hook_chain[1],
															side='left',
															region='hook',
															lock_child_translate_axes=[],
															lock_root_translate_axes=['v'])
		l_hook_component.attach_component(base_component, base_chain)
		l_hook_flag = l_hook_component.get_flags()[0]
		
		# Right Hook
		r_hook_chain = chain.get_chain('right_grap', 'right')
		r_hook_component = frag.FKComponent.create(frag_rig,
														r_hook_chain[0],
														r_hook_chain[1],
														side='right',
														region='hook',
														lock_child_translate_axes=[],
														lock_root_translate_axes=['v'])
		r_hook_component.attach_component(base_component, base_chain)
		r_hook_flag = r_hook_component.get_flags()[0]
		
		# Back Hook
		b_hook_chain = chain.get_chain('back_grap', 'back')
		b_hook_component = frag.FKComponent.create(frag_rig,
															b_hook_chain[0],
															b_hook_chain[1],
															side='back',
															region='hook',
															lock_child_translate_axes=[],
															lock_root_translate_axes=['v'])
		b_hook_component.attach_component(base_component, base_chain)
		b_hook_flag = b_hook_component.get_flags()[0]
		
		# Front Hook
		f_hook_chain = chain.get_chain('front_grap', 'front')
		f_hook_component = frag.FKComponent.create(frag_rig,
															f_hook_chain[0],
															f_hook_chain[1],
															side='front',
															region='hook',
															lock_child_translate_axes=[],
															lock_root_translate_axes=['v'])
		f_hook_component.attach_component(base_component, base_chain)
		f_hook_flag = f_hook_component.get_flags()[0]
		
		if finalize:
			frag_rig.rigTemplate.set(GrappleHook03.__name__)
			frag_rig.finalize_rig(self.get_flags_path())
		
		return frag_rig


class GrappleHook02(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = 'grapple_hook_03'
	ASSET_TYPE = 'weapon'
	
	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(GrappleHook02, self).__init__(asset_id, asset_type)
	
	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):
		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		world_root = pm.PyNode('root')
		
		frag_root = frag.FRAGRoot.create(world_root, self.asset_type, self.asset_id)
		frag.SkeletalMesh.create(frag_root)
		frag_rig = frag.FRAGRig.create(frag_root)
		
		root = pm.PyNode('root')
		chain = chain_markup.ChainMarkup(root)
		# world
		
		world_component = frag.WorldComponent.create(frag_rig,
															root,
															'center',
															'world',
															orientation=[-90, 0, 0])
		world_flag = world_component.world_flag
		root_flag = world_component.root_flag
		root_flag.set_as_sub()
		offset_flag = world_component.offset_flag
		offset_flag.set_as_detail()
		
		# Base
		base_chain = chain.get_start('base', 'center')
		base_component = frag.FKComponent.create(frag_rig,
														base_chain,
														base_chain,
														side='center',
														region='base',
														lock_child_translate_axes=[],
														lock_root_rotate_axes=['rx', 'ry'],
														lock_root_translate_axes=['v'])
		base_component.attach_component(world_component, root)
		base_flag = base_component.get_flags()[0]
		
		# Left Hook
		l_hook_chain = chain.get_start('top_frap', 'left')
		l_hook_component = frag.FKComponent.create(frag_rig,
															l_hook_chain,
															l_hook_chain,
															side='left',
															region='hook',
															lock_child_translate_axes=[],
															lock_root_rotate_axes=['rx', 'ry'],
															lock_root_translate_axes=['v'])
		l_hook_component.attach_component(base_component, base_chain)
		l_hook_flag = l_hook_component.get_flags()[0]
		
		# Right Hook
		r_hook_chain = chain.get_start('top_frap', 'right')
		r_hook_component = frag.FKComponent.create(frag_rig,
															r_hook_chain,
															r_hook_chain,
															side='right',
															region='hook',
															lock_child_translate_axes=[],
															lock_root_rotate_axes=['rx', 'ry'],
															lock_root_translate_axes=['v'])
		r_hook_component.attach_component(base_component, base_chain)
		r_hook_flag = r_hook_component.get_flags()[0]
		
		# Back Hook
		b_hook_chain = chain.get_start('top_frap', 'back')
		b_hook_component = frag.FKComponent.create(frag_rig,
															b_hook_chain,
															b_hook_chain,
															side='back',
															region='hook',
															lock_child_translate_axes=[],
															lock_root_rotate_axes=['rx', 'ry'],
															lock_root_translate_axes=['v'])
		b_hook_component.attach_component(base_component, base_chain)
		b_hook_flag = b_hook_component.get_flags()[0]
		
		# Front Hook
		f_hook_chain = chain.get_start('top_frap', 'front')
		f_hook_component = frag.FKComponent.create(frag_rig,
															f_hook_chain,
															f_hook_chain,
															side='front',
															region='hook',
															lock_child_translate_axes=[],
															lock_root_rotate_axes=['rx', 'ry'],
															lock_root_translate_axes=['v'])
		f_hook_component.attach_component(base_component, base_chain)
		f_hook_flag = f_hook_component.get_flags()[0]
		
		# Front Small Hook
		f_small_hook_chain = chain.get_start('small_frap', 'front')
		f_small_hook_component = frag.FKComponent.create(frag_rig,
															f_small_hook_chain,
															f_small_hook_chain,
															side='front',
															region='small_hook',
															lock_child_translate_axes=[],
															lock_root_rotate_axes=['rx', 'ry'],
															lock_root_translate_axes=['v'])
		f_small_hook_component.attach_component(base_component, base_chain)
		f_small_hook_flag = f_small_hook_component.get_flags()[0]
		
		# Front Small Hook
		b_small_hook_chain = chain.get_start('small_frap', 'back')
		b_small_hook_component = frag.FKComponent.create(frag_rig,
																b_small_hook_chain,
																b_small_hook_chain,
																side='back',
																region='small_hook',
																lock_root_rotate_axes=['rx', 'ry'],
																lock_child_translate_axes=[],
																lock_root_translate_axes=['v'])
		b_small_hook_component.attach_component(base_component, base_chain)
		b_small_hook_flag = b_small_hook_component.get_flags()[0]
		
		# Front Small Hook
		l_small_hook_chain = chain.get_start('small_frap', 'left')
		l_small_hook_component = frag.FKComponent.create(frag_rig,
																l_small_hook_chain,
																l_small_hook_chain,
																side='left',
																region='small_hook',
																lock_root_rotate_axes=['rx', 'ry'],
																lock_child_translate_axes=[],
																lock_root_translate_axes=['v'])
		l_small_hook_component.attach_component(base_component, base_chain)
		l_small_hook_flag = l_small_hook_component.get_flags()[0]
		
		# Front Small Hook
		r_small_hook_chain = chain.get_start('small_frap', 'right')
		r_small_hook_component = frag.FKComponent.create(frag_rig,
																r_small_hook_chain,
																r_small_hook_chain,
																side='right',
																region='small_hook',
																lock_root_rotate_axes=['rx', 'ry'],
																lock_child_translate_axes=[],
																lock_root_translate_axes=['v'])
		r_small_hook_component.attach_component(base_component, base_chain)
		r_small_hook_flag = r_small_hook_component.get_flags()[0]
		
		if finalize:
			frag_rig.rigTemplate.set(GrappleHook02.__name__)
			frag_rig.finalize_rig(self.get_flags_path())
		
		return frag_rig

