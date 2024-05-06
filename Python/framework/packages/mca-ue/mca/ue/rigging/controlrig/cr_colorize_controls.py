"""
Interacts an Unreal Control Rig Sequence Node
"""

# mca python imports
# software specific imports
# mca python imports
from mca.ue.rigging.controlrig import cr_nodes, cr_pins


SCRIPT_STRUCT_PATH = '/ControlRig/StandardFunctionLibrary/StandardFunctionLibrary.StandardFunctionLibrary_C'
BASE_NODE_NAME = 'ColorizeControls'


class ColorizeControlsNode(cr_pins.PinsBase):
    VERSION = '1.0.0'
    NODE_SIZE = [4, 6]

    def __init__(self, control_rig, fnode):
        super().__init__(control_rig=control_rig, fnode=fnode)

    @classmethod
    def spawn(cls, control_rig, position=(816.0, 96.0), side='center', region='color_controls'):
        node_name = f'{BASE_NODE_NAME}_{side}_{region}'
        cr_nodes.create_external_control_rig_node(control_rig=control_rig,
                                                    position=position,
                                                    script_struct_path=SCRIPT_STRUCT_PATH,
                                                    external_function_name=BASE_NODE_NAME,
                                                    node_name=node_name)

        return cls(control_rig, fnode=node_name)

    def get_first_input_link_name(self):
        pass

    def get_first_input_link(self):
        pass

    def link(self, target_pin_name):
        self.cr_controller.add_link(f'{self.get_fname()}.Items', target_pin_name)

    def link_to_controls(self, target, connect_name=None):
        pass

    def get_input_pins(self):
        return ['controls', 'CenterColor', 'LeftColor', 'RightColor', 'ignore_ctrls']

    @property
    def controls(self):
        return 'controls'

    @property
    def center_control(self):
        return 'CenterColor'

    @property
    def left_control(self):
        return 'LeftColor'

    @property
    def right_control(self):
        return 'RightColor'

    @property
    def ignore_ctrls(self):
        return 'ignore_ctrls'


