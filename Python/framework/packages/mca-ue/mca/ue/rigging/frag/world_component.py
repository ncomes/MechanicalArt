"""
Creates a world component in Unreal Control Rig.
"""

# System global imports
# mca python imports
# software specific imports
import unreal
# mca python imports
# Internal module imports
from mca.ue.rigging.frag import pins_component

WORLD_COMPONENT_PATH = '/Game/Characters/Gunsmith/Rigs/CR_Human_FRAG.CR_Human_FRAG_C'
WORLD_COMPONENT_NAME = 'FRAG Create World Flags'
WORLD_COMPONENT_EXE = f'{WORLD_COMPONENT_NAME}.ExecuteContext'


class UEWorldComponent(pins_component.PinsComponent):
    """
    Creates a world component in Unreal Control Rig.
    """

    def __init__(self, control_rig, fnode=WORLD_COMPONENT_NAME):
        super().__init__(control_rig=control_rig, fnode=fnode)

    @classmethod
    def create(cls, control_rig):
        if isinstance(control_rig, str):
            control_rig = unreal.load_object(name=control_rig, outer=None)

        cr_controller = control_rig.get_controller_by_name('RigVMModel')

        world_flags_nodes = cr_controller.add_external_function_reference_node(WORLD_COMPONENT_PATH,
                                                                               WORLD_COMPONENT_NAME,
                                                                               unreal.Vector2D(831.9, -1935.7),
                                                                               WORLD_COMPONENT_NAME)
        return cls(control_rig)

    @classmethod
    def spawn(cls, control_rig):
        if isinstance(control_rig, str):
            control_rig = unreal.load_object(name=control_rig, outer=None)

        cr_controller = control_rig.get_controller_by_name('RigVMModel')

        world_flags_nodes = cr_controller.add_external_function_reference_node(WORLD_COMPONENT_PATH,
                                                                               WORLD_COMPONENT_NAME,
                                                                               unreal.Vector2D(831.9, -1935.7),
                                                                               WORLD_COMPONENT_NAME)
        return cls(control_rig)

    def connect_to_sequence(self, source_node, letter='A'):
        self.connect_from_sequence(source_node.get_fname(), self.get_fname(), letter)

    def set_default_comment(self):
        self.add_comment_node(comment_text='Create World Flags',
                              position=[784.0, -2000.0],
                              size=[477.0, 219.0],
                              color=[1.0, 0.944, 0.72, 1.0],
                              node_name='',
                              setup_undo_redo=True,
                              print_python_command=False)

