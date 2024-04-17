#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains fncs for dealing with SkeletonBuilders' main registries.
"""
# System global imports
import copy
import os
# software specific imports
# mca python imports
from mca.common.paths import paths, path_utils, project_paths
from mca.common.utils import dict_utils, strings, fileio
from mca.common.textio import yamlio
from mca.common.modifiers import singleton

from mca.mya.rigging import skel_utils


SKELETON_ARCHETYPE_LIST_PATH = os.path.join(project_paths.MCA_PROJECT_ROOT, r'Tools\Common\Asset List\skeleton_archetype_list.yaml')


class SkeletonArchetypeRegistry(singleton.SimpleSingleton):
    REGISTRY_DICT = {}
    NAME_REGISTRY = {}
    PATH_REGISTRY = {}
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
        self.PATH_REGISTRY = {}

        if os.path.exists(SKELETON_ARCHETYPE_LIST_PATH):
            self.REGISTRY_DICT = yamlio.read_yaml_file(SKELETON_ARCHETYPE_LIST_PATH)
        else:
            # could not find the registry file.
            if not force:
                raise f'{SKELETON_ARCHETYPE_LIST_PATH} The registry file was not found on disk, please verify you have latest.'
            self.REGISTRY_DICT = {}

        for name, data_dict in self.REGISTRY_DICT.items():
            skeleton_archetype = SkeletonArchetype(data_dict)
            self.NAME_REGISTRY[name] = skeleton_archetype
            skel_path = data_dict.get('skel_path', None)
            if skel_path:
                self.PATH_REGISTRY[skel_path] = skeleton_archetype

    def commit(self):
        """
        Save changes to the registry if there was a change made.

        """
        if self.DIRTY:
            fileio.touch_path(SKELETON_ARCHETYPE_LIST_PATH)
            yamlio.write_to_yaml_file(self.REGISTRY_DICT, SKELETON_ARCHETYPE_LIST_PATH)
            self.DIRTY = False

    def register_archetype(self, skeleton_archetype, commit=False):
        """
        This will serialize one of our data classes to the main register.

        :param SkeletonArchetype skeleton_archetype: The helios archetype to be registered.
        :param bool commit: If the registry should be saved after the addition. For perf reasons this can be held until
            multiple registers are completed.
        :return: if the task was completed or failed.
        :rtype: bool
        """

        register_asset = True
        if skeleton_archetype.skel_path and skeleton_archetype.skel_path in self.PATH_REGISTRY:
            if skeleton_archetype.name != self.PATH_REGISTRY[skeleton_archetype.skel_path].name:
                # we're trying to register an entry with an existing name, but different data.
                return False

        if register_asset:
            registry_asset = copy.deepcopy(skeleton_archetype)
            self.NAME_REGISTRY[registry_asset.name] = registry_asset
            self.REGISTRY_DICT[registry_asset.name] = registry_asset.get_data_dict()

            self.DIRTY = True
            if commit:
                self.commit()
        return True

    def remove_entry(self, name, commit=False):
        """
        Remove a skeleton entry by name.

        :param str name: The name associated with a skeleton entry.
        :param bool commit: If the changes should be committed to the registry as part of the remove.
        """
        if name in self.REGISTRY_DICT:
            del self.REGISTRY_DICT[name]
            del self.NAME_REGISTRY[name]
            self.DIRTY = True

            if commit:
                self.commit()

    def get_entry(self, name):
        """
        Return a SKeletonArchetype by name.

        :param str name: The name to look up a skeleton by.
        :return: The found SkeletonArchetype or None
        :rtype: SkeletonArchetype
        """
        data_dict = self.REGISTRY_DICT.get(name)
        if data_dict:
            return SkeletonArchetype(data_dict)


class SkeletonArchetype(object):
    def __init__(self, data_dict):
        self._name = data_dict.get('name', '')
        self._skel_path = data_dict.get('skel_path', '')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def skel_path(self):
        return path_utils.to_full_path(self._skel_path)

    @skel_path.setter
    def skel_path(self, val):
        self._skel_path = path_utils.to_relative_path(val)

    def get_data_dict(self):
        return_dict = {}
        return_dict['name'] = self.name
        return_dict['skel_path'] = self.skel_path
        return return_dict

    def register(self, commit=True):
        registry = SkeletonArchetypeRegistry()
        registry.register_archetype(self, commit=commit)

    def import_skel(self, skel_root=None):
        return skel_utils.import_merge_skeleton(self.skel_path, skel_root)