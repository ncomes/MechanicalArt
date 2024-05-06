"""
Unreal Definitions for Control Rig:
"""

# mca python imports
# software specific imports
# mca python imports

# The controller name for the main graph in the Control Rig Editor
# The RigVM is the main object for evaluating FRigVMByteCode instructions.
# It combines the byte code, a list of required function pointers for execute instructions and
# required memory in one class.
RIGVMMODEL = 'RigVMModel'

CONSTRUCTION_EVENT = 'PrepareForExecution'
FORWARD_SOLVE = 'RigUnit_BeginExecution'

YELLOW_RGBA = [1.0, 0.930672, 0.0, 1.0]
BLUE_RGBA = [0.0, 0.077639, 1.0, 1.0]
RED_RGBA = [1.0, 0.0, 0.0, 1.0]