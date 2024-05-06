"""
purpose: single fk component. Single joint with translate and rotation options available
"""

# System global imports
# Software specific imports
import logging

import pymel.core as pm

# mca Python imports
from mca.common import log
from mca.mya.modifiers import ma_decorators
from mca.mya.modifiers import ma_decorators
from mca.mya.animation import anim_curves
from mca.mya.rigging import chain_markup

# internal module imports
from mca.mya.rigging.frag import aim_component


logger = log.MCA_LOGGER


class EyeComponent(aim_component.AimComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent,
                bind_joint,
                side,
                region,
                aim_target=None,
                flag_distance=20,
                aim_axis=(0, -1, 0),
                up_axis=(0, 0, 1),
                proxy=False):
        """
        Creates an eye component for a single object.

        :param FRAGNode frag_parent: FRAG Rig FRAGNode.
        :param pm.nt.Joint bind_joint: Joint that will be the aim joint.
        :param string side: the side in which the eye is on the face. Examples: 'right', 'left', 'back_left'
        :param string region: Name of the region.  Ex: 'Eye'
        :param float flag_distance: distance between start_joint and the flag
        :param vector aim_axis: which direction in local space is up.
        :param vector up_axis: which axis + or negative will be pointing down the joint in local space.
        :param bool proxy: if True then it won't affect the bind joints.
        :return: Returns the AimComponent component.
        :rtype: EyeComponent
        """

        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = aim_component.AimComponent.create(frag_parent=frag_parent,
                                                    bind_joint=bind_joint,
                                                    side=side,
                                                    region=region,
                                                    aim_target=aim_target,
                                                    flag_distance=flag_distance,
                                                    aim_axis=aim_axis,
                                                    up_axis=up_axis,
                                                    proxy=proxy)

        new_name = f'{EyeComponent.__name__}_{side}_{region}'
        node.pynode.rename(new_name)
        node.set_version(EyeComponent.VERSION)
        node.pynode.fragType.set(EyeComponent.__name__)

        node.pynode.addAttr('poseLocators', at='message')

        node.pynode.addAttr('parameters', numberOfChildren=6, attributeType='compound', multi=True)
        node.pynode.addAttr('parameter', dt='string', parent='parameters')
        node.pynode.addAttr('controlStart', at='float', parent='parameters')
        node.pynode.addAttr('controlEnd', at='float', parent='parameters')
        node.pynode.addAttr('controlAttr', attributeType='message', parent='parameters')
        node.pynode.addAttr('faceParameters', attributeType='message', parent='parameters')
        node.pynode.addAttr('poseFrame', at='float', parent='parameters')
        node.pynode.addAttr('isFragFace', at='bool', dv=True)

        node = EyeComponent(node)

        # Tracking the eye translate so we can re-animate easier.

        eye_joint = node.bind_joints
        if not isinstance(eye_joint, pm.nt.Joint):
            eye_joint = pm.PyNode(eye_joint)
        eye_flag = node.get_aim_flag()

        if not eye_joint.hasAttr('flagTx'):
            eye_joint.addAttr('flagTx', at='float', k=True, h=True)
        if not eye_joint.hasAttr('flagTy'):
            eye_joint.addAttr('flagTy', at='float', k=True, h=True)
        if not eye_joint.hasAttr('flagTz'):
            eye_joint.addAttr('flagTz', at='float', k=True, h=True)

        eye_flag.tx >> eye_joint.flagTx
        eye_flag.ty >> eye_joint.flagTy
        eye_flag.tz >> eye_joint.flagTz

        return node

    def get_flag_attr(self, pose_name):
        """

        :param str pose_name: name of the pose.
        :return: Returns the flag attribute the pose is connected.
        :rtype: pm.nt.general.Attribute
        """

        flag_attr = self.attr(pose_name).controlAttr.listConnections(plugs=True)
        if not flag_attr:
            return
        return flag_attr[0]

    def get_min_pose_value(self, pose_name):
        """
        Returns the min rotation value of a pose.

        :param string pose_name: name of the pose.
        :return: Returns the min rotation value of a pose.
        :rtype: float
        """

        min_val = None
        if self.pynode.hasAttr(pose_name):
            block = self.pynode.attr(pose_name)
            min_val = block.controlStart.get()
        return min_val

    def get_max_pose_value(self, pose_name):
        """
        Returns the max rotation value of a pose.

        :param string pose_name: name of the pose.
        :return: Returns the max rotation value of a pose.
        :rtype: float
        """

        max_val = None
        if self.pynode.hasAttr(pose_name):
            block = self.pynode.attr(pose_name)
            max_val = block.controlEnd.get()
        return max_val

    def get_parameters_node(self, pose_name):
        """
        Returns the parameters node that has all the pose values.

        :param str pose_name: name of the pose.
        :return: Returns the parameters node that has all the pose values.
        :rtype: FRAGFaceParameters
        """

        parameters_node = None
        if self.pynode.hasAttr(pose_name):
            block = self.pynode.attr(pose_name)
            parameters_node = block.input.get()
        return parameters_node

    # FaceParameterInput Overdrive
    def config_input(self, obj, attr_name, min_value, max_value, parameter_name, face_parameters_node, pose_frame):
        """
        Gives information which should be stored for correct information later, info needed for set_parameter

        :param nt.PyNode obj: object that will have an attribute added to.
        Must be connected to a Frag node or be a FRAG node.
        :param str attr_name: Attribute name to that connects to the blend shape
        :param float min_value: min value
        :param float max_value: Max value
        :param str parameter_name: Name of the pose
        :param float pose_frame: frame number to set keyframe
        :param FRAGFaceParameters face_parameters_node: The parameter node.s
        :return: Returns the obj
        :rtype: nt.PyNode
        """

        block = self.parameters[self.parameters.numElements()]
        block.parameter.set(parameter_name)
        block.controlStart.set(min_value)
        block.controlEnd.set(max_value)
        block.setAlias(parameter_name)
        block.poseFrame.set(pose_frame)
        obj.attr(attr_name) >> block.controlAttr
        face_parameters_node.message >> block.faceParameters

    def convert_rotation_to_translate(self, rot_value, rot_axis):
        """
        Returns the value of the rotation aim flag so we can key it later.

        :param float rot_value: Rotation value a single attribute.
        :param str rot_axis: the attribute to set the value.
        :return: Returns the value of the rotation aim flag so we can key it later.
        """

        if isinstance(rot_axis, pm.nt.general.Attribute) or '.' in str(rot_axis):
            rot_axis = rot_axis.split('.')[-1]

        eye_flag = self.get_aim_flag()
        locators = self.create_rotate_pose_locators()
        pm.makeIdentity(locators[0], apply=True, t=True, r=True, s=True, pn=True, n=0)
        constraint = pm.pointConstraint(locators[1], eye_flag, w=1, mo=False)

        loc_val = locators[0].attr(rot_axis).get()
        locators[0].attr(rot_axis).set(rot_value + loc_val)
        value = eye_flag.translate.get()
        locators[0].attr(rot_axis).set(0)
        pm.delete(constraint, locators)
        return value

    def create_rotate_pose_locators(self):
        """
        Creates locators to help plot where to set the rotation aim controls.

        :return: Returns a locator positioned at the rotation and a locator out away from the rotation
                        to position the flag.
        :rtype: list(float)
        """

        bind_joint = self.bind_joints
        eye_flag = self.get_flag()
        rot_temp = pm.joint(n='rot_temp_loc')
        rot_target = pm.joint(n='rot_target_temp_loc')
        pm.parent(rot_temp, w=True)
        pm.makeIdentity(rot_temp, apply=True, t=True, r=True, s=True, pn=True, n=0)

        pm.delete(pm.parentConstraint(bind_joint, rot_temp, w=1, mo=False))
        pm.delete(pm.pointConstraint(eye_flag, rot_target, w=1, mo=False))

        pm.delete(pm.pointConstraint(bind_joint, rot_temp, w=1, mo=False))
        return [rot_temp, rot_target]

    def keyframe_flags_max_values(self):
        """
        Sets a keyframe for the pose on the max value on the correct pose frame.
        """

        num_elements = self.pynode.parameters.numElements()
        eye_flag = self.get_flag()
        for x in range(num_elements):
            pose_name = self.pynode.parameters[x].parameter.get()
            max_value = self.get_max_pose_value(pose_name)
            attr_control = self.pynode.parameters[x].controlAttr.listConnections(p=True)[0]
            pose_frame = self.pynode.parameters[x].poseFrame.get()
            value = round(self.convert_rotation_to_translate(max_value, attr_control), 4)

            self.set_padded_keys(obj=eye_flag, frame=pose_frame, value=value)
            eye_flag.translate.set(0, 0, 0)

    @staticmethod
    def set_padded_keys(obj, frame, value):
        """
        Sets the keys on the eye flag's attribute

        :param pm.nt.attribute obj: attribute name
        :param float frame: frame number
        :param float value: value the flag attribute is set to.
        """

        pm.setKeyframe(obj.translateX, t=[frame], v=value[0])
        pm.setKeyframe(obj.translateY, t=[frame], v=value[1])
        pm.setKeyframe(obj.translateZ, t=[frame], v=value[2])
        keyed_frames = pm.keyframe(obj, q=True)
        if not frame - 1 in keyed_frames:
            obj.translate.set((0, 0, 0))
            pm.setKeyframe(obj, t=[frame - 1])
        if not frame + 1 in keyed_frames:
            obj.translate.set((0, 0, 0))
            pm.setKeyframe(obj, t=[frame + 1])

    def reanimate(self, other_root, start_time=None, end_time=None):
        """
        Transfers animation from a skeleton back onto a face rig.

        :param pm.nt.Joint other_root: The root joint that has all the animation curves
        """

        current_eye_joint = pm.PyNode(self.bind_joints)
        side = current_eye_joint.skelSide.get()
        # get eye_joint from the root
        markup = chain_markup.ChainMarkup(other_root)
        eye_joint = markup.get_start('eye', side)

        # Get Eye Curves
        tx_curve = eye_joint.attr('flagTx').listConnections(type=pm.nt.AnimCurve)
        ty_curve = eye_joint.attr('flagTy').listConnections(type=pm.nt.AnimCurve)
        tz_curve = eye_joint.attr('flagTz').listConnections(type=pm.nt.AnimCurve)

        curves = {}
        if tx_curve:
            curves['tx'] = tx_curve[0]
        if ty_curve:
            curves['ty'] = ty_curve[0]
        if tz_curve:
            curves['tz'] = tz_curve[0]

        if not curves:
            return

        # Get flags
        flag = self.get_flag()

        # Transfer Anim Curves
        # Attach or merge anim curve to flag attribute
        for flag_attr, curve in curves.items():
            anim_curves.reanimate_from_anim_curves(anim_curve=curve,
                                                   object_attribute=flag.attr(flag_attr),
                                                   start_time=start_time,
                                                   end_time=end_time)

    def attach_to_skeleton(self, namespace=None):
        """
        Overrides the attach to skeleton.  Face components currently do not support attaching to skeleton.

        :param str namespace: if there is an expected namespace or not.
        :return: Returns and empty list
        :rtype: list()
        """

        logging.info(f'{self.pynode}: Face components currently do not support attaching to skeleton.')
        return []

    def get_flag(self):
        """
        Returns the first flag connected to the component.

        :return: Returns the first flag connected to the component.
        :rtype: flag.Flag
        """

        return self.get_aim_flag()

