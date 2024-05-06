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
from mca.common.textio import yamlio
from mca.common.modifiers import singleton
from mca.ue.paths import ue_paths
from mca.ue.texturetypes import texture_2d
from mca.ue.utils import materials
from mca.ue.startup.configs import ue_consts
from mca.ue.assettypes import parent_materials, py_base

logger = log.MCA_LOGGER

ASSET_TOOLS = unreal.AssetToolsHelpers.get_asset_tools()
MEL = unreal.MaterialEditingLibrary


MATERIAL_PROPERTIES_EXT = '.matprops'
PROPERTIES_FOLDER = 'MaterialProperties'


class PyMaterialBase(py_base.PyUnrealBaseAssetObject):
    def __init__(self, u_asset, **kwargs):
        super(PyMaterialBase, self).__init__(u_asset)
        self._u_asset = u_asset

    def set_attr(self, property_name, value):
        """
        Sets the value of a property of a material instance constant

        :param str property_name: Name of a property on the material instance constant.
        :param str/vector/float value:
        """

        if isinstance(value, bool):
            MEL.set_material_instance_static_switch_parameter_value(self.u_asset, property_name, bool(str(value)))

        elif isinstance(value, (list, tuple)):
            MEL.set_material_instance_vector_parameter_value(self.u_asset, property_name, value)

        elif isinstance(value, (int, float)):
            MEL.set_material_instance_scalar_parameter_value(self.u_asset, property_name, float(value))

    def get_attr(self, property_name):
        """
        Gets the value of a property of a material instance constant.

        :param str property_name: Name of a property on the material instance constant.
        :return: Returns the value of a property of a material instance constant.
        :rtype: str/vector/float
        """

        result = None
        try:
            result = MEL.get_material_instance_static_switch_parameter_value(self.u_asset, property_name)
        except:
            pass

        try:
            result = MEL.set_material_instance_vector_parameter_value(self.u_asset, property_name)
        except:
            pass

        try:
            MEL.set_material_instance_scalar_parameter_value(self.u_asset, property_name)
        except:
            pass
        return result


class PyMaterialInstanceConstant(PyMaterialBase):
    """
    Base Class for our Python version of Material Instance Constant.
    """

    def __init__(self, u_asset, texture_list=None):
        super().__init__(u_asset)
        if not isinstance(u_asset, unreal.MaterialInstanceConstant):
            msg = f'{u_asset}: Must be an instance of MaterialInstanceConstant'
            logger.error(msg)
            raise TypeError(msg)
        self._u_asset = u_asset
        self.texture_list = texture_list
        if not self.texture_list:
            self.texture_list = self.get_textures()
        self.settings_dict = self.read_property_options()

    @classmethod
    def create(cls, name, folder, parent_material=None, texture_list=None):
        """
        Creates a new PyMaterialInstance

        :param str name: Name of the new material instance
        :param str folder: Path to the new material instance
        :param str or unreal.MaterialInstance or unreal.AssetData parent_material: Parent material instance
        :param list(PyTexture2d) texture_list: List of textures
        :return: New material instance
        :rtype: PyMaterialInstance
        """

        mi_asset = ASSET_TOOLS.create_asset(asset_name=name,
                                            package_path=folder,
                                            asset_class=unreal.MaterialInstanceConstant,
                                            factory=unreal.MaterialInstanceConstantFactoryNew())

        if parent_material:
            if isinstance(parent_material, unreal.AssetData):
                unreal.MaterialEditingLibrary.set_material_instance_parent(mi_asset, parent_material.get_asset())
            elif isinstance(parent_material, unreal.Material):
                unreal.MaterialEditingLibrary.set_material_instance_parent(mi_asset, parent_material)
            elif isinstance(parent_material, str) and os.path.exists(parent_material):
                base_mtl = unreal.EditorAssetLibrary.find_asset_data(parent_material)
                unreal.MaterialEditingLibrary.set_material_instance_parent(mi_asset, base_mtl.get_asset())
            else:
                logger.error(f'Invalid parent material: {parent_material}\n'
                             f'Please make sure you have the correct path or it is a material instance')

        return cls(u_asset=mi_asset, texture_list=texture_list)

    def set_parent_material(self, parent_material):
        """
        Sets the parent material of this material instance.

        :param Unreal.Material parent_material: The material that will be the parent of this material instance
        """

        self.parent_material = parent_material
        unreal.MaterialEditingLibrary.set_material_instance_parent(self.u_asset, self.parent_material)

    def set_parent_material_as_skin_dual(self):
        """
        Sets the parent material of this material instance as a skin dual.
        """

        parent_material = materials.get_master_character_duel_skin()
        self.set_parent_material(parent_material)

    def set_parent_material_as_character(self):
        """
        Sets the parent material of this material instance as a character.
        """

        parent_material = materials.get_character_master()
        self.set_parent_material(parent_material)

    def set_parent_material_as_eye(self):
        """
        Sets the parent material of this material instance for eyes.
        """

        parent_material = materials.get_character_eyeball_master()
        self.set_parent_material(parent_material)

    def set_parent_material_as_eye_wet(self):
        """
        Sets the parent material of this material instance for eyes wetness.
        """

        parent_material = materials.get_character_eye_wet_master()
        self.set_parent_material(parent_material)

    def set_parent_material_as_hair(self):
        """
        Sets the parent material of this material instance for hair.
        """

        parent_material = materials.get_character_hair_master()
        self.set_parent_material(parent_material)

    def get_local_properties_path(self):
        """
        Gets the local properties path of the material instance.
        This is from the folder and not the asset.

        :return: Local properties path
        :rtype: str
        """

        return ue_paths.get_local_tool_prefs_folder(PROPERTIES_FOLDER)

    def get_textures(self):
        """
        Gets the textures paths associated with material instance.
        This is from the folder and not the asset.

        :return: List of textures
        :rtype: list(texture_2d.PyTexture2d)
        """

        textures_paths = texture_2d.get_textures_paths_from_mca_inst_path(self.path)
        textures_path = textures_paths.get('game_paths', None)
        abs_path = textures_paths.get('full_paths', None)
        if not os.path.exists(abs_path):
            return
        texture_list = texture_2d.get_list_of_textures_from_path(abs_path, textures_path)
        return texture_list

    def set_textures(self, textures_list=None, **kwargs):
        """
        Sets the textures of the material instance

        :param list(PyTexture2d) textures_list: List of textures
        """

        if not textures_list:
            textures_list = self.texture_list

        for texture in textures_list:
            if isinstance(texture, texture_2d.PyDiffuse):
                texture_map = texture.game_path_name
                self._set_texture("Albedo Texture", texture_map)
            elif isinstance(texture, texture_2d.PyNormalMap):
                texture_map = texture.game_path_name
                self._set_texture("Normal Texture", texture_map)
            elif isinstance(texture, texture_2d.PyORME):
                texture_map = texture.game_path_name
                self._set_texture("ORME Texture", texture_map)
            elif isinstance(texture, texture_2d.PySSTD):
                texture_map = texture.game_path_name
                self._set_texture("SSTD Texture", texture_map)

    def _set_texture(self, property_name, tex_path):
        """
        Sets a texture for a material instance.

        :param str property_name: Name of the property associated with the texture on the material instance.
        :param str tex_path: Game path to the texture
        :return: Returns if the texture was successfully set.
        :rtype: bool
        """

        if not unreal.EditorAssetLibrary.does_asset_exist(tex_path):
            unreal.log_warning(f"Can't find texture: \n{tex_path}")
            return False
        tex_asset = unreal.EditorAssetLibrary.find_asset_data(tex_path).get_asset()
        return unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(self._u_asset,
                                                                                           property_name,
                                                                                           tex_asset)

    def get_default_properties(self):
        """
        The default properties for the Material Instance.  This is a default set, and should be overridden.
        """

        mat_dict = {}
        mat_dict['Version'] = '1.0.0'
        mat_dict['default'] = {}
        mat_dict['default']['bool'] = {}
        mat_dict['default']['vector'] = {}
        mat_dict['default']['color'] = {}
        mat_dict['default']['float'] = {}
        mat_dict['default']['file'] = {}
        mat_dict['Textures'] = []
        mat_dict['options'] = {}
        self.settings_dict = mat_dict

    def write_property_options(self, file_path, settings_dict=None):
        """
        Writes the property options of the material instance Constant

        :param dict settings_dict: A dictionary all the properties to be set.
        :param str file_path: File path to the settings file.  This is a local path to the documents folder.
        """

        if not settings_dict:
            settings_dict = self.settings_dict

        yamlio.write_to_yaml_file(settings_dict, file_path)

    def read_property_options(self, file_path=None):
        """
        Reads the property options of the material instance Constant

        :param str file_path: File path to the settings file.  This is a local path to the documents' folder.
        """
        if not file_path or not os.path.exists(file_path):
            self.settings_dict = self.get_default_properties()
        else:
            self.settings_dict = yamlio.read_yaml_file(file_path)
        return self.settings_dict

    def set_editor_attributes(self, settings_dict=None):
        """
        Sets the editor attributes of the material instance Constant

        :param dict settings_dict: A dictionary all the properties to be set.
        """

        if not settings_dict:
            settings_dict = self.settings_dict

        for property_name, value in settings_dict['default']['bool'].items():
            MEL.set_material_instance_static_switch_parameter_value(self.u_asset, property_name, bool(str(value)))

        for property_name, value in settings_dict['default']['color'].items():
            MEL.set_material_instance_vector_parameter_value(self.u_asset, property_name, value)

        for property_name, value in settings_dict['default']['float'].items():
            MEL.set_material_instance_scalar_parameter_value(self.u_asset, property_name, float(value))

        for property_name, value in settings_dict['default']['file'].items():
            try:
                MEL.set_material_instance_texture_parameter_value(self.u_asset, property_name, float(value))
            except:
                logger.warning(f'Unable to set Texture: {property_name}.  This is likely due to "Comes" not'
                               f'knowing what function to use to set the value...  Disappointing...')


class PyMCharacterSkinDualMaster(PyMaterialInstanceConstant):
    """
    Material Instance Class for an Instance that uses the M_Character_SkinDual_Master parent Material
    """

    def __init__(self, u_asset, texture_list=None):
        super().__init__(u_asset, texture_list=texture_list)
        self.parent_material = self._u_asset.get_editor_property('parent')
        if not self.parent_material:
            self.set_parent_material_as_skin_dual()

    def set_editor_properties(self):
        """
        Set the editor properties for this material instance as a skin dual.
        """

        self.set_editor_attributes(settings_dict=self.settings_dict)
        self.set_textures(self.texture_list)

    def get_default_properties(self):
        """
        Returns the default properties for the Parent Materials

        :return: Returns the default properties for the Parent Materials
        :rtype: dict
        """

        mat_dict = {}
        mat_dict['Version'] = '1.0.0'
        mat_dict['default'] = {}
        mat_dict['default']['bool'] = {}
        mat_dict['default']['bool'].update({'Albedo Strength': True})
        mat_dict['default']['bool'].update({'Use Hair Noise Breakup': True})
        mat_dict['default']['bool'].update({'Use Hair Mask Edge': True})
        mat_dict['default']['bool'].update({'Use Hair Depth Offset': True})
        mat_dict['default']['bool'].update({'Fake Shader Lighting': True})
        mat_dict['default']['bool'].update({'Two Sided': True})

        mat_dict['default']['vector'] = {}
        mat_dict['default']['color'] = {}
        mat_dict['default']['color'].update({'Albedo Color Tint': (1.0, 1.0, 1.0, 1.0)})  # RGBA
        mat_dict['default']['color'].update({'Albedo Occlusion Color': (0.385417, 0.0135, 0.0, 1.0)})  # RGBA

        mat_dict['default']['float'] = {}
        mat_dict['default']['float'].update({'Albedo Strength': 0.9})
        mat_dict['default']['float'].update({'Albedo Occlusion Power': 2.0})
        mat_dict['default']['float'].update({'Albedo Occlusion Strength': 0.8})
        mat_dict['default']['float'].update({'Skin Roughness Scale': 1.1})
        mat_dict['default']['float'].update({'Skin Detail Roughness Strength': 20.0})
        mat_dict['default']['float'].update({'Skin Fuzz Rough Exponent': 2.0})
        mat_dict['default']['float'].update({'Skin Fuzz Rough Strength': 0.2})

        mat_dict['default']['file'] = {}

        mat_dict['options'] = {}
        mat_dict['options'].update({'Use Subsurface Profile': False})
        mat_dict['options'].update({'Use Subsurface Distance Fading': False})

        self.settings_dict = mat_dict
        return mat_dict

    def write_property_options(self, **kwargs):
        """
        Writes the property options of the material instance Constant
        """

        settings_dict = kwargs.get('settings_dict', None)
        if not settings_dict:
            settings_dict = self.settings_dict

        local_path = self.get_local_properties_path()
        full_path = os.path.join(local_path, ue_consts.SKINDUAL + MATERIAL_PROPERTIES_EXT)
        yamlio.write_to_yaml_file(settings_dict, full_path)

    def read_property_options(self, **kwargs):
        """
        Reads the property options of the material instance Constant
        """

        local_path = self.get_local_properties_path()
        full_path = os.path.join(local_path, ue_consts.SKINDUAL + MATERIAL_PROPERTIES_EXT)

        if not os.path.exists(full_path):
            self.settings_dict = self.get_default_properties()
        else:
            self.settings_dict = yamlio.read_yaml_file(full_path)
        return self.settings_dict

    def set_textures(self, textures_list=None, **kwargs):
        """
        Sets the textures of the material instance

        :param list(PyTexture2d) textures_list: List of textures
        """

        bent_normals = kwargs.get('bent_normals', False)

        if not textures_list:
            textures_list = self.texture_list

        for texture in textures_list:
            if isinstance(texture, texture_2d.PyDiffuse):
                texture_map = texture.game_path_name
                self._set_texture("Albedo Texture", texture_map)
            elif isinstance(texture, texture_2d.PyNormalMap):
                texture_map = texture.game_path_name
                self._set_texture("Normal Texture", texture_map)
            elif isinstance(texture, texture_2d.PyORME):
                texture_map = texture.game_path_name
                self._set_texture("ORME Texture", texture_map)
            elif isinstance(texture, texture_2d.PySSTD):
                texture_map = texture.game_path_name
                self._set_texture("SSTD Texture", texture_map)
            elif isinstance(texture, texture_2d.PyBentNormalMap) and bent_normals:
                texture_map = texture.game_path_name
                self._set_texture("Bent Normal Texture", texture_map)


class PyMCharacterMaster(PyMaterialInstanceConstant):
    """
    Material Instance Class for an Instance that uses the M_Character_Master parent Material
    """

    def __init__(self, u_asset, texture_list=None):
        super().__init__(u_asset, texture_list=texture_list)
        self.parent_material = self._u_asset.get_editor_property('parent')
        if not self.parent_material:
            self.set_parent_material_as_character()

    def set_editor_properties(self):
        """
        Set the editor properties for this material instance as a character.
        """

        self.set_editor_attributes(settings_dict=self.settings_dict)
        self.set_textures(self.texture_list)

    def get_default_properties(self):
        """
        Returns the default properties for the Parent Materials

        :return: Returns the default properties for the Parent Materials
        :rtype: dict
        """

        mat_dict = {}
        mat_dict['Version'] = '1.0.0'
        mat_dict['default'] = {}
        mat_dict['default']['bool'] = {}
        mat_dict['default']['vector'] = {}
        mat_dict['default']['color'] = {}
        mat_dict['default']['float'] = {}
        mat_dict['default']['file'] = {}

        mat_dict['options'] = {}
        mat_dict['options'].update({'Use Bent Normals': False})
        mat_dict['options'].update({'Use Emissive': False})
        mat_dict['options'].update({'Use Filigree': False})
        mat_dict['options'].update({'Use Detail Texture': False})
        mat_dict['options'].update({'Use Simple Decals': False})
        mat_dict['options'].update({'Use Carbon Fiber': False})
        mat_dict['options'].update({'Use Iridescent': False})
        mat_dict['options'].update({'Fuzzy Clothing': False})

        self.settings_dict = mat_dict
        return mat_dict

    def set_textures(self, textures_list=None, **kwargs):
        """
        Sets the textures of the material instance

        :param list(PyTexture2d) textures_list: List of textures
        """

        bent_normals = kwargs.get('bent_normals', False)

        if not textures_list:
            textures_list = self.texture_list

        for texture in textures_list:
            if isinstance(texture, texture_2d.PyDiffuse):
                texture_map = texture.game_path_name
                self._set_texture("Albedo Texture ", texture_map)
            elif isinstance(texture, texture_2d.PyNormalMap):
                texture_map = texture.game_path_name
                self._set_texture("Normal Texture", texture_map)
            elif isinstance(texture, texture_2d.PyORME):
                texture_map = texture.game_path_name
                self._set_texture("ORME Texture", texture_map)
            elif isinstance(texture, texture_2d.PyBentNormalMap) and bent_normals:
                texture_map = texture.game_path_name
                self._set_texture("Bent Normal Texture", texture_map)


class PyMCharacterEyeBallMaster(PyMaterialInstanceConstant):
    """
    Material Instance Class for an Instance that uses the M_Character_EyeBall_Master parent Material
    """


    def __init__(self, u_asset, texture_list=None):
        super().__init__(u_asset, texture_list=texture_list)
        self.parent_material = self._u_asset.get_editor_property('parent')
        if not self.parent_material:
            self.set_parent_material_as_eye()

    def set_editor_properties(self):
        """
        Set the editor properties for this material instance as an eye.
        """

        self.set_editor_attributes(settings_dict=self.settings_dict)
        self.set_textures(self.texture_list)

    def get_default_properties(self):
        """
        Returns the default properties for the Parent Materials

        :return: Returns the default properties for the Parent Materials
        :rtype: dict
        """

        mat_dict = {}
        mat_dict['Version'] = '1.0.0'
        mat_dict['default'] = {}
        mat_dict['default']['bool'] = {}
        mat_dict['default']['bool'].update({'Use Iris Refraction': True})
        mat_dict['default']['bool'].update({'Use Iris Pupil Shaper': True})

        mat_dict['default']['vector'] = {}
        mat_dict['default']['color'] = {}
        mat_dict['default']['float'] = {}
        mat_dict['default']['float'].update({'Eye Refraction Depth': 3.5})
        mat_dict['default']['float'].update({'Iris Radius Scale': 0.17})
        mat_dict['default']['float'].update({'Iris Pupil Dilation': 1.05})
        mat_dict['default']['float'].update({'Iris Pupil Strength': 3.0})

        mat_dict['default']['file'] = {}
        mat_dict['default']['file'].update({'Subsurface Profile': 'SP_Male_01_Head_Caucasian_EyeProfile'})

        mat_dict['options'] = {}

        self.settings_dict = mat_dict
        return mat_dict

    def set_textures(self, textures_list=None, **kwargs):
        """
        Sets the textures of the material instance

        :param list(PyTexture2d) textures_list: List of textures
        """

        if not textures_list:
            textures_list = self.texture_list

        for texture in textures_list:
            if isinstance(texture, texture_2d.PyDiffuse):
                texture_map = texture.game_path_name
                if 'iris' in os.path.basename(texture_map).lower():
                    self._set_texture("Iris Albedo Texture", texture_map)
            elif isinstance(texture, texture_2d.PyNormalMap):
                texture_map = texture.game_path_name
                if 'iris' in os.path.basename(texture_map).lower():
                    self._set_texture("Iris Normal Texture", texture_map)
            elif isinstance(texture, texture_2d.PyDiffuse):
                texture_map = texture.game_path_name
                if 'sclera' in os.path.basename(texture_map).lower():
                    self._set_texture("Sclera Albedo Texture", texture_map)
            elif isinstance(texture, texture_2d.PyNormalMap):
                texture_map = texture.game_path_name
                if 'sclera' in os.path.basename(texture_map).lower():
                    self._set_texture("Sclera Normal Texture", texture_map)


class PyMCharacterEyeOccBlurMaster(PyMaterialInstanceConstant):
    """
    Material Instance Class for an Instance that uses the M_Character_EyeOccBlur_Master parent Material
    """

    def __init__(self, u_asset, texture_list=None):
        super().__init__(u_asset, texture_list=texture_list)
        self.parent_material = self._u_asset.get_editor_property('parent')
        if not self.parent_material:
            self.set_parent_material_as_eye()

    def set_editor_properties(self):
        """
        Set the editor properties for this material instance as an eye.
        """

        self.set_editor_attributes(settings_dict=self.settings_dict)

    def get_default_properties(self):
        """
        Returns the default properties for the Parent Materials

        :return: Returns the default properties for the Parent Materials
        :rtype: dict
        """

        mat_dict = {}
        mat_dict['Version'] = '1.0.0'
        mat_dict['default'] = {}
        mat_dict['default']['bool'] = {}
        mat_dict['default']['bool'].update({'Use Shadow Gradient Debug': True})

        mat_dict['default']['vector'] = {}
        mat_dict['default']['color'] = {}
        mat_dict['default']['color'].update({'ShadowOcclusionColor': (0.3, 0.081750, 0.03, 1.000000)})  # RGBA

        mat_dict['default']['float'] = {}
        mat_dict['default']['float'].update({'Shadow Occlusion Strength': 1.2})
        mat_dict['default']['float'].update({'Overall Opacity': 1.0})
        mat_dict['default']['float'].update({'Blur Mask Border Top Radius': 0.472})
        mat_dict['default']['float'].update({'Blur Mask Border Bottom Radius': 0.128})
        mat_dict['default']['float'].update({'Shadow Top Radius': 0.7})
        mat_dict['default']['float'].update({'Shadow Bottom Radius': 0.3})
        mat_dict['default']['float'].update({'Shadow Inner Radius': 0.208})
        mat_dict['default']['float'].update({'Shadow Outer Radius': 0.424})

        mat_dict['default']['file'] = {}
        mat_dict['Textures'] = {}

        mat_dict['options'] = {}

        self.settings_dict = mat_dict
        return mat_dict


class PyMCharacterEyeWetMaster(PyMaterialInstanceConstant):
    """
    Material Instance Class for an Instance that uses the M_Character_EyeWet_Master parent Material
    """

    def __init__(self, u_asset, texture_list=None):
        super().__init__(u_asset, texture_list=texture_list)
        self.parent_material = self._u_asset.get_editor_property('parent')
        if not self.parent_material:
            self.set_parent_material_as_eye_wet()

    def set_editor_properties(self):
        """
        Set the editor properties for this material instance as eye wet.
        """

        self.set_editor_attributes(settings_dict=self.settings_dict)
        self.set_textures(self.texture_list)

    def get_default_properties(self):
        """
        Returns the default properties for the Parent Materials

        :return: Returns the default properties for the Parent Materials
        :rtype: dict
        """

        mat_dict = {}
        mat_dict['Version'] = '1.0.0'
        mat_dict['default'] = {}
        mat_dict['default']['bool'] = {}
        mat_dict['default']['vector'] = {}
        mat_dict['default']['color'] = {}
        mat_dict['default']['float'] = {}
        mat_dict['default']['float'].update({'Metallic': 0.992})
        mat_dict['default']['float'].update({'Specular': 0.008})
        mat_dict['default']['float'].update({'Roughness': 0.0})
        mat_dict['default']['float'].update({'Opacity': 0.132})

        mat_dict['default']['file'] = {}
        mat_dict['options'] = {}

        self.settings_dict = mat_dict
        return mat_dict

    def set_textures(self, textures_list=None, **kwargs):
        """
        Sets the textures of the material instance

        :param list(PyTexture2d) textures_list: List of textures
        """

        if not textures_list:
            textures_list = self.texture_list

        for texture in textures_list:
            if isinstance(texture, texture_2d.PyRoughnessMap):
                texture_map = texture.game_path_name
                self._set_texture("Wet Fluid Roughness", texture_map)
            elif isinstance(texture, texture_2d.PyNormalMap):
                texture_map = texture.game_path_name
                self._set_texture("Wet Fluid Normal", texture_map)


class PyMCharacterHairMaster(PyMaterialInstanceConstant):
    """
    Material Instance Class for an Instance that uses the M_Character_Hair_Master parent Material
    """

    def __init__(self, u_asset, texture_list=None):
        super().__init__(u_asset, texture_list=texture_list)
        self.parent_material = self._u_asset.get_editor_property('parent')
        if not self.parent_material:
            self.set_parent_material_as_hair()

    def set_editor_properties(self):
        """
        Set the editor properties for this material instance as hair.
        """

        self.set_editor_attributes(settings_dict=self.settings_dict)
        self.set_textures(self.texture_list)

    def get_default_properties(self):
        """
        Returns the default properties for the Parent Materials

        :return: Returns the default properties for the Parent Materials
        :rtype: dict
        """

        mat_dict = {}
        mat_dict['Version'] = '1.0.0'
        mat_dict['default'] = {}
        mat_dict['default']['bool'] = {}
        mat_dict['default']['bool'].update({'Use Hair Occlusion Gradient': True})
        mat_dict['default']['bool'].update({'Use Hair Noise Breakup': True})
        mat_dict['default']['bool'].update({'Use Hair Mask Edge': True})
        mat_dict['default']['bool'].update({'Use Hair Depth Offset': True})
        mat_dict['default']['bool'].update({'Fake Shader Lighting': True})
        mat_dict['default']['bool'].update({'Two Sided': True})

        mat_dict['default']['vector'] = {}
        mat_dict['default']['color'] = {}
        mat_dict['default']['float'] = {}

        mat_dict['default']['file'] = {}
        mat_dict['options'] = {}

        self.settings_dict = mat_dict
        return mat_dict

    def set_textures(self, textures_list=None, **kwargs):
        """
        Sets the textures of the material instance

        :param list(PyTexture2d) textures_list: List of textures
        """

        if not textures_list:
            textures_list = self.texture_list

        for texture in textures_list:
            if isinstance(texture, texture_2d.PyRIDA):
                texture_map = texture.game_path_name
                self._set_texture("PBRTexture_RIDA", texture_map)
            elif isinstance(texture, texture_2d.PyNormalMap):
                texture_map = texture.game_path_name
                self._set_texture("PBRTexture_Normal", texture_map)


def create_mic_names(mic_folder):
    """
    This is before creation.  This returns a dictionary of the mic names and the textures associated with them.

    :param str mic_folder: Path to the Materials folder
    :return: Returns a dictionary of the mic names and the textures associated with them
    :rtype: dict
    """

    # Check to see if the MaterialInstanceConstant folder exists
    if not unreal.EditorAssetLibrary.does_directory_exist(mic_folder):
        unreal.EditorAssetLibrary.make_directory(mic_folder)
    # Get the Texture path
    texture_dict = texture_2d.get_textures_paths_from_mca_inst_path(mic_folder)
    if not texture_dict:
        logger.warning(f'No textures found in folder: {mic_folder}')
        return None

    # Get a list of PyTexture2d objects.  These are the valid textures used in PyUnreal.
    abs_path = texture_dict.get('full_paths', None)
    game_path = texture_dict.get('game_paths', None)
    texture_list = texture_2d.get_list_of_textures_from_path(abs_path, game_path)
    if not texture_list:
        logger.warning(f'No textures found in folder that can be loaded.  '
                       f'D, N, ORME, and SSTD are the only ones support at this time.')
        return

    # Get the texture names
    body_name_list = []
    for texture in texture_list:
        texture_name = texture.name.split('_')[1:-1]
        asset_base_name = '_'.join(texture_name)
        if asset_base_name not in body_name_list:
            body_name_list.append(asset_base_name)

    # Assemble the names into the mic names
    mic_name_list = [f'MI_{x}' for x in body_name_list]

    # Create a dictionary with the mic names and the textures associated with them.
    mic_dict = {}
    for x, name in enumerate(body_name_list):
        texture_inst = [x for x in texture_list if name in x.name]
        if not texture_inst:
            continue
        mic_dict.update({mic_name_list[x]: texture_inst})

    return mic_dict


def create_material_instance(mat_inst_folder):
    """
    Creates materials from the list of textures in the texture path.

    :param str mat_inst_folder: folder path to the Materials folder
    :return: Returns a list of PyMaterialInstanceConstant objects
    :rtype: list(PyMaterialInstanceConstant)
    """

    mic_dict = create_mic_names(mat_inst_folder)
    if not mic_dict:
        return
    mic_assets = []
    for name, texture_list in mic_dict.items():
        parent_material = parent_materials.get_parent_materials(texture_list)
        mi_asset = PyMaterialInstanceConstant.create(name=name,
                                                       folder=mat_inst_folder,
                                                       parent_material=parent_material)
        mi_asset.set_textures(texture_list)
        mi_asset.set_editor_attributes()
        mic_assets.append(mi_asset)
    return mic_assets


class ParentMaterialMapping:
    """
    A class to handle the mapping of the Material Instance Constant attributes
    """

    mi_dict = {ue_consts.SKINDUAL: PyMCharacterSkinDualMaster,
                  ue_consts.MST_CHARACTER: PyMCharacterMaster,
                  ue_consts.MST_EYE: PyMCharacterEyeBallMaster,
                  ue_consts.MST_EYE_WET: PyMCharacterEyeWetMaster,
                  ue_consts.MST_HAIR: PyMCharacterHairMaster,
                  ue_consts.MST_EYE_OCC_BLUR: PyMCharacterEyeOccBlurMaster
                  }

    @classmethod
    def attr(cls, attr_instance):
        """
        Redirects the asset to our PyMaterial and Texture classes

        :param unreal.Object attr_instance: An unreal object
        :return: The asset as an Unreal asset or our PyNode asset.
        :rtype: unreal.Object or PyNode
        """

        if isinstance(attr_instance, str):
            name = attr_instance
        elif isinstance(attr_instance, unreal.MaterialInstanceConstant):
            name = attr_instance.get_editor_property('parent').get_name()
        else:
            name = attr_instance.get_name()
        new_instance = cls.mi_dict.get(name, attr_instance)
        if new_instance == attr_instance:
            return attr_instance
        return new_instance

    def get_parent_material_names(self):
        """
        Returns a list of the names of the materials in the mapping.

        :return: Returns a list of the names of the materials in the mapping.
        :rtype: list(str)
        """

        return list(self.mi_dict.keys())


class PlainMaterialInstances(singleton.SimpleSingleton):
    def __init__(self):
        self.default_materials = self.get_plain_materials()

    def get_plain_materials(self):
        """
        Returns a list of the plain materials.

        :return: Returns a list of the plain materials.
        :rtype: list(unreal.MaterialInstanceConstant)
        """

        plain_materials = []
        for mat in ue_consts.PLAIN_MATERIALS:
            found_mat = materials.get_material(mat)
            if found_mat:
                # Loading asset a second time.  The 1st time it is loaded it returns as a RedirectObject
                plain_materials.append(unreal.load_asset(found_mat.get_path_name()))
        return plain_materials
