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


SCRIPT_STRUCT_PATH = '/Game/Characters/Gunsmith/Rigs/CR_Human_FRAG.CR_Human_FRAG_C'
NODE_NAME = 'FRAG Create Root Flag'
NODE_SIZE = [3, 2]


class UERootComponent(pins_component.PinsComponent):
    """
    interacts with a root component in the Unreal Control Rig Graph.
    """

    def __init__(self, control_rig, fnode):
        super().__init__(control_rig=control_rig, fnode=fnode)

    @classmethod
    def create(cls, control_rig):
        pass

    @classmethod
    def spawn(cls, control_rig, side='center', region='root'):
        if isinstance(control_rig, str):
            control_rig = unreal.load_object(name=control_rig, outer=None)

        cr_controller = control_rig.get_controller_by_name('RigVMModel')
        node_name = f'{NODE_NAME}_{side}_{region}'
        fnodes = cr_controller.add_external_function_reference_node(SCRIPT_STRUCT_PATH,
                                                                       NODE_NAME,
                                                                       unreal.Vector2D(1500.0, -1952.0),
                                                                       node_name=node_name)
        return cls(control_rig, fnode=node_name)

    def connect_to_sequence(self, source_node, letter='A'):
        self.connect_from_sequence(source_node.get_fname(), self.get_fname(), letter)

    def set_default_comment(self):
        self.add_comment_node(comment_text='Create Root Flag',
                              position=[1500.0, -2000.0],
                              size=[500.0, 300.0],
                              color=[1.0, 0.944, 0.72, 1.0],
                              node_name='',
                              setup_undo_redo=True,
                              print_python_command=False)

    def expand_pin_parent(self, expand=True):
        self.set_expand_pin(node_name=NODE_NAME, pin_name='parent', expand=expand)

    def set_parent_pin(self, in_type, other_name):
        self.set_rig_element_pin(node_name=NODE_NAME, pin_name='parent', in_type=in_type, other_name=other_name)

    def set_parent_flag(self, other_flag_name):
        self.set_parent_pin(in_type='Control', other_name=other_flag_name)

    def connect_execute_content_in(self, other_component):
        self.connect_execute_content_nodes(other_component.fnode, self.fnode)

    def connect_execute_content_out(self, other_component):
        self.connect_execute_content_nodes(self.fnode, other_component.fnode)

