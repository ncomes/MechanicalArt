#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.utils import constraint
from mca.mya.animation import baking
# Internal module imports
from mca.mya.rigging.frag import rig_component


class KeyableComponent(rig_component.RigComponent):
    """
    All flag based FRAG components should be of this type.
    This would include keyable elements like FKComponents.

    """

    @staticmethod
    def create(frag_parent, frag_type, version, side, region, align_component=None):
        """

        :param frag_parent:
        :param frag_type:
        :param version:
        :param side:
        :param region:
        :param align_component:
        :return:
        """
        node = rig_component.RigComponent.create(frag_parent,
                                                    frag_type,
                                                    version,
                                                    side=side.lower(),
                                                    region=region,
                                                    align_component=align_component)
        flag_group = pm.group(empty=1, n="flags_{0}_{1}".format(side, region))
        if align_component:
            pm.delete(pm.parentConstraint(align_component, flag_group))
        pm.makeIdentity(flag_group, apply=1, t=1, r=1, s=1)
        # Add Attributes and connect attributes
        node.connect_node(flag_group, 'flagGroup', 'fragParent')
        if frag_parent.get_type() == "FRAGRig":
            flag_group.setParent(frag_parent.flagsAll.get())
        return node

    # quick access properties
    @property
    def flag_group(self):
        return self.getAttr('flagGroup')

    @property
    def bind_joints(self):
        if self.pynode.hasAttr('bindJoints'):
            return self.pynode.getAttr('bindJoints')
        return []

    def remove(self):
        """
        Remove this component and its build groups.

        :return:
        """
        pm.delete([self.no_touch_grp, self.flag_group, self.pynode])

    def bake_to_skeleton(self, bake_range=None, **kwargs):
        """
        Pass bind joints to bake function.
        :param list[int, int] bake_range: Two ints representing a range of frame values to bake between.
        :param dict kwargs: A list of args to pass to bakeResults.
        """

        bind_joint_list = self.bindJoints.listConnections()
        extra_attrs = []
        for bind_joint in bind_joint_list:
            # check for keyable custom attrs.
            extra_attrs += bind_joint.listAttr(ud=True, k=True)
        baking.bake_objects(bind_joint_list, bake_range=bake_range, custom_attrs=extra_attrs, **kwargs)

    def attach_to_skeleton(self, *args, **kwargs):
        """
        Drive the component with a given skeleton.

        :return: A list of all constraints created during the attachment process.
        :rtype: list[Constraint]
        """

        return []

    def get_bakeable_rig_nodes(self):
        """
        Returns a list of bakeable flags and the helpers/constraints driving them.

        :return: A list of transforms, keyable attrs, and things to remove after baking.
        :rtype: list[Transform], list[str] list[PyNode]
        """

        flag_list = self.get_flags()
        things_to_delete = []
        attr_list = []
        bakeable_flags = []
        for flag_node in flag_list:
            constraint_list = flag_node.getChildren(type=pm.nt.ParentConstraint)
            for constraint_node in constraint_list:
                things_to_delete += [x for x in constraint.get_constraint_targets(constraint_node) if hasattr(x, 'bake_helper')]
            things_to_delete += constraint_list
            # only return attributes with an incoming connection
            # $Hack FSchorsch fuck toeTap why is it on the offset flag as a pass through.
            # it can't be keyed and it can't be set there.
            # scooping it here causes a bake failure down range cause Maya is a drama queen.
            attr_list += [x.attrName() for x in flag_node.listAttr(ud=True, keyable=True, settable=True) if x.listConnections(d=False and x.attrName() not in ['toeTap'])]
            if constraint_list or attr_list:
                bakeable_flags.append(flag_node)

        return bakeable_flags, attr_list, things_to_delete

    def get_bakeable_skeleton_nodes(self):
        """
        Returns a list of driven joints.

        :return: A list of joints this component is driving.
        :rtype: list[Joint]
        """

        return self.bindJoints.listConnections()

    def set_scale(self):
        """
        overridable function to handle this component's scale attachment settings.

        """
        pass
