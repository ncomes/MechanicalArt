#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module Loads the mat_package.yaml and makes the data available.
"""

# python imports
import os

# software specific imports

# mca python imports
from mca import common
from mca.common.textio import yamlio, jsonio
from mca.common import log
from mca.common.startup.configs import consts
from mca.common.paths import project_paths

logger = log.MCA_LOGGER


def get_package_config_file():
	"""
	Returns the config file for the project
	
	:return: Returns the config file for the project
	:rtype: str
	"""
	
	config_path = project_paths.get_package_python_config_path()
	config_file = os.path.join(config_path, consts.PROJECT_CONFIG_NAME)
	if os.path.isfile(config_file):
		# "\mca_framework\config\"
		return config_file


def read_config_file(config_file=None):
	if not config_file:
		config_file = get_package_config_file()
	result = yamlio.read_yaml_file(config_file)
	return result


def get_common_package():
	common_paths = os.getenv(consts.MCA_COMMON_TOP_ROOT)
	common_package = os.path.join(common_paths, consts.PKG_NAME)
	package_dict = read_config_file(common_package)
	return package_dict
	

def get_package_dict(yaml_pkg):
	return yamlio.read_yaml_file(yaml_pkg)


def mat_package_env_vars(yaml_pkg):
	pkg_dict = get_package_dict(yaml_pkg)
	if not pkg_dict:
		logger.warning('Cannot add COMMON environment variables.  Package does not exist.')
		return
	
	top_level_path = common.TOP_ROOT
	
	# create env variables
	env_vars = pkg_dict.get('environment', None)
	if env_vars:
		for var_name, values in env_vars.items():
			if isinstance(values, list):
				values = f"{[os.path.normpath(x.replace('{self}', top_level_path)) for x in values]}"
			else:
				values = os.path.normpath(values.replace('{self}', top_level_path))
			os.environ[str(var_name)] = f'{values}'
		logger.info('Common Environment Variables Were Set.')
		
		
def package_depot_name(yaml_pkg):
	pkg_dict = get_package_dict(yaml_pkg)
	return pkg_dict.get('depotName', None)


class ProjectPackageManager:
	def __init__(self, package_file=None):
		if not package_file:
			package_file = common.MCA_PACKAGE
		self.package_dict = read_config_file(package_file)
	
	@property
	def get_env_paths(self):
		return self.package_dict.get('environment')
	
	@property
	def mat_path(self):
		return os.path.normpath(self.get_env_paths['MCA_PATH'].replace('{self}', project_paths.get_mca_package_path()))
	
	@property
	def common_path(self):
		return os.getenv(consts.MCA_COMMON_TOP_ROOT)
	
	@property
	def dependencies_path(self):
		return os.path.normpath(self.get_env_paths['MCA_COMMON_DEPENDENCIES'].replace('{self}', self.common_path))
	
	@property
	def resources_path(self):
		return os.path.normpath(self.get_env_paths['MCA_RESOURCES_PATH'].replace('{self}', self.common_path))
	
	@property
	def icons_path(self):
		return os.path.normpath(self.get_env_paths['MCA_COMMON_ICONS_PATH'].replace('{self}', self.common_path))
	
	@property
	def images_path(self):
		return os.path.normpath(self.get_env_paths['MCA_COMMON_IMAGES_PATH'].replace('{self}', self.common_path))
	
	@property
	def styles_path(self):
		return os.path.normpath(self.get_env_paths['MCA_COMMON_STYLES_PATH'].replace('{self}', self.common_path))
	
	@property
	def fonts_path(self):
		return os.path.normpath(self.get_env_paths['MCA_COMMON_FONTS_PATH'].replace('{self}', self.common_path))
	
	@property
	def common_startup_path(self):
		return os.path.normpath(self.get_env_paths['MCA_COMMON_STARTUP_PATH'].replace('{self}', self.common_path))
	
	@property
	def project_url(self):
		return self.package_dict.get('project_url')
	
	@property
	def animation_url(self):
		return self.package_dict.get('animation_url')
	
	@property
	def modeling_url(self):
		return self.package_dict.get('modeling_url')
	
	@property
	def rigging_url(self):
		return self.package_dict.get('rigging_url')
	
	@property
	def jira_url(self):
		return self.package_dict.get('jira_url')
	
	@property
	def dcc_setup_url(self):
		return self.package_dict.get('dcc_setup_url')
