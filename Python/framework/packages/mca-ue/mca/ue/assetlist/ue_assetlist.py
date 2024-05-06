# -*- coding: utf-8 -*-

"""
Unreal Asset Singleton.  This will allow separate ui is use the same asset information
"""

# mca python imports
import os
# software specific imports
# mca python imports
from mca.common import log
from mca.common.assetlist import assetlist
from mca.common.modifiers import singleton, decorators
from mca.common.paths import paths
from mca.common.textio import yamlio

logger = log.MCA_LOGGER


ASSET_LIST_DICT = {'asset_type': None, 'asset_name': None}


class UnrealAssetListToolBox(singleton.SimpleSingleton):
    def __init__(self, filename=None):
        self.local_prefs = filename
        if not filename:
            self.local_prefs = get_local_asset_list_prefs()
        self._data = self.read_file()

    @property
    def data(self):
        return self._data

    @property
    def asset_type(self):
        """
        Returns the asset type from the preferences file.

        :return: Returns the asset type from the preferences file.
        :rtype: str
        """

        return self.data.get('asset_type', None)

    @asset_type.setter
    def asset_type(self, value):
        """
        Sets the asset type in the preferences file.

        :param str value: An asset type in the asset list.
        """

        self._data.update({'asset_type': value})

    @property
    def asset_name(self):
        """
        Returns the asset name from the preferences file.

        :return: Returns the asset name from the preferences file.
        :rtype: str
        """

        return self.data.get('asset_name', None)

    @asset_name.setter
    def asset_name(self, value):
        """
        Sets the asset name from the preferences file.

        :param str value: an asset name in the asset list.
        """

        self._data.update({'asset_name': value})

    def get_sub_type_filter(self):
        """
        Returns the subtype filter from the asset list.

        :return: Returns the subtype filter from the asset list.
        :rtype: list(str)
        """

        return [x for x in assetlist.AssetListRegistry().CATEGORY_DICT.get('model', {}).keys() if x not in ['reference']]

    def get_names_from_type(self, type_name=None):
        """
        Returns the names of the assets from the asset list from the asset type.

        :param str type_name: The category of the asset
        :return: Returns the names of the assets from the asset list from the asset type.
        :rtype: list(str)
        """

        if not type_name:
            type_name = self.asset_type
        if not type_name:
            return
        names = assetlist.get_asset_category_dict(type_name)
        return names

    @property
    def asset_data(self, asset_name=None):
        """
        Returns the asset entry from the asset list.

        :param str asset_name: Name of the asset.
        :return: Returns the asset entry from the asset list.
        :rtype: assetlist.MATAsset
        """

        if not asset_name:
            asset_name = self.asset_name
        if not asset_name:
            return
        asset_data = assetlist.get_asset_by_name(asset_name)
        if not asset_data:
            return
        return asset_data

    def reload_asset_list(self):
        """
        Reloads the asset list
        """

        assetlist.AssetListRegistry().reload()

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


def get_local_asset_list_prefs():
    """
    Returns the 'local asset list' preferences file path

    :return: Returns the 'local asset list' preferences file path
    :rtype: str
    """

    local_prefs = paths.get_local_tools_prefs_folder('unreal', 'ue_asset_list')
    local_prefs = os.path.join(local_prefs, 'asset_list_prefs.yaml')
    if not os.path.exists(local_prefs):
        yamlio.write_to_yaml_file(ASSET_LIST_DICT, local_prefs)

    return local_prefs
