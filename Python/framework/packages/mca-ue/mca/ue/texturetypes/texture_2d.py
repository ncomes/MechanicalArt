# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
import os
# software specific imports
import unreal
# mca python imports
from mca.ue.paths import ue_path_utils
from mca.ue.assettypes import py_base
from mca.common import log


logger = log.MCA_LOGGER


# Todo ncomes: The redirecting classes can be reduced to functions now.
class PyTextureCompressionSettings:
    """
    Class for handling the TextureCompressionSettings enum.
    """

    class_dict = {'default': unreal.TextureCompressionSettings.TC_DEFAULT,
                  'normal_map': unreal.TextureCompressionSettings.TC_NORMALMAP,
                  'masks': unreal.TextureCompressionSettings.TC_MASKS,
                  'grayscale': unreal.TextureCompressionSettings.TC_GRAYSCALE,
                  'displacement_map': unreal.TextureCompressionSettings.TC_DISPLACEMENTMAP,
                  'vector_displacement_map': unreal.TextureCompressionSettings.TC_DISPLACEMENTMAP,
                  'hdr': unreal.TextureCompressionSettings.TC_HDR,
                  'user_interface_2d': unreal.TextureCompressionSettings.TC_EDITOR_ICON,
                  'alpha': unreal.TextureCompressionSettings.TC_ALPHA,
                  'distance_field_font': unreal.TextureCompressionSettings.TC_DISTANCE_FIELD_FONT,
                  'hdr_compressed': unreal.TextureCompressionSettings.TC_HDR_COMPRESSED,
                  'bc7': unreal.TextureCompressionSettings.TC_BC7,
                  'half_float': unreal.TextureCompressionSettings.TC_HALF_FLOAT,
                  'single_float': unreal.TextureCompressionSettings.TC_SINGLE_FLOAT,
                  'hdr_high_precision': unreal.TextureCompressionSettings.TC_SINGLE_FLOAT,
                  }

    @classmethod
    def attr(cls, str_name):
        instance = cls.class_dict.get(str_name, None)
        return instance


class PyTextureLODGroup:
    """
    Class for handling the TextureLODGroup enum.
    """

    class_dict = {'WorldMasks': unreal.TextureGroup.TEXTUREGROUP_PROJECT01,
                  'Character': unreal.TextureGroup.TEXTUREGROUP_CHARACTER,
                  'CharacterMasks': unreal.TextureGroup.TEXTUREGROUP_PROJECT02,
                  'CharacterCEOMasks': unreal.TextureGroup.TEXTUREGROUP_PROJECT03,
                  'WeaponMasks': unreal.TextureGroup.TEXTUREGROUP_PROJECT04,
                  'Vista': unreal.TextureGroup.TEXTUREGROUP_PROJECT05,
                  'World_BC7': unreal.TextureGroup.TEXTUREGROUP_PROJECT06,
                  'HairCoeff': unreal.TextureGroup.TEXTUREGROUP_PROJECT07,
                  'OptTiny_Sharpen': unreal.TextureGroup.TEXTUREGROUP_PROJECT08,
                  'OptSmall_Sharpen': unreal.TextureGroup.TEXTUREGROUP_PROJECT09,
                  'OptMedium_Sharpen': unreal.TextureGroup.TEXTUREGROUP_PROJECT10,
                  'OptLarge_Sharpen': unreal.TextureGroup.TEXTUREGROUP_PROJECT11,
                  'OptTiny_Average': unreal.TextureGroup.TEXTUREGROUP_PROJECT12,
                  'OptSmall_Average': unreal.TextureGroup.TEXTUREGROUP_PROJECT13,
                  'OptMedium_Average': unreal.TextureGroup.TEXTUREGROUP_PROJECT14,
                  'OptLarge_Average': unreal.TextureGroup.TEXTUREGROUP_PROJECT15,
                  '2K_Sharpen': unreal.TextureGroup.TEXTUREGROUP_PROJECT16,
                  '2K_Average': unreal.TextureGroup.TEXTUREGROUP_PROJECT17,
                  'FX_MipBias': unreal.TextureGroup.TEXTUREGROUP_PROJECT18,
                  'WorldNormalMap': unreal.TextureGroup.TEXTUREGROUP_WORLD_NORMAL_MAP,
                  'CharacterNormalMap': unreal.TextureGroup.TEXTUREGROUP_CHARACTER_NORMAL_MAP,
                  'CharacterSpecular': unreal.TextureGroup.TEXTUREGROUP_CHARACTER_SPECULAR,
                  'World': unreal.TextureGroup.TEXTUREGROUP_WORLD
                  }


    @classmethod
    def attr(cls, str_name):
        instance = cls.class_dict.get(str_name, None)
        if not instance:
            logger.warning(f'LODGroup (aka Texture Group) {str_name} was not found. defaulting to "Character"')
            instance = unreal.TextureGroup.TEXTUREGROUP_CHARACTER
        return instance


class PyTexture2D(py_base.PyUnrealBaseAssetObject):
    """
    Class for handling the PyTexture2D asset.  This is a MAT class for the Unreal Texture2D asset.
    """

    def __init__(self, u_asset):
        super().__init__(u_asset=u_asset)

    # Compression settings.  Display Name: Compression Settings
    def set_compression_setting(self, str_name):
        """
        Sets the compression settings for the asset.  It uses the property string name to set the compression setting.

        :param str str_name: property string name
        """

        compression = PyTextureCompressionSettings.attr(str_name)
        if not compression:
            logger.warning(f'{str_name}: was not found in the compression settings list.')
            return

        self.asset_compression(compression)

    def asset_compression(self, compression):
        """
        Sets the compression settings for the asset.  It uses the Unreal.TextureCompressionSettings
        to set the compression setting.

        :param Unreal.TextureCompressionSettings compression: Unreal.TextureCompressionSettings enum.
        """

        self.set_attr('compression_settings', compression)

    def set_default_compression(self):
        """ Set the default compression settings for the asset. """

        self.set_compression_setting('default')

    def set_normalmap_compression(self):
        """ Set the normal map compression settings for the asset. """

        self.set_compression_setting('normal_map')

    def set_masks_compression(self):
        """ Set the masks compression settings for the asset. """

        self.set_compression_setting('masks')

    def set_grayscale_compression(self):
        """ Set the grayscale compression settings for the asset. """

        self.set_compression_setting('grayscale')

    def set_displacement_map_compression(self):
        """ Set the displacement map compression settings for the asset. """

        self.set_compression_setting('displacement_map')

    def set_vector_displacement_map_compression(self):
        """ Set the vector displacement map compression settings for the asset. """

        self.set_compression_setting('vector_displacement_map')

    def set_hdr_compression(self):
        """ Set the hdr compression settings for the asset. """

        self.set_compression_setting('hdr')

    def set_user_interface_2d_compression(self):
        """ Set the user interface 2d compression settings for the asset. """

        self.set_compression_setting('user_interface_2d')

    def set_alpha_compression(self):
        """ Set the alpha compression settings for the asset. """

        self.set_compression_setting('alpha')

    def set_distance_field_font_compression(self):
        """ Set the distance field font compression settings for the asset. """

        self.set_compression_setting('distance_field_font')

    def set_hdr_compressed_compression(self):
        """ Set the hdr compressed compression settings for the asset. """

        self.set_compression_setting('hdr_compressed')

    def set_bc7_compression(self):
        """ Set the bc7 compression settings for the asset. """

        self.set_compression_setting('bc7')

    def set_half_float_compression(self):
        """ Set the half float compression settings for the asset. """

        self.set_compression_setting('half_float')

    def set_single_float_compression(self):
        """ Set the single float compression settings for the asset. """

        self.set_compression_setting('single_float')

    def set_hdr_high_precision_compression(self):
        """ Set the hdr high precision compression settings for the asset. """

        self.set_compression_setting('hdr_high_precision')

    # LODGroup AKA Texture Group.  Texture Group is the display name.

    def get_lod_grp(self, str_name):
        """
        Returns the unreal.TextureLODGroup for the given string name.

        :param str str_name: property string name
        :return: Returns the unreal.TextureLODGroup for the given string name.
        :rtype: unreal.TextureLODGroup
        """

        return PyTextureLODGroup.attr(str_name)

    def set_lod_grp(self, str_name):
        """
        Sets the unreal.TextureLODGroup for the given string name.

        :param str str_name: property string name
        """

        lod_grp = self.get_lod_grp(str_name)
        self.set_attr('LODGroup', lod_grp)


class PyDiffuse(PyTexture2D):

    def __init__(self, u_asset):
        super().__init__(u_asset=u_asset)

    def set_editor_attributes(self):
        self.set_default_compression()
        self.set_attr('sRGB', True)
        self.set_lod_grp('Character')


class PyNormalMap(PyTexture2D):

    def __init__(self, u_asset):
        super().__init__(u_asset=u_asset)

    def set_editor_attributes(self):
        self.set_normalmap_compression()
        self.set_attr('sRGB', False)
        self.set_lod_grp('CharacterNormalMap')


class PyBentNormalMap(PyTexture2D):

    def __init__(self, u_asset):
        super().__init__(u_asset=u_asset)

    def set_editor_attributes(self):
        self.set_normalmap_compression()
        self.set_attr('sRGB', False)
        self.set_lod_grp('CharacterNormalMap')


class PyRoughnessMap(PyTexture2D):

    def __init__(self, u_asset):
        super().__init__(u_asset=u_asset)

    def set_editor_attributes(self):
        self.set_default_compression()
        self.set_attr('sRGB', False)
        self.set_lod_grp('World')


class PyORME(PyTexture2D):

    def __init__(self, u_asset):
        super().__init__(u_asset=u_asset)

    def set_editor_attributes(self):
        self.set_masks_compression()
        self.set_attr('sRGB', False)
        self.set_lod_grp('CharacterMasks')


class PySSTD(PyTexture2D):

    def __init__(self, u_asset):
        super().__init__(u_asset=u_asset)

    def set_editor_attributes(self):
        self.set_default_compression()
        self.set_attr('sRGB', False)
        self.set_lod_grp('CharacterMasks')


class PyRIDA(PyTexture2D):

    def __init__(self, u_asset):
        super().__init__(u_asset=u_asset)

    def set_editor_attributes(self):
        self.set_masks_compression()
        self.set_attr('sRGB', False)
        self.set_lod_grp('World')


class TextureMapping:
    """
    A class to handle the mapping of the texture attributes
    """

    texture_dict = {'d': PyDiffuse,
                  'n': PyNormalMap,
                  'nb': PyBentNormalMap,
                  'orme': PyORME,
                  'sstd': PySSTD,
                  'r': PyRoughnessMap,
                  'rida': PyRIDA
                  }

    @classmethod
    def attr(cls, attr_instance):
        """
        Redirects the asset to our PyMaterial and Texture classes

        :param unreal.Object attr_instance: An unreal object
        :return: The asset as an Unreal asset or our PyNode asset.
        :rtype: unreal.Object or PyNode
        """

        name = attr_instance.get_name().split('_')[-1]
        new_instance = cls.texture_dict.get(name.lower(), attr_instance)
        if new_instance == attr_instance:
            return attr_instance
        return new_instance(u_asset=attr_instance)


def get_textures_paths_from_mca_inst_path(mat_inst_folder):
    """
    Returns a dictionary with the following keys:
    - 'game_paths': The path to the game's material instance constant texture's folder.
    - 'full_paths': The absolute path to the material instance constant texture's folder.

    :param str mat_inst_folder: path to the material instance constant.
    :return: Returns a dictionary with the game path and the full path to the texture's folder.
    :rtype: dict
    """

    textures_path = os.path.dirname(mat_inst_folder)
    if textures_path.endswith('Materials'):
        textures_path = os.path.dirname(textures_path)
    textures_path = os.path.join(textures_path, 'Textures')
    abs_path = ue_path_utils.convert_to_project_path(textures_path)
    paths = {}
    paths['game_paths'] = textures_path
    paths['full_paths'] = abs_path

    return paths


def get_list_of_textures_from_path(abs_path, game_path=None, convert_to_pynodes=True):
    """
    Returns a list of texture files in the given path.  Full Paths.

    :param str abs_path: The absolute path to the texture's folder.
    :param str game_path: The game path to the texture's folder.
    :param bool convert_to_pynodes: If True, the textures will be converted to pynodes.
    :return: Returns a list of texture files in the given path.
    :rtype: list[general.PyNode]
    """

    if ue_path_utils.is_game_path(abs_path):
        abs_path = ue_path_utils.convert_to_project_path(abs_path)

    # Using the full path, get a list of texture files.
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)
    file_list = os.listdir(abs_path)
    file_list = [x for x in file_list if x.endswith('.uasset')]
    # Get the game path.  This is the one that starts with /Game/
    if not game_path:
        game_path = ue_path_utils.convert_to_game_path(abs_path)
    texture_list = [os.path.normpath(os.path.join(game_path, x.split('.')[0])) for x in file_list]
    texture_list = [x.replace('\\', '/') for x in texture_list]

    # Get unreal instances of the textures
    texture_instances = []
    for tex in texture_list:
        texture_instances.append(unreal.EditorAssetLibrary.find_asset_data(tex).get_asset())

    if not convert_to_pynodes:
        return texture_instances
    # Convert them to our PyNodes
    pynode_list = [TextureMapping.attr(x) for x in texture_instances]
    pynode_list = [x for x in pynode_list if isinstance(x, PyTexture2D)]
    return pynode_list


# Result: __class__
# Result: __delattr__
# Result: __dir__
# Result: __doc__
# Result: __eq__
# Result: __format__
# Result: __ge__
# Result: __getattribute__
# Result: __gt__
# Result: __hash__
# Result: __init__
# Result: __init_subclass__
# Result: __le__
# Result: __lt__
# Result: __ne__
# Result: __new__
# Result: __reduce__
# Result: __reduce_ex__
# Result: __repr__
# Result: __setattr__
# Result: __sizeof__
# Result: __str__
# Result: __subclasshook__
# Result: _post_init
# Result: _wrapper_meta_data
# Result: acquire_editor_element_handle
# Result: address_x
# Result: address_y
# Result: adjust_brightness
# Result: adjust_brightness_curve
# Result: adjust_hue
# Result: adjust_max_alpha
# Result: adjust_min_alpha
# Result: adjust_rgb_curve
# Result: adjust_saturation
# Result: adjust_vibrance
# Result: alpha_coverage_thresholds
# Result: blueprint_get_memory_size
# Result: blueprint_get_size_x
# Result: blueprint_get_size_y
# Result: call_method
# Result: cast
# Result: chroma_key_color
# Result: chroma_key_texture
# Result: chroma_key_threshold
# Result: composite_power
# Result: composite_texture
# Result: composite_texture_mode
# Result: compress_final
# Result: compression_no_alpha
# Result: compression_quality
# Result: compression_settings
# Result: defer_compression
# Result: do_scale_mips_for_alpha_coverage
# Result: export_to_disk
# Result: filter
# Result: flip_green_channel
# Result: get_class
# Result: get_default_object
# Result: get_editor_property
# Result: get_fname
# Result: get_full_name
# Result: get_name
# Result: get_outer
# Result: get_outermost
# Result: get_package
# Result: get_path_name
# Result: get_typed_outer
# Result: get_world
# Result: global_force_mip_levels_to_be_resident
# Result: is_package_external
# Result: lod_bias
# Result: lod_group
# Result: lossy_compression_amount
# Result: max_texture_size
# Result: mip_gen_settings
# Result: mip_load_options
# Result: modify
# Result: never_stream
# Result: num_cinematic_mip_levels
# Result: oodle_texture_sdk_version
# Result: padding_color
# Result: power_of_two_mode
# Result: preserve_border
# Result: rename
# Result: set_editor_properties
# Result: set_editor_property
# Result: set_force_mip_levels_to_be_resident
# Result: source_color_settings
# Result: srgb
# Result: static_class
# Result: use_legacy_gamma
# Result: use_new_mip_filter
# Result: virtual_texture_streaming


"""
-- Compression settings --
Default (DXT1/5, BC1/3 on DX11) == unreal.TextureCompressionSettings.TC_DEFAULT # index 0
Normalmap (DXT5, BC5 on DX11) == TextureCompressionSettings.TC_NORMALMAP # index 1
Masks (no sRGB) == TextureCompressionSettings.TC_MASKS # index 2
Grayscale (G8/16, RGB8 sRGB sRGB) == TextureCompressionSettings.TC_GRAYSCALE # index 3
Displacementmap (G8/16) == TextureCompressionSettings.TC_DISPLACEMENTMAP # index 4
VectorDisplacementmap (RGBA8) == TextureCompressionSettings.TC_VECTOR_DISPLACEMENTMAP # index 5
HDR (RGBA16F, no sRGB) == TextureCompressionSettings.TC_HDR # index 6
UserInterface2D (RGBA) == TextureCompressionSettings.TC_EDITOR_ICON # index 7
Alpha (no RGB, BC4 on DX11) == TextureCompressionSettings.TC_ALPHA # index 8
DistanceFieldFont (G8) == TextureCompressionSettings.TC_DISTANCE_FIELD_FONT # index 9
HDR Compressed (RGB, BC6H, DX11) == TextureCompressionSettings.TC_HDR_COMPRESSED # index 10
BC7 (DX11, optional A) == TextureCompressionSettings.TC_BC7 # index 11
Half Float (R16F) == TextureCompressionSettings.TC_HALF_FLOAT # index 12
Single Float (R32F) == TextureCompressionSettings.TC_SINGLE_FLOAT # index 13
HDR High Precision (RGBA32F) == TextureCompressionSettings.TC_HDR_F32 # index 13
"""