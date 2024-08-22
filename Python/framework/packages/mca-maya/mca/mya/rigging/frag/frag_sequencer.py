#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to the frag sequencer and their usage.
"""

# python imports
import os

# software specific imports
import pymel.all as pm

# Project python imports
from mca.common.assetlist import assetlist
from mca.common.utils import list_utils, path_utils

from mca.mya.animation import time_utils
from mca.mya.modifiers import ma_decorators

from mca.mya.rigging.frag import frag_base
from mca.mya.rigging.frag.components import frag_root

from mca.common import log
logger = log.MCA_LOGGER

class AnimSequence(object):
    """
    Class wrapper for the animation sequencer attributes, just to make these a little easier to work with.

    # NOTE: Do not switch .get/.set calls here to getAttr/setAttr as they're attributes NOT a base PyNode.
    """

    def __init__(self, sequencer_attr):
        self.pynode = sequencer_attr

    @property
    def rig(self):
        found_connection = self.pynode.rig.get()
        if found_connection:
            try:
                return frag_base.FRAGNode(found_connection)
            except:
                logger.warning('Rig connection is missing or not a valid FRAGRig')
                return None

    @rig.setter
    def rig(self, frag_rig):
        pm.disconnectAttr(self.pynode.rig)
        if frag_rig:
            frag_rig.pynode.message >> self.pynode.rig
            asset_id = frag_rig.asset_id
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
            bookmark_node.setAttr('timeRangeStart', frame_range[0])
            bookmark_node.setAttr('timeRangeStop', frame_range[-1])
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
        if self.sequence_path:
            return '.'.join(os.path.split(self.sequence_path)[-1].split('.')[:-1])
        else:
            ''

    def get_data(self):
        return_dict = {'frag_rig': self.rig}
        return_dict['sequence_path'] = self.sequence_path
        return_dict['frame_range'] = self.frame_range
        return_dict['start_at_zero'] = self.start_at_zero
        return_dict['root_to_origin'] = self.root_to_origin
        return_dict['sequence_notes'] = self.sequence_notes
        return_dict['ui_index'] = self.ui_index
        return return_dict

    def set_data(self, data_dict):
        self.rig = data_dict.get('frag_rig', None)
        self.sequence_path = data_dict.get('sequence_path', '')
        self.frame_range = data_dict.get('frame_range', [0, 100])
        self.start_at_zero = data_dict.get('start_at_zero', True)
        self.root_to_origin = data_dict.get('root_to_origin', False)
        self.sequence_notes = data_dict.get('sequence_notes', '')
        self.ui_index = data_dict.get('ui_index', 0)


class FRAGSequencer(frag_base.FRAGNode):
    _version = 1.0

    @classmethod
    @ma_decorators.keep_namespace_decorator
    def create(cls, **kwargs):
        """
        Note this will try and return an existing node rather than make a new one. There should only be one FRAGSequence per scene.

        :return: A new or existing FRAGSequencer node.
        :rtype: FRAGSequencer
        """
        frag_sequencer_list = frag_base.get_all_frag_nodes(frag_type=FRAGSequencer)
        prime_sequencer = None
        if len(frag_sequencer_list) > 1:
            # We have more than one sequencer node.
            prime_sequencer = frag_sequencer_list[0]
            for frag_sequencer in frag_sequencer_list[1:]:
                prime_sequencer.merge_sequence(frag_sequencer)
        elif frag_sequencer_list:
            prime_sequencer = frag_sequencer_list[0]
        
        if prime_sequencer:
            return prime_sequencer

        frag_sequencer = super().create(**kwargs)
        sequencer_pynode = frag_sequencer.pynode
        
        # Set Namespace
        pm.namespace(set=':')

        # Create the FRAG Rig Network Node
        pm.addAttr(sequencer_pynode, longName='anchor', attributeType='message')
        # Create a second network connection to keep the node live in case its other connections are removed.
        sequence_anchor = list_utils.get_first_in_list(pm.ls('frag_anchor', r=True)) or pm.createNode(pm.nt.Network, n='frag_anchor')
        sequence_anchor.message >> sequencer_pynode.anchor

        pm.addAttr(sequencer_pynode, longName='sequence_list', attributeType='compound', numberOfChildren=10, multi=True)

        pm.addAttr(sequencer_pynode, longName='rig', attributeType='message', parent='sequence_list')
        pm.addAttr(sequencer_pynode, longName='asset_id', dataType='string', parent='sequence_list')
        pm.addAttr(sequencer_pynode, longName='bookmark', attributeType='message', parent='sequence_list')

        pm.addAttr(sequencer_pynode, longName='sequence_path', dataType='string', parent='sequence_list')

        pm.addAttr(sequencer_pynode, longName='start_frame', attributeType='short', parent='sequence_list')
        pm.addAttr(sequencer_pynode, longName='end_frame', attributeType='short', parent='sequence_list')

        pm.addAttr(sequencer_pynode, longName='start_at_zero', attributeType='bool', parent='sequence_list')
        pm.addAttr(sequencer_pynode, longName='root_to_origin', attributeType='bool', parent='sequence_list')
        pm.addAttr(sequencer_pynode, longName='sequence_notes', dataType='string', parent='sequence_list')
        pm.addAttr(sequencer_pynode, longName='ui_index', attributeType='short', parent='sequence_list')

        return frag_sequencer
    
    def remove(self):
        sequence_anchor = self.pynode.getAttr('anchor')
        if sequence_anchor:
            pm.delete(sequence_anchor)
        super().remove()

    def merge_sequence(self, frag_sequencer):
        """
        Merge the data contained on another FRAGSequencer to this one.

        :param FRAGSequencer frag_sequencer: The FRAGSequencer we should merge data from.
        """
        sequence_dict = frag_sequencer.get_sequences()
        for _, sequence_data in sequence_dict.items():
            for _, sequence_wrapper in sequence_data.items():
                self.set_sequence(**sequence_wrapper.get_data())
        frag_sequencer.remove()

    def _get_sequences_and_index(self):
        sequence_dict = {}
        current_index = 0
        for sequence_entry in self.pynode.sequence_list.iterDescendants(1):
            current_index = sequence_entry.index() + 1
            sequence_wrapper = AnimSequence(sequence_entry)
            frag_rig = sequence_wrapper.rig
            if frag_rig not in sequence_dict:
                # None entries are okay.
                sequence_dict[frag_rig] = {}
            sequence_dict[frag_rig][sequence_wrapper.sequence_path] = sequence_wrapper
        return sequence_dict, current_index

    def get_sequences(self):
        """
        Return data on all sequences registered with this FRAGSequencer node, along with this Sequencer's current open index.

        :return: A dictionary containing all frag rigs registered with this node, and every animation registered to that rig.
        :rtype: dict, int
        """
        sequence_dict, _ = self._get_sequences_and_index()
        return sequence_dict
    
    def set_sequence(self, sequence_path, frag_rig, frame_range, start_at_zero=True, root_to_origin=True, sequence_notes=None, **kwargs):
        """
        Set a new sequence on the FragSequencer.

        :param str sequence_path: The unique identifying fbx path for this rig's sequence.
        :param FRAGRig frag_rig: The FRAGRig related to the sequence entry.
        :param list[int, int] frame_range: A list containing the starting and ending frames of the sequence.
        :param bool start_at_zero: Stored value if the animation should be set to frame 0 before exporting.
        :param bool root_to_origin: Stored value if the animation should move the root node to origin before exporting.
        :param str sequence_notes: Any notes about this particular sequence.
        :return: The newly set AnimSequence wrapper class.
        :rtype: AnimSequence
        """
        sequence_dict, current_index = self._get_sequences_and_index()

        sequence_path = path_utils.to_relative_path(sequence_path)
        if not sequence_path:
            return

        sequence_wrapper = sequence_dict.get(frag_rig, {}).get(sequence_path)
        if not sequence_wrapper:
            sequence_wrapper = AnimSequence(self.pynode.sequence_list[current_index])
            ui_index = len(sequence_dict.get(frag_rig, {}))
        else:
            ui_index = sequence_wrapper.ui_index

        sequence_wrapper.set_data({'frag_rig': frag_rig,
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
    
    def remove_sequence(self, sequence_path, frag_rig):
        """
        Remove an entry in the FRAGSequencer based on the path and frag rig.

        :param str sequence_path: The unique identifying fbx path for this rig's sequence.
        :param FRAGRig frag_rig: The FRAGRig related to the sequence entry.
        """
        sequence_dict = self.get_sequences()
        sequence_path = path_utils.to_relative_path(sequence_path)
        sequence_wrapper = None
        if frag_rig in sequence_dict:
            if sequence_path in sequence_dict[frag_rig]:
                sequence_wrapper = sequence_dict[frag_rig][sequence_path]
        if sequence_wrapper:
            pm.delete(sequence_wrapper.bookmark)
            sequence_wrapper.pynode.remove(b=True)

    def reorder_sequence(self, sequence_path, frag_rig, positive_move):
        """
        Adjust the ui_index value for an entry based on the frag_rig and sequence_path

        :param str sequence_path: The unique identifying fbx path for this rig's sequence.
        :param FRAGRig frag_rig: The FRAGRig related to the sequence entry.
        :param bool positive_move: If the entry's ui_index should be moved towards the head of the list or further down.
            True = lower index position, False = higher index position.
        :return:
        """
        sequence_dict = self.get_sequences()
        sequence_dict = sequence_dict.get(frag_rig)
        if sequence_dict:
            sequence_wrapper = sequence_dict.get(sequence_path)
            if sequence_wrapper:
                sorted_entry_list = sorted(sequence_dict.values(), key=lambda sequence_wrapper: sequence_wrapper.ui_index)
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
                
    def reconnect_orphaned_sequences(self):
        """
        For all entries on the FRAGSequencer that no longer have a FRAGRig connection see if there is a matching rig left in the scene.

        """
        sequence_dict = self.get_sequences()
        if None in sequence_dict:
            frag_root_dict = {frag_root.asset_id: frag_root.get_rig() for frag_root in frag_root.get_all_frag_roots()}
            for _, sequence_wrapper in sequence_dict[None].items():
                asset_id = sequence_wrapper.asset_id
                frag_rig = frag_root_dict.get(asset_id, None)
                cpg_asset = assetlist.get_asset_by_id(asset_id)
                if cpg_asset and cpg_asset.asset_name.lower() == asset_id:
                    # Match by asset_id or asset_name.
                    frag_rig = frag_root_dict.get(cpg_asset.asset_id, None) or frag_root_dict.get(cpg_asset.asset_name.lower(), None)

                if frag_rig:
                    sequence_wrapper.rig = frag_rig
    
def get_frag_sequencer(create=True):
    """
    Find or create the FRAGSequencer node.

    :param bool create: If the new node should be created.
    :return: The scenes FRAGSequencer
    :rtype: FRAGSequencer
    """

    frag_sequencer_list = frag_base.get_all_frag_nodes(frag_type=FRAGSequencer)
    prime_sequencer = None
    if len(frag_sequencer_list) > 1:
        # We have more than one sequencer node.
        prime_sequencer = frag_sequencer_list[0]
        for frag_sequencer in frag_sequencer_list[1:]:
            prime_sequencer.merge_sequence(frag_sequencer)
    elif frag_sequencer_list:
        prime_sequencer = frag_sequencer_list[0]
    elif create:
        prime_sequencer = FRAGSequencer.create()
    return prime_sequencer
