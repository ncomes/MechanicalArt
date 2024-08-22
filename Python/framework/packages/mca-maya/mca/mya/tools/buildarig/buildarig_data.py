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
# Qt imports
from mca.common.pyqt.pygui import qtwidgets

# mca python imports
from mca.common.pyqt import messages, movies
from mca.common.utils import list_utils, pymaths

from mca.mya.rigging import joint_utils, frag
from mca.mya.utils import attr_utils, dag_utils

SCA_MULTIPLIER = 180.0
DISTANCE_LIMIT = 10.71428571428571


class FallbackComponentRigBuilder:
    details = '''This component does not have a rig builder class, and will be unavailable for use in Build a Rig'''
    gif_path = None

    def __init__(self, main_ui):
        if main_ui:
            # do some stuff
            self.main_ui = main_ui
            self.main_ui.ui.component_info_plainTextEdit.setPlainText(self.details)
            self.setup_extra_options()
            self.play_movie()

    def play_movie(self):
        if self.gif_path:
            new_movie_widget = movies.MovieLabel(self.gif_path, parent=self.main_ui)
            new_movie_widget.setObjectName(u'Component_Movie')
            new_movie_widget.setFixedSize(384, 216)
            self.main_ui.ui.picture_horizontalLayout.addWidget(new_movie_widget)

    def setup_extra_options(self):
        pass
    
    def build_component(self, *args):
        pass

    def get_component_info(self, start_joint):
        root_joint = dag_utils.get_absolute_parent(start_joint, pm.nt.Joint)
        skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

        skel_bb = pm.xform(root_joint, q=True, ws=True, bb=True)
        scale = pymaths.get_distance_between_points(skel_bb[:3], skel_bb[3:]) / SCA_MULTIPLIER

        wrapped_joint = joint_utils.JointMarkup(start_joint)

        if start_joint != root_joint:
            region = wrapped_joint.region
            side = wrapped_joint.side
            start_joint, end_joint = skel_hierarchy.get_chain_bookend(side, region)
            if len(set([start_joint, end_joint])) > 1:
                dis = pymaths.get_distance_between_points(*[pm.xform(x, q=True, ws=True, t=True) for x in [start_joint, end_joint]])
                if dis <= DISTANCE_LIMIT * scale * .5:
                    scale = scale * .15
                elif dis <= DISTANCE_LIMIT * scale:
                    scale = scale * .5
        else:
            end_joint = None

        return start_joint, end_joint, scale, wrapped_joint, skel_hierarchy


class CogComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''CogComponent
    The first flag in a rig structure, this behaves like a simple FK flag'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        start_joint, end_joint, scale, wrapped_joint, skel_hierarchy = self.get_component_info(start_joint)
        scale = scale * 16

        frag_rig = self.main_ui.frag_rig

        # Post check
        single_check = list_utils.get_first_in_list(frag_rig.get_frag_children(frag_type=frag.CogComponent))
        if single_check:
            messages.error_message('Build Error', 'Only a single COG is allowed per rig.')
            return

        parent_component = list_utils.get_first_in_list(frag_rig.get_frag_children(frag_type=frag.WorldComponent))
        if not parent_component:
            messages.error_message('Build Error', 'The COG expects to attach to a world component please add one before attempting to add a COG component.')
            return
        parent_object = parent_component.pynode.offset_flag.get()

        # Build and auto attach
        new_component = frag.CogComponent.create(frag_rig,
                                                 start_joint,
                                                 scale=scale)
        new_component.attach_component(parent_object)
        return new_component


class FKComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''FKComponent
    A simple FK Component consisting of one Flag per joint in the chain. Options to lock translation and rotation for both the root flag and all children.'''

    def setup_extra_options(self):
        root_limits = QtWidgets.QGroupBox(parent=self.main_ui)
        self.main_ui.ui.additional_ops_verticalLayout.addWidget(root_limits)
        root_limits.setTitle('Root Attr Locks')
        root_groupbox_grid_layout = QtWidgets.QGridLayout(self.main_ui)
        root_limits.setLayout(root_groupbox_grid_layout)

        self.rt_checkbox = QtWidgets.QCheckBox()
        self.rt_checkbox.setText('Translate')
        self.rt_checkbox.setChecked(True)
        root_groupbox_grid_layout.addWidget(self.rt_checkbox, 0, 0)
        self.rr_checkbox = QtWidgets.QCheckBox()
        self.rr_checkbox.setText('Rotation')
        root_groupbox_grid_layout.addWidget(self.rr_checkbox, 0, 1)
        self.rs_checkbox = QtWidgets.QCheckBox()
        self.rs_checkbox.setText('Scale')
        self.rs_checkbox.setChecked(True)
        root_groupbox_grid_layout.addWidget(self.rs_checkbox, 0, 2)

        child_limits = QtWidgets.QGroupBox(parent=self.main_ui)
        self.main_ui.ui.additional_ops_verticalLayout.addWidget(child_limits)
        child_limits.setTitle('Child Attr Locks')
        child_groupbox_grid_layout = QtWidgets.QGridLayout(self.main_ui)
        child_limits.setLayout(child_groupbox_grid_layout)

        self.ct_checkbox = QtWidgets.QCheckBox()
        self.ct_checkbox.setText('Translate')
        self.ct_checkbox.setChecked(True)
        child_groupbox_grid_layout.addWidget(self.ct_checkbox, 0, 0)
        self.cr_checkbox = QtWidgets.QCheckBox()
        self.cr_checkbox.setText('Rotation')
        child_groupbox_grid_layout.addWidget(self.cr_checkbox, 0, 1)
        self.cs_checkbox = QtWidgets.QCheckBox()
        self.cs_checkbox.setText('Scale')
        self.cs_checkbox.setChecked(True)
        child_groupbox_grid_layout.addWidget(self.cs_checkbox, 0, 2)

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        start_joint, end_joint, scale, wrapped_joint, skel_hierarchy = self.get_component_info(start_joint)

        frag_rig = self.main_ui.frag_rig

        parent_joint = start_joint.getParent()

        # Post check

        # Unique to Component

        root_translate = attr_utils.TRANSLATION_ATTRS if self.rt_checkbox.isChecked() else []
        root_rotate = attr_utils.ROTATION_ATTRS if self.rr_checkbox.isChecked() else []
        root_scale = attr_utils.SCALE_ATTRS if self.rs_checkbox.isChecked() else []

        child_translate = attr_utils.TRANSLATION_ATTRS if self.ct_checkbox.isChecked() else []
        child_rotate = attr_utils.ROTATION_ATTRS if self.cr_checkbox.isChecked() else []
        child_scale = attr_utils.SCALE_ATTRS if self.cs_checkbox.isChecked() else []

        # Build and auto attach
        new_component = frag.FKComponent.create(frag_rig,
                                                start_joint,
                                                end_joint,
                                                scale=scale,
                                                lock_child_rotate_axes=child_rotate,
                                                lock_child_translate_axes=child_translate,
                                                lock_child_scale_axes=child_scale,
                                                lock_root_rotate_axes=root_rotate,
                                                lock_root_translate_axes=root_translate,
                                                lock_root_scale_axes=root_scale,
                                                constrain_scale=True if not any(child_scale+root_scale) else False)
        new_component.attach_component(parent_joint)
        return new_component


class IKFKComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''IKFKComponent
    A dual IK/FK switch component, useful for arms or other 3 joint chains which need positional controls in addition to simple rotation. A switch object will be automatically created near the last joint of the chain.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        start_joint, end_joint, scale, wrapped_joint, skel_hierarchy = self.get_component_info(start_joint)

        frag_rig = self.main_ui.frag_rig

        parent_joint = start_joint.getParent()

        # Post check
        if len(skel_hierarchy.get_full_chain(wrapped_joint.side, wrapped_joint.region)) != 3:
            messages.error_message('Build Error', 'Leg length is incorrect, 3 joints are the expected length for a IKFK Component')
            return

        # Build and auto attach
        new_component = frag.IKFKComponent.create(frag_rig,
                                                   start_joint,
                                                   end_joint,
                                                   scale=scale)
        new_component.attach_component(parent_joint)
        return new_component

class PelvisComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''PelvisComponent
    A unqiue FK component that represents the lower spine of the character, this moves independently of the primary spine, and uses a reverse FK setup from the joint above it.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        start_joint, end_joint, scale, wrapped_joint, skel_hierarchy = self.get_component_info(start_joint)
        scale = scale * 10

        frag_rig = self.main_ui.frag_rig

        parent_component = list_utils.get_first_in_list(frag_rig.get_frag_children(frag_type=frag.CogComponent)) or frag_rig

        # Post check
        single_check = list_utils.get_first_in_list(frag_rig.get_frag_children(frag_type=frag.PelvisComponent))
        if single_check:
            messages.error_message('Build Error', 'Only a single pelvis is allowed per rig.')
            return
            

        # Build and auto attach
        new_component = frag.PelvisComponent.create(frag_rig,
                                                    start_joint,
                                                    end_joint,
                                                    scale=scale)
        new_component.attach_component(parent_component.flags[0].pynode)
        return new_component


class PistonComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''PistonComponent
    A Piston Component made for a two joint chain. Each joint looks back at the other using aim constraints, with up vector look ats attached to their parents.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        start_joint, end_joint, scale, wrapped_joint, skel_hierarchy = self.get_component_info(start_joint)

        frag_rig = self.main_ui.frag_rig

        # Post check
        side = wrapped_joint.side
        region = wrapped_joint.region
        if len(skel_hierarchy.get_full_chain(side, region)) != 2:
            messages.error_message('Build Error', 'Build chain is incorrect exactly 2 joints are the expected length.')
            return

        # Unique to Component

        # Build and auto attach
        new_component = frag.PistonComponent.create(frag_rig,
                                                    start_joint,
                                                    end_joint)
        return new_component
    

class ReverseFootComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''ReverseFootComponent
    A dual IK/FK switch component, with reverse foot attachment. This should be used for a standard bipedal leg and foot.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        start_joint, end_joint, scale, wrapped_joint, skel_hierarchy = self.get_component_info(start_joint)

        frag_rig = self.main_ui.frag_rig

        parent_joint = start_joint.getParent()
        for x in parent_joint.listConnections(type=pm.nt.Network):
            if 'Constraint' in x.name() or not isinstance(x, frag.FRAGAnimatedComponent):
                continue
            frag_component = frag.FRAGNode(x)
            if parent_joint in frag_component.joints:
                parent_component = frag_component
                break
        else:
            parent_component = frag_rig

        # Post check
        side = wrapped_joint.side
        region = wrapped_joint.region
        if len(skel_hierarchy.get_full_chain(side, region)) != 4:
            messages.error_message('Build Error', 'Leg length is too short, 4 joints are the expected length for a leg.')
            return

        toe_contact_joint = skel_hierarchy.get_chain_start(side, f'{region}_toe_null')
        ball_contact_joint = skel_hierarchy.get_chain_start(side, f'{region}_ball_null')
        heel_contact_joint = skel_hierarchy.get_chain_start(side, f'{region}_heel_null')
        interior_lean_joint = skel_hierarchy.get_chain_start(side, f'{region}_inner_rock_null')
        exterior_lean_joint = skel_hierarchy.get_chain_start(side, f'{region}_outer_rock_null')

        if not all([toe_contact_joint, ball_contact_joint, heel_contact_joint, interior_lean_joint, exterior_lean_joint]):
            messages.error_message('Build Error', 'Missing one or more null contract joints for foot attributes, verify the skeleton.')
            return

        # Build and auto attach
        new_component = frag.ReverseFootComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         scale=scale)
        new_component.attach_component(parent_joint)
        return new_component


class RFKComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''RFKComponent
    A reverse FK component, Commonly used for spines. This will build flags that control the spine from either direction.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        start_joint, end_joint, scale, wrapped_joint, skel_hierarchy = self.get_component_info(start_joint)

        frag_rig = self.main_ui.frag_rig

        parent_joint = start_joint.getParent()

        # Post check

        # Build and auto attach
        new_component = frag.RFKComponent.create(frag_rig,
                                                 start_joint,
                                                 end_joint,
                                                 scale=scale)
        new_component.attach_component(parent_joint)
        return new_component


class TwoPointIKComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''TwoPointIKComponent
    A IK Component made for a two joint chain. Rotation is handled by the end flag. Optionally avaliable is a stretch feature where the end flag drives the location of the end joint.'''

    def setup_extra_options(self):
        self.can_stretch = QtWidgets.QCheckBox()
        self.can_stretch.setText('Can Stretch')
        self.can_stretch.setChecked(False)
        self.main_ui.ui.additional_ops_verticalLayout.addWidget(self.can_stretch)

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        start_joint, end_joint, scale, wrapped_joint, skel_hierarchy = self.get_component_info(start_joint)

        frag_rig = self.main_ui.frag_rig

        parent_joint = start_joint.getParent()

        # Post check
        side = wrapped_joint.side
        region = wrapped_joint.region
        if len(skel_hierarchy.get_full_chain(side, region)) != 2:
            messages.error_message('Build Error', 'Build chain is incorrect exactly 2 joints are the expected length.')
            return

        # Unique to Component
        can_stretch = self.can_stretch.isChecked()

        # Build and auto attach
        new_component = frag.TwoPointIKComponent.create(frag_rig,
                                                        start_joint,
                                                        end_joint,
                                                        scale=scale,
                                                        stretch=can_stretch)
        new_component.attach_component(parent_joint)
        return new_component
    
class TwoPointIKFKComponentRigBuilder(TwoPointIKComponentRigBuilder):
    details = '''TwoPointIKFKComponent
    A IK/FK switching Component made for a two joint chain. Rotation is handled by the end flag. Optionally avaliable is a stretch feature where the end flag drives the location of the end joint.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        start_joint, end_joint, scale, wrapped_joint, skel_hierarchy = self.get_component_info(start_joint)

        frag_rig = self.main_ui.frag_rig

        parent_joint = start_joint.getParent()

        # Post check
        side = wrapped_joint.side
        region = wrapped_joint.region
        if len(skel_hierarchy.get_full_chain(side, region)) != 2:
            messages.error_message('Build Error', 'Build chain is incorrect exactly 2 joints are the expected length.')
            return
        
        # Unique to Component
        can_stretch = self.can_stretch.isChecked()

        # Build and auto attach
        new_component = frag.TwoPointIKFKComponent.create(frag_rig,
                                                          start_joint,
                                                          end_joint,
                                                          scale=scale,
                                                          stretch=can_stretch)
        new_component.attach_component(parent_joint)
        return new_component

class WorldComponentRigBuilder(FallbackComponentRigBuilder):
    details = '''WorldComponent
    Primary control flag that represents the absolute position of the rig system.'''

    def build_component(self, start_joint):
        # Pre check

        # Standard data finding.
        start_joint, end_joint, scale, wrapped_joint, skel_hierarchy = self.get_component_info(start_joint)
        scale = scale * 8

        frag_rig = self.main_ui.frag_rig

        # Post check
        single_check = list_utils.get_first_in_list(frag_rig.get_frag_children(frag_type=frag.WorldComponent))
        if single_check:
            messages.error_message('Build Error', 'Only a single world component is allowed per rig.')
            return
            

        # Build and auto attach
        new_component = frag.WorldComponent.create(frag_rig, start_joint, scale=scale)
        world_flag, offset_flag, root_flag = new_component.flags

        # Root Multiconstraint
        frag.MultiConstraintComponent.create(frag_rig, root_flag.pynode, [world_flag.pynode, offset_flag.pynode])
        return new_component
