#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interacting with Google Sheets
"""

# mca python imports
import os
# software specific imports

# mca python imports
from mca import common
from mca.common.textio import yamlio


USER_DATA_DICT = {'username': {'country': {},
			'email': {},
			'full_name': {},
			'location': {},
			'team': {},
			'title': {},
			'local_username': {}}}

DCC_TRACKING_DATA = os.path.normpath(os.path.join(common.MCA_CONFIGS_PATH, 'dcc_user_data.yaml'))
DCC_EXCLUDE_TRACKING_USER = os.path.normpath(os.path.join(os.path.dirname(__file__), 'dcc_user_exclude_tracking.yaml'))
DCC_TEAM_TRACKING = os.path.normpath(os.path.join(os.path.dirname(__file__), 'dcc_teams_tracking.yaml'))


class DCCTrackingIgnoreUsers:
	def __init__(self, exclude_data):
		self._exclude_data = exclude_data
	
	@property
	def exclude_data(self):
		return self._exclude_data
	
	@property
	def usernames(self):
		return self.exclude_data.get('usernames', [])
	
	def export(self, file_name=None):
		"""
		Exports the file.
		
		:param str file_name: name of the file to export.
		"""
		
		if not file_name:
			file_name = DCC_EXCLUDE_TRACKING_USER
		yamlio.write_to_yaml_file(self.exclude_data, file_name)
	
	@classmethod
	def load(cls, file_name=None):
		"""
		Loads the file.

		:param str file_name: name of the file to load.
		"""
		
		if not file_name:
			file_name = DCC_EXCLUDE_TRACKING_USER
		exclude_dict = yamlio.read_yaml_file(file_name)
		return cls(exclude_dict)


class DCCTrackingTeams:
	def __init__(self, team_data):
		self._team_data = team_data
	
	@property
	def team_data(self):
		return self._team_data
	
	@property
	def teams(self):
		return self.team_data.get('teams', [])
	
	@property
	def teams_names(self):
		return list(self.teams.keys())
	
	def export(self, file_name=None):
		"""
		Exports the file.

		:param str file_name: name of the file to export.
		"""
		
		if not file_name:
			file_name = DCC_TEAM_TRACKING
		yamlio.write_to_yaml_file(self.team_data, file_name)
	
	@classmethod
	def load(cls, file_name=None):
		"""
		Loads the file.

		:param str file_name: name of the file to load.
		"""
		
		if not file_name:
			file_name = DCC_TEAM_TRACKING
		team_dict = yamlio.read_yaml_file(file_name)
		return cls(team_dict)


class DCCTrackingRiggingTeam(DCCTrackingTeams):
	def __init__(self, data, team):
		super(DCCTrackingRiggingTeam, self).__init__(data)
		self._data = data
		self._team = team
	
	@property
	def data(self):
		return self._data
	
	@property
	def team(self):
		return self._team
	
	@property
	def team_data(self):
		self._data.setdefault('teams', {})
		return self.data['teams']
	
	@property
	def team_members(self):
		return self.team_data.get(self.team, None)

