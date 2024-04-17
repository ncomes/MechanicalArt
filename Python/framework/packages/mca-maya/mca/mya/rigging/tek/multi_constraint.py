#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.utils import attr_utils
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import multi_constraint_rig
# Internal module imports
from mca.mya.rigging.tek import tek_base


class MultiConstraint(tek_base.TEKNode):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(tek_parent,
                side,
                region,
                source_object,
                target_list,
                switch_obj=None,
                translate=True,
                rotate=True,
                scale=True,
                switch_attr='follow',
                **kwargs):

        """
        Creates a Multi Constraint Component.  Allows an object to switch constraints between multiple objects.

        :param TEKNode tek_parent: TEK Rig TEKNode.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :param pm.nt.transform source_object: The object that will be driven.
        :param list(pm.nt.transform) target_list: The objects that will be driving the source object.
        :param bool translate: Allows the source object to be driven by translate.
        :param bool rotate: Allows the source object to be driven by rotate.
        :param bool scale: Allows the source object to be driven by scale.
        :param str switch_attr: Name of the switch attribute.
        :return: Returns the MultiConstraint component.
        :rtype: MultiConstraint
        """

        t = kwargs.get('t', translate)
        r = kwargs.get('r', rotate)
        s = kwargs.get('s', scale)

        kwargs_dict = {}
        kwargs_dict['translate'] = t
        kwargs_dict['rotate'] = r
        kwargs_dict['scale'] = s
        kwargs_dict['side'] = side
        kwargs_dict['region'] = region
        kwargs_dict['switch_attr'] = switch_attr

        # Set Namespace
        root_namespace = tek_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = tek_base.TEKNode.create(tek_parent,
                                         MultiConstraint.__name__,
                                         version=MultiConstraint.VERSION)
        node.rename('{0}_{1}_{2}'.format(MultiConstraint.__name__, side, region))

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        # Add rig attributes
        node.side = side
        node.region = region

        if not switch_obj:
            switch_obj = source_object

        # Create the multiconstraint.
        result_multi = multi_constraint_rig.multi_constraint(target_list=target_list,
                                                             source_object=source_object,
                                                             switch_obj=switch_obj,
                                                             translate=t,
                                                             rotate=r,
                                                             scale=s,
                                                             switch_attr=switch_attr,
                                                             default_name=kwargs.get('default_name', None))
        # Add attrs
        if not node.has_attribute('switchAttrName'):
            node.addAttr('switchAttrName', dt='string')
        node.switchAttrName.set(switch_attr)

        # Set results
        m_matrix = result_multi['multi_matrix']
        d_matrix = result_multi['decomp_matrix']
        source_grp = result_multi['constraint_group']
        parent_grp = result_multi['parent_constraint_group']
        choice_offset = result_multi['choice_offset']
        choice_space = result_multi['choice_space']

        # Connect all the nodes
        node.connect_node(m_matrix, "multiMatrix", 'tekParent')
        node.connect_node(d_matrix, "decompMatrix", 'tekParent')
        node.connect_node(source_grp, "constraintGroup", 'tekParent')
        node.connect_node(parent_grp, "parentConstraintGroup", 'tekParent')
        node.connect_node(choice_offset, "choiceOffset", 'tekParent')
        node.connect_node(choice_space, "choiceSpace", 'tekParent')
        node.connect_node(source_object, 'sourceObject', parent_attr="sourceMultiConstraint")
        node.connect_node(switch_obj, 'switchObject', parent_attr="switchObject")

        # strip wrapped nodes
        node.connect_nodes(target_list, 'targets')

        return node

    def get_constraint_group(self):
        """
        Returns constraint group.

        :return: Returns constraint group.
        :rtype: pm.nt.Group
        """

        return self.constraintGroup.get()

    def get_parent_constraint_group(self):
        """
        Returns parent constraint group.

        :return: Returns parent constraint group.
        :rtype: pm.nt.Group
        """

        return self.parentConstraintGroup.get()

    def get_switch_attr(self):
        """
        Returns switch attr.

        :return: Returns switch attr.
        :rtype: str
        """

        return self.switchAttrName.get()

    def get_targets(self):
        """
        Returns multi targets, objects that can drive the source object.

        :return: Returns multi targets, objects that can drive the source object.
        :rtype: list(pm.nt.Transform)
        """

        return self.targets.listConnections()

    def get_source_object(self):
        """
        Returns the source object.  The object being driven.

        :return: Returns the source object.  The object being driven.
        :rtype: pm.nt.Transform
        """

        return self.sourceObject.get()

    def remove(self):
        switch_object = self.switchObject.get()
        source_object = self.get_source_object()

        attr_list = ['matrixConstraint', 'parentMatrixConstraint', 'parentConstraintObject', 'switchObject', '__']
        attr_list.append(self.get_switch_attr())

        for attr_name in attr_list:
            for multi_object in [switch_object, source_object]:
                if multi_object.hasAttr(attr_name):
                    multi_object.attr(attr_name).unlock()
                    multi_object.deleteAttr(attr_name)

        source_object.sourceMultiConstraint.unlock()
        source_object.deleteAttr('sourceMultiConstraint')

        constraint_group = self.get_constraint_group()
        parent_constraint_group = self.get_parent_constraint_group()
        pm.parent(pm.listRelatives(constraint_group), parent_constraint_group.getParent())
        pm.delete(parent_constraint_group, self.pynode, self.multiMatrix.get(), self.decompMatrix.get())

    def get_build_kwargs(self):
        """
        Gets a dictionary of kwargs that represent the build args of a component and their values on creation.

        :return: A dictionary of the names of kwargs for the component's build and their values on creation
        :rtype dict{}:
        """

        return_dict = {}
        if self.hasAttr('buildKwargs'):
            for attr in self.buildKwargs.children():
                attr_name = attr.attrName()
                if not attr_name.endswith('_hidden'):
                    return_dict[attr_name.replace('buildKwargs_', '')] = attr.get()
        return return_dict

    def get_flags(self):
        return []

