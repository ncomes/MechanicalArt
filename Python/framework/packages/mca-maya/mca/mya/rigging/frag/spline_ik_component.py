#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.common.utils import lists
from mca.mya.utils import attr_utils as attr_utils, constraint, dag
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import chain_markup, joint_utils, spline_ik_rig
from mca.mya.rigging.flags import frag_flag
# Internal module imports
from mca.mya.rigging.frag import keyable_component


class SplineIKComponent(keyable_component.KeyableComponent):
    VERSION = 1

    ATTACH_ATTRS = ['retract']

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent,
               start_joint,
               end_joint,
               leaf_joint_list,
               end_helper_joint,
               mid_helper_joint,
               side,
               region,
               start_helper_joint=None,
               mid_flag=True,
               can_retract=True,
               **kwargs):
        """
        This will create a new complex splineIK rig component for use within the FRAG system.

        :param FRAGNode frag_parent: FRAG Rig FRAGNode.
        :param Joint start_joint: Start joint of the chain.
        :param Joint end_joint: End joint of the chain.
        :param Joint start_helper_joint: A joint separated, but co-located with the start joint of the primary chain. If a joint is not supplied a flag will not be created for this.
        :param Joint end_helper_joint: A joint separated, but co-located with the end joint of the primary chain.
        :param Joint mid_helper_joint: A joint located between the start/end joint, but not part of the primary chain.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :param bool mid_flag: If we should create a mid component flag.
        :param bool can_retract: If this component will be setup with the ability to retract.
        :return: The newly created SplineIKComponent
        :rtype: SplineIKComponent
        """

        # serialize build kwargs for later.
        kwargs_dict = {}
        kwargs_dict['mid_flag'] = mid_flag
        kwargs_dict['can_retract'] = can_retract

        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = keyable_component.KeyableComponent.create(frag_parent,
                                                         SplineIKComponent.__name__,
                                                         SplineIKComponent.VERSION,
                                                         side=side,
                                                         region=region,
                                                         align_component=start_joint)

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        chain_between = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)
        # Get local level groups
        flag_grp = node.flagGroup.get()
        flag_grp_parent = flag_grp.getParent()

        mid_flag_grp = pm.group(n=f'flags_{side}_{region}_mid', em=True, w=True)
        mid_flag_grp.setParent(flag_grp_parent)

        main_flags_grp = pm.group(n=f'flags_{side}_{region}_main', em=True, w=True)
        pm.delete(pm.parentConstraint(flag_grp, main_flags_grp))
        pm.makeIdentity(main_flags_grp, apply=1, t=1, r=1, s=1)
        main_flags_grp.setParent(flag_grp_parent)

        mid_flag_grp.setParent(flag_grp)
        main_flags_grp.setParent(flag_grp)

        nt_grp = node.noTouch.get()

        # duplicate chain and set up the fk chain
        spline_joint_chain = joint_utils.duplicate_chain(start_joint, end_joint, suffix='spline_ik')
        spline_joint_chain[0].setParent(nt_grp)

        spline_ik_results = spline_ik_rig.spline_ctrl(spline_joint_chain, end_helper_joint, mid_helper_joint,
                                                      region, side, start_helper_joint=start_helper_joint, mid_flag=mid_flag, can_retract=can_retract, root_align_transform=True)
        spline_skin_cluster = spline_ik_results['spline_skin_cluster']
        mult_nodes = spline_ik_results['mult_nodes']
        info_node = spline_ik_results['info_node']
        ik_solver = spline_ik_results['ik_solver']

        if not start_helper_joint:
            # if we did not supply a start_helper_joint, constraint the alignment one to the flags group. This will
            # allow the base of the spline IK to follow the motion of its parent.
            constraint.parent_constraint_safe(main_flags_grp, spline_ik_results['start_helper_joint'], mo=True)

        if can_retract:
            if not mid_helper_joint.hasAttr('retract'):
                mid_helper_joint.addAttr('retract', dv=0, min=0, max=10, k=True)
            # drive the attr on our helper joint with the end flag attr.
            # this will help us restore animation if we need to bake from a skel.
            if start_helper_joint:
                spline_ik_results['flag_nodes'][2].retract >> mid_helper_joint.retract
            else:
                spline_ik_results['flag_nodes'][1].retract >> mid_helper_joint.retract
            motion_path = spline_ik_results['motion_path']
            remap_nodes = spline_ik_results['remap_nodes']
            condition = spline_ik_results['condition']
            constraint_reverse = spline_ik_results['reverse_nodes']

        if mid_flag:
            mid_joint_flag = spline_ik_results['flag_nodes'][-1]
            mid_joint_flag.get_align_transform().setParent(mid_flag_grp)

        # parent flag align groups to the rig flag group.
        pm.parent(spline_ik_results['do_not_touch'], nt_grp)
        for flag_node in spline_ik_results['flag_nodes']:
            if flag_node not in [spline_ik_results['aux_flag'], mid_joint_flag]:
                flag_node.get_align_transform().setParent(main_flags_grp)

        if can_retract:
            remap = pm.createNode(pm.nt.RemapValue, n=f'{region}_{side}_spline_ik_remap_end')
            remap.setAttr('outputMin', .001)
            remap_nodes.append(remap)
            spline_ik_results['orient_end'].sy >> remap.inputValue

        for driver_joint, chain_joint, leaf_joint in zip(spline_joint_chain[:-1]+[spline_ik_results['orient_end']], chain_between, leaf_joint_list):
            # connect our drive hierarchy joints to our live joints.
            constraint.parent_constraint_safe(driver_joint, chain_joint)
            # only drive the scale x the default component will only use this channel.
            # the leaper tongue component has other features that use sy/sz
            if leaf_joint != leaf_joint_list[-1]:
                # ignore the sx value on the last joint, causes some awkward stretching during normal use.
                driver_joint.sx >> leaf_joint.sx
            if can_retract:
                remap.outValue >> leaf_joint.sy
                remap.outValue >> leaf_joint.sz

        if can_retract:
            # if we can retract make sure that all downstream joints inherit the scale.
            # create remap to force a .001-1 range. Unreal does not like 0 value scales.
            for child_joint in chain_between[-1].listRelatives(ad=True, type=pm.nt.Joint):
                if child_joint not in leaf_joint_list:
                    # Little bit of a hack to make sure on retract we're uniformly scaling all child joints.
                    remap.outValue >> child_joint.sx
                    remap.outValue >> child_joint.sy
                    remap.outValue >> child_joint.sz

        alignment_joints = [start_helper_joint, end_helper_joint, mid_helper_joint] if start_helper_joint else [end_helper_joint, mid_helper_joint]
        node.connect_nodes(chain_between+alignment_joints, 'bindJoints')
        node.connect_nodes(spline_ik_results['flag_nodes'], 'flags', 'fragParent')
        node.connect_node(spline_ik_results['end_flag'], 'end_flag')
        node.connect_nodes(leaf_joint_list, 'leafJoints')
        node.connect_node(mid_helper_joint, 'helper_joint')
        node.connect_node(spline_skin_cluster, 'splineSkinCluster', 'fragParent')
        node.connect_node(ik_solver, 'ikSolver', 'fragParent')
        node.connect_node(mid_flag_grp, 'midFlagGroup', 'fragParent')
        node.connect_node(main_flags_grp, 'mainFlagsGroup', 'fragParent')

        if can_retract:
            node.connect_nodes(remap_nodes, 'remapNodes', 'fragParent')
            node.connect_node(motion_path, 'motionPath', 'fragParent')
            node.connect_nodes(mult_nodes, 'multNodes', 'fragParent')
            node.connect_node(condition, 'condition', 'fragParent')
            node.connect_node(constraint_reverse, 'reverseNodes', 'fragParent')
            node.connect_node(info_node, 'infoNode', 'fragParent')

        return node

    def get_flags(self):
        flags = self.flags.listConnections()
        flags = list(map(lambda x: frag_flag.Flag(x), flags))
        return flags

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

        flag_grp = self.pynode.getAttr('mainFlagsGroup')
        mid_flag_grp = self.pynode.getAttr('midFlagGroup')
        nt_grp = self.pynode.getAttr('noTouch')

        for align_grp in [flag_grp]:
            pm.delete(pm.listRelatives(align_grp, type=pm.nt.Constraint))

        attr_utils.set_attr_state(nt_grp, False, attr_utils.TRANSLATION_ATTRS + attr_utils.ROTATION_ATTRS)

        if point:
            constraint.parent_constraint_safe(parent_object_list, flag_grp, mo=1, skip_rotate_attrs=['x', 'y', 'z'])

        if orient:
            constraint.parent_constraint_safe(parent_object_list, flag_grp, mo=1, skip_translate_attrs=['x', 'y', 'z'])

        if mid_flag_grp:
            constraint.point_constraint_safe(parent_object_list + [self.pynode.end_flag.get()], mid_flag_grp, mo=1)


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

    def attach_to_skeleton(self, attach_skeleton_root, mo=True):
        """
        Drive the component with a given skeleton.

        :param Joint attach_skeleton_root: Top level joint of the hierarchy to drive the component.
        :param bool mo: If object offsets should be maintained.
        :return: A list of all created constraints.
        :rtype: list[Constraint]
        """

        target_root_hierarchy = chain_markup.ChainMarkup(attach_skeleton_root)
        constraint_list = []

        # get a list of all our flags.
        flag_list = self.get_flags()
        flags_to_constrain = []
        # find out if we expect a mid flag
        has_mid_flag = self.getAttr('buildKwargs_mid_flag')
        mid_flag = None
        if has_mid_flag:
            mid_flag = flag_list[-1]
        # find out if we also have a start flag min flag are end, end aux, +1 for mid +1 for start 2-4 flags total
        has_start_flag = len(flag_list) == 3+int(has_mid_flag)
        if has_start_flag:
            start_flag = flag_list[0]
            end_flag = flag_list[2]
            flags_to_constrain = [start_flag, end_flag, mid_flag] if mid_flag else [start_flag, end_flag]
        else:
            end_flag = flag_list[1]
            flags_to_constrain = [end_flag, mid_flag] if mid_flag else [end_flag]
        # setup our slice index for our bind joints. There will always be a mid helper even if there is not a mid flag.
        # So we're expecting the full chain and then 2-3 joints for helping recover animation.
        expected_bind_joints = 2+int(has_start_flag)

        bind_joint_list = self.bind_joints[-1 * expected_bind_joints:]
        if not has_mid_flag:
            # if we don't have a mid flag, pop off the mid_helper joint.
            bind_joint_list.pop(-1)
        # slice will always be, last of the chain joints, for end aux
        # then in order: start_helper, end_helper, mid_helper | this will line up with the flag list, including if elements are missing.

        if len(flags_to_constrain) == len(bind_joint_list):
            for wrapped_flag, joint_node in zip(flags_to_constrain, bind_joint_list):
                wrapped_node = chain_markup.JointMarkup(joint_node)
                found_joint = target_root_hierarchy.get_start(wrapped_node.region, wrapped_node.side)
                if found_joint:
                    constraint_list.append(constraint.parent_constraint_safe(found_joint, wrapped_flag))

            end_flag = self.getAttr('end_flag')
            wrapped_mid_helper = chain_markup.JointMarkup(self.getAttr('helper_joint'))
            bind_mid_helper = target_root_hierarchy.get_start(wrapped_mid_helper.region, wrapped_mid_helper.side)
            if bind_mid_helper:
                for attr_name in self.ATTACH_ATTRS:
                    # handle attrs that were baked to the skeleton.
                    if bind_mid_helper.hasAttr(attr_name):
                        bind_mid_helper.attr(attr_name) >> end_flag.attr(attr_name)

        return constraint_list
