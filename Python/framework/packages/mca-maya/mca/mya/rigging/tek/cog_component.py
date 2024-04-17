#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Center Of Gravity Component.
"""

# System global imports
# software specific imports
import pymel.core as pm
# mca python imports
from mca.mya.utils import attr_utils, constraint, dag, naming
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import joint_utils
from mca.mya.rigging import chain_markup, cog_chain_rig
from mca.mya.rigging.flags import tek_flag
# internal module imports
from mca.mya.rigging.tek import keyable_component


class CogComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(tek_parent,
                start_joint,
                end_joint,
                side,
                region,
                scale=1.0,
                orientation=(-90,0,0), **kwargs):
        """
        Creates an COG component.

        :param TEKNode tek_parent: TEK Rig TEKNode.
        :param pm.nt.Joint start_joint: Start joint of the chain.
        :param pm.nt.Joint end_joint: End joint of the chain.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :return: Returns an instance of IKFKComponent.
        :rtype: IKFKComponent
        """

        # serialize build kwargs for later.
        kwargs_dict = {}
        kwargs_dict['scale'] = scale
        kwargs_dict['orientation'] = orientation

        # Set Namespace
        root_namespace = tek_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = keyable_component.KeyableComponent.create(tek_parent,
                                                                            CogComponent.__name__,
                                                                            CogComponent.VERSION,
                                                                            side=side,
                                                                            region=region,
                                                                            align_component=start_joint)

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        chain_between = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        # Create the FK Chain ##############
        # Cog should only ever be a single joint.
        chain_cog = [joint_utils.duplicate_joint(start_joint, f'cog_chain_{naming.get_basename(start_joint)}')]
        chain_cog_result = cog_chain_rig.cog_chain(chain_cog[0],
                                                    chain_cog[-1],
                                                    scale=scale,
                                                    orientation=orientation)

        # Organize the groups
        cog_flag = chain_cog_result['flags'][0]
        cog_zero_grp = cog_flag.get_align_transform()
        pm.parent(cog_zero_grp, flag_grp)
        chain_cog[0].setParent(nt_grp)

        # Add attributes and connect
        node.connect_node(cog_flag, 'cogFlag', 'tekParent')
        node.connect_nodes(chain_cog, 'cogChain', 'tekParent')
        node.connect_nodes([start_joint], 'bindJoints')

        # Lock and hide attrs
        cog_flag.lock_and_hide_attrs(['sx', 'sy', 'sz', 'v'])

        return node

    def get_flags(self):
        return [tek_flag.Flag(self.cogFlag.get())]

    def attach_to_skeleton(self, attach_skeleton_root, mo=True):
        """
        Drive the component with a given skeleton.

        :param Joint attach_skeleton_root: Top level joint of the hierarchy to drive the component.
        :param bool mo: If object offsets should be maintained.
        :return: A list of all created constraints.
        :rtype list[Constraint]:
        """

        target_root_hierarchy = chain_markup.ChainMarkup(attach_skeleton_root)
        constraint_list = []

        flag_list = self.get_flags()
        flag_node = flag_list[0] if flag_list else None

        bind_joint_list = self.bind_joints

        skel_region = None
        skel_side = None
        if bind_joint_list:
            wrapped_node = chain_markup.JointMarkup(bind_joint_list[0])
            skel_region = wrapped_node.region
            skel_side = wrapped_node.side

        skel_region = skel_region or self.region
        skel_side = skel_side or self.side

        joint_list = target_root_hierarchy.get_full_chain(skel_region, skel_side)
        if not joint_list:
            # We'll likely need to cascade through a few of these, since hte COG isn't associated with a joint,
            # and it's region/side markup doesn't match the skeletons as well.
            joint_list = [target_root_hierarchy.hierarchyStart]
            if not joint_list:
                joint_list = target_root_hierarchy.get_full_chain('pelvis', 'center')

        joint_node = joint_list[0] if joint_list else None
        if joint_node and flag_node:
            constraint_node = constraint.parent_constraint_safe(joint_node,
                                                                flag_node,
                                                                skip_rotate_attrs=['x', 'y', 'z'],
                                                                mo=mo)
            if constraint_node:
                constraint_list.append(constraint_node)
        return constraint_list
