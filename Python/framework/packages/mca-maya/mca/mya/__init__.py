import os
import inspect

MAYA_INIT_PATH = os.path.normpath(os.path.join(os.path.abspath(inspect.getfile(inspect.currentframe()))))
MAYA_PATH = os.path.dirname(MAYA_INIT_PATH)
MAYA_TOP_ROOT = os.path.dirname(MAYA_INIT_PATH)
MAYA__PACKAGE = os.path.join(MAYA_TOP_ROOT, '../../_package.yaml')

