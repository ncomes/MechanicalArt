#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains fncs for dealing with mca's asset list.
"""
# System global imports
import copy
import difflib
import os
# software specific imports
# mca python imports
from mca.common import log
from mca.common.modifiers import singleton
from mca.common.paths import path_utils, project_paths, paths
from mca.common.textio import yamlio
from mca.common.utils import fileio, lists

logger = log.MCA_LOGGER

NON_RIG_ASSETS = ['apparel', 'reference']


class AssetListRegistry(singleton.SimpleSingleton):
    REGISTRY_DICT = {}
    NAME_REGISTRY = {}
    ASSET_ID_DICT = {}
    CATEGORY_DICT = {}
    CATEGORY_NAME_DICT = {}
    PATH_DICT = {}
    DIRTY = False

    def __init__(self, force=False):
        self.reload(force=force)

    def reload(self, force=False):
        """
        Regenerate the registry's lookups.

        :param bool force: If the lookups should be regenerated. Normally once this is initialized they are not reloaded unless requested.
        """
        self.REGISTRY_DICT = {}
        self.NAME_REGISTRY = {}
        self.ASSET_ID_DICT = {}
        self.CATEGORY_DICT = {}
        self.CATEGORY_NAME_DICT = {}
        self.PATH_DICT = {}

        if os.path.exists(paths.get_asset_list_file_path()):
            # Read the file or if the file is empty yield an empty dict.
            self.REGISTRY_DICT = yamlio.read_yaml_file(paths.get_asset_list_file_path()) or {}
        else:
            # could not find the registry file.
            if not force:
                raise f'{paths.get_asset_list_file_path()} The registry file was not found on disk, please verify you have latest.'
            self.REGISTRY_DICT = {}

        for asset_id, data_dict in self.REGISTRY_DICT.items():
            # Build our cached lookups.
            # The name registry is the asset_name to asset_entry
            # The asset_id_dict is unique identifier to asset_entry
            # the category_dict is the organization of type and subtype to asset_entry
            # the path_dict is the asset's full sm_path to asset_entry
            asset_entry = MATAsset(asset_id, data_dict)
            self.ASSET_ID_DICT[asset_id] = asset_entry
            self.NAME_REGISTRY[asset_entry.asset_name] = asset_entry
            if asset_entry.asset_type not in self.CATEGORY_DICT:
                self.CATEGORY_DICT[asset_entry.asset_type] = {}
                self.CATEGORY_NAME_DICT[asset_entry.asset_type] = {}
            if asset_entry.asset_subtype not in self.CATEGORY_DICT[asset_entry.asset_type]:
                self.CATEGORY_DICT[asset_entry.asset_type][asset_entry.asset_subtype] = {}
                self.CATEGORY_NAME_DICT[asset_entry.asset_type][asset_entry.asset_subtype] = {}
            self.CATEGORY_DICT[asset_entry.asset_type][asset_entry.asset_subtype][asset_id] = asset_entry
            self.CATEGORY_NAME_DICT[asset_entry.asset_type][asset_entry.asset_subtype][asset_entry.asset_name] = asset_entry
            self.PATH_DICT[asset_entry.sm_path] = asset_entry

    def commit(self):
        """
        Save changes to the registry if there was a change made.

        """
        if self.DIRTY:
            fileio.touch_path(paths.get_asset_list_file_path())
            yamlio.write_to_yaml_file(self.REGISTRY_DICT, paths.get_asset_list_file_path())
            self.DIRTY = False

    def register_asset(self, mat_asset, commit=False):
        """
        This will serialize one of our data classes to the main register.

        :param MATAsset mat_asset: The mca asset to be registered.
        :param bool commit: If the registry should be saved after the addition. For perf reasons this can be held until
            multiple registers are completed.
        """

        existing_entry = self.ASSET_ID_DICT.get(mat_asset.asset_id)

        if not mat_asset.DIRTY:
            # If nothing has been changed.
            return

        if existing_entry and existing_entry is not mat_asset:
            if existing_entry.get_data_dict() == mat_asset.get_data_dict():
                # We're using a replica of the entry and nothing has been changed.
                return

        mat_asset.DIRTY = False
        registry_asset = copy.deepcopy(mat_asset)
        self.REGISTRY_DICT[registry_asset.asset_id] = registry_asset.get_data_dict()
        self.ASSET_ID_DICT[registry_asset.asset_id] = registry_asset
        self.NAME_REGISTRY[registry_asset.asset_name] = registry_asset
        if registry_asset.asset_type not in self.CATEGORY_DICT:
            self.CATEGORY_DICT[registry_asset.asset_type] = {}
        if registry_asset.asset_subtype not in self.CATEGORY_DICT[registry_asset.asset_type]:
            self.CATEGORY_DICT[registry_asset.asset_type][registry_asset.asset_subtype] = {}
        self.CATEGORY_DICT[registry_asset.asset_type][registry_asset.asset_subtype][registry_asset.asset_id] = registry_asset
        self.PATH_DICT[registry_asset.sm_path] = registry_asset

        if commit:
            self.commit()

    def remove_entry(self, asset_id, commit=False):
        """
        Remove an asset entry by asset_id.

        :param str asset_id: The asset id associated with this MATAsset.
        :param bool commit: If the changes should be committed to the registry as part of the remove.
        """
        if asset_id in self.ASSET_ID_DICT:
            mat_asset = self.ASSET_ID_DICT[asset_id]
            del self.ASSET_ID_DICT[asset_id]
            del self.NAME_REGISTRY[mat_asset.asset_name]
            del self.REGISTRY_DICT[mat_asset.asset_id]
            del self.CATEGORY_DICT[mat_asset.asset_type][mat_asset.asset_subtype][mat_asset.asset_id]
            del self.PATH_DICT[mat_asset.sm_path]
            self.DIRTY = True

            if commit:
                self.commit()

    def get_entry(self, asset_id):
        """
        Return a MATAsset by asset_id.

        :param str asset_id: The asset_id to look up an entry by.
        :return: The found MATAsset or None
        :rtype: MATAsset
        """
        return self.ASSET_ID_DICT.get(asset_id)

    def get_entry_by_name(self, asset_name):
        """
        Return a MATAsset by asset_name.

        :param str asset_name: The name of an asset to lookup.
        :return: The found MATAsset or None
        :rtype: MATAsset
        """
        return self.NAME_REGISTRY.get(asset_name)

    def get_entry_by_path(self, sm_path):
        """
        Return a MATAsset by asset_path.

        :param str sm_path: The path to an entry's SM file.
        :return: The found MATAsset or None
        :rtype: MATAsset
        """
        sm_path = path_utils.to_full_path(sm_path)
        return self.PATH_DICT.get(sm_path)


class MATAsset(object):
    _asset_name = ''
    _asset_namespace = ''
    _sm_path = ''
    _asset_type = ''
    _asset_subtype = ''
    _asset_archetype = ''
    _local_asset_list = []
    
    DIRTY = False

    def __init__(self, asset_id, data_dict):
        self._asset_id = asset_id
        self._set_data(data_dict)

    def _set_data(self, data_dict):
        self._asset_name = data_dict.get('name', '')
        self._asset_namespace = data_dict.get('namespace', '')
        self._sm_path = data_dict.get('path', '')
        self._asset_type = data_dict.get('type', '')
        self._asset_subtype = data_dict.get('subtype', '')
        self._asset_archetype = data_dict.get('archetype', '')
        self._local_asset_list = data_dict.get('local_asset_list', [])
        # We don't want to dirty the class here because this is used to initialize it.
        # If it's a new asset the registry will add it because the asset id is unique.
        # Or if it's a replica of an entry with different data that will trigger the registry to save it as well.

    @property
    def asset_id(self):
        return self._asset_id

    @asset_id.setter
    def asset_id(self, val):
        if val != self._asset_id:
            self.DIRTY = True
        self._asset_id = str(val)

    @property
    def asset_name(self):
        return self._asset_name

    @asset_name.setter
    def asset_name(self, val):
        if val != self._asset_name:
            self.DIRTY = True
        self._asset_name = str(val)

    @property
    def asset_namespace(self):
        return self._asset_namespace

    @asset_namespace.setter
    def asset_namespace(self, val):
        if val != self._asset_namespace:
            self.DIRTY = True
        self._asset_namespace = str(val)

    @property
    def file_name(self):
        # Naming conventions
        # All lower, replace any spaces with underscores.
        return self._asset_name.lower().replace(' ', '_')

    @property
    def asset_type(self):
        # This is the major category: model, collection, <<Gear_Slot>>
        # This should be used or organize the list by how the entry is to be used.
        return self._asset_type

    @asset_type.setter
    def asset_type(self, val):
        if val != self._asset_type:
            self.DIRTY = True
        self._asset_type = str(val)

    @property
    def asset_subtype(self):
        # This is a relative category which refines how the asset can be organized: apparel, npc, combatant, player, prop
        # This is used to organize the entry within user facing lists.
        return self._asset_subtype

    @asset_subtype.setter
    def asset_subtype(self, val):
        if val != self._asset_subtype:
            self.DIRTY = True
        self._asset_subtype = str(val)

    @property
    def asset_archetype(self):
        # This lets us know if the asset is a derivative of another. This is useful for loading rigs from a similar skel type.
        return self._asset_archetype

    @asset_archetype.setter
    def asset_archetype(self, val):
        if val != self._asset_archetype:
            self.DIRTY = True
        self._asset_archetype = str(val)

    @property
    def local_asset_list(self):
        return_list = []
        for entry in self._local_asset_list:
            if isinstance(entry, MATAsset):
                return_list.append(entry)
            else:
                found_entry = get_asset_by_id(entry)
                if found_entry:
                    return_list.append(found_entry)
                else:
                    return_list.append(entry)
        return return_list

    @local_asset_list.setter
    def local_asset_list(self, val_list):
        self.DIRTY = True
        self._local_asset_list = val_list

    # Files
    @property
    def sk_path(self):
        return path_utils.to_full_path(self._sm_path.replace('SM_', 'SK_'))

    @property
    def game_sk_path(self):
        return os.path.join(project_paths.MCA_UNREAL_ROOT, '.'.join(self._sm_path.replace('SM_', 'SK_').split('.')[:-1]))

    @property
    def sm_path(self):
        return path_utils.to_full_path(self._sm_path)

    @sm_path.setter
    def sm_path(self, val):
        # All paths are derived from this original setter.
        relative_val = path_utils.to_relative_path(val)
        if self._sm_path != relative_val:
            self.DIRTY = True
        self._sm_path = relative_val

    @property
    def game_sm_path(self):
        return os.path.join(project_paths.MCA_UNREAL_ROOT, '.'.join(self._sm_path.split('.')[:-1]))

    @property
    def skel_path(self):
        skel_path = os.path.join(path_utils.to_full_path(self.rigs_path), f'{self.file_name}.skl')
        if not os.path.exists(skel_path) and self.asset_archetype:
            asset_entry = get_asset_by_id(self.asset_archetype)
            if asset_entry:
                skel_path = asset_entry.skel_path

        if not os.path.exists(skel_path):
            skel_list = path_utils.all_file_types_in_directory(self.rigs_path, '.skl')
            # see if we have a local skeleton
            if skel_list:
                skel_path = skel_list[0]

        return skel_path

    @property
    def skin_path(self):
        # $TODO think about where to place this. It probably belongs in source but.
        return '.'.join(path_utils.to_full_path(self.sm_path).split('.')[:-1])+'_skn.fbx'

    # Directories
    @property
    def general_path(self):
        # Returns the dir one above the SM's local dir.
        return os.path.split(os.path.dirname(path_utils.to_full_path(self._sm_path)))[0]

    @property
    def game_general_path(self):
        return os.path.join(paths.get_unreal_content_path(), os.path.split(os.path.dirname(self._sm_path))[0])

    @property
    def animations_path(self):
        return os.path.join(self.general_path, 'Animations')

    @property
    def game_animations_path(self):
        return os.path.join(self.game_general_path, 'Animations')

    @property
    def meshes_path(self):
        return os.path.dirname(path_utils.to_full_path(self._sm_path))

    @property
    def game_meshes_path(self):
        return os.path.join(project_paths.MCA_UNREAL_ROOT, os.path.dirname(self._sm_path))

    @property
    def textures_path(self):
        return os.path.join(self.general_path, 'Textures')

    @property
    def game_textures_path(self):
        return os.path.join(self.game_general_path, 'Textures')

    @property
    def game_material_path(self):
        return os.path.join(self.game_general_path, 'Materials')

    @property
    def source_path(self):
        return os.path.join(self.general_path, '_Source')

    @property
    def rigs_path(self):
        return os.path.join(self.source_path, 'Rig')

    @property
    def skin_data_path(self):
        return os.path.join(self.rigs_path, 'Skin_Data')

    @property
    def flags_path(self):
        return os.path.join(self.rigs_path, 'Flags')

    # Registry functions
    def get_data_dict(self):
        return_dict = {}
        return_dict['name'] = self.asset_name
        return_dict['namespace'] = self.asset_namespace
        return_dict['path'] = path_utils.to_relative_path(self.sm_path)
        return_dict['type'] = self.asset_type
        return_dict['subtype'] = self.asset_subtype
        return_dict['archetype'] = self.asset_archetype
        return_dict['local_asset_list'] = [entry.asset_id if isinstance(entry, MATAsset) else entry for entry in self.local_asset_list]
        return return_dict

    def register(self, commit=True):
        registry = AssetListRegistry()
        if self.asset_id not in registry.ASSET_ID_DICT:
            self.DIRTY = True

        if self.DIRTY:
            registry.DIRTY = True
            registry.register_asset(self, commit=commit)

    # Helpers
    def get_rig_list(self):
        """
        Find all rigs associated with this entry.
        Start by looking for all local .rig files.
        If we fail to find check for an explicit .ma rig file.
        If we find no rigs at all check our archetype recursively.

        :return: A list of all found rigs compatible with this asset.
        :rtype: list
        """

        rig_list = path_utils.all_file_types_in_directory(self.rigs_path, '.ma')
        rig_list = [x for x in rig_list if x.lower().endswith('_rig.ma') and all(True if y in os.path.basename(x) else False for y in self.asset_name.lower().replace('_', ' ').split(' '))]

        if not rig_list and self.asset_archetype:
            asset_entry = get_asset_by_id(self.asset_archetype)
            if asset_entry:
                rig_list = asset_entry.get_rig_list()

        return rig_list


def _find_best_match(asset_id):
    """
    Legacy asset lookup. Some of our older asset used the assetname as their asset_id this lets us find a best match.

    :param str asset_id: The asset id we're looking for.
    :return: MATAsset that matches the original name based asset_id
    :rtype: MATAsset
    """
    if not asset_id:
        return

    model_asset_dict = dict([(asset_name.lower(), mat_asset) for asset_name, mat_asset in get_asset_category_dict(None).items()])

    found_match = lists.get_first_in_list(difflib.get_close_matches(asset_id.lower(), model_asset_dict))
    if found_match:
        return model_asset_dict[found_match]


def get_asset_by_id(asset_id):
    """
    Return a MATAsset by asset_id

    :param str asset_id: The asset_id to look up by.
    :return: The MATAsset that matches the asset_id or None
    :rtype: MATAsset
    """
    if not asset_id:
        return

    mat_asset_list = AssetListRegistry()
    found_entry = mat_asset_list.get_entry(asset_id)
    if not found_entry:
        found_entry = _find_best_match(asset_id)
    return found_entry


def get_asset_by_name(asset_name):
    """
    Return a MATAsset by asset name

    :param str asset_name: The asset name to look up by.
    :return: The MATAsset that matches the asset name or None
    :rtype: MATAsset
    """
    if not asset_name:
        return

    logger.debug('Avoid using this function when possible it\'s a weak link to the MATAsset')

    mat_asset_list = AssetListRegistry()
    return mat_asset_list.get_entry_by_name(asset_name)


def get_asset_by_path(sm_path):
    """
    Return a MATAsset by asset_path

    :param str sm_path: The asset_path to look up by.
    :return: The MATAsset that matches the asset_path or None
    :rtype: MATAsset
    """
    if not sm_path:
        return

    mat_asset_list = AssetListRegistry()
    return mat_asset_list.get_entry_by_path(sm_path)


def get_asset_category_dict(asset_subtype=None, asset_type='model', by_name=True):
    """
    Return the entry dictionary of the given category lookups.

    :param str, list asset_subtype: The subtype that should be gotten.
    :param str asset_type: The type that should be gotten.
    :param bool by_name: If a name to asset entry should be returned.
    :return: A dictionary of all entries that match the lookup criteria
    :rtype: dict
    """
    mat_asset_list = AssetListRegistry()
    asset_type = asset_type or 'model'

    if asset_subtype and not isinstance(asset_subtype, list):
        asset_subtype = [asset_subtype]

    return_dict = {}
    if by_name:
        lookup_dict = mat_asset_list.CATEGORY_NAME_DICT
    else:
        lookup_dict = mat_asset_list.CATEGORY_DICT
    for subtype, entry_dict in lookup_dict.get(asset_type, {}).items():
        if asset_subtype and subtype not in asset_subtype:
            continue
        for lookup_identifier, asset_entry in entry_dict.items():
            return_dict[lookup_identifier] = asset_entry
    return return_dict

