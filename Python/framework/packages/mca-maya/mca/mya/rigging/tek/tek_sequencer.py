#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.modifiers import ma_decorators
from mca.common.utils import lists
# Internal module imports
from mca.mya.rigging.tek import tek_base


def get_tek_sequencer(create=True):
    """
    Find or create the TEKSequencer node.

    :param bool create: If the new node should be created.
    :return: The scenes TEKSequencer
    :rtype: TEKSequencer
    """
    
    #TODO Maybe merge multiple nodes if they exist?
    sequencer_list = pm.ls('TEKSequencer', r=True, type=pm.nt.Network)
    if sequencer_list:
        return lists.get_first_in_list(sequencer_list)
    elif create:
        return TEKSequencer.create()


class TEKSequencer(tek_base.TEKNode):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create():
        """
        Note this will try and return an existing node rather than make a new one. There should only be one TEKSequence per scene.

        :return: A new or existing TEKSequencer node.
        :rtype: TEKSequencer
        """
        
        # Set Namespace
        pm.namespace(set=':')

        # Create the TEK Rig Network Node
        node = get_tek_sequencer(create=False)
        if not node:
            node = tek_base.TEKNode.create(None, TEKSequencer.__name__, TEKSequencer.VERSION)
            pm.addAttr(node, longName='anchor', attributeType='message')
            # Create a second network connection to keep the node live incase its other connections are removed.
            sequence_anchor = lists.get_first_in_list(pm.ls('tek_anchor', r=True)) or pm.createNode(pm.nt.Network, n='tek_anchor')
            sequence_anchor.message >> node.anchor

            pm.addAttr(node, longName='sequence_list', attributeType='compound', numberOfChildren=10, multi=True)

            pm.addAttr(node, longName='rig', attributeType='message', parent='sequence_list')
            pm.addAttr(node, longName='asset_id', dataType='string', parent='sequence_list')
            pm.addAttr(node, longName='bookmark', attributeType='message', parent='sequence_list')

            pm.addAttr(node, longName='sequence_path', dataType='string', parent='sequence_list')

            pm.addAttr(node, longName='start_frame', attributeType='short', parent='sequence_list')
            pm.addAttr(node, longName='end_frame', attributeType='short', parent='sequence_list')

            pm.addAttr(node, longName='start_at_zero', attributeType='bool', parent='sequence_list')
            pm.addAttr(node, longName='root_to_origin', attributeType='bool', parent='sequence_list')
            pm.addAttr(node, longName='sequence_notes', dataType='string', parent='sequence_list')
            pm.addAttr(node, longName='ui_index', attributeType='short', parent='sequence_list')

        return node
