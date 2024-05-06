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


class UEWorldFlagsComponent:
    def __init__(self, control_rig):
        self.control_rig = control_rig

    def world_flags(self):
        pass


