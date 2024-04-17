#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Build a component building information.

"""

# python imports
import os
import re

# software specific imports
import pymel.core as pm

from PySide2.QtWidgets import QCheckBox, QHBoxLayout, QGroupBox, QGridLayout

# mca python imports
from mca.common.pyqt import messages
from mca.common.tools.dcctracking import dcc_tracking
from mca.common.utils import lists, pymaths

from mca.mya.rigging import chain_markup, tek
from mca.mya.utils import attr_utils

SCA_MULTIPLIER = 651.7317791852719
DISTANCE_LIMIT = 18.50931008978995

class FallbackComponentRigBuilder:
    details = '''This component does not have a rig builder class, and will be unavailable for use in Build a Rig'''

    def __init__(self, main_ui):
        # do some stuff
        self.main_ui = main_ui
        self.main_ui.ui.component_info_plainTextEdit.setPlainText(self.details)
        self.setup_extra_options()

    def setup_extra_options(self):
        pass

    def build_component(self, *args):
        pass

    def get_component_info(self, start_joint):
        skel_hierarchy = chain_markup.ChainMarkup(start_joint)
        wrapped_joint = chain_markup.JointMarkup(start_joint)
        region = wrapped_joint.region
        side = wrapped_joint.side
        start_joint, end_joint = skel_hierarchy.get_chain(region, side)
        return region, side, start_joint, end_joint

    def get_component_scale(self, start_joint):
        tek_rig = self.main_ui.tek_rig
        tek_root = tek.get_tek_root(tek_rig)
        skel_root = tek_root.root_joint
        skel_bb = pm.xform(skel_root, q=True, ws=True, bb=True)

        scale = pymaths.find_distance_between_points(skel_bb[:3], skel_bb[3:]) / SCA_MULTIPLIER
        return scale * .35 if pymaths.find_vector_length(start_joint.t.get()) <= DISTANCE_LIMIT * scale else scale


class CogComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''CogComponent
    The first flag in a rig structure, this behaves like a simple FK flag'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        scale = self.get_component_scale(start_joint)

        tek_rig = self.main_ui.tek_rig

        parent_component = tek_rig.get_tek_child(tek.WorldComponent)
        if not parent_component:
            messages.error_message('Build Error', 'The COG expects to attach to a world component please add one before attempting to add a COG component.')
            return
        parent_object = parent_component.offset_flag

        # Post check

        # Build and auto attach
        rfk_component = tek.CogComponent.create(tek_rig,
                                                 start_joint,
                                                 start_joint,
                                                 'center',
                                                 'cog',
                                                 scale=scale)
        rfk_component.attach_component(parent_component, parent_object)
        return rfk_component


class FKComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''FKComponent
    A simple FK Component consisting of one Flag per joint in the chain. Options to lock translation and rotation for both the root flag and all children.'''

    def setup_extra_options(self):
        root_limits = QGroupBox(parent=self.main_ui)
        self.main_ui.ui.additional_ops_verticalLayout.addWidget(root_limits)
        root_limits.setTitle('Root Attr Locks')
        root_groupbox_grid_layout = QGridLayout(self.main_ui)
        root_limits.setLayout(root_groupbox_grid_layout)

        self.rt_checkbox = QCheckBox()
        self.rt_checkbox.setText('Translate')
        self.rt_checkbox.setChecked(True)
        root_groupbox_grid_layout.addWidget(self.rt_checkbox, 0, 0)
        self.rr_checkbox = QCheckBox()
        self.rr_checkbox.setText('Rotation')
        root_groupbox_grid_layout.addWidget(self.rr_checkbox, 0, 1)
        self.rs_checkbox = QCheckBox()
        self.rs_checkbox.setText('Scale')
        self.rs_checkbox.setChecked(True)
        root_groupbox_grid_layout.addWidget(self.rs_checkbox, 0, 2)

        child_limits = QGroupBox(parent=self.main_ui)
        self.main_ui.ui.additional_ops_verticalLayout.addWidget(child_limits)
        child_limits.setTitle('Child Attr Locks')
        child_groupbox_grid_layout = QGridLayout(self.main_ui)
        child_limits.setLayout(child_groupbox_grid_layout)

        self.ct_checkbox = QCheckBox()
        self.ct_checkbox.setText('Translate')
        self.ct_checkbox.setChecked(True)
        child_groupbox_grid_layout.addWidget(self.ct_checkbox, 0, 0)
        self.cr_checkbox = QCheckBox()
        self.cr_checkbox.setText('Rotation')
        child_groupbox_grid_layout.addWidget(self.cr_checkbox, 0, 1)
        self.cs_checkbox = QCheckBox()
        self.cs_checkbox.setText('Scale')
        self.cs_checkbox.setChecked(True)
        child_groupbox_grid_layout.addWidget(self.cs_checkbox, 0, 2)

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        region, side, start_joint, end_joint = self.get_component_info(start_joint)
        scale = self.get_component_scale(start_joint)

        tek_rig = self.main_ui.tek_rig

        parent_joint = start_joint.getParent()
        parent_component = lists.get_first_in_list(list(set([x for x in parent_joint.listConnections(type=pm.nt.Network) if 'Constraint' not in x.name()])))
        parent_component = tek.TEKNode(parent_component) if parent_component else tek_rig

        # Post check

        # Unique to Component

        root_translate = attr_utils.TRANSLATION_ATTRS if self.rt_checkbox.isChecked() else ()
        root_rotate = attr_utils.ROTATION_ATTRS if self.rr_checkbox.isChecked() else ()
        root_scale = attr_utils.SCALE_ATTRS if self.rs_checkbox.isChecked() else ()

        child_translate = attr_utils.TRANSLATION_ATTRS if self.ct_checkbox.isChecked() else ()
        child_rotate = attr_utils.ROTATION_ATTRS if self.cr_checkbox.isChecked() else ()
        child_scale = attr_utils.SCALE_ATTRS if self.cs_checkbox.isChecked() else ()

        # Build and auto attach
        fk_component = tek.FKComponent.create(tek_rig,
                                               start_joint,
                                               end_joint,
                                               side,
                                               region,
                                               scale=scale,
                                               lock_child_rotate_axes=child_rotate,
                                               lock_child_translate_axes=child_translate,
                                               lock_child_scale_axes=child_scale,
                                               lock_root_rotate_axes=root_rotate,
                                               lock_root_translate_axes=root_translate,
                                               lock_root_scale_axes=root_scale,
                                               constrain_scale=True if not any(child_scale+root_scale) else False)
        fk_component.attach_component(parent_component, parent_joint)
        return fk_component


class IKFKComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''IKFKComponent
    A dual IK/FK switch component, useful for arms or other 3 joint chains which need positional controls in addition to simple rotation. A switch object will be automatically created near the last joint of the chain.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        region, side, start_joint, end_joint = self.get_component_info(start_joint)
        scale = self.get_component_scale(start_joint)

        tek_rig = self.main_ui.tek_rig

        parent_joint = start_joint.getParent()
        parent_component = lists.get_first_in_list(list(set([x for x in parent_joint.listConnections(type=pm.nt.Network) if 'Constraint' not in x.name()])))
        parent_component = tek.TEKNode(parent_component) if parent_component else tek_rig

        # Post check
        skel_hierarchy = chain_markup.ChainMarkup(start_joint)
        if len(skel_hierarchy.get_full_chain(region, side)) != 3:
            messages.error_message('Build Error', 'Leg length is too short, 3 joints are the expected length for a IKFK Component')
            return

        # Build and auto attach
        ikfk_component = tek.IKFKComponent.create(tek_rig,
                                                   start_joint,
                                                   end_joint,
                                                   side,
                                                   region,
                                                   scale=scale)
        ikfk_component.attach_component(parent_component, parent_joint)
        return ikfk_component


class PelvisComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''PelvisComponent
    A unqiue FK component that represents the lower spine of the character, this moves independently of the primary spine, and uses a reverse FK setup from the joint above it.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        region, side, start_joint, end_joint = self.get_component_info(start_joint)
        scale = self.get_component_scale(start_joint)

        tek_rig = self.main_ui.tek_rig

        parent_component = lists.get_first_in_list(list(set([x for x in start_joint.listConnections(type=pm.nt.Network) if 'Constraint' not in x.name()])))
        parent_component = tek.TEKNode(parent_component) if parent_component else tek_rig

        # Post check

        # Build and auto attach
        rfk_component = tek.PelvisComponent.create(tek_rig,
                                                             start_joint,
                                                             end_joint,
                                                             side,
                                                             region,
                                                             scale=scale)
        rfk_component.attach_component(parent_component, parent_component.get_flags()[0])
        return rfk_component


class ReverseFootComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''ReverseFootComponent
    A dual IK/FK switch component, with reverse foot attachment. This should be used for a standard bipedal leg and foot.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        region, side, start_joint, end_joint = self.get_component_info(start_joint)
        scale = self.get_component_scale(start_joint)

        tek_rig = self.main_ui.tek_rig

        parent_joint = start_joint.getParent()
        parent_component = lists.get_first_in_list(list(set([x for x in parent_joint.listConnections(type=pm.nt.Network) if 'Constraint' not in x.name()])))
        parent_component = tek.TEKNode(parent_component) if parent_component else tek_rig

        # Post check
        skel_hierarchy = chain_markup.ChainMarkup(start_joint)
        if len(skel_hierarchy.get_full_chain(region, side)) != 4:
            messages.error_message('Build Error', 'Leg length is too short, 4 joints are the expected length for a leg.')
            return

        toe_contact_joint = skel_hierarchy.get_start(f'{region}_toe', side)
        ball_contact_joint = skel_hierarchy.get_start(f'{region}_ball', side)
        heel_contact_joint = skel_hierarchy.get_start(f'{region}_heel', side)
        interior_lean_joint = skel_hierarchy.get_start(f'{region}_interior', side)
        exterior_lean_joint = skel_hierarchy.get_start(f'{region}_exterior', side)

        for x in [toe_contact_joint, ball_contact_joint, heel_contact_joint, interior_lean_joint, exterior_lean_joint]:
            if not x:
                messages.error_message('Build Error', 'Missing one or more null contract joints for foot attributes, verify the skeleton.')
                return

        # Build and auto attach
        leg_component = tek.ReverseFootComponent.create(tek_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side,
                                                         region,
                                                         scale=scale)
        leg_component.attach_component(parent_component, parent_joint)
        return leg_component


class RFKComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''RFKComponent
    A reverse FK component, Commonly used for spines. This will build flags that control the spine from either direction.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        region, side, start_joint, end_joint = self.get_component_info(start_joint)
        scale = self.get_component_scale(start_joint)*2.5

        tek_rig = self.main_ui.tek_rig

        parent_object = start_joint.getParent()
        parent_component = None
        for x in parent_object.listConnections(type=pm.nt.Network):
            if 'Constraint' in x.name():
                continue
            parent_component = x
            if 'Cog' in x.name():
                parent_object = parent_component.cogFlag.get()
                break
        parent_component = tek.TEKNode(parent_component) if parent_component else tek_rig

        # Post check

        # Build and auto attach
        rfk_component = tek.RFKComponent.create(tek_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side,
                                                         region,
                                                         scale=scale)
        rfk_component.attach_component(parent_component, parent_object)
        return rfk_component


class SplineIKComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''SplineIK
    A spline IK component best used for retractable tentacle like appendages. It requires two helper joints to recover animation for reanimator, one for the mid and one for the end, with an optional joint for the start.'''

    def setup_extra_options(self):
        tentacle_options = QGroupBox(parent=self.main_ui)
        self.main_ui.ui.additional_ops_verticalLayout.addWidget(tentacle_options)
        tentacle_options.setTitle('Tentacle Options')
        horizontal_layout = QHBoxLayout(self.main_ui)
        tentacle_options.setLayout(horizontal_layout)

        self.add_mid_flag_checkbox = QCheckBox()
        self.add_mid_flag_checkbox.setText('Add mid flag')
        self.add_mid_flag_checkbox.setChecked(True)
        horizontal_layout.addWidget(self.add_mid_flag_checkbox)
        self.can_retract_checkbox = QCheckBox()
        self.can_retract_checkbox.setText('Is able to retract')
        self.can_retract_checkbox.setChecked(True)
        horizontal_layout.addWidget(self.can_retract_checkbox)

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        region, side, start_joint, end_joint = self.get_component_info(start_joint)
        scale = self.get_component_scale(start_joint)

        tek_rig = self.main_ui.tek_rig

        parent_joint = start_joint.getParent()
        parent_component = lists.get_first_in_list(
            list(set([x for x in parent_joint.listConnections(type=pm.nt.Network) if 'Constraint' not in x.name()])))
        parent_component = tek.TEKNode(parent_component) if parent_component else tek_rig

        # Post check

        skel_hierarchy = chain_markup.ChainMarkup(parent_joint)
        mid_helper_joint = skel_hierarchy.get_start(f'{region}_mid', side)
        if not mid_helper_joint:
            messages.error_message('Build Error', 'The mid spline helper joint is missing, verify the joint exists and has the expected markup.')
            return

        end_helper_joint = skel_hierarchy.get_start(f'{region}_end', side)
        if not end_helper_joint:
            messages.error_message('Build Error', 'The end spline helper joint is missing, verify the joint exists and has the expected markup.')
            return

        start_helper_joint = skel_hierarchy.get_start(f'{region}_start', side)

        print(start_joint, end_joint, start_helper_joint, mid_helper_joint, end_helper_joint)
        # Build and auto attach
        spline_component = tek.SplineIKComponent.create(tek_rig,
                                                         start_joint,
                                                         end_joint,
                                                         end_helper_joint,
                                                         mid_helper_joint,
                                                         side,
                                                         region,
                                                         scale=scale,
                                                         start_helper_joint=start_helper_joint,
                                                         mid_flag=self.add_mid_flag_checkbox.isChecked(),
                                                         can_retract=self.can_retract_checkbox.isChecked())
        spline_component.attach_component(parent_component, parent_joint)
        return spline_component


class SplineIKRibbonComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''SplineIKRibbon
    A spline ribbon component best used for non retractable tail like appendages. It requires two helper joints to recover animation for reanimator, one for the mid and one for the end.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        region, side, start_joint, end_joint = self.get_component_info(start_joint)
        scale = self.get_component_scale(start_joint)

        tek_rig = self.main_ui.tek_rig

        parent_joint = start_joint.getParent()
        parent_component = lists.get_first_in_list(list(set([x for x in parent_joint.listConnections(type=pm.nt.Network) if 'Constraint' not in x.name()])))
        parent_component = tek.TEKNode(parent_component) if parent_component else tek_rig

        # Post check

        skel_hierarchy = chain_markup.ChainMarkup(parent_joint)
        mid_helper_joint = skel_hierarchy.get_start(f'{region}_mid', side)
        if not mid_helper_joint:
            messages.error_message('Build Error', 'The mid spline helper joint is missing, verify the joint exists and has the expected markup.')
            return

        end_helper_joint = skel_hierarchy.get_start(f'{region}_end', side)
        if not end_helper_joint:
            messages.error_message('Build Error', 'The end spline helper joint is missing, verify the joint exists and has the expected markup.')
            return

        # Build and auto attach
        ribbon_component = tek.SplineIKRibbonComponent.create(tek_rig,
                                                               start_joint,
                                                               end_joint,
                                                               side,
                                                               region,
                                                               scale=scale)
        ribbon_component.attach_component(parent_component, parent_joint)
        return ribbon_component


class WorldComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''WorldComponent
    Primary control flag that represents the absolute position of the rig system.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        region, side, start_joint, end_joint = self.get_component_info(start_joint)
        scale = self.get_component_scale(start_joint)

        tek_rig = self.main_ui.tek_rig

        # Post check
        world_component = tek_rig.get_tek_child(tek.WorldComponent)
        if world_component:
            # We already have a world component, don't build another.
            return

        # Build and auto attach
        world_component = tek.WorldComponent.create(tek_rig,
                                                     start_joint,
                                                     'center',
                                                     'world',
                                                     scale=scale)
        world_flag = world_component.get_flags()[0]
        root_flag = world_component.root_flag
        offset_flag = world_component.offset_flag

        # Root Multiconstraint
        tek.MultiConstraint.create(tek_rig,
                                    side='center',
                                    region='root',
                                    source_object=root_flag,
                                    target_list=[world_flag,
                                                 offset_flag])
        return world_component


class ZLegComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''ZLegComponent
    An alternative leg component for use with digitigrade legs, common on some quadrupeds.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        region, side, start_joint, end_joint = self.get_component_info(start_joint)
        scale = self.get_component_scale(start_joint)

        tek_rig = self.main_ui.tek_rig

        parent_joint = start_joint.getParent()
        parent_component = lists.get_first_in_list(list(set([x for x in parent_joint.listConnections(type=pm.nt.Network) if 'Constraint' not in x.name()])))
        parent_component = tek.TEKNode(parent_component) if parent_component else tek_rig

        # Post check
        skel_hierarchy = chain_markup.ChainMarkup(start_joint)
        if len(skel_hierarchy.get_full_chain(region, side)) < 4:
            messages.error_message('Build Error', 'Leg length is too short, 4 joints are the expected length for a leg.')
            return

        toe_contact_joint = skel_hierarchy.get_start(f'{region}_toe', side)
        ball_contact_joint = skel_hierarchy.get_start(f'{region}_ball', side)
        heel_contact_joint = skel_hierarchy.get_start(f'{region}_heel', side)
        interior_lean_joint = skel_hierarchy.get_start(f'{region}_interior', side)
        exterior_lean_joint = skel_hierarchy.get_start(f'{region}_exterior', side)

        for x in [toe_contact_joint, ball_contact_joint, heel_contact_joint, interior_lean_joint, exterior_lean_joint]:
            if not x:
                messages.error_message('Build Error', 'Missing one or more null contract joints for foot attributes, verify the skeleton.')
                return

        # Build and auto attach
        z_leg_component = tek.ZLegComponent.create(tek_rig,
                                                    start_joint,
                                                    end_joint,
                                                    side,
                                                    region,
                                                    scale=scale)
        z_leg_component.attach_component(parent_component, parent_joint)
        return z_leg_component
