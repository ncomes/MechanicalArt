"""
Creates a world component in Unreal Control Rig.
"""

# System global imports
# mca python imports
# software specific imports
import unreal
# mca python imports
# Internal module imports
from mca.ue.rigging.controlrig import cr_colorize_controls, cr_make_color, cr_find_item_with_tag


class UECollectionColorize:
    def __init__(self, control_rig):
        self.control_rig = control_rig

    def spawn_nodes(self):
        colorize_node = cr_colorize_controls.ColorizeControlsNode.spawn(self.control_rig, position=[0.0, 0.0])

        colorize_size = cr_colorize_controls.NODE_SIZE
        find_items_size = cr_find_item_with_tag.NODE_SIZE
        color_size = cr_make_color.NODE_SIZE




