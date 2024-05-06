#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.ue.rigging.controlrig import cr_config


def get_top_level_graph_node(control_rig, node_name):
    """
    Returns a top level graph node.

    :param unreal.ControlRigBlueprint control_rig: The Control Rig blueprint.
    :param str node_name: name of the node
    :return: a top level graph node.
    :rtype: unreal.RigVMUnitNode
    """

    cr_controller = control_rig.get_controller_by_name(cr_config.RIGVMMODEL)
    top_level_graph = cr_controller.get_top_level_graph()
    node = top_level_graph.find_node(node_name)
    return node


def get_forward_solve_node(control_rig):
    """
    Returns the forward solve node.

    :param unreal.ControlRigBlueprint control_rig: The Control Rig blueprint.
    :return: Returns the forward solve node.
    :rtype: unreal.RigVMUnitNode
    """

    return get_top_level_graph_node(control_rig=control_rig, node_name=cr_config.FORWARD_SOLVE)


def get_construction_event_node(control_rig):
    """
    Returns the construction event node.

    :param unreal.ControlRigBlueprint control_rig: The Control Rig blueprint.
    :return: Returns the construction event node.
    :rtype: unreal.RigVMUnitNode
    """

    return get_top_level_graph_node(control_rig=control_rig, node_name=cr_config.CONSTRUCTION_EVENT)


def create_control_rig_node(control_rig, position, script_struct_path, node_name):
    """
    Returns a control rig node that was created.

    :param unreal.ControlRigBlueprintFactory control_rig: control_rig asset
    :param list(float) position: 2d position in the blueprint
    :param str script_struct_path: path top the script struct file.
    :param str node_name: Name of the control rig node.
    :return: Returns the newly created control rig node.
    :rtype: unreal.RigVMController
    """

    cr_controller = control_rig.get_controller_by_name('RigVMModel')
    twod_position = unreal.Vector2D(position[0], position[1])
    new_node = cr_controller.add_unit_node_from_struct_path(script_struct_path=script_struct_path,
                                                   method_name='Execute',
                                                   position=twod_position,
                                                   node_name=node_name)

    return new_node


def create_external_control_rig_node(control_rig, position, script_struct_path, external_function_name, node_name=None):
    """
    Returns a control rig node that was created.

    :param unreal.ControlRigBlueprintFactory control_rig: control_rig asset
    :param list(float) position: 2d position in the blueprint
    :param str script_struct_path: path top the script struct file.
    :param str external_function_name: Name of the control rig node.
    :param str node_name: Name of the control rig node.
    :return: Returns the newly created control rig node.
    :rtype: unreal.RigVMController
    """
    if not node_name:
        node_name = external_function_name
    cr_controller = control_rig.get_controller_by_name('RigVMModel')
    twod_position = unreal.Vector2D(position[0], position[1])
    new_node = cr_controller.add_external_function_reference_node(host_path=script_struct_path,
                                                                   function_name=external_function_name,
                                                                   node_position=twod_position,
                                                                   node_name=node_name)

    return new_node


def construction_event(control_rig, position=(-134.0, -1286.0)):
    construction_path = '/Script/ControlRig.RigUnit_PrepareForExecution'
    construction_event = create_control_rig_node(control_rig=control_rig,
                                                   position=position,
                                                   script_struct_path=construction_path,
                                                   node_name='PrepareForExecution')
    return construction_event


def sequence(control_rig, position=(192.0, -1296.0), number_of_pins=2):
    script_struct_path = '/Script/RigVM.RigVMFunction_Sequence'
    controller = control_rig.get_controller_by_name('RigVMModel')
    node = create_control_rig_node(control_rig=control_rig,
                                   position=position,
                                   script_struct_path=script_struct_path,
                                   node_name='RigVMFunction_Sequence')
    if number_of_pins > 2:
        for i in range(number_of_pins - 2):
            controller.add_aggregate_pin('RigVMFunction_Sequence', '', '')
    return node


def connect_single_node(control_rig, source_node, target_node, controller=None):
    if not controller:
        controller = control_rig.get_controller_by_name('RigVMModel')

    source_str = f'{source_node.get_fname()}.ExecuteContext'
    target_str = f'{target_node.get_fname()}.ExecuteContext'
    controller.add_link(source_str, target_str)

