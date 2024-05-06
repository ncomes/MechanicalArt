"""
Interacts an Unreal Control Rig "Math Make Color" Node
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.common import log
from mca.ue.rigging.controlrig import cr_nodes, cr_config, cr_pins

logger = log.MCA_LOGGER

SCRIPT_STRUCT_PATH = '/Script/RigVM.RigVMFunction_MathColorMake'
BASE_NODE_NAME = 'RigVMFunction_MathColorMake'


class MakeColorNode(cr_pins.PinsBase):
    VERSION = '1.0.0'
    NODE_SIZE = [2, 2]

    def __init__(self, control_rig, fnode):
        super().__init__(control_rig=control_rig, fnode=fnode)

    @classmethod
    def spawn(cls, control_rig,  side='center', region='make_color', position=(504.0, 320.0)):
        controller = control_rig.get_controller_by_name(cr_config.RIGVMMODEL)
        node_name = f'{BASE_NODE_NAME}_{side}_{region}'
        node = cr_nodes.create_control_rig_node(control_rig=control_rig,
                                       position=position,
                                       script_struct_path=SCRIPT_STRUCT_PATH,
                                       node_name=node_name)

        return cls(control_rig, fnode=node_name)

    def set_color(self, rgba=(1.0, 1.0, 1.0, 1.0)):
        self.cr_controller.set_pin_default_value(f'{self.get_fname()}.R', str(rgba[0]))
        self.cr_controller.set_pin_default_value(f'{self.get_fname()}.G', str(rgba[1]))
        self.cr_controller.set_pin_default_value(f'{self.get_fname()}.B', str(rgba[2]))
        self.cr_controller.set_pin_default_value(f'{self.get_fname()}.A', str(rgba[3]))

    def set_default_yellow(self):
        self.set_color(cr_config.YELLOW_RGBA)

    def set_default_blue(self):
        self.set_color(cr_config.BLUE_RGBA)

    def set_default_red(self):
        self.set_color(cr_config.RED_RGBA)

    def link(self, target, target_pin):
        self.add_link(pin_name='Result', target=target, target_pin=target_pin)


