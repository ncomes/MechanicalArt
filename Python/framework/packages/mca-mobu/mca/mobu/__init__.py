import os
import inspect

MOBU_INIT_PATH = os.path.normpath(os.path.join(os.path.abspath(inspect.getfile(inspect.currentframe()))))
MOBU_PATH = os.path.dirname(MOBU_INIT_PATH)
MOBU_TOP_ROOT = os.path.dirname(MOBU_INIT_PATH)
MOBU_MAT_PACKAGE = os.path.join(MOBU_TOP_ROOT, '../../mat_package.yaml')
