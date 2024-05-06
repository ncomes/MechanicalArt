#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
# software specific imports
import unreal
# mca python imports


def create_control_rig_from_skeletal_mesh(sk_path):
    """


    :param str sk_path: path to a skeletal mesh or skeleton.
    :return: Returns The control rig created from the given skeletal mesh or skeleton.
    :rtype: unreal.ControlRigBlueprintFactory
    """
    # load a skeletal mesh
    sk = unreal.load_object(name=sk_path, outer=None)

    # create a control rig for the sk
    factory = unreal.ControlRigBlueprintFactory
    cr_rig = factory.create_control_rig_from_skeletal_mesh_or_skeleton(selected_object=sk)
    return cr_rig


def access_existing_control_rig(cr_path):
    """


    :param str cr_path: path to a Control Rig Asset.
    :return: Returns The control rig created from the given Control Rig Asset.
    :rtype: unreal.ControlRigBlueprintFactory
    """

    unreal.load_module('ControlRigDeveloper')
    rig = unreal.load_object(name=cr_path, outer=None)

    return rig


def access_open_control_rig():
    """


    :param str cr_path: path to a Control Rig Asset.
    :return: Returns The control rig created from the given Control Rig Asset.
    :rtype: unreal.ControlRigBlueprintFactory
    """

    unreal.load_module('ControlRigDeveloper')
    rigs = unreal.ControlRigBlueprint.get_currently_open_rig_blueprints()

    return rigs


def create_new_control_rig(cr_path):
    """


    :param str cr_path: path to a Control Rig Asset.
    :return: Returns The control rig created from the given Control Rig Asset.
    :rtype: unreal.ControlRigBlueprintFactory
    """

    factory = unreal.ControlRigBlueprintFactory()
    rig = factory.create_new_control_rig_asset(desired_package_path=cr_path)

    return rig

