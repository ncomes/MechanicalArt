# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.ue.assettypes import py_skeletalmesh
from mca.ue.assettypes import py_staticmesh


class AssetMapping:
    """
    Class used for mapping an Unreal asset type to a MAT asset type.
    """

    class_dict = {unreal.SkeletalMesh: py_skeletalmesh.PySkelMesh,
                  unreal.StaticMesh: py_staticmesh.PyStaticMesh
                  }

    @classmethod
    def attr(cls, attr_instance):
        inst_name = attr_instance.__class__
        new_instance = cls.class_dict.get(inst_name, attr_instance)
        if new_instance == attr_instance:
            return attr_instance
        return new_instance(u_asset=attr_instance)

    def getAttr(self, attr_instance):
        inst_name = attr_instance.__class__
        new_instance = self.class_dict.get(inst_name, attr_instance)
        if new_instance == inst_name:
            return inst_name
        return new_instance(u_asset=attr_instance)


