#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
# software specific imports
# mca python imports
from mca.ue.rigging.controlrig import create_cr, cr_nodes
from mca.ue.rigging.frag import world_component


# path = r'/Game/Characters/Gunsmith/Meshes/SK_Gunsmith'
# cr_rig = create_cr.create_control_rig_from_skeletal_mesh(path)


path = r'/Game/Characters/Gunsmith/Meshes/SK_Gunsmith_CtrlRig'
cr_rig = create_cr.access_existing_control_rig(path)
if cr_rig:
    print('Control Rig Loaded!')


#blueprint = unreal.load_object(name = '/Game/Characters/Gunsmith/Rigs/CR_Human_FRAG.CR_Human_FRAG', outer = None)
library = cr_rig.get_local_function_library()
library_controller = cr_rig.get_controller(library)
hierarchy = cr_rig.hierarchy
hierarchy_controller = hierarchy.get_controller()

cr_controller = cr_rig.get_controller_by_name('RigVMModel')

construction_event = cr_nodes.construction_event(cr_rig)
sequence_node = cr_nodes.sequence(control_rig=cr_rig, number_of_pins=11)



cr_nodes.connect_single_node(control_rig=cr_rig, source_node=construction_event, target_node=sequence_node)


# World Flags
wld_component = world_component.UEWorldComponent.create(control_rig=cr_rig)
wld_component.connect_to_sequence(sequence_node.get_fname())



# cr_controller.add_external_function_reference_node('/Game/Characters/Gunsmith/Rigs/CR_Human_FRAG.CR_Human_FRAG_C',
#                                                    'FRAG FWD World',
#                                                    unreal.Vector2D(831.973648, -1935.763474),
#                                                    'FRAG FWD World')
# cr_controller.add_link('RigVMFunction_Sequence.A', 'FRAG FWD World.ExecuteContext')
# cr_controller.mark_function_as_public('FRAG FWD World', True)






# # ADD FUNCTION TO LIBRARY
# library_controller.add_function_to_library('New Function', True, unreal.Vector2D(0.000000, 0.000000))
# library_controller.rename_function('New Function', 'TestFunction')
# cr_rig.get_controller_by_name('RigVMFunctionLibrary').set_node_category_by_name('TestFunction', 'TestGrp')






# cr_rig.get_controller_by_name('RigVMModel').add_link('PrepareForExecution.ExecuteContext', 'RigVMFunction_Sequence.ExecuteContext')

# https://docs.unrealengine.com/5.3/en-US/PythonAPI/class/RigHierarchyController.html






# Create a new Control Rig Blueprint
# path = r'/Game/Characters/Gunsmith/Rigs'
# cr = r'simple_prop'
# control_rig_blueprint = unreal.ControlRigBlueprintFactory()
#
# # Add a control rig component
# actor = asset_utils.selected()[0]
#
# asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
# control_rig_component = asset_tools.create_asset(cr, path, None, control_rig_blueprint)
# #control_rig_component = actor.add_component_by_class(unreal.ControlRigComponent)
#
#
# # Assign the Control Rig blueprint to the Control Rig component
# control_rig_component.set_control_rig_blueprint(control_rig_blueprint)
#
# # Create Control Rig component
# control_rig_control = control_rig_blueprint.add_control("FkChain")

