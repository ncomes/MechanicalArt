#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains misc utils for use within the animation export system.

"""

# python imports
import os

# software specific imports
import pymel.core as pm

# mca python imports
from mca.common import log

from mca.common.assetlist import assetlist
from mca.common.modifiers import decorators
from mca.common.paths import path_utils
from mca.common.pyqt import messages
from mca.common.utils import pymaths

from mca.mya.animation import anim_curves, time_utils
from mca.mya.rigging import tek, rig_utils
from mca.mya.utils import fbx_utils, namespace as namespace_utils, scene_utils

logger = log.MCA_LOGGER


class AnimSequence(object):
    """
    Class wrapper for the animation sequencer attributes, just to make these a little easier to work with.

    """

    def __init__(self, sequencer_attr):
        self.pynode = sequencer_attr

    @property
    def rig(self):
        found_connection = self.pynode.rig.get()
        if found_connection:
            try:
                return tek.TEKNode(found_connection)
            except:
                logger.warning('Rig connection is missing or not a valid TEKRig')
                return None

    @rig.setter
    def rig(self, tek_rig):
        pm.disconnectAttr(self.pynode.rig)
        if tek_rig:
            tek_rig.message >> self.pynode.rig
            asset_id = tek_rig.get_asset_id(tek_rig)
            self.asset_id = asset_id

    @property
    def asset_id(self):
        return self.pynode.asset_id.get()

    @asset_id.setter
    def asset_id(self, val):
        if isinstance(val, str):
            self.pynode.asset_id.set(val)

    @property
    def bookmark(self):
        found_connection = self.pynode.bookmark.get()
        if found_connection:
            return found_connection

    @bookmark.setter
    def bookmark(self, timeslider_bookmark):
        pm.disconnectAttr(self.pynode.bookmark)
        timeslider_bookmark.message >> self.pynode.bookmark

    @property
    def sequence_path(self):
        return self.pynode.sequence_path.get()

    @sequence_path.setter
    def sequence_path(self, val):
        if isinstance(val, str):
            self.pynode.sequence_path.set(val)

    @property
    def frame_range(self):
        return self.pynode.start_frame.get(), self.pynode.end_frame.get()

    @frame_range.setter
    def frame_range(self, frame_range):
        self.pynode.start_frame.set(frame_range[0])
        self.pynode.end_frame.set(frame_range[-1])
        bookmark_node = self.bookmark
        if bookmark_node:
            bookmark_node.timeRangeStart.set(frame_range[0])
            bookmark_node.timeRangeStop.set(frame_range[-1])
        else:
            timeslider_bookmark = time_utils.create_bookmark(self.name, [frame_range[0], frame_range[-1]])
            self.bookmark = timeslider_bookmark

    @property
    def start_at_zero(self):
        return self.pynode.start_at_zero.get()

    @start_at_zero.setter
    def start_at_zero(self, val):
        self.pynode.start_at_zero.set(val)

    @property
    def root_to_origin(self):
        return self.pynode.root_to_origin.get()

    @root_to_origin.setter
    def root_to_origin(self, val):
        self.pynode.root_to_origin.set(val)

    @property
    def sequence_notes(self):
        return self.pynode.sequence_notes.get()

    @sequence_notes.setter
    def sequence_notes(self, val):
        if isinstance(val, str):
            self.pynode.sequence_notes.set(val)

    @property
    def ui_index(self):
        if self.pynode.node().hasAttr('ui_index'):
            return self.pynode.ui_index.get()
        return 0

    @ui_index.setter
    def ui_index(self, val):
        if isinstance(val, int):
            self.pynode.ui_index.set(val)

    # Helper properties.
    @property
    def name(self):
        return '.'.join(os.path.split(self.sequence_path)[-1].split('.')[:-1])

    def get_data(self):
        return_dict = {'tek_rig': self.rig}
        return_dict['sequence_path'] = self.sequence_path
        return_dict['frame_range'] = self.frame_range
        return_dict['start_at_zero'] = self.start_at_zero
        return_dict['root_to_origin'] = self.root_to_origin
        return_dict['sequence_notes'] = self.sequence_notes
        return_dict['ui_index'] = self.ui_index
        return return_dict

    def set_data(self, data_dict):
        self.rig = data_dict.get('tek_rig', None)
        self.sequence_path = data_dict.get('sequence_path', '')
        self.frame_range = data_dict.get('frame_range', [0, 100])
        self.start_at_zero = data_dict.get('start_at_zero', True)
        self.root_to_origin = data_dict.get('root_to_origin', False)
        self.sequence_notes = data_dict.get('sequence_notes', '')
        self.ui_index = data_dict.get('ui_index', 0)


def _get_sequences():
    """
    From the FragSequencer return all registered sequences.

    :return: A dictionary of TEKRigs to sequence_paths to AnimSequencer, the TEKSequencer node, and the current index.
    :rtype: dict, TEKSequencer, int
    """
    tek_sequencer = tek.get_tek_sequencer()
    entry_dict = {}
    current_index = 0
    for sequence_entry in tek_sequencer.sequence_list.iterDescendants(1):
        current_index = sequence_entry.index() + 1
        sequence_wrapper = AnimSequence(sequence_entry)
        sequence_tek_rig = sequence_wrapper.rig or sequence_wrapper.pynode.rig.get()
        if sequence_tek_rig not in entry_dict:
            # None entries are okay.
            entry_dict[sequence_tek_rig] = {}
        entry_dict[sequence_tek_rig][sequence_wrapper.sequence_path] = sequence_wrapper
    return entry_dict, tek_sequencer, current_index


def get_sequences():
    """
    Wrapper function that returns only the sequencer's data dict.

    :return: A dictionary of TEKRigs to sequence_paths to AnimSequencer
    :rtype dict
    """
    entry_dict, _, __ = _get_sequences()
    return entry_dict


def set_sequence(sequence_path, tek_rig, frame_range, start_at_zero=True, root_to_origin=True, sequence_notes=None):
    """
    Set a new sequence on the FragSequencer.

    :param str sequence_path: The unique identifying fbx path for this rig's sequence.
    :param TEKRig tek_rig: The TEKRig related to the sequence entry.
    :param list[int, int] frame_range: A list containing the starting and ending frames of the sequence.
    :param bool start_at_zero: Stored value if the animation should be set to frame 0 before exporting.
    :param bool root_to_origin: Stored value if the animation should move the root node to origin before exporting.
    :param str sequence_notes: Any notes about this particular sequence.
    :return: The newly set AnimSequence wrapper class.
    :rtype: AnimSequence
    """
    entry_dict, tek_sequencer, current_index = _get_sequences()

    sequence_path = path_utils.to_relative_path(sequence_path)

    sequence_wrapper = None
    if tek_rig in entry_dict:
        if sequence_path in entry_dict[tek_rig]:
            sequence_wrapper = entry_dict[tek_rig][sequence_path]

    if not sequence_wrapper:
        sequence_wrapper = AnimSequence(tek_sequencer.sequence_list[current_index])
        ui_index = len(entry_dict.get(tek_rig, {}))
    else:
        ui_index = sequence_wrapper.ui_index

    sequence_wrapper.set_data({'tek_rig': tek_rig,
                               'sequence_path': sequence_path,
                               'frame_range': frame_range,
                               'start_at_zero': start_at_zero,
                               'root_to_origin': root_to_origin,
                               'sequence_notes': sequence_notes,
                               'ui_index': ui_index})

    if not sequence_wrapper.bookmark:
        timeslider_bookmark = time_utils.create_bookmark(sequence_wrapper.name, [frame_range[0], frame_range[-1]])
        sequence_wrapper.bookmark = timeslider_bookmark
        # $BUG FSchorsch the timeslider cannot have incoming connections to its start/stop ranges it won't update.
        #sequence_wrapper.pynode.start_frame >> timeslider_bookmark.timeRangeStart
        #sequence_wrapper.pynode.end_frame >> timeslider_bookmark.timeRangeStop
    else:
        sequence_wrapper.bookmark.timeRangeStart.set(frame_range[0])
        sequence_wrapper.bookmark.timeRangeStop.set(frame_range[-1])

    return sequence_wrapper


def remove_sequence(sequence_path, tek_rig):
    """
    Remove an entry in the TEKSequencer based on the path and tek rig.

    :param str sequence_path: The unique identifying fbx path for this rig's sequence.
    :param TEKRig tek_rig: The TEKRig related to the sequence entry.
    """
    entry_dict, tek_sequencer, current_index = _get_sequences()
    sequence_path = path_utils.to_relative_path(sequence_path)
    sequence_wrapper = None
    if tek_rig in entry_dict:
        if sequence_path in entry_dict[tek_rig]:
            sequence_wrapper = entry_dict[tek_rig][sequence_path]
    if sequence_wrapper:
        pm.delete(sequence_wrapper.bookmark)
        sequence_wrapper.pynode.remove(b=True)
        refresh_ui_index()


def reorder_sequence(sequence_path, tek_rig, positive_move):
    """
    Adjust the ui_index value for an entry based on the tek_rig and sequence_path

    :param str sequence_path: The unique identifying fbx path for this rig's sequence.
    :param TEKRig tek_rig: The TEKRig related to the sequence entry.
    :param bool positive_move: If the entry's ui_index should be moved towards the head of the list or further down.
        True = lower index position, False = higher index position.
    :return:
    """
    entry_dict, _, _ = _get_sequences()
    entry_dict = entry_dict.get(tek_rig)
    if entry_dict:
        sequence_wrapper = entry_dict.get(sequence_path)
        if sequence_wrapper:
            sorted_entry_list = sorted(entry_dict.values(), key=lambda sequence_wrapper: sequence_wrapper.ui_index)
            entry_index = sorted_entry_list.index(sequence_wrapper)

            replacement_entry = None
            if positive_move and entry_index > 0:
                replacement_entry = sorted_entry_list[entry_index-1]
            elif not positive_move and entry_index < len(sorted_entry_list)-1:
                replacement_entry = sorted_entry_list[entry_index + 1]

            if replacement_entry:
                sequence_wrapper.ui_index = replacement_entry.ui_index
                replacement_entry.ui_index = entry_index
                return True


def refresh_ui_index():
    """
    Iterate through all our sequences and reset the ui_index positions to compensate for gaps or duplicates.

    """
    entry_dict, tek_sequencer, current_index = _get_sequences()

    for tek_rig, sequence_dict in entry_dict.items():
        ui_index_dict = {}
        for _, sequence_wrapper in sequence_dict.items():
            ui_index = sequence_wrapper.ui_index

            while ui_index in ui_index_dict:
                # negate duplicate ui_index values
                ui_index += 1
            ui_index_dict[ui_index] = sequence_wrapper

        for index, (_, sequence_wrapper) in enumerate(sorted(ui_index_dict.items(), key=lambda entry_tuple: entry_tuple[0])):
            sequence_wrapper.ui_index = index


def convert_legacy():
    """
    Convert legacy .notes attribute markup to new entries on the TEK sequencer node.

    """
    for notes_attr in pm.ls('*.notes', r=True):
        notes_str = notes_attr.get()
        # Split notes str on new line and formatting characters.
        split_notes = '::'.join(notes_str.split('\n')[1:]).split('::')
        # Organize them into groups of 8 which includes all the sequence data.
        sequence_str_list = [split_notes[(0 + n) * 9:n * 9 + 9][:-1] for n in range(int(len(split_notes) / 9))]
        # Collect our TEK rig from the objects the notes attr is on.
        tek_rig = tek.get_tek_rig(notes_attr.node()) or notes_attr.node()
        for sequence_str in sequence_str_list:
            if sequence_str[0]:
                sequence_path, start_frame, end_frame, _, __, sequence_notes, root_to_origin, start_at_zero = sequence_str # sequence_path, start_frame, end_frame, exportable, frame_rate, sequence_notes, root_to_origin, start_at_origin
                set_sequence(os.path.normpath(sequence_path), tek_rig, [int(start_frame), int(end_frame)], bool(start_at_zero), bool(root_to_origin), sequence_notes)
        # Remove notes attr so we don't leave this laying around.
        # Node can be locked, so just unlock first then purge.
        notes_attr.unlock()
        notes_attr.node().unlock()
        notes_attr.delete()

    tek_sequencer = tek.get_tek_sequencer()
    tek_sequence_data_dict = {}
    if not tek_sequencer.hasAttr('ui_index'):
        tek_sequence_dict = get_sequences()
        for tek_rig, sequence_dict in tek_sequence_dict.items():
            tek_sequence_data_dict[tek_rig] = []
            for sequence_path, sequence_wrapper in sequence_dict.items():
                tek_sequence_data_dict[tek_rig].append(sequence_wrapper.get_data())
        pm.delete(tek_sequencer)

    for x in pm.ls(type=pm.nt.TimeSliderBookmark):
        # Cleanup old TimeSliderBookmarks
        if not x.message.listConnections():
            pm.delete(x)

    for tek_rig, entries_list in tek_sequence_data_dict.items():
        for entry in entries_list:
            entry.pop('ui_index', None)
            set_sequence(**entry)


def reconnect_orphaned_sequences():
    """
    For all entries on the TEKSequencer that no longer have a TEKRig connection see if there is a matching rig left in the scene.

    """
    sequence_dict = get_sequences()
    if None in sequence_dict:
        tek_root_dict = {tek_root.asset_id: tek_root.get_rig() for tek_root in tek.get_all_tek_roots()}
        for _, sequence_wrapper in sequence_dict[None].items():
            asset_id = sequence_wrapper.asset_id
            tek_rig = tek_root_dict.get(asset_id, None)
            mca_asset = assetlist.get_asset_by_id(asset_id)
            if mca_asset and mca_asset.asset_name.lower() == asset_id:
                # Match by asset_id or asset_name.
                tek_rig = tek_root_dict.get(mca_asset.asset_id, None) or tek_root_dict.get(mca_asset.asset_name.lower(), None)

            if tek_rig:
                sequence_wrapper.rig = tek_rig


def export_tek_sequences(tek_rig_list=None, sequences_to_skip=None):
    """
    From the TEK Sequencer export all registered animations filtering by inclusive tek rig list, or exclusively by sequence path.

    :param list(TEKRig) tek_rig_list: A list of TEKRigs to export. This is done to facilitate selection based rig exporting.
    :param list(str) sequences_to_skip: A list of sequences that should be skipped. This is done so the UI can send a list of sequences to skip.
    """
    scene_utils.backup_scene('animation_exporter')

    namespace_utils.set_namespace('')
    convert_legacy()

    if sequences_to_skip is None:
        sequences_to_skip = []
    else:
        # In case full paths are passed to the fnc.
        sequences_to_skip = [path_utils.to_relative_path(sequence_path) for sequence_path in sequences_to_skip]

    for tek_rig, sequence_dict_list in get_sequences().items():
        if tek_rig:
            current_scale = tek_rig.rig_scale
            if current_scale != 1.0:
                tek_rig.rig_scale = 1.0

        if tek_rig_list and tek_rig not in tek_rig_list:
            # If this tek rig in the sequencer should be skipped
            logger.warning(f'TEKRig: {tek_rig} is not on the whitelist for export.')
            continue

        sequences_to_export = []
        for sequence_path, sequence_wrapper in sequence_dict_list.items():
            if path_utils.to_relative_path(sequence_path) in sequences_to_skip:
                continue
            if sequence_wrapper.sequence_path.lower().endswith('.fbx'):
                sequences_to_export.append(sequence_wrapper)

        if not sequences_to_export:
            # If every sequence in this rig's sequence are skipped.
            logger.warning(f'All sequences are skipped for {tek_rig}.')
            continue

        if len(sequences_to_export) == 1 or len(sequences_to_export) >= .25 * len(sequence_dict_list):
            # if we only have one sequence OR the total number of sequences we're exporting is greater than 25% of the possible sequences.
            if len(sequences_to_export) == 1:
                # Bake selectively
                start_frame, end_frame = sequences_to_export[0].frame_range
                export_root = rig_utils.bake_skeleton_from_rig(tek_rig, start_frame, end_frame, False)
            else:
                start_frame, end_frame = time_utils.get_keyframe_range_from_nodes(tek_rig.get_flags())
                if start_frame is None or end_frame is None:
                    logger.warning(f'There are no keyframes on this rig {tek_rig}.')
                    continue
                # We don't want to shift the keys here our sequences are all coded based on the scene range.
                export_root = rig_utils.bake_skeleton_from_rig(tek_rig, start_frame, end_frame, False)

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
                export_root = rig_utils.bake_skeleton_from_rig(tek_rig, start_frame, end_frame, False)

                if not export_root:
                    logger.warning('Skeleton was not baked, verify .skl file, aborting export.')
                    return

                export_hierarchy = _trim_export_hierarchy(export_root)
                _export_baked_skeleton(export_hierarchy, wrapped_sequence)
                pm.delete(export_root)

        if current_scale != 1.0:
            tek_rig.rig_scale = current_scale


def export_tek_sequences_cmd(tek_rig_list=None, sequences_to_skip=None):
    """
    UI wrapper for the export tek sequences fnc. This will abort if the frame rate isn't set as expected.

    :param list(TEKRig) tek_rig_list: A list of TEKRigs to export. This is done to facilitate selection based rig exporting.
    :param list(str) sequences_to_skip: A list of sequences that should be skipped. This is done so the UI can send a list of sequences to skip.
    """
    frame_rate = pm.currentUnit(q=True, time=True)
    if frame_rate != 'ntsc':
        if messages.question_message('Continue Export?', 'Your frame rate is not set to NTSC 30 FPS. It\'s recommended to have your frame rate set to 30 FPS.') != 'Yes':
            return

    export_tek_sequences(tek_rig_list, sequences_to_skip)


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
    baked_hierarchy = pm.listRelatives(export_root, ad=True) + [export_root]
    joints_to_delete = []
    for joint_node in baked_hierarchy:
        # Trim hierarchy to only animatable joints.
        if not isinstance(joint_node, pm.nt.Joint) or not joint_node.getAttr('animationExport'):
            joints_to_delete.append(joint_node)
    pm.delete(joints_to_delete)
    # Repull hierarchy don't trust the for loop, if we have any odd skeletal markup we could have deleted a joint that
    # is not animation exportable, but has a child that is.
    export_hierarchy = pm.listRelatives(export_root, ad=True, type=pm.nt.Joint)+[export_root]
    return export_hierarchy


def _export_baked_skeleton(export_hierarchy, sequence_wrapper):
    """
    From a baked skeleton and a sequence wrapper export the animation to its destination.

    :param list(Joint) export_hierarchy: A list of all exportable joints.
    :param AnimSequence sequence_wrapper: A wrapped sequence entry representing this export.
    """
    export_path = path_utils.to_full_path(sequence_wrapper.sequence_path)
    frame_range = sequence_wrapper.frame_range
    export_root = export_hierarchy[-1]

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


@decorators.track_fnc
def quick_export_tek_sequences_cmd():
    """
    Wrapper command to convert a selection into a list of TEKRigs, then export all sequences associated with those rigs.

    """
    selection = pm.selected()
    if not selection:
        logger.warning('Please select a rig to continue.')
        return

    frame_rate = pm.currentUnit(q=True, time=True)
    if frame_rate != 'ntsc':
        if messages.question_message('Continue Export?', 'Your frame rate is not set to NTSC 30 FPS. It\'s recommended to have your frame rate set to 30 FPS.') != 'Yes':
            return

    tek_rig_list = set([tek.get_tek_rig(x) for x in selection])
    export_tek_sequences_cmd(tek_rig_list)
