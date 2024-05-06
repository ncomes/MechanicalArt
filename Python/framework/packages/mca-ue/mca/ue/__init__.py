import os
import inspect

UNREAL_INIT_PATH = os.path.normpath(os.path.join(os.path.abspath(inspect.getfile(inspect.currentframe()))))
UNREAL_PATH = os.path.dirname(UNREAL_INIT_PATH)
UNREAL_TOP_ROOT = os.path.dirname(UNREAL_INIT_PATH)
UNREAL_MCA_PACKAGE = os.path.join(UNREAL_TOP_ROOT, '../../mat_package.yaml')