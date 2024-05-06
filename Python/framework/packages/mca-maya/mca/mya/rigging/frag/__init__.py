###############################################################################
### STANDARD PACKAGE INIT ###
### PLEASE DO NOT MESS WITH THIS FILE IF YOU DO NOT KNOW WHAT YOU ARE DOING ###
###############################################################################
import os
import sys
import inspect

_module = sys.modules[__name__]
_safe_import_list = [_x.__name__ for _x in (_module, os, sys, inspect)]

for mod in [m for m in sys.modules.keys() if m != __name__ and sys.modules[m] != None and m.startswith(
		__name__) and len(m.split(__name__ + ".")[-1].split(".")) == 1 and (not sys.modules[m].__file__.split(
	os.path.sep)[-1].startswith("__init__"))]:
	del(sys.modules[mod])

from mca.mya.rigging.frag.aim_component import *
from mca.mya.rigging.frag.animated_curves import *
from mca.mya.rigging.frag.attachment_component import *
from mca.mya.rigging.frag.channel_float_component import *
from mca.mya.rigging.frag.cog_component import *
from mca.mya.rigging.frag.display_layers import *
from mca.mya.rigging.frag.eye_center_component import *
from mca.mya.rigging.frag.eye_component import *
from mca.mya.rigging.frag.face_edit_component import *
from mca.mya.rigging.frag.face_fk_component import *
from mca.mya.rigging.frag.face_mesh_component import *
from mca.mya.rigging.frag.face_parameters import *
from mca.mya.rigging.frag.frag_base import *
from mca.mya.rigging.frag.frag_rig import *
from mca.mya.rigging.frag.frag_root import *
from mca.mya.rigging.frag.frag_sequencer import *
from mca.mya.rigging.frag.fk_component import *
from mca.mya.rigging.frag.ik_component import *
from mca.mya.rigging.frag.ikfk_component import *
from mca.mya.rigging.frag.keyable_component import *
from mca.mya.rigging.frag.leaper_tongue_component import *
from mca.mya.rigging.frag.mesh_component import *
from mca.mya.rigging.frag.multi_constraint import *
from mca.mya.rigging.frag.pelvis_component import *
from mca.mya.rigging.frag.pin_component import *
from mca.mya.rigging.frag.reverse_foot_component import *
from mca.mya.rigging.frag.rfk_component import *
from mca.mya.rigging.frag.ribbon_component import *
from mca.mya.rigging.frag.rig_component import *
from mca.mya.rigging.frag.spline_ik_component import *
from mca.mya.rigging.frag.twist_fixup_component import *
from mca.mya.rigging.frag.s_sdk_component import *
from mca.mya.rigging.frag.skeletal_mesh import *
from mca.mya.rigging.frag.world_component import *
from mca.mya.rigging.frag.z_leg_component import *
from mca.mya.rigging.frag.cine_sequence_component import *
from mca.mya.rigging.frag.camera_component import *


#deleting classes, functions, modules not in module
for _function_name in [_member[0] for _member in inspect.getmembers(
		_module, inspect.isfunction) if not _member[1].__module__.startswith(__name__)]:
	delattr(_module,_function_name)

for _class_name in [_member[0] for _member in inspect.getmembers(
		_module, inspect.isclass) if not _member[1].__module__.startswith(__name__)]:
	delattr(_module, _class_name)

for _module_info in [_member for _member in inspect.getmembers(
		_module, inspect.ismodule) if _member[1].__name__ not in _safe_import_list]:
	if not hasattr(_module_info[1], "__file__"):
		delattr(_module, _module_info[0])
		continue
	if not _module_info[1].__file__.lower().startswith(__file__.rpartition("\\")[0].lower()):
		delattr(_module, _module_info[0])
