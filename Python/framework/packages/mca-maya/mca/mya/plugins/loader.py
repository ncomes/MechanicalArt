#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains  Maya plugin loader/u functions
"""

from __future__ import print_function, division, absolute_import

import os
import inspect

from mca.common import log
from mca.common.utils import pyutils
from mca.mya.utils import plugins, maya_utils

logger = log.MCA_LOGGER


def get_root_path():
	return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def load_clone_to_quad_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'cloneToQuad_maya{}.mll'.format(maya_utils.get_version())
	plugin_path = os.path.join(get_root_path(), 'cloneToQuad', 'plug-in', str(maya_utils.get_version()), 'Release')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_clone_to_quad_plugin():
	plugin_name = 'cloneToQuad_maya{}.mll'.format(maya_utils.get_version())
	return _unload_plugin(plugin_name)


def load_dynamic_chain_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'dynamicChain.py'
	plugin_path = os.path.join(get_root_path(), 'dynamicChain')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_dynamic_chain_plugin():
	return _unload_plugin('dynamicChain.py')


def load_dynamic_constraint_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'dynamicConstraint.py'
	plugin_path = os.path.join(get_root_path(), 'dynamicConstraint')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_dynamic_constraint_plugin():
	return _unload_plugin('dynamicConstraint.py')


def load_dynamic_slide_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'dynamicSlide.py'
	plugin_path = os.path.join(get_root_path(), 'dynamicSlide')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_dynamic_slide_plugin():
	return _unload_plugin('dynamicSlide.py')


def load_green_deformer_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'greenDeformer_maya{}.mll'.format(maya_utils.get_version())
	plugin_path = os.path.join(get_root_path(), 'greenDeformer', 'plug-in', str(maya_utils.get_version()), 'Release')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_green_deformer_plugin():
	plugin_name = 'greenDeformer_maya{}.mll'.format(maya_utils.get_version())
	return _unload_plugin(plugin_name)


def load_make_roll_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'makeRoll.py'
	plugin_path = os.path.join(get_root_path(), 'makeRoll')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_make_roll_plugin():
	return _unload_plugin('makeRoll.py')


def load_rbf_retargeter_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'rbfRetargeter_maya{}.mll'.format(maya_utils.get_version())
	plugin_path = os.path.join(get_root_path(), 'rbfRetargeter', 'plug-in', str(maya_utils.get_version()), 'Release')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_rbf_retargeter_plugin():
	plugin_name = 'rbfRetargeter_maya{}.mll'.format(maya_utils.get_version())
	return _unload_plugin(plugin_name)


def load_rbf_solver_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'rbfSolver.py'
	plugin_path = os.path.join(get_root_path(), 'rbfSolver')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_rbf_solver_plugin():
	return _unload_plugin('rbfSolver.py')


def load_skinning_converter_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'skinningConverter_maya{}.mll'.format(maya_utils.get_version())
	plugin_path = os.path.join(get_root_path(), 'skinningConverter', 'plug-in', str(maya_utils.get_version()), 'Release')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_skinning_converter_plugin():
	plugin_name = 'skinningConverter_maya{}.mll'.format(maya_utils.get_version())
	return _unload_plugin(plugin_name)


def load_yaw_pitch_roll_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'yawPitchRoll.py'
	plugin_path = os.path.join(get_root_path(), 'yawPitchRoll')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_yaw_pitch_roll_plugin():
	return _unload_plugin('yawPitchRoll.py')


def load_zapan_smooth_distance_plugin(reload=False):
	plugins.add_trusted_plugin_location_path(get_root_path())
	plugin_name = 'zapanSmoothDistance.py'
	plugin_path = os.path.join(get_root_path(), 'zapanSmoothDistance')
	return _load_plugin(plugin_name, plugin_path, reload=reload, add_to_trusted_paths=False)


def unload_zapan_smooth_distance_plugin():
	return _unload_plugin('yawPitchRoll.py')


def _load_plugin(plugin_name, plugin_path=None, reload=False, add_to_trusted_paths=True):
	logger.info('Loading Maya Plugin: {} : {}'.format(plugin_name, plugin_path))
	try:
		if os.path.exists(plugin_path):
			pyutils.append_path_env_var('MAYA_PLUG_IN_PATH', plugin_path)
		if not plugins.is_plugin_loaded(plugin_name):
			plugins.load_plugin(plugin_name)
		elif plugins.is_plugin_loaded(plugin_name) and reload:
			plugins.unload_plugin(os.path.basename(plugin_name))
			plugins.load_plugin(plugin_name)
		if os.path.exists(plugin_path) and add_to_trusted_paths:
			plugins.add_trusted_plugin_location_path(plugin_path)
		return True
	except Exception as exc:
		logger.error('Failed to {} plugin: {}'.format(plugin_name, exc))

	return False


def _unload_plugin(plugin_name):
	logger.info('Unloading Maya Plugin: {} : {}'.format(plugin_name, plugin_name))
	try:
		if plugins.is_plugin_loaded(plugin_name):
			plugins.unload_plugin(os.path.basename(plugin_name))
		return True
	except Exception as exc:
		logger.error('Failed to unload {} plugin! {}'.format(plugin_name, exc))

	return False
