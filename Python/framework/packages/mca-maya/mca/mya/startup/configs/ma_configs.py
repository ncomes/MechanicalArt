#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that sets up the environment variables for MCA
"""

# mca python imports
import os
import sys

# software specific imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.common.textio import yamlio
from mca.mya.utils import maya_utils


logger = log.MCA_LOGGER


def add_maya_system_paths(path_list):
	if not isinstance(path_list, (list, tuple)):
		path_list = [path_list]
		
	for path in path_list:
		if os.path.isdir(path) and os.path.normpath(path) not in sys.path:
			sys.path.append(path)


class MayaDefaultStartOptions:
	def __init__(self, data=None):
		self._data = data
		if not data:
			self.set_default_options()

	@property
	def data(self):
		return self._data

	@property
	def use_defaults(self):
		"""
		If True, defaults will be set in Maya.

		:return: If True, defaults will be set in Maya.
		:rtype: boolean
		"""

		return self._data.get('use_defaults', True)

	@use_defaults.setter
	def use_defaults(self, value):
		"""
		If True, defaults will be set in Maya.

		:param bool value: If True, defaults will be set in Maya.
		"""

		self._data.update({'use_defaults': value})

	@property
	def working_unit_linear(self):
		"""
		Unit settings to be applied in maya.

		:return: Returns the Unit settings to be applied in maya.
		:rtype: str
		"""

		return self._data.get('workingUnitLinear', 'cm')

	@working_unit_linear.setter
	def working_unit_linear(self, value):
		"""
		Sets the unit settings to be applied in maya.

		:param str value: unit measure.
		"""

		self._data.update({'workingUnitLinear': value})

	@property
	def working_unit_linear_default(self):
		"""
		Default Unit settings to be applied in maya.

		:return: Returns the Default Unit settings to be applied in maya.
		:rtype: str
		"""

		return self._data.get('workingUnitLinearDefault', 'cm')

	@working_unit_linear_default.setter
	def working_unit_linear_default(self, value):
		"""
		Sets the Default unit settings to be applied in maya.

		:param str value: Default unit measure.
		"""

		self._data.update({'workingUnitLinearDefault': value})

	@property
	def working_unit_time(self):
		"""
		Returns the unit time for Maya's timeline that will be set.

		:return: Returns the unit time for Maya's timeline that will be set.
		:rtype: str
		"""

		return self._data.get('workingUnitTime', 'ntsc')

	@working_unit_time.setter
	def working_unit_time(self, value):
		"""
		Sets unit time for Maya's timeline.

		:param str value: Unit time.
		"""

		self._data.update({'workingUnitTime': value})

	@property
	def working_unit_time_default(self):
		"""
		Returns the default unit time for Maya's timeline that will be set.

		:return: Returns the default unit time for Maya's timeline that will be set.
		:rtype: str
		"""

		return self._data.get('workingUnitTimeDefault', 'ntsc')

	@working_unit_time_default.setter
	def working_unit_time_default(self, value):
		"""
		Sets default unit time for Maya's timeline.

		:param str value: Unit default time.
		"""

		self._data.update({'workingUnitTimeDefault': value})

	@property
	def playback_max(self):
		"""
		Returns the playback max for Maya's timeline that will be set.

		:return: Returns the playback max for Maya's timeline that will be set.
		:rtype: int
		"""

		return self._data.get('playbackMax', 120)

	@playback_max.setter
	def playback_max(self, value):
		"""
		Sets the playback max for Maya's timeline.

		:param int value: the playback max for Maya's timeline.
		"""

		self._data.update({'playbackMax': value})

	@property
	def playback_max_default(self):
		"""
		Returns the default playback max for Maya's timeline that will be set.

		:return: Returns the default playback max for Maya's timeline that will be set.
		:rtype: int
		"""

		return self._data.get('playbackMaxDefault', 120)

	@playback_max_default.setter
	def playback_max_default(self, value):
		"""
		Sets the default playback max for Maya's timeline.

		:param int value: the default playback max for Maya's timeline.
		"""

		self._data.update({'playbackMaxDefault': value})

	@property
	def playback_max_range(self):
		"""
		Returns the playback max range for Maya's timeline that will be set.

		:return: Returns the playback max range for Maya's timeline that will be set.
		:rtype: int
		"""

		return self._data.get('playbackMaxRange', 120)

	@playback_max_range.setter
	def playback_max_range(self, value):
		"""
		Sets the playback max range for Maya's timeline.

		:param int value: the range playback max for Maya's timeline.
		"""

		self._data.update({'playbackMaxRange': value})

	@property
	def playback_max_range_default(self):
		"""
		Returns the default playback max range for Maya's timeline that will be set.

		:return: Returns the default playback max range for Maya's timeline that will be set.
		:rtype: int
		"""

		return self._data.get('playbackMaxRangeDefault', 120)

	@playback_max_range_default.setter
	def playback_max_range_default(self, value):
		"""
		Sets the default playback max range for Maya's timeline.

		:param int value: the default range playback max for Maya's timeline.
		"""

		self._data.update({'playbackMaxRangeDefault': value})

	@property
	def playback_min(self):
		"""
		Returns the playback min for Maya's timeline that will be set.

		:return: Returns the playback min for Maya's timeline that will be set.
		:rtype: int
		"""

		return self._data.get('playbackMin', 0)

	@playback_min.setter
	def playback_min(self, value):
		"""
		Sets the playback min for Maya's timeline.

		:param int value: the playback min for Maya's timeline.
		"""

		self._data.update({'playbackMin': value})

	@property
	def playback_min_default(self):
		"""
		Returns the default playback min for Maya's timeline that will be set.

		:return: Returns the default playback min for Maya's timeline that will be set.
		:rtype: int
		"""

		return self._data.get('playbackMinDefault', 0)

	@playback_min_default.setter
	def playback_min_default(self, value):
		"""
		Sets the default playback min for Maya's timeline.

		:param int value: the default playback min for Maya's timeline.
		"""

		self._data.update({'playbackMinDefault': value})

	@property
	def playback_min_range(self):
		"""
		Returns the playback min range for Maya's timeline that will be set.

		:return: Returns the playback min range for Maya's timeline that will be set.
		:rtype: int
		"""

		return self._data.get('playbackMinRange', 0)

	@playback_min_range.setter
	def playback_min_range(self, value):
		"""
		Sets the playback min range for Maya's timeline.

		:param int value: the range playback min for Maya's timeline.
		"""

		self._data.update({'playbackMinRange': value})

	@property
	def playback_min_range_default(self):
		"""
		Returns the default playback min range for Maya's timeline that will be set.

		:return: Returns the default playback min range for Maya's timeline that will be set.
		:rtype: int
		"""

		return self._data.get('playbackMinRangeDefault', 0)

	@playback_min_range_default.setter
	def playback_min_range_default(self, value):
		"""
		Sets the default playback min range for Maya's timeline.

		:param int value: the default range playback min for Maya's timeline.
		"""

		self._data.update({'playbackMinRangeDefault': value})

	@property
	def grid_divisions(self):
		"""
		Returns the number of grid divisions that will be set.

		:return: Returns the number of grid divisions that will be set.
		:rtype: int
		"""

		return self._data.get('gridDivisions', 10)

	@grid_divisions.setter
	def grid_divisions(self, value):
		"""
		Sets the number of grid divisions.

		:param int value: the number of grid divisions.
		"""

		self._data.update({'gridDivisions': value})

	@property
	def grid_size(self):
		"""
		Returns the grid size that will be set.

		:return: Returns the grid size that will be set.
		:rtype: int
		"""

		return self._data.get('gridSize', 200)

	@grid_size.setter
	def grid_size(self, value):
		"""
		Sets the grid size.

		:param int value: the grid size.
		"""

		self._data.update({'gridSize': value})

	@property
	def grid_spacing(self):
		"""
		Returns the grid spacing that will be set.

		:return: Returns the grid spacing that will be set.
		:rtype: int
		"""

		return self._data.get('gridSpacing', 100)

	@grid_spacing.setter
	def grid_spacing(self, value):
		"""
		Sets the grid spacing.

		:param int value: the grid spacing.
		"""

		self._data.update({'gridSpacing': value})

	def set_default_options(self):
		"""
		Default Maya options.
		"""

		self._data = {}
		self._data.update({"use_defaults": True})
		# setting the units
		self._data.update({"workingUnitLinear": "cm"})
		self._data.update({"workingUnitLinearDefault": "cm"})
		self._data.update({"workingUnitTime": "ntsc"})
		self._data.update({"workingUnitTimeDefault": "ntsc"})

		# setting the timeline durations and defaults
		self._data.update({"playbackMax": 120})
		self._data.update({"playbackMaxDefault": 120})
		self._data.update({"playbackMaxRange": 120})
		self._data.update({"playbackMaxRangeDefault": 120})
		self._data.update({"playbackMin": 0})
		self._data.update({"playbackMinDefault": 0})
		self._data.update({"playbackMinRange": 0})
		self._data.update({"playbackMinRangeDefault": 0})

		# setting the grid settings
		self._data.update({"gridDivisions": 10})
		self._data.update({"gridSize": 200})
		self._data.update({"gridSpacing": 100})

	def apply_maya_defaults(self):
		"""
		Applies the settings to Maya.
		"""
		if not self._data.get('use_defaults'):
			return

		for k, v in self._data.items():
			if k is 'use_defaults':
				continue
			elif isinstance(v, str):
				pm.optionVar(sv=(k, v))
			elif isinstance(v, (float, int)):
				pm.optionVar(fv=(k, v))
			else:
				logger.warning(f'Cannot set type for {k}: {type(v)} not declared in class.')
				continue

	@classmethod
	def load(cls, save_data=True):
		"""
		Returns an instance of MayaDefaultStartOptions with either saved data or default data.

		:param save_data:
		:return: Returns an instance of MayaDefaultStartOptions with either saved data or default data.
		:rtype: MayaDefaultStartOptions
		"""

		default_prefs = maya_utils.get_default_preferences_file()
		if not os.path.exists(default_prefs):
			logger.warning("No preferences file was found.  Returning default settings.")
			default_cls = cls()
			if save_data:
				yamlio.write_yaml(default_prefs, default_cls.data)
			return default_cls
		prefs = yamlio.read_yaml(default_prefs)
		return cls(prefs)

	def save(self):
		"""
		Saves the default settings to a yaml file in the preferences folder.
		"""

		default_prefs = maya_utils.get_default_preferences_file()
		yamlio.write_yaml(default_prefs, self._data)

