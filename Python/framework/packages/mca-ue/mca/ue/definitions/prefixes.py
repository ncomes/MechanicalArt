# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.ue.assettypes import py_skeletalmesh, py_staticmesh, py_material_instance
from mca.ue.texturetypes import texture_2d


class PrefixStringMapping:
    """
        Class used for mapping an Unreal asset type to a MAT asset type.
        """

    class_dict = {'AnimationBlueprint': "ABP",
                    'PostAnimationBlueprint': "PABP",
                    'Sequence': "ANIM",
                    'Animation': "A",
                    'AnimationMontage': "AM",
                    'AnimationOffset': "AO",
                    'BlendSpace': "BS",
                    'Blueprint': "BP",
                    'Level': "LVL",
                    'Material': "M",
                    'MaterialFunction': "MIF",
                    'MaterialInstance': "MI",
                    'ParticleSystem': "VFX",
                    'PhysicsAsset': "PHYS",
                    'SkeletalMesh': "SK",
                    'Skeleton': "SKEL",
                    'StaticMesh': "SM",
                    'Texture2D': "T",
                    'TextureCube': "HDRI"
                  }

    @classmethod
    def attr(cls, str_name, separator='_'):
        prefix = cls.class_dict.get(str_name, '')
        if not prefix == '':
            prefix = f'{prefix}{separator}'
        return prefix

    def getAttr(self, str_name, separator='_'):
        return self.class_dict.get(str_name, '')


class AssetMapping:
    """
    Class used for mapping an Unreal asset type to a MAT asset type.
    """

    class_dict = {unreal.AnimBlueprint: "ABP",
                    unreal.AnimSequence: "ANIM",
                    unreal.AnimationAsset: "A",
                    unreal.AnimMontage: "AM",
                    unreal.BlendSpace: "BS",
                    unreal.Blueprint: "BP",
                    unreal.Level: "LVL",
                    unreal.Material: "M",
                    unreal.MaterialFunction: "MIF",
                    py_material_instance.PyMaterialInstanceConstant: 'MI',
                    unreal.MaterialInstanceConstant: 'MI',
                    unreal.ParticleSystem: "VFX",
                    unreal.PhysicsAsset: "PHYS",
                    unreal.SkeletalMesh: "SK",
                    py_skeletalmesh.PySkelMesh: "SK",
                    unreal.Skeleton: "SKEL",
                    unreal.StaticMesh: "SM",
                    py_staticmesh.PyStaticMesh: "SM",
                    texture_2d.PyTexture2D: "T",
                  }

    @classmethod
    def attr(cls, attr_instance, separator='_'):
        inst_name = attr_instance.__class__
        prefix = cls.class_dict.get(inst_name, '')
        if not prefix == '':
            prefix = f'{prefix}{separator}'
        return prefix

    def getAttr(self, attr_instance, separator='_'):
        inst_name = attr_instance.__class__
        prefix = self.class_dict.get(inst_name, '')
        if not prefix == '':
            prefix = f'{prefix}{separator}'
        return prefix
