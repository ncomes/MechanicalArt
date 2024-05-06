"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import os

# software specific imports

# mca python imports
from mca import mobu
from mca.mobu.startup.configs import mo_consts


def get_mobu_root_path():
	return mobu.MOBU_TOP_ROOT


def get_mobu_package_path():
	return mobu.MOBU_MAT_PACKAGE


def get_mobu_path():
	return mobu.MOBU_PATH


def get_mobu_tools_path():
	return os.getenv(mo_consts.TOOLS_PATH, None)


def get_mobu_configs_path():
	return os.getenv(mo_consts.CONFIGS_PATH, None)
