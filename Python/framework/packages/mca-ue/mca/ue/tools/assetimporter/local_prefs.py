# -*- coding: utf-8 -*-

"""
Saving preferences for the toolbox
"""

# mca python imports
import os
# software specific imports
# mca python imports
from mca.common.paths import paths
from mca.common.textio import yamlio
from mca.ue.paths import ue_paths


class AssetImportPreferences:
    """
    Saving preferences for the Asset Import Tool
    """

    def __init__(self, filename=None):
        self.local_prefs = filename
        if not filename:
            self.local_prefs = get_local_asset_import_prefs()
        self._data = self.read_file()

    @property
    def data(self):
        return self._data

    def read_file(self):
        """
        Reads the preferences file
        """

        data = yamlio.read_yaml_file(self.local_prefs)
        return data

    def write_file(self):
        """
        Writes the preferences file
        """
        if not os.path.exists(self.local_prefs):
            os.makedirs(os.path.dirname(self.local_prefs))
        yamlio.write_to_yaml_file(self.data, self.local_prefs)

    @property
    def asset_type(self):
        return self.data.get('asset_type', None)

    @asset_type.setter
    def asset_type(self, value):
        self._data.update({'asset_type': value})

    @property
    def asset_name(self):
        return self.data.get('asset_name', None)

    @asset_name.setter
    def asset_name(self, value):
        self._data.update({'asset_name': value})

    @property
    def create_materials(self):
        return self.data.get('create_materials', 0)

    @create_materials.setter
    def create_materials(self, value):
        self._data.update({'create_materials': value})

    @property
    def master_material(self):
        return self.data.get('master_material', None)

    @master_material.setter
    def master_material(self, value):
        self._data.update({'master_material': value})

    @property
    def subsurface_profile(self):
        return self.data.get('use_subsurface_profile', None)

    @subsurface_profile.setter
    def subsurface_profile(self, value):
        self._data.update({'use_subsurface_profile': value})

    @property
    def use_subsurface_distance_fading(self):
        return self.data.get('use_subsurface_distance_fading', None)

    @use_subsurface_distance_fading.setter
    def use_subsurface_distance_fading(self, value):
        self._data.update({'use_subsurface_distance_fading': value})

    @property
    def use_emissive(self):
        return self.data.get('use_emissive', None)

    @use_emissive.setter
    def use_emissive(self, value):
        self._data.update({'use_emissive': value})

    @property
    def use_bent_normals(self):
        return self.data.get('use_bent_normals', None)

    @use_bent_normals.setter
    def use_bent_normals(self, value):
        self._data.update({'use_bent_normals': value})

    @property
    def use_filigree(self):
        return self.data.get('use_filigree', None)

    @use_filigree.setter
    def use_filigree(self, value):
        self._data.update({'use_filigree': value})

    @property
    def use_detail_texture(self):
        return self.data.get('use_detail_texture', None)

    @use_detail_texture.setter
    def use_detail_texture(self, value):
        self._data.update({'use_detail_texture': value})

    @property
    def use_iridescent(self):
        return self.data.get('use_iridescent', None)

    @use_iridescent.setter
    def use_iridescent(self, value):
        self._data.update({'use_iridescent': value})

    @property
    def use_fuzzy_clothing(self):
        return self.data.get('use_fuzzy_clothing', None)

    @use_fuzzy_clothing.setter
    def use_fuzzy_clothing(self, value):
        self._data.update({'use_fuzzy_clothing': value})

    @property
    def use_carbon_fiber(self):
        return self.data.get('use_carbon_fiber', None)

    @use_carbon_fiber.setter
    def use_carbon_fiber(self, value):
        self._data.update({'use_carbon_fiber': value})

    @property
    def use_simple_decals(self):
        return self.data.get('use_simple_decals', None)

    @use_simple_decals.setter
    def use_simple_decals(self, value):
        self._data.update({'use_simple_decals': value})


def get_local_asset_import_prefs():
    local_prefs = paths.get_local_tools_prefs_folder('unreal', 'asset_importer')
    local_prefs = os.path.join(local_prefs, 'asset_import_prefs.yaml')
    if not os.path.exists(local_prefs):
        yamlio.write_to_yaml_file({}, local_prefs)

    return local_prefs


def get_asset_import_prefs(filename):
    common_prefs = ue_paths.get_tool_prefs_folder('asset_importer')
    local_prefs = os.path.join(common_prefs, filename)
    if not '.properties' in common_prefs:
        common_prefs += '.properties'
    if not os.path.exists(common_prefs):
        yamlio.write_to_yaml_file({}, common_prefs)

    return common_prefs
