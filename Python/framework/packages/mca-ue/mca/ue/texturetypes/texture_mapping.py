# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
import os
# software specific imports
import unreal
# mca python imports
from mca.common.paths import paths
from mca.common.textio import yamlio
from mca.ue.startup.configs import ue_consts

MEL = unreal.MaterialEditingLibrary


class TextureAttrSettings:

    def export_standard_default_skindual(self):
        """
        Exports the default values for the Parent Material SkinDual

        :return: Returns a dictionary with the default values
        :rtype: dict
        """

        data_dict = {}
        data_dict.update({'bool': {}})  # static_switch_parameter_value
        data_dict['bool'].update({"Use Texture UDIMs": False})
        data_dict['bool'].update({"Use Subsurface Profile": True})
        data_dict['bool'].update({"Use Subsurface Distance Fading": True})
        data_dict['bool'].update({"Use Emissive": True})

        data_dict.update({'color': {}})  # vector_parameter_value
        data_dict['color'].update({"Emissive Color": (0.531250, 0.042531, 0.000000, 1.000000)})  # RGBA

        data_dict.update({'float': {}})  # scalar_parameter_value
        data_dict['float'].update({"Albedo Occlusion Power": 1.0})
        data_dict['float'].update({"Albedo Occlusion Strength": 0.2})
        data_dict['float'].update({"Emissive inner Glow": 0.5})
        data_dict['float'].update({"Emissive inner Base": 2.0})
        data_dict['float'].update({"Emissive Darken Fresnel": 0.25})
        data_dict['float'].update({"Emissive Mask Bias": 0.1})
        data_dict['float'].update({"Emissive Strength": 250.0})
        data_dict['float'].update({"Emissive Motion Speed": 0.0})
        data_dict['float'].update({"Skin Roughness Scale": 0.9})
        data_dict['float'].update({"Skin Detail Normal Strength": 0.0})

        path = os.path.join(self.common_path(), ue_consts.SKINDUAL)
        yamlio.write_to_yaml_file(data_dict, path)

    def export_standard_default_master_character(self):
        """
        Exports the default values for the Parent Material SkinDual

        :return: Returns a dictionary with the default values
        :rtype: dict
        """

        data_dict = {}
        data_dict.update({'bool': {}})  # static_switch_parameter_value
        data_dict['bool'].update({"Use Texture UDIMs": False})
        data_dict['bool'].update({"Use Subsurface Profile": True})
        data_dict['bool'].update({"Use Subsurface Distance Fading": True})
        data_dict['bool'].update({"Use Emissive": True})

        data_dict.update({'color': {}})  # vector_parameter_value
        data_dict['color'].update({"Emissive Color": (0.531250, 0.042531, 0.000000, 1.000000)})  # RGBA

        data_dict.update({'float': {}})  # scalar_parameter_value
        data_dict['float'].update({"Albedo Occlusion Power": 1.0})
        data_dict['float'].update({"Albedo Occlusion Strength": 0.2})
        data_dict['float'].update({"Emissive inner Glow": 0.5})
        data_dict['float'].update({"Emissive inner Base": 2.0})
        data_dict['float'].update({"Emissive Darken Fresnel": 0.25})
        data_dict['float'].update({"Emissive Mask Bias": 0.1})
        data_dict['float'].update({"Emissive Strength": 250.0})
        data_dict['float'].update({"Emissive Motion Speed": 0.0})
        data_dict['float'].update({"Skin Roughness Scale": 0.9})
        data_dict['float'].update({"Skin Detail Normal Strength": 0.0})

        path = os.path.join(self.common_path(), ue_consts.SKINDUAL)
        yamlio.write_to_yaml_file(data_dict, path)

    def common_path(self):
        """
        Returns the path to the folder where the settings are stored

        :return: Returns the path to the folder where the settings are stored
        :rtype: str
        """

        folder_path = paths.get_common_tools_path()
        settings_path = os.path.join(folder_path, ue_consts.UNREAL_FOLDER, ue_consts.MCA_SETTINGS)
        if not os.path.exists(settings_path):
            os.makedirs(settings_path)
        return settings_path
