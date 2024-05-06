#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.utils import naming
from mca.common.utils import lists
from mca.mya.rigging.flags import frag_flag
from mca.mya.rigging import chain_markup
from mca.mya.utils import attr_utils, constraint
# Internal module imports
from mca.mya.rigging.frag import frag_base


class RigComponent(frag_base.FRAGNode):
    """
    All FRAG rig components should be of this type.
    This represents the base node for all potential FRAG components that could be used with a rig.
    This class would include support rig elements like twist helpers

    """

    @staticmethod
    def create(frag_parent, frag_type, version, side, region, align_component=None):

        # create the base rig component
        node = frag_base.FRAGNode.create(frag_parent, frag_type, version)
        pm.rename(node, '{0}_{1}_{2}'.format(naming.get_basename(node), side, region))
        # Create Do_Not_Touch group
        nt_grp = pm.group(em=1, n="NO_TOUCH_{0}_{1}".format(side, region))
        # If the group node needs to be aligned, align it to an object
        if align_component:
            align_component = pm.PyNode(align_component)
            pm.delete(pm.parentConstraint(align_component, nt_grp, w=True, mo=False))
        # Zero out the attributes and lock and hide them
        pm.makeIdentity(nt_grp, apply=1, t=1, r=1, s=1)
        nt_grp.v.set(0)
        attr_utils.lock_all_keyable_attrs(nt_grp)
        # Parent the ToNotTouch node under the main do not touch node
        if frag_parent.get_type() == "FRAGRig":
            nt_grp.setParent(frag_parent.doNotTouch.get())

        node.connect_node(nt_grp, 'noTouch', 'fragParent')
        # Add rig attributes
        node.side = side
        node.region = region

        # This is a list of child components attached to this FRAG node.
        node.addAttr("childAttachments", at='message', m=True) # ToDo change this to a compound attribute

        # This is the first orient attach parent component.
        node.addAttr("orientParentAttachments", at="message", m=True)
        # This is a list of orient attach parent objects.
        node.addAttr("orientParentObjects", at="message", m=True)

        # This is the first point attach parent component.
        node.addAttr("pointParentAttachments", at="message", m=True)
        # This is a list of point attach parent  objects.
        node.addAttr("pointParentObjects", at="message", m=True)

        return node

    # quick access properties
    @property
    def no_touch_grp(self):
        return self.getAttr('noTouch')

    def _connect_parent(self, node, attach_attr):
        current_index = 0
        for entry in attach_attr.iterDescendants(1):
            current_index = entry.index() + 1
        node.message >> attach_attr[current_index]

    def attach_component(self, parent_component_list, parent_object_list, point=True, orient=True):
        """
        Constrain the flag and no touch groups to a list of given parent objects for point and orient.

        :param list[FRAGNode] parent_component_list: The FRAG Nodes that should be registered as parents for attachment.
        :param list[Transform] parent_object_list: A list of transforms this component should be constrainted between.
        :param bool point: If this FRAG component should constrain its translation.
        :param bool orient: If this FRAG component should constrain its rotation.
        """
        # Get local level groups
        if not parent_object_list or not parent_component_list or not any([point, orient]):
            return

        if not isinstance(parent_object_list, list):
            parent_object_list = [parent_object_list]

        if not isinstance(parent_component_list, list):
            parent_component_list = [parent_component_list]

        flag_grp = self.pynode.getAttr('flagGroup')
        nt_grp = self.pynode.getAttr('noTouch')

        for align_grp in [flag_grp, nt_grp]:
            # Reset the constraints by stripping the old ones.
            pm.delete(pm.listRelatives(align_grp, type=pm.nt.Constraint))

        attr_utils.set_attr_state(nt_grp, False, attr_utils.TRANSLATION_ATTRS + attr_utils.ROTATION_ATTRS)

        if point:
            constraint.parent_constraint_safe(parent_object_list, flag_grp, mo=1, skip_rotate_attrs=['x', 'y', 'z'])
            constraint.parent_constraint_safe(parent_object_list, nt_grp, mo=1, skip_rotate_attrs=['x', 'y', 'z'])

        if orient:
            constraint.parent_constraint_safe(parent_object_list, flag_grp, mo=1, skip_translate_attrs=['x', 'y', 'z'])
            constraint.parent_constraint_safe(parent_object_list, nt_grp, mo=1, skip_translate_attrs=['x', 'y', 'z'])

        self.pointParentAttachments.disconnect()
        self.orientParentAttachments.disconnect()
        for node in parent_component_list:
            if point:
                self._connect_parent(node, self.pointParentAttachments)
            if orient:
                self._connect_parent(node, self.orientParentAttachments)

        for node in parent_object_list:
            if point:
                self._connect_parent(node, self.pointParentObjects)
            if orient:
                self._connect_parent(node, self.orientParentObjects)

        attr_utils.set_attr_state(nt_grp, True, attr_utils.TRANSLATION_ATTRS + attr_utils.ROTATION_ATTRS)

    def _return_frag_attachments(self, attached_frag_list):
        components = [frag_base.FRAGNode(x) for x in attached_frag_list]
        return components

    @property
    def attached_children(self):
        return self._return_frag_attachments(self.pynode.getAttr('childAttachments'))

    @property
    def attached_frag_parents(self):
        return self._return_frag_attachments(self.pynode.getAttr('pointParentAttachments'))

    @property
    def orient_frag_parents(self):
        return self._return_frag_attachments(self.pynode.getAttr('orientwintParentAttachments'))

    @property
    def point_object_parents(self):
        return self.pynode.getAttr('pointParentObjects')

    @property
    def orient_object_parents(self):
        return self.pynode.getAttr('orientParentObjects')

    def get_build_kwargs(self):
        """
        Gets a dictionary of kwargs that represent the build args of a component and their values on creation.

        :return: A dictionary of the names of kwargs for the component's build and their values on creation
        :rtype: dict{}
        """

        return_dict = {}
        if self.hasAttr('buildKwargs'):
            for attr in self.buildKwargs.children():
                attr_name = attr.attrName()
                if not attr_name.endswith('_hidden'):
                    return_dict[attr_name.replace('buildKwargs_', '')] = attr.get()
        return return_dict

    def serialize_component(self):
        """
        Converts a FRAG component into a dictionary of build instructions for regeneration later.

        :return: A dictionary containing all notable information to recreate this instance of a rig component.
        :rtype: dict{}
        """

        data_dict = {}
        data_dict['build_vars'] = {'side': self.side,
                                   'region': self.region,
                                   'type': self.get_type()}
        data_dict['build_vars']['skeleton'] = {}
        if hasattr(self, 'bindJoints'):
            found_joint = lists.get_first_in_list(self.bindJoints.listConnections())
            if found_joint:
                joint_node = chain_markup.JointMarkup(found_joint)
                skeleton_side = joint_node.side
                skeleton_region = joint_node.region
                data_dict['build_vars']['skeleton'] = {'side': skeleton_side,
                                                       'region': skeleton_region}
        kwargs_dict = self.get_build_kwargs()
        data_dict['build_vars']['kwargs'] = kwargs_dict

        constraint_dict = {}
        data_dict['constraints'] = constraint_dict
        primary_constraint_dict = {}
        for attr_list, constraint_type in [(attr_utils.TRANSLATION_ATTRS, 'point'), (attr_utils.ROTATION_ATTRS, 'orient'), (attr_utils.SCALE_ATTRS, 'scale')]:
            axis_constraint_list = []
            for attr_name in attr_list:
                constraint_node = lists.get_first_in_list(self.noTouch.get().attr(attr_name).listConnections(type=pm.nt.Constraint))
                if constraint_node and constraint_node not in axis_constraint_list:
                    # this handles the components primary attach configuration.
                    if 'primary' not in data_dict['constraints']:
                        data_dict['constraints']['primary'] = primary_constraint_dict

                    axis_constraint_list.append(constraint_node)
                    primary_constraint_dict[constraint_type] = {}

                    target_node = lists.get_first_in_list(constraint.get_constraint_targets(constraint_node))
                    if not target_node:
                        continue

                    if not primary_constraint_dict[constraint_type]:
                        if frag_flag.is_flag_node(target_node):
                            # we have a flag
                            constraint_data_dict = {}
                            flag_node = frag_flag.Flag(target_node)
                            rig_node = frag_base.FRAGNode(flag_node.fragParent.get())
                            constraint_data_dict['side'] = rig_node.side
                            constraint_data_dict['region'] = rig_node.region
                            constraint_data_dict['index'] = rig_node.get_flags().index(flag_node)
                            constraint_data_dict['type'] = 'flag'
                            primary_constraint_dict[constraint_type] = constraint_data_dict
                        elif isinstance(target_node, pm.nt.Joint):
                            # we have a joint
                            constraint_data_dict = {}
                            joint_node = chain_markup.JointMarkup(target_node)
                            joint_side = joint_node.side
                            constraint_data_dict['side'] = joint_side
                            constraint_data_dict['region'] = joint_node.region
                            constraint_data_dict['index'] = joint_node.get_joint_index()
                            constraint_data_dict['type'] = 'joint'
                            primary_constraint_dict[constraint_type] = constraint_data_dict

                    if 'attach_component' not in primary_constraint_dict:
                        constraint_data_dict = {}
                        primary_constraint_dict['attach_component'] = constraint_data_dict

                        parent_component = getattr(self, 'get_{}_attach_component'.format(constraint_type))()
                        constraint_data_dict['side'] = parent_component.side
                        constraint_data_dict['region'] = parent_component.region
        if hasattr(self, 'get_flags'):
            # we have a rig component with flags.
            # this handles any multiconstraints attached to this rig component.

            flag_node_list = self.get_flags()
            multiconstraint_dict = {}
            for index, wrapped_flag_node in enumerate(flag_node_list):
                if wrapped_flag_node.node.hasAttr('sourceMultiConstraint'):
                    multiconstraint_node = frag_base.FRAGNode(wrapped_flag_node.sourceMultiConstraint.get())

                    if len(multiconstraint_node.get_targets()) < 1:
                        continue

                    if 'multiconstraint' not in data_dict['constraints']:
                        data_dict['constraints']['multiconstraint'] = multiconstraint_dict

                    multiconstraint_dict[index] = multiconstraint_node.serialize_component()
        return data_dict


