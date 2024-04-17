#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains fncs for dealing with Helios' main registries.
"""

# System global imports
import copy
import os
# software specific imports
# mca python imports
from mca.common.assetlist import assetlist
from mca.common.paths import paths, path_utils, project_paths
from mca.common.utils import dict_utils, strings, fileio
from mca.common.textio import yamlio
from mca.common.modifiers import singleton


HELIOS_ASSET_LIST_PATH = os.path.join(project_paths.MCA_PROJECT_ROOT, r'Tools\Common\Asset List\helios_asset_list.yaml')
HELIOS_ARCHETYPE_LIST_PATH = os.path.join(project_paths.MCA_PROJECT_ROOT, r'Tools\Common\Asset List\helios_archetype_list.yaml')


class HeliosArchetypeRegistry(singleton.SimpleSingleton):
    REGISTRY_DICT = {}
    NAME_REGISTRY = {}
    DIR_REGISTRY = {}
    DIRTY = False

    def __init__(self, force=False):
        self.reload(force=force)

    def reload(self, force=False):
        self.REGISTRY_DICT = {}
        self.NAME_REGISTRY = {}
        self.DIR_REGISTRY = {}

        if os.path.exists(HELIOS_ARCHETYPE_LIST_PATH):
            self.REGISTRY_DICT = yamlio.read_yaml_file(HELIOS_ARCHETYPE_LIST_PATH)
        else:
            # could not find the registry file.
            if not force:
                raise f'{HELIOS_ARCHETYPE_LIST_PATH} The registry file was not found on disk, please verify you have latest.'
            self.REGISTRY_DICT = {}

        for name, data_dict in self.REGISTRY_DICT.items():
            helios_archetype = HeliosArchetype(data_dict)
            self.NAME_REGISTRY[name] = helios_archetype
            base_dir = data_dict.get('base_dir', None)
            if base_dir:
                self.DIR_REGISTRY[base_dir] = helios_archetype

    def commit(self):
        if self.DIRTY:
            fileio.touch_path(HELIOS_ARCHETYPE_LIST_PATH)
            yamlio.write_to_yaml_file(self.REGISTRY_DICT, HELIOS_ARCHETYPE_LIST_PATH)
            self.DIRTY = False

    def register_asset(self, helios_archetype, commit=False):
        """
        This will serialize one of our data classes to the main register.

        :param HeliosArchetype helios_archetype: The helios archetype to be registered.
        :param bool commit: If the registry should be saved after the addition. For perf reasons this can be held until
            multiple registers are completed.
        """

        registry_asset = copy.deepcopy(helios_archetype)
        self.NAME_REGISTRY[helios_archetype.name] = registry_asset
        self.REGISTRY_DICT[helios_archetype.name] = helios_archetype.get_data_dict()

        self.DIRTY = True
        if commit:
            self.commit()

class HeliosArchetype(object):
    def __init__(self, data_dict):
        self._set_data(data_dict)

    def _set_data(self, data_dict):
        self._asset_name = data_dict.get('name', '')
        self._hierarchy = data_dict.get('hierarchy', {})
        self._base_dir = data_dict.get('base_dir', '')

    @property
    def name(self):
        return self._asset_name

    @name.setter
    def name(self, val):
        self._asset_name = val

    @property
    def hierarchy(self):
        return self._hierarchy

    @hierarchy.setter
    def hierarchy(self, val):
        self._hierarchy = val

    @property
    def base_dir(self):
        return self._base_dir

    @base_dir.setter
    def base_dir(self, val):
        self._base_dir = path_utils.to_full_path(val)

    def get_data_dict(self):
        return_dict = {}
        return_dict['name'] = self._asset_name
        return_dict['hierarchy'] = self._hierarchy
        return_dict['base_dir'] = self._base_dir
        return return_dict

    def register(self, commit=True):
        registry = HeliosArchetypeRegistry()
        registry.register_asset(self, commit=commit)


def create_new_assets_from_archetype(helios_archetype, asset_name, base_dir=None, modified_base_dir=False):
    """
    From a Helios Archetype return the Helios Asset build structure.

    :param HeliosArchetype helios_archetype: A Helios Archetype class.
    :param str asset_name: Name of the new template.
    :param str base_dir: The base directory this asset should be built.
    :param bool modified_base_dir: If the base directory has been modified from the templates expectations.
    :return: A freshly minted mca_asset based off this archetype.
    :rtype: MCAAsset
    """

    mca_asset = convert_template_to_asset(asset_name, base_dir or helios_archetype.base_dir, helios_archetype.hierarchy, modified_base_dir=modified_base_dir)
    return mca_asset


def convert_template_to_asset(asset_name, base_dir, build_dict, remap_dict=None, modified_base_dir=False):
    """
    This converts a template into valid Helios Assets. This is often called recursively depending on the complexity
    of the template.

    :param str asset_name: Name of the new Helios Asset build structure
    :param str base_dir: The base directory this asset should be built.
    :param dict build_dict: Dictionary containing the build structure for the MCA asset.
        Rough example template.
        {'markup':{property_name:property_value},
        'children':nested_dict, #This is optional
        'iterable_data':{'$childname':[str],} # This should only be used with children.
        }
    :param dict remap_dict: A dictionary of strings to values that are remapped within each template entry.
    :param bool modified_base_dir: If the base directory has been modified from the templates expectations.
    :return: MCAAsset that are built from the template.
    :rtype: MCAAsset
    """

    asset_id = strings.generate_guid()
    mca_asset = assetlist.MCAAsset(asset_id, {})

    local_markup = build_dict.get('markup', {})
    iterable_markup = {'$name': asset_name}
    if remap_dict:
        iterable_markup.update(remap_dict)
    for property_name, property_value in local_markup.items():
        for search_str, replace_str in iterable_markup.items():
            property_value = property_value.replace(search_str, replace_str)
        setattr(mca_asset, f'asset_{property_name}', property_value)

    if mca_asset.asset_type == 'model':
        # If a user modified the assumed base dir path to use an alternate naming scheme than what the template expects
        # it'll use that instead of appending the asset name to the path.
        # EG: asset_name is The_Boulder, but the directory path is characters//NPC//Boulder we'll keep "Boulder" and not
        # append "The_Boulder"
        if not modified_base_dir:
            mca_asset.sm_path = os.path.join(base_dir, mca_asset.asset_name, 'Meshes',
                                             f'SM_{mca_asset.asset_name}.fbx')
        else:
            mca_asset.sm_path = os.path.join(base_dir, 'Meshes',
                                             f'SM_{mca_asset.asset_name}.fbx')
    if not modified_base_dir:
        base_dir = os.path.join(base_dir, mca_asset.asset_name)
    child_dict = build_dict.get('children')
    if child_dict:
        for index in range(len(child_dict['iterable_data']['$childname'])):
            child_remap_dict = dict_utils.get_dict_slice(child_dict.get('iterable_data', {}), index)
            child_asset = convert_template_to_asset(asset_name, base_dir, child_dict, child_remap_dict)
            mca_asset.local_asset_list.append(child_asset)
    return mca_asset
