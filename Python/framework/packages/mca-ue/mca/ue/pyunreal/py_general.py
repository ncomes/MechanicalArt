# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
# software specific imports
# mca python imports
from mca.ue.utils import asset_utils, asset_import
from mca.ue.assettypes import py_material_instance


def PyNode(u_asset):
    defined = asset_utils.PyNode(u_asset)
    return defined


def selected():
    defined_list = asset_utils.selected()
    return defined_list


def import_asset(filename, game_path, asset_name, import_options=None, replace_existing=True, save=False):
    u_asset = asset_import.import_asset(filename=filename,
                                            game_path=game_path,
                                            asset_name=asset_name,
                                            import_options=import_options,
                                            replace_existing=replace_existing,
                                            save=save)
    return PyNode(u_asset)


def create_material_instance(mat_inst_folder):
    return py_material_instance.create_material_instance(mat_inst_folder)


class PyMaterialInstanceConstant(py_material_instance.PyMaterialInstanceConstant):
    def __init__(self, u_asset):
        super().__init__(u_asset)



