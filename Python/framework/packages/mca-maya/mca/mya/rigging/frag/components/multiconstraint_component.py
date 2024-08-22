#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related the multiconstraint rig component.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.utils import attr_utils, naming

from mca.mya.rigging import flags, joint_utils
from mca.mya.rigging.frag.build import multiconstraint
from mca.mya.rigging.frag.components import frag_rig


from mca.common import log
logger = log.MCA_LOGGER

class MultiConstraintComponent(frag_rig.FRAGComponent):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, source_node, target_list, switch_node=None, translate=True, rotate=True, scale=True, **kwargs):
        """

        """
        if not source_node:
            logger.error('No source node provided will abort build.')
            return
        
        if not target_list:
            logger.error('No target list provided will abort build.')
            return

        if isinstance(source_node, flags.Flag):
            source_node = source_node.pynode
        target_list = [x.pynode if isinstance(x, flags.Flag) else x for x in target_list]
        if isinstance(switch_node, flags.Flag):
            switch_node = switch_node.pynode

        rig_region = naming.get_basename(source_node)
        rig_side = 'multiconstraint'

        frag_rig_node = super().create(frag_rig, rig_side, rig_region, None, **kwargs)

        # Save kwargs to node attrs we'll use these for serializing.
        t = kwargs.get('t', translate)
        r = kwargs.get('r', rotate)
        s = kwargs.get('s', scale)

        kwargs_dict = {}
        kwargs_dict['translate'] = t
        kwargs_dict['rotate'] = r
        kwargs_dict['scale'] = s

        attr_utils.set_compound_attribute_groups(frag_rig_node.pynode, 'buildKwargs', kwargs_dict)

        # Start building shiet.
        switch_node = switch_node or source_node
        result_multi = multiconstraint.build_multi_constraint(target_list=target_list,
                                                              source_node=source_node,
                                                              switch_node=switch_node,
                                                              translate=t,
                                                              rotate=r,
                                                              scale=s,
                                                              switch_attr='follow',
                                                              default_name=kwargs.get('default_name', None))

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_node(result_multi.get('multi_matrix'), "multi_matrix", 'fragParent')
        frag_rig_node.connect_node(result_multi.get('decomp_matrix'), "decomp_matrix", 'fragParent')
        frag_rig_node.connect_node(result_multi.get('constraint_group'), "constraint_group", 'fragParent')
        frag_rig_node.connect_node(result_multi.get('parent_constraint_group'), "parent_constraint_group", 'fragParent')
        frag_rig_node.connect_node(result_multi.get('choice_offset'), "choice_offset", 'fragParent')
        frag_rig_node.connect_node(result_multi.get('choice_space'), "choice_space", 'fragParent')
        frag_rig_node.connect_node(source_node, 'source_node', parent_attr="source_multi_constraint")
        frag_rig_node.connect_node(switch_node, 'switch_node', parent_attr="switch_node")
        frag_rig_node.connect_nodes(target_list, 'targets')

        return frag_rig_node
    
    @property
    def targets(self):
        return self.pynode.getAttr('targets')
    
    def remove(self):
        switch_node = self.pynode.switch_node.get()
        source_node = self.pynode.source_node.get()

        attr_list = ['matrix_constraint', 'parent_matrix_constraint', 'parent_constraint_node', 'switch_node', '__', 'follow']

        for attr_name in attr_list:
            for multi_object in [switch_node, source_node]:
                if multi_object.hasAttr(attr_name):
                    multi_object.attr(attr_name).unlock()
                    multi_object.deleteAttr(attr_name)

        source_node.source_multi_constraint.unlock()
        source_node.deleteAttr('source_multi_constraint')

        constraint_group = self.pynode.constraint_group.get()
        parent_constraint_group = self.pynode.parent_constraint_group.get()
        pm.parent(pm.listRelatives(constraint_group), parent_constraint_group.getParent())
        pm.delete(parent_constraint_group, self.pynode, self.pynode.multi_matrix.get(), self.pynode.decomp_matrix.get())

    def serialize_component(self, skel_hierarchy=None):
        if not skel_hierarchy:
            root_joint = self.get_frag_root().root_joint
            skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

        data_dict = {}
        # Component type and side/region lookup.
        data_dict['component'] = {}
        data_dict['component']['frag_type'] = self.frag_type
        data_dict['component']['side'] = self.side
        data_dict['component']['region'] = self.region

        # Lets get our build kwargs
        data_dict['build_kwargs'] = {}
        # source_node, target_list, switch_node
        data_dict['build_kwargs']['source_node'] = frag_rig.get_object_identifier(self.pynode.source_node.get(), skel_hierarchy)
        data_dict['build_kwargs']['target_list'] = [frag_rig.get_object_identifier(x, skel_hierarchy) for x in self.pynode.targets.get()]
        data_dict['build_kwargs']['switch_node'] = frag_rig.get_object_identifier(self.pynode.switch_node.get(), skel_hierarchy)

        data_dict['build_kwargs'] = {**data_dict['build_kwargs'], **self.get_build_kwargs()}

        return data_dict, skel_hierarchy
                    