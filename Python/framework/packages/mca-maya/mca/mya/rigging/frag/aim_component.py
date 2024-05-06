#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports

# Software specific imports
import pymel.core as pm
# mca Python imports
from mca.common import log
from mca.mya.utils import attr_utils
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging.frag import keyable_component
from mca.mya.rigging import rig_aim_joint
from mca.mya.rigging.flags import frag_flag
from mca.common.utils import lists
# internal module imports

logger = log.MCA_LOGGER


class AimComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent,
                bind_joint,
                side,
                region,
                aim_target=None,
                flag_distance=20,
                aim_axis=(1, 0, 0),
                up_axis=(0, 0, 1),
                proxy=False):
        """
        Creates an aim component for a single object.

        :param FRAGNode frag_parent: FRAG Rig FRAGNode.
        :param pm.nt.Joint bind_joint: Joint that will be the aim joint.
        :param string side: the side in which the eye is on the face. Examples: 'right', 'left', 'back_left'
        :param string region: Name of the region.  Ex: 'Eye'
        :param float flag_distance: distance between start_joint and the flag
        :param vector aim_axis: which direction in local space is up.
        :param vector up_axis: which axis + or negative will be pointing down the joint in local space.
        :param bool proxy: if True then it won't affect the bind joints.
        :return: Returns the AimComponent component.
        :rtype: AimComponent
        """

        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        # serialize build kwargs for later.
        kwargs_dict = {}
        kwargs_dict['aim_target'] = aim_target if aim_target else None
        kwargs_dict['flag_distance'] = flag_distance
        kwargs_dict['aim_axis'] = aim_axis
        kwargs_dict['up_axis'] = up_axis
        kwargs_dict['proxy'] = proxy

        node = keyable_component.KeyableComponent.create(frag_parent,
                                                            AimComponent.__name__,
                                                            AimComponent.VERSION,
                                                            side=side,
                                                            region=region,
                                                            align_component=bind_joint)

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        aim_dict = rig_aim_joint.rig_aim_joint(bind_joint=bind_joint,
                                                    flag_distance=flag_distance,
                                                    aim_axis=aim_axis,
                                                    up_axis=up_axis,
                                                    proxy=proxy)

        aim_flag = aim_dict['flag']
        rotate_loc = aim_dict['rotate_locator']
        up_loc = aim_dict['up_locator']
        rotate_loc_align_grp = aim_dict['rotate_loc_align_grp']
        pm.parent(rotate_loc_align_grp, nt_grp)

        bind_joint.setAttr('side', aim_flag.getAttr('side'))
        bind_joint.setAttr('type', aim_flag.getAttr('type'))
        bind_joint.setAttr('otherType', aim_flag.getAttr('otherType'))

        aim_align_grp = aim_flag.get_align_transform()
        pm.parent(aim_align_grp, flag_grp)

        pm.parent(rotate_loc, rotate_loc_align_grp)
        pm.parent(up_loc, rotate_loc_align_grp)

        # Connect to nodes
        node.connect_node(aim_flag, 'flag', 'fragParent')
        node.connect_node(bind_joint, 'bindJoints', 'fragParent')
        node.connect_node(rotate_loc, 'rotateObject', 'fragParent')

        node.addAttr('distance', at='float')
        node.distance.set(flag_distance)
        node.addAttr('aimAxis', at='float3')
        node.addAttr('aimAxisX', at='float', parent='aimAxis')
        node.addAttr('aimAxisY', at='float', parent='aimAxis')
        node.addAttr('aimAxisZ', at='float', parent='aimAxis')
        node.aimAxis.set(aim_axis)
        node.addAttr('upAxis', at='float3')
        node.addAttr('upAxisX', at='float', parent='upAxis')
        node.addAttr('upAxisY', at='float', parent='upAxis')
        node.addAttr('upAxisZ', at='float', parent='upAxis')
        node.upAxis.set(up_axis)

        return node

    def get_aim_flag(self):
        """
        Returns the connected flag.

        :return: Returns the connected flag.
        :rtype: frag.Flag
        """
        _flag = self.flag.listConnections()
        if _flag:
            _flag = lists.get_first_in_list(_flag)
            return frag_flag.Flag(_flag)
        return

    def get_flags(self):
        """
        Returns the connected flags.

        :return: Returns the connected flags.
        :rtype: list(flag.Flag)
        """

        flags = self.flag.listConnections()
        if not flags:
            logger.warning(f'{self.pynode}: Does not have any flags')
            return
        flags = list(map(lambda x: frag_flag.Flag(x), flags))
        return flags

    def select_flag(self):
        """
        Selects all the flags associated with the rig implementation.
        """

        pm.select(self.get_aim_flag())

    def key_flag(self):
        """
        Keys all the flags associated with the rig implementation.
        """
        flag = self.get_aim_flag()
        pm.setKeyframe(flag, shape=0)

    def to_default_pose(self):
        """
        Moves the rig implementation back to the default pose.
        """
        flags = self.get_flags()
        for _flag in flags:
            attr_utils.reset_attrs(_flag)

    def get_aim_axis(self):
        """
        Returns the aim axis. The axis which is pointing to the aim object.

        :return:  Returns the aim axis as a vector.
        :rtype: dt.Vector
        """

        return pm.dt.Vector(self.aimAxis.get())

    def get_up_axis(self):
        """
        Returns the up axis. The axis which is pointing to the up object.

        :return:  Returns the up axis as a vector.
        :rtype: dt.Vector
        """

        return pm.dt.Vector(self.upAxis.get())

    def get_rotate_object(self):
        """
        Returns the object that is using the aim constraint.  This is usually a locator in which the bind joint
        gets constrained to.

        :return: Returns the object that is using the aim constraint.
        :rtype: pm.nt.Transform
        """

        return self.rotateObject.listConnections()[0]

    def get_eye_rotations(self):
        """
        Returns the rotation value of the eyes

        :return: left_eye_right_left, + = degrees right, - = degrees left
        left_eye_up_down, + = degrees up, - = degrees down
        right_eye_right_left, + = degrees right, - = degrees left
        right_eye_up_down, + = degrees up, - = degrees down
        :rtype: list(float)
        """

        # Assumes up axis is [0,1,0] and forward axis is [0,0,1]
        r_object = self.get_rotate_object()
        r_rot = r_object.rotate.get()
        return [-r_rot[1], -r_rot[0]]
