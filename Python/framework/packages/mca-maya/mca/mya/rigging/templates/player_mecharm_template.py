#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rig Template for Mech Arms
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.rigging import tek
from mca.mya.rigging.templates import rig_templates
from mca.mya.utils import attr_utils
from mca.mya.rigging import chain_markup


class MechArm(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'mech_arm'

    def __init__(self, asset_id=ASSET_ID):
        super(MechArm, self).__init__(asset_id)

    def build(self, asset_type='attachment'):

        root_joint = pm.PyNode('root')
        skel_markup = chain_markup.ChainMarkup(root_joint)

        tek_root = tek.TEKRoot.create(root_joint, asset_type, self.asset_id)
        tek.SkeletalMesh.create(tek_root)
        tek_rig = tek.TEKRig.create(tek_root)

        # world
        start_joint = pm.PyNode('root')
        world_component = tek.WorldComponent.create(tek_rig,
                                                            start_joint,
                                                            'center',
                                                            'world',
                                                            orientation=[-90,0,0])
        world_flag = world_component.get_flags()[0]
        offset_flag = world_component.offset_flag
        root_flag = world_component.root_flag
        root_flag.set_as_sub()
        offset_flag.set_as_detail()

        # Right Clavicle
        start_joint = pm.PyNode('clavicle_r')
        end_joint = pm.PyNode('clavicle_r')
        r_clav_component = tek.FKComponent.create(tek_rig,
                                                        start_joint,
                                                        end_joint,
                                                        side='right',
                                                        region='clav',
                                                        lock_root_translate_axes=['v'])
        r_clav_component.attach_component(world_component, pm.PyNode('root'))


        # IKFK Right arm
        start_joint = pm.PyNode('upperarm_r')
        end_joint = pm.PyNode('hand_r')
        r_arm_component = tek.IKFKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='arm',
                                                            ik_flag_pv_orient=[-90, 0, 0])
        r_arm_component.attach_component(r_clav_component, pm.PyNode('clavicle_r'))

        # wrist trans door
        start_joint = pm.PyNode('wrist_door_trans_r')
        end_joint = pm.PyNode('wrist_door_trans_r')
        wrist_door_trans_component = tek.FKComponent.create(tek_rig,
                                                             start_joint,
                                                             end_joint,
                                                             side='right',
                                                             region='mecharm_wrist_trans_door',
                                                             lock_child_translate_axes=[],
                                                             lock_root_translate_axes=[])
        wrist_door_trans_component.attach_component(r_arm_component, pm.PyNode('lowerarm_r'))
        wrist_trans_door_flag = wrist_door_trans_component.get_flags()[0]
        wrist_trans_door_flag.set_as_detail()
        attr_utils.unlock_and_show_attrs(wrist_trans_door_flag.v)
        wrist_trans_door_flag.v.set(0)
        attr_utils.lock_and_hide_attrs(wrist_trans_door_flag, 'v')

        # wrist door
        start_joint = pm.PyNode('wrist_mecharm_door_01_r')
        end_joint = pm.PyNode('wrist_mecharm_door_02_r')
        wrist_door_component = tek.FKComponent.create(tek_rig,
                                                       start_joint,
                                                       end_joint,
                                                       side='right',
                                                       region='mecharm_wrist_door',
                                                       lock_child_translate_axes=[],
                                                       lock_root_translate_axes=[])
        wrist_door_component.attach_component(wrist_door_trans_component, pm.PyNode('wrist_door_trans_r'))
        wrist_door_flags = wrist_door_component.get_flags()
        [flag.set_as_detail() for flag in wrist_door_flags]



        ####  Right Fingers #######
        # left Index Finger
        start_joint = pm.PyNode('index_metacarpal_r')
        end_joint = pm.PyNode('index_03_r')
        r_index_component = tek.FKComponent.create(tek_rig, start_joint, end_joint, side='right', region='index_finger', scale=0.2)
        r_index_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # left middle Finger
        start_joint = pm.PyNode('middle_metacarpal_r')
        end_joint = pm.PyNode('middle_03_r')
        r_middle_component = tek.FKComponent.create(tek_rig, start_joint, end_joint, side='right', region='middle_finger', scale=0.2)
        r_middle_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # left ring Finger
        start_joint = pm.PyNode('ring_metacarpal_r')
        end_joint = pm.PyNode('ring_03_r')
        r_ring_component = tek.FKComponent.create(tek_rig, start_joint, end_joint, side='right', region='ring_finger', scale=0.2)
        r_ring_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # left Pinky Finger
        start_joint = pm.PyNode('pinky_metacarpal_r')
        end_joint = pm.PyNode('pinky_03_r')
        r_pinky_component = tek.FKComponent.create(tek_rig, start_joint, end_joint, side='right', region='pinky_finger', scale=0.2)
        r_pinky_component.attach_component(r_arm_component, pm.PyNode('hand_r'))


        # left Thumb Finger
        start_joint = pm.PyNode('thumb_01_r')
        end_joint = pm.PyNode('thumb_03_r')
        r_thumb_component = tek.FKComponent.create(tek_rig, start_joint, end_joint, side='right', region='thumb', scale=0.2)
        r_thumb_component.attach_component(r_arm_component, pm.PyNode('hand_r'))


        start_joint = pm.PyNode('front_shoulder_plate')
        end_joint = pm.PyNode('front_shoulder_plate')
        front_plate_component = tek.FKComponent.create(tek_rig,
                                                                    start_joint,
                                                                    end_joint,
                                                                    side='right',
                                                                    region='shoulder',
                                                                    lock_root_translate_axes=['ty', 'tz', 'ry', 'rz'])
        front_plate_component.attach_component(r_arm_component, pm.PyNode('upperarm_twist_01_r'))
        front_plate_flag = front_plate_component.get_flags()[0]
        front_plate_flag.set_as_detail()

        start_joint = pm.PyNode('back_shoulder_plate')
        end_joint = pm.PyNode('back_shoulder_plate')
        back_plate_component = tek.FKComponent.create(tek_rig,
                                                                    start_joint,
                                                                    end_joint,
                                                                    side='right',
                                                                    region='shoulder',
                                                                    lock_root_translate_axes=['ty', 'tz', 'ry', 'rz'])
        back_plate_component.attach_component(r_arm_component, pm.PyNode('upperarm_twist_01_r'))
        back_plate_flag = back_plate_component.get_flags()[0]
        back_plate_flag.set_as_detail()

        # SDKs
        # Bicep
        drive_attr = pm.PyNode('lowerarm_r.rz')
        driven_obj = pm.PyNode('upperarm_mecharm_bicep_r')
        driven_attrs = {'start':{}, 'end':{}}
        driven_attrs['start']['tx'] = driven_obj.tx.get()
        driven_attrs['start']['ty'] = driven_obj.ty.get()
        driven_attrs['start']['tz'] = driven_obj.tz.get()

        driven_attrs['end']['tx'] = -14.953
        driven_attrs['end']['ty'] = 8.093
        driven_attrs['end']['tz'] = 2.566

        bicep_sdk_component = tek.SingleSDKComponent.create(tek_rig,
                                                            drive_attr,
                                                            driven_obj,
                                                            side='right',
                                                            region='bicep_sdk',
                                                            driven_attrs=driven_attrs,
                                                            drive_attr_values=(0,-80))

        # Wrist
        drive_attr = pm.PyNode('hand_r.rz')
        driven_obj = wrist_trans_door_flag
        driven_attrs = {'start': {}, 'end': {}}
        driven_attrs['start']['tx'] = driven_obj.tx.get()
        driven_attrs['start']['ty'] = driven_obj.ty.get()
        driven_attrs['start']['tz'] = driven_obj.tz.get()

        driven_attrs['end']['tx'] = 2.979
        driven_attrs['end']['ty'] = -0.396
        driven_attrs['end']['tz'] = -0.445

        wrist_sdk_component = tek.SingleSDKComponent.create(tek_rig,
                                                                drive_attr,
                                                                driven_obj,
                                                                side='right',
                                                                region='wrist_sdk',
                                                                driven_attrs=driven_attrs,
                                                                drive_attr_values=(0, -95))


        # # Front Shoulder Plate

        drive_attr = pm.PyNode('upperarm_r.rx')
        driven_obj = pm.PyNode('f_front_shoulder_plate')
        driven_attrs = {'start': {}, 'end': {}}
        driven_attrs['start']['rx'] = driven_obj.rx.get()

        driven_attrs['end']['rx'] = -15

        front_shoulder_plate_sdk_component = tek.SingleSDKComponent.create(tek_rig,
                                                                   drive_attr,
                                                                   driven_obj,
                                                                   side='right',
                                                                   region='shoulder_sdk',
                                                                   driven_attrs=driven_attrs,
                                                                   drive_attr_values=(0, 70))

        # # Back Shoulder Plate

        drive_attr = pm.PyNode('upperarm_r.rx')
        driven_obj = pm.PyNode('f_back_shoulder_plate')
        driven_attrs = {'start': {}, 'end': {}}
        driven_attrs['start']['rx'] = driven_obj.rx.get()

        driven_attrs['end']['rx'] = 5
        back_shoulder_plate_sdk_component = tek.SingleSDKComponent.create(tek_rig,
                                                                   drive_attr,
                                                                   driven_obj,
                                                                   side='right',
                                                                   region='shoulder_sdk',
                                                                   driven_attrs=driven_attrs,
                                                                   drive_attr_values=(0, -90))


        ###################### Below will be separate rigs in the future ########################
        # tri Doors ######
        # Tri Arm
        start_joint = pm.PyNode('upperarm_mecharm_tri_r')
        end_joint = pm.PyNode('upperarm_mecharm_tri_r')
        mecharm_tri_component = tek.FKComponent.create(tek_rig,
                                                        start_joint,
                                                        end_joint,
                                                        side='right',
                                                        region='mecharm_tri',
                                                        lock_child_translate_axes=[],
                                                        lock_root_translate_axes=[])
        mecharm_tri_component.attach_component(r_arm_component, pm.PyNode('upperarm_r'))
        mecharm_tri_flag = mecharm_tri_component.get_flags()[0]
        mecharm_tri_flag.set_as_detail()
        align_grp = mecharm_tri_flag.get_align_transform()
        align_grp.v.set(0)

        # Tri
        drive_attr = pm.PyNode('lowerarm_r.rz')
        driven_obj = mecharm_tri_flag
        driven_attrs = {'start': {}, 'end': {}}
        driven_attrs['start']['tx'] = 0
        driven_attrs['start']['ty'] = 0
        driven_attrs['start']['tz'] = 0

        driven_attrs['end']['tx'] = 2
        driven_attrs['end']['ty'] = 0
        driven_attrs['end']['tz'] = 0

        tri_sdk_component = tek.SingleSDKComponent.create(tek_rig,
                                                                 drive_attr,
                                                                 driven_obj,
                                                                 side='right',
                                                                 region='tri_sdk',
                                                                 driven_attrs=driven_attrs,
                                                                 drive_attr_values=(-30, 20))

        tek_rig.rigTemplate.set(MechArm.__name__)
        tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig


class MechArmJetTri(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'jet_mecharm_tri'

    def __init__(self, asset_id=ASSET_ID):
        super(MechArmJetTri, self).__init__(asset_id)

    def build(self, asset_type='prop'):
        root_joint = pm.PyNode('root')

        tek_root = tek.TEKRoot.create(root_joint, asset_type, self.asset_id)
        skel_mesh = tek.SkeletalMesh.create(tek_root)
        tek_rig = tek.TEKRig.create(tek_root)

        # world
        start_joint = pm.PyNode('root')
        world_component = tek.WorldComponent.create(tek_rig,
                                                            start_joint,
                                                            'center',
                                                            'world',
                                                            orientation=[-90, 0, 0])

        # base
        start_joint = pm.PyNode('base_triceps_r')
        end_joint = pm.PyNode('base_triceps_r')
        tri_base_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='tri_jets')
        tri_base_component.attach_component(world_component, pm.PyNode('root'))

        # hinges
        start_joint = pm.PyNode('hinge_triceps_01_r')
        end_joint = pm.PyNode('hinge_triceps_01_r')
        upper_tri_hinge_component = tek.FKComponent.create(tek_rig,
                                                                    start_joint,
                                                                    end_joint,
                                                                    side='right',
                                                                    region='tri_upper_hinge')
        upper_tri_hinge_component.attach_component(upper_tri_hinge_component, pm.PyNode('base_triceps_r'))


        start_joint = pm.PyNode('hinge_triceps_02_r')
        end_joint = pm.PyNode('hinge_triceps_02_r')
        lower_tri_hinge_component = tek.FKComponent.create(tek_rig,
                                                                    start_joint,
                                                                    end_joint,
                                                                    side='right',
                                                                    region='tri_lower_hinge')
        lower_tri_hinge_component.attach_component(upper_tri_hinge_component, pm.PyNode('base_triceps_r'))

        # jets
        start_joint = pm.PyNode('jet_triceps_01_r')
        end_joint = pm.PyNode('jet_triceps_01_r')
        upper_tri_jet_component = tek.FKComponent.create(tek_rig,
                                                                    start_joint,
                                                                    end_joint,
                                                                    side='right',
                                                                    region='tri_upper_jet')
        upper_tri_jet_component.attach_component(upper_tri_hinge_component, pm.PyNode('base_triceps_r'))

        start_joint = pm.PyNode('jet_triceps_02_r')
        end_joint = pm.PyNode('jet_triceps_02_r')
        lower_tri_jet_component = tek.FKComponent.create(tek_rig,
                                                                    start_joint,
                                                                    end_joint,
                                                                    side='right',
                                                                    region='tri_lower_jet')
        lower_tri_jet_component.attach_component(upper_tri_hinge_component, pm.PyNode('base_triceps_r'))

        tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig


class MechArmJetTop(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'jet_mecharm_top'

    def __init__(self, asset_id=ASSET_ID):
        super(MechArmJetTop, self).__init__(asset_id)

    def build(self, asset_type='prop'):
        root_joint = pm.PyNode('root')

        tek_root = tek.TEKRoot.create(root_joint, asset_type, self.asset_id)
        skel_mesh = tek.SkeletalMesh.create(tek_root)
        tek_rig = tek.TEKRig.create(tek_root)

        # world
        start_joint = pm.PyNode('root')
        world_component = tek.WorldComponent.create(tek_rig,
                                                            start_joint,
                                                            'center',
                                                            'world',
                                                            orientation=[-90, 0, 0])

        # base
        start_joint = pm.PyNode('base_upper_forearm')
        end_joint = pm.PyNode('base_upper_forearm')
        top_base_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='top_jets')
        top_base_component.attach_component(world_component, pm.PyNode('root'))

        # hinges
        start_joint = pm.PyNode('hinge_upper_forearm')
        end_joint = pm.PyNode('hinge_upper_forearm')
        upper_top_hinge_component = tek.FKComponent.create(tek_rig,
                                                                    start_joint,
                                                                    end_joint,
                                                                    side='right',
                                                                    region='top_hinge')
        upper_top_hinge_component.attach_component(top_base_component, pm.PyNode('base_upper_forearm'))

        # jets
        start_joint = pm.PyNode('jet_upper_forearm_01')
        end_joint = pm.PyNode('jet_upper_forearm_01')
        upper_top_jet_component = tek.FKComponent.create(tek_rig,
                                                                start_joint,
                                                                end_joint,
                                                                side='right',
                                                                region='top_upper_jet')
        upper_top_jet_component.attach_component(top_base_component, pm.PyNode('base_upper_forearm'))

        start_joint = pm.PyNode('jet_upper_forearm_02')
        end_joint = pm.PyNode('jet_upper_forearm_02')
        lower_top_jet_component = tek.FKComponent.create(tek_rig,
                                                                start_joint,
                                                                end_joint,
                                                                side='right',
                                                                region='top_lower_jet')
        lower_top_jet_component.attach_component(top_base_component, pm.PyNode('base_upper_forearm'))

        tek_rig.rigTemplate.set(MechArm.__name__)
        tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig


class MechArmJetSide(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'jet_mecharm_side'

    def __init__(self, asset_id=ASSET_ID):
        super(MechArmJetSide, self).__init__(asset_id)

    def build(self, asset_type='prop'):
        root_joint = pm.PyNode('root')

        tek_root = tek.TEKRoot.create(root_joint, asset_type, self.asset_id)
        skel_mesh = tek.SkeletalMesh.create(tek_root)
        tek_rig = tek.TEKRig.create(tek_root)

        # world
        start_joint = pm.PyNode('root')
        world_component = tek.WorldComponent.create(tek_rig,
                                                            start_joint,
                                                            'center',
                                                            'world',
                                                            orientation=[-90, 0, 0])

        # base
        start_joint = pm.PyNode('base_side_forearm')
        end_joint = pm.PyNode('base_side_forearm')
        side_base_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='side_jets')
        side_base_component.attach_component(world_component, pm.PyNode('root'))

        # hinges
        start_joint = pm.PyNode('hinge_side_forearm')
        end_joint = pm.PyNode('hinge_side_forearm')
        side_hinge_component = tek.FKComponent.create(tek_rig,
                                                                    start_joint,
                                                                    end_joint,
                                                                    side='right',
                                                                    region='side_hinge')
        side_hinge_component.attach_component(side_base_component, pm.PyNode('base_side_forearm'))

        # jets
        start_joint = pm.PyNode('jet_side_forearm')
        end_joint = pm.PyNode('jet_side_forearm')
        side_jet_component = tek.FKComponent.create(tek_rig,
                                                                start_joint,
                                                                end_joint,
                                                                side='right',
                                                                region='side_jet')
        side_jet_component.attach_component(side_base_component, pm.PyNode('base_side_forearm'))

        tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig


class MechArmJetBottom(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'jet_mecharm_bottom'

    def __init__(self, asset_id=ASSET_ID):
        super(MechArmJetBottom, self).__init__(asset_id)

    def build(self, asset_type='prop'):
        root_joint = pm.PyNode('root')

        tek_root = tek.TEKRoot.create(root_joint, asset_type, self.asset_id)
        skel_mesh = tek.SkeletalMesh.create(tek_root)
        tek_rig = tek.TEKRig.create(tek_root)

        # world
        start_joint = pm.PyNode('root')
        world_component = tek.WorldComponent.create(tek_rig,
                                                            start_joint,
                                                            'center',
                                                            'world',
                                                            orientation=[-90, 0, 0])

        # base
        start_joint = pm.PyNode('base_under_forearm')
        end_joint = pm.PyNode('base_under_forearm')
        bottom_base_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='bottom_jets')
        bottom_base_component.attach_component(world_component, pm.PyNode('root'))

        # hinges
        start_joint = pm.PyNode('hinge_under_forearm')
        end_joint = pm.PyNode('hinge_under_forearm')
        bottom_hinge_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='bottom_hinge')
        bottom_hinge_component.attach_component(bottom_base_component, pm.PyNode('base_under_forearm'))

        # jets
        start_joint = pm.PyNode('jet_under_forearm')
        end_joint = pm.PyNode('jet_under_forearm')
        bottom_jet_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='bottom_jet')
        bottom_jet_component.attach_component(bottom_base_component, pm.PyNode('base_under_forearm'))

        tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig

