"""
Creates a world component in Unreal Control Rig.
"""

# System global imports
# mca python imports
# software specific imports
import unreal
# mca python imports
# Internal module imports
from mca.ue.rigging.controlrig import cr_pins

SCRIPT_STRUCT_PATH = '/Game/Characters/Gunsmith/Rigs/CR_Human_FRAG.CR_Human_FRAG_C'
BASE_NODE_NAME = 'FRAG Create World Flags'


class UEWorldConstruction(cr_pins.PinsBase):
    """
    Creates a world component in Unreal Control Rig.
    """

    VERSION = '1.0.0'
    NODE_SIZE = [3, 2]

    def __init__(self, control_rig, fnode):
        super().__init__(control_rig=control_rig, fnode=fnode)

    @classmethod
    def create(cls, control_rig):
        pass

    @classmethod
    def spawn(cls, control_rig, side='center', region='world'):
        if isinstance(control_rig, str):
            control_rig = unreal.load_object(name=control_rig, outer=None)

        cr_controller = control_rig.get_controller_by_name('RigVMModel')
        node_name = f'{BASE_NODE_NAME}_{side}_{region}'
        cr_controller.add_external_function_reference_node(host_path=SCRIPT_STRUCT_PATH,
                                                           function_name=BASE_NODE_NAME,
                                                           node_position=unreal.Vector2D(830.0, -1870.0),
                                                           node_name=node_name,
                                                           setup_undo_redo=True,
                                                           print_python_command=False)
        return cls(control_rig, fnode=node_name)

    def connect_to_sequence(self, source_node, letter='A'):
        self.connect_from_sequence(source_node.get_fname(), self.get_fname(), letter)

    def set_default_comment(self):
        self.add_comment_node(comment_text='Create World Flags',
                              position=[790.0, -1950.0],
                              size=[500.0, 300.0],
                              color=[1.0, 0.944, 0.72, 1.0],
                              node_name='',
                              setup_undo_redo=True,
                              print_python_command=False)

    def get_flags(self):
        return ['f_world', 'f_offset_world']

    def get_output_pins(self):
        return ['world flag', 'world offset flag']

    @property
    def world_flag(self):
        return 'f_world'

    @property
    def world_output(self):
        return 'world flag'

    @property
    def offset_flag(self):
        return 'f_offset_world'

    @property
    def offset_output(self):
        return 'world offset flag'
