from mca.ue import pyunreal as pue
from mca.ue.pyunreal import general
from mca.ue.tools.scripteditor import script_editor_ui
import unreal

reload(script_editor_ui)
reload(script_editor_ui)
reload(pue)
reload(general)

sk_skel = pue.selected()

skel_mesh = sk_skel[0]
print(skel_mesh)
print(skel_mesh.get_class())

print(type(skel_mesh))



# print(skel_mesh.get_class())
# skel_mesh = unreal.SkeletalMesh(skel_mesh)

skel = pue.PySkelMesh(skel_mesh)

print(skel)
print(pue)

print(skel_mesh.get_name())


[print(x) for x in dir(skel_mesh)]




sm_skel = pue.selected()
sm = sm_skel[0]

print(sm.get_name())