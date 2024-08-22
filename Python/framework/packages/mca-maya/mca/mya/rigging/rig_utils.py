#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to interacting with rigs.
"""

# python imports
import abc
import os
import re

# software specific imports
import maya.cmds as cmds
import pymel.all as pm

# Project python imports
from mca.common.assetlist import assetlist
from mca.common.utils import list_utils, fileio, pymaths, string_utils
from mca.common.textio import yamlio

from mca.mya.animation import baking, time_utils
from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import maya_dialogs
from mca.mya.rigging import flags, frag, joint_utils
from mca.mya.tools.helios import helios_utils
from mca.mya.utils import attr_utils, constraint_utils, dag_utils, naming, namespace_utils
from mca.mya.utils.om import om_utils

from mca.common import log
logger = log.MCA_LOGGER

@ma_decorators.keep_namespace_decorator
def import_rig(asset_entry, rig_path, use_namespace=True):
    if use_namespace:
        namespace_to_use = asset_entry.asset_namespace
        if not namespace_to_use:
            base_namespace = re.sub('[^a-zA-Z]+', '', asset_entry.asset_name[:3])
            i = 4
            while len(base_namespace) < 3 and i <= 20:
                base_namespace = re.sub('[^a-zA-Z]+', '', asset_entry.asset_name[:i])
                i += 1
            if base_namespace == '':
                base_namespace = 'zzz'
            found_namespace = namespace_utils.get_namespace(f'{base_namespace}')

            if found_namespace:
                i = 0
                while namespace_utils.get_namespace(found_namespace) != '':
                    i += 1
                    found_namespace = f'{base_namespace}{i}'
            namespace_to_use = found_namespace if found_namespace != '' else base_namespace
        namespace_utils.set_namespace(namespace_to_use.lower())

    frag_root = None
    if rig_path.endswith('ma'):
        # attempting to import a cached rig.
        if not os.path.exists(rig_path):
            result = maya_dialogs.question_prompt('Rig file missing', f'{rig_path}\nFile was missing on disk, sync files.\n\nWould you like to attempt to rebuild the rig instead?')
            if result != 'Yes':
                # Bail out of build
                logger.error('User canceled, import aborted when we couldn\'t find the cached rig.')
                return
            rig_path = rig_path.replace('.ma', '.rig')
        else:
            imported_node_list = pm.importFile(rig_path, returnNewNodes=True)
            for node in pm.ls(imported_node_list, type=pm.nt.Network):
                if node.hasAttr('frag_type') and node.getAttr('frag_type') == 'FRAGRoot':
                    frag_root = frag.FRAGNode(node)
                    break
            pass
    
    if rig_path.endswith('.rig'):
        # attempting to rebuild the rig from scratch.
        organization_group, root_joint_dict = helios_utils.import_asset(asset_entry, with_skinning=True)
        root_joint = None
        if root_joint_dict:
            root_joint = list(root_joint_dict.values())[0]
        else:
            # failed to import a skinned model.
            if result != 'Yes':
                # Bail out of build.
                logger.error('User canceled, import failed to grab mesh + skeleton.')
                pm.delete(organization_group)
                return
            skeleton_path = asset_entry.skeleton_path
            if not skeleton_path or not os.path.exists(skeleton_path):
                # Bail out of build.
                logger.error(f'{Skeleton_path}: Skeleton path was empty or not on disk, aborting import.')
                pm.delete(organization_group)
                return
            root_joint = joint_utils.import_merge_skeleton(skeleton_path)

        if root_joint:
            # From the root joint build out FRAG network and load the rig from the .rig file.
            frag_root = frag.FRAGRoot.create(root_joint, asset_entry.asset_id)
            frag.FRAGDisplay.create(frag_root)
            if organization_group:
                frag_mesh = frag.FRAGMesh.create(frag_root)
                skins_group = frag_mesh.add_skins_group()
                organization_group.setParent(skins_group)

            frag_root.organize_content()
            frag_rig = frag.FRAGRig.create(frag_root)
            frag.load_serialized_rig(frag_rig, rig_path)

    return frag_root