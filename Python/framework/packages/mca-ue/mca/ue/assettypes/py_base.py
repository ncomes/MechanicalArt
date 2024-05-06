# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
import os
# software specific imports
import unreal
# mca python imports
from mca.common import log
from mca.ue.paths import ue_path_utils


logger = log.MCA_LOGGER


class PyUnrealBaseAssetObject:

    def __init__(self, u_asset):
        self._u_asset = u_asset
        logger.info(self.__class__)

    @property
    def u_asset(self):
        """
        Returns the unreal object

        :return: Returns the unreal object
        :rtype: unreal.Object
        """

        return self._u_asset

    @property
    def path(self):
        """
        Returns the full path name of the asset.
        ex: /path/to/SK_ChaosCaster.SK_ChaosCaster

        :return: Returns the full path name of the asset.
        :rtype: str
        """

        return self.u_asset.get_path_name()

    @property
    def full_path(self):
        """
        Returns the full path name of the asset.
        ex: /path/to/my_asset

        :return: Returns the full path name of the asset.
        :rtype: str
        """

        asset_path = ue_path_utils.convert_to_project_path(self.path)
        full_path = f'{asset_path.split(".")[0]}.uasset'
        return full_path

    @property
    def game_path_name(self):
        """
        Returns the full path name of the asset.
        ex: /path/to/my_asset

        :return: Returns the full path name of the asset.
        :rtype: str
        """

        full_name = self.path.split('.')[0]
        return full_name

    @property
    def character_folder(self):
        """
        Returns the path to the character folder.
        ex: /path/to/my_asset/Characters

        :return: Returns the path to the character folder.
        :rtype: str
        """

        character_path = os.path.dirname(os.path.dirname(self.path))
        return character_path

    @property
    def materials_path(self):
        """
        Returns the path to the materials folder.
        ex: /path/to/my_asset/Materials

        :return: Returns the path to the materials folder.
        :rtype: str
        """

        path = os.path.join(self.character_folder, 'Materials')
        return os.path.normpath(path)

    @property
    def textures_path(self):
        """
        Returns the path to the textures folder.
        ex: /path/to/my_asset/Textures

        :return: Returns the path to the textures folder.
        :rtype: str
        """

        path = os.path.join(self.character_folder, 'Textures')
        return os.path.normpath(path)

    @property
    def animations_path(self):
        """
        Returns the path to the animations folder.
        ex: /path/to/my_asset/Animations

        :return: Returns the path to the animations folder.
        :rtype: str
        """

        path = os.path.join(self.character_folder, 'Animations')
        return os.path.normpath(path)

    @property
    def meshes_path(self):
        """
        Returns the path to the meshes folder.
        ex: /path/to/my_asset/Meshes

        :return: Returns the path to the meshes folder.
        :rtype: str
        """

        path = os.path.join(self.character_folder, 'Meshes')
        return os.path.normpath(path)

    @property
    def asset_name(self):
        """
        Returns the name of the asset.
        EX: SK_ChaosCaster.SK_ChaosCaster

        :return: Returns the name of the asset.
        :rtype: str
        """

        name = os.path.basename(self.path)
        return name

    @property
    def name(self):
        """
        Returns the name of the asset.
        EX: SK_ChaosCaster

        :return: Returns the name of the asset.
        :rtype: str
        """

        name = os.path.basename(self.asset_name.split('.')[0])
        return name

    def get_name(self):
        return self.name

    def get_class(self):
        """
        Returns the Unreal class.

        :return: Returns the Unreal class.
        :rtype: unreal.Object
        """

        return self._u_asset.get_class()

    def set_meta_tags(self, tags):
        """
        Set metadata on the asset.

        :param list(str) tags: list of str attributes to set on the asset.
        """

        for tag in tags:
            unreal.EditorAssetLibrary.set_metadata_tag(self.u_asset, tag, tags[tag])

    def get_meta_tag(self, tag):
        """
        Returns the metadata from the asset.

        :param str tag: string attribute that is used to identify the metadata
        :return: Returns the metadata from the asset.
        :rtype: str
        """

        return unreal.EditorAssetLibrary.get_metadata_tag(self.u_asset, tag)

    @property
    def asset_dir(self):
        """
        Returns the game directory to the asset.
        ex: /path/to/my_asset minus the asset name

        :return: Returns the game directory to the asset.
        :rtype: str
        """

        return os.path.dirname(os.path.dirname(self.path))

    @property
    def asset_id(self):
        """
        Returns the asset id, if it is set.

        :return: Returns the asset id, if it is set.
        :rtype: str
        """

        asset_id = self.get_meta_tag('asset_id')
        if not asset_id:
            logger.warning(f'{self.name} does not have the asset_id set.')
            return
        return asset_id

    @asset_id.setter
    def asset_id(self, value):
        """
        Set the asset id on the asset.

        :param str value: Asset ID
        """

        self.set_meta_tags({'asset_id': value})

    @property
    def original_import_path(self):
        """
        Returns the original FBX import path of the asset.

        :return: Returns the original import path of the asset.
        :rtype: str
        """

        return self.u_asset.get_editor_property("asset_import_data").get_first_filename()

    def set_attr(self, attr_name, value):
        """
        Sets an attribute on the uasset.

        :param str attr_name: attribute name from the editor properties.
        """

        self.u_asset.set_editor_property(attr_name, value)

    def get_attr(self, attr_name):
        """
        Returns an attribute on the uasset.

        :param str attr_name: attribute name from the editor properties.
        :return: Returns an attribute on the uasset.
        :rtype: unreal.EditorProperty
        """

        self.u_asset.get_editor_property(attr_name)

    def save(self):
        """
        Saves the asset.
        """

        unreal.EditorAssetLibrary.save_asset(self.path)
