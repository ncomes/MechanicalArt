#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains misc utils for use within the animation export system.

"""

# python imports

# software specific imports
from mca.mya.utils import namespace_utils as namespace_utils
import pymel.core as pm

# mca python imports
from mca.common import log

from mca.common.modifiers import decorators
from mca.common.pyqt import messages
from mca.common.utils import path_utils, pymaths

from mca.mya.animation import anim_curves, time_utils
from mca.mya.rigging import frag, joint_utils
from mca.mya.utils import fbx_utils, scene_utils

logger = log.MCA_LOGGER


def refresh_ui_index():
    """
    Iterate through all our sequences and reset the ui_index positions to compensate for gaps or duplicates.

    """
    frag_sequencer = frag.get_frag_sequencer()
    sequence_dict = frag_sequencer.get_sequences()

    for _, sequence_dict in sequence_dict.items():
        ui_index_dict = {}
        for _, sequence_wrapper in sequence_dict.items():
            ui_index = sequence_wrapper.ui_index

            while ui_index in ui_index_dict:
                # negate duplicate ui_index values
                ui_index += 1
            ui_index_dict[ui_index] = sequence_wrapper

        for index, (_, sequence_wrapper) in enumerate(sorted(ui_index_dict.items(), key=lambda entry_tuple: entry_tuple[0])):
            sequence_wrapper.ui_index = index


def export_frag_sequences(frag_rig_list=None, sequences_to_skip=None):
    """
    From the FRAG Sequencer export all registered animations filtering by inclusive frag rig list, or exclusively by sequence path.

    :param list(FRAGRig) frag_rig_list: A list of FRAGRigs to export. This is done to facilitate selection based rig exporting.
    :param list(str) sequences_to_skip: A list of sequences that should be skipped. This is done so the UI can send a list of sequences to skip.
    """
    scene_utils.backup_scene('animation_exporter')
    namespace_utils.set_namespace('')

    if sequences_to_skip is None:
        sequences_to_skip = []
    else:
        # In case full paths are passed to the fnc.
        sequences_to_skip = [path_utils.to_relative_path(sequence_path) for sequence_path in sequences_to_skip]

    frag_sequencer = frag.get_frag_sequencer()
    sequence_dict = frag_sequencer.get_sequences()

    for frag_rig, sequence_dict_list in sequence_dict.items():
        frag_rig = frag.FRAGNode(frag_rig)
        if frag_rig:
            current_scale = frag_rig.rig_scale
            if current_scale != 1.0:
                frag_rig.rig_scale = 1.0

        if frag_rig_list and frag_rig not in frag_rig_list:
            # If this frag rig in the sequencer should be skipped
            logger.warning(f'FRAGRig: {frag_rig.asset_name} is not on the whitelist for export.')
            continue

        sequences_to_export = []
        for sequence_path, sequence_wrapper in sequence_dict_list.items():
            if path_utils.to_relative_path(sequence_path) in sequences_to_skip:
                continue
            if sequence_wrapper.sequence_path.lower().endswith('.fbx'):
                sequences_to_export.append(sequence_wrapper)

        if not sequences_to_export:
            # If every sequence in this rig's sequence are skipped.
            logger.warning(f'All sequences are skipped for {frag_rig}.')
            continue

        if len(sequences_to_export) == 1 or len(sequences_to_export) >= .25 * len(sequence_dict_list):
            # if we only have one sequence OR the total number of sequences we're exporting is greater than 25% of the possible sequences.
            if len(sequences_to_export) == 1:
                # Bake selectively
                start_frame, end_frame = sequences_to_export[0].frame_range
                export_root = frag_rig.bake_rig_to_skeleton(start_frame, end_frame, False)
            else:
                start_frame, end_frame = time_utils.get_keyframe_range_from_nodes(frag_rig.get_flags())
                if start_frame is None or end_frame is None:
                    logger.warning(f'There are no keyframes on this rig {frag_rig}.')
                    continue
                # We don't want to shift the keys here our sequences are all coded based on the scene range.
                export_root = frag_rig.bake_rig_to_skeleton(start_frame, end_frame, False)

            if not export_root:
                logger.warning('Skeleton was not baked, verify .skl file, aborting export.')
                return

            export_hierarchy = _trim_export_hierarchy(export_root)
            for wrapped_sequence in sequences_to_export:
                _export_baked_skeleton(export_hierarchy, wrapped_sequence)
            pm.delete(export_root)
        else:
            # if we have less than 25% of sequences do them individually.
            for wrapped_sequence in sequences_to_export:
                start_frame, end_frame = wrapped_sequence.frame_range
                export_root = frag_rig.bake_rig_to_skeleton(start_frame, end_frame, False)

                if not export_root:
                    logger.warning('Skeleton was not baked, verify .skl file, aborting export.')
                    return

                export_hierarchy = _trim_export_hierarchy(export_root)
                _export_baked_skeleton(export_hierarchy, wrapped_sequence)
                pm.delete(export_root)

        if current_scale != 1.0:
            frag_rig.rig_scale = current_scale


def export_frag_sequences_cmd(frag_rig_list=None, sequences_to_skip=None):
    """
    UI wrapper for the export frag sequences fnc. This will abort if the frame rate isn't set as expected.

    :param list(FRAGRig) frag_rig_list: A list of FRAGRigs to export. This is done to facilitate selection based rig exporting.
    :param list(str) sequences_to_skip: A list of sequences that should be skipped. This is done so the UI can send a list of sequences to skip.
    """
    frame_rate = pm.currentUnit(q=True, time=True)
    if frame_rate != 'ntsc':
        if messages.question_message('Continue Export?', 'Your frame rate is not set to NTSC 30 FPS. It\'s recommended to have your frame rate set to 30 FPS.') != 'Yes':
            return

    export_frag_sequences(frag_rig_list, sequences_to_skip)


def _trim_export_hierarchy(export_root):
    """
    Clean the given hierarchy in preperation for export, removing all joints not marked for animationExport

    :param Joint export_root: The root of the export skeleton.
    :return: A list of all the exportable joints
    :rtype: list(Joint)
    """
    if export_root.name() not in ['root', '|root']:
        existing_root = pm.PyNode('root')
        if existing_root:
            existing_root.rename('root1')
        export_root.rename('root')
    baked_hierarchy = joint_utils.SkeletonHierarchy(export_root)
    joints_to_delete = list(set(baked_hierarchy.all_joints) - (set(baked_hierarchy.animated_joints)))
    # Repull hierarchy don't trust the for loop, if we have any odd skeletal markup we could have deleted a joint that
    # is not animation exportable, but has a child that is.
    pm.delete(joints_to_delete)

    # Repull hierarchy don't trust the for loop, if we have any odd skeletal markup we could have deleted a joint that
    # is not animation exportable, but has a child that is.
    export_hierarchy = [export_root] + pm.listRelatives(export_root, ad=True, type=pm.nt.Joint)
    return export_hierarchy


def _export_baked_skeleton(export_hierarchy, sequence_wrapper):
    """
    From a baked skeleton and a sequence wrapper export the animation to its destination.

    :param list(Joint) export_hierarchy: A list of all exportable joints.
    :param AnimSequence sequence_wrapper: A wrapped sequence entry representing this export.
    """
    export_path = path_utils.to_full_path(sequence_wrapper.sequence_path)
    frame_range = sequence_wrapper.frame_range
    export_root = export_hierarchy[0]

    export_frame_range = frame_range[:]
    if sequence_wrapper.start_at_zero and frame_range[0] != 0:
        # Shift Keys so the animation starts at zero.
        offset_keys = 0 - frame_range[0]
        anim_curves.change_curve_start_time(export_hierarchy, shift_length=offset_keys)

        export_frame_range = [x + offset_keys for x in export_frame_range]

    if sequence_wrapper.root_to_origin:
        root_pos = export_root.getAttr('translate', time=export_frame_range[0])
        root_rot = export_root.getAttr('rotate', time=export_frame_range[0])
        if root_pos != pm.dt.Vector([0, 0, 0]):
            for axis, val in zip('XYZ', pymaths.scale_vector(list(root_pos), -1)):
                pm.keyframe(export_root, e=True, iub=True, r=True, at=f'translate{axis}', vc=val)
        if root_rot != pm.dt.Vector([0, 0, 0]):
            for axis, val in zip('XYZ', pymaths.scale_vector(list(root_rot), -1)):
                pm.keyframe(export_root, e=True, iub=True, r=True, at=f'rotate{axis}', vc=val)

    fbx_utils.export_fbx(export_path, export_hierarchy, sequence_wrapper.name, export_frame_range[0], export_frame_range[1])

    if sequence_wrapper.root_to_origin:
        if root_pos != pm.dt.Vector([0, 0, 0]):
            for axis, val in zip('XYZ', root_pos):
                pm.keyframe(export_root, e=True, iub=True, r=True, at=f'translate{axis}', vc=val)
        if root_rot != pm.dt.Vector([0, 0, 0]):
            for axis, val in zip('XYZ', root_rot):
                pm.keyframe(export_root, e=True, iub=True, r=True, at=f'rotate{axis}', vc=val)

    if sequence_wrapper.start_at_zero and frame_range[0] != 0:
        # Move keys back if we shifted them so we're starting fresh for the next sequence.
        anim_curves.change_curve_start_time(export_hierarchy, shift_length=offset_keys * -1)



def quick_export_frag_sequences_cmd():
    """
    Wrapper command to convert a selection into a list of FRAGRigs, then export all sequences associated with those rigs.

    """
    selection = pm.selected()
    if not selection:
        logger.warning('Please select a rig to continue.')
        return

    frame_rate = pm.currentUnit(q=True, time=True)
    if frame_rate != 'ntsc':
        if messages.question_message('Continue Export?', 'Your frame rate is not set to NTSC 30 FPS. It\'s recommended to have your frame rate set to 30 FPS.') != 'Yes':
            return

    frag_rig_list = set([frag.get_frag_rig(x) for x in selection])
    export_frag_sequences_cmd(frag_rig_list)
