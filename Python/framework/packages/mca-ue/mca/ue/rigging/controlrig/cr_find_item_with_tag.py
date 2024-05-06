"""
Interacts an Unreal Control Rig "Find Item With Tag" Node
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.common import log
from mca.ue.rigging.controlrig import cr_nodes, cr_pins

logger = log.MCA_LOGGER

SCRIPT_STRUCT_PATH = '/Script/ControlRig.RigUnit_FindItemsWithMetadataTag'
BASE_NODE_NAME = 'FindItemsWithMetadataTag'


class FindItemWithTagNode(cr_pins.PinsBase):
    VERSION = '1.0.0'
    NODE_SIZE = [2, 1]

    def __init__(self, control_rig, fnode):
        super().__init__(control_rig=control_rig, fnode=fnode)

    @classmethod
    def spawn(cls, control_rig, side='center', region='find_item', position=(512.0, 160.0)):
        node_name = f'{BASE_NODE_NAME}_{side}_{region}'
        node = cr_nodes.create_control_rig_node(control_rig=control_rig,
                                       position=position,
                                       script_struct_path=SCRIPT_STRUCT_PATH,
                                       node_name=node_name)

        return cls(control_rig, fnode=node_name)

    def set_pin_default_value(self, value, pin_name='Tag'):
        self.cr_controller.set_pin_default_value(pin_path=f'{self.get_fname()}.{pin_name}',
                                                 default_value=value,
                                                 resize_arrays=False,
                                                 setup_undo_redo=True,
                                                 merge_undo_action=False,
                                                 print_python_command=False)

    def set_pin_value_to_flags(self):
        self.set_pin_default_value('isFlag')

    def set_pin_value_to_offset_flags(self):
        self.set_pin_default_value('isOffsetFlag')

    def set_pin_value_to_sub_flags(self):
        self.set_pin_default_value('isSubFlag')

    def set_pin_value_to_detail_flags(self):
        self.set_pin_default_value('isDetailFlag')

    def link(self, target, connect_name=None):
        if isinstance(target, cr_pins.PinsBase) and isinstance(connect_name, str):
            target = f'{target.get_fname()}.{connect_name}'

        elif isinstance(target, str) and '.' in target:
            target = target

        elif isinstance(target, str) and isinstance(connect_name, str):
            target = f'{target}.{target}'

        else:
            logger.warning('Unable to link nodes, It looks like the source or target link does not exist.')
            return

        source = f'{self.get_fname()}.Items'
        self.cr_controller.add_link(source, target)

