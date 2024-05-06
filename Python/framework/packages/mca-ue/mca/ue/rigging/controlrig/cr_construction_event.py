"""
Interacts an Unreal Control Rig Sequence Node
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.ue.rigging.controlrig import cr_nodes, cr_pins


SCRIPT_STRUCT_PATH = '/Script/ControlRig.RigUnit_PrepareForExecution'
BASE_NODE_NAME = 'PrepareForExecution'


class ConstructionEventNode(cr_pins.PinsBase):
    VERSION = '1.0.0'
    NODE_SIZE = [1, 2]

    def __init__(self, control_rig, fnode=BASE_NODE_NAME):
        super().__init__(control_rig=control_rig, fnode=fnode)

    @classmethod
    def spawn(cls, control_rig, position=(-134.0, -1286.0)):
        node = cr_nodes.create_control_rig_node(control_rig=control_rig,
                                       position=position,
                                       script_struct_path=SCRIPT_STRUCT_PATH,
                                       node_name=BASE_NODE_NAME)
        return cls(control_rig)

