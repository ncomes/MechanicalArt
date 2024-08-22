# mca python imports
import os

# PySide6 imports
# mca imports
from mca.launcher.utils import path_utils


ROOT_PATH = path_utils.get_launcher_path()
ICONS_PATH = os.path.join(ROOT_PATH, 'resources', 'icons')
IMAGES_PATH = os.path.join(ROOT_PATH, 'resources', 'images')
STYLESHEET_PATH = os.path.join(ROOT_PATH, 'resources', 'stylesheets')
MOVIES_PATH = os.path.join(ROOT_PATH, 'resources', 'movies')
UI_PATH = os.path.join(ROOT_PATH, 'ui', 'launcher.ui')
INFO_PACKAGE = os.path.join(ROOT_PATH, 'mca_package.yaml')
MESSAGE_PATH = os.path.join(ROOT_PATH, 'widgets', 'missing_depots.ui')