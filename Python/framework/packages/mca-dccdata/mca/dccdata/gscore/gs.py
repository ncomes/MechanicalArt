#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interacting with Google Sheets
"""

# mca python imports
from collections import OrderedDict
import os
# software specific imports
from googleapiclient import discovery
from google.oauth2 import service_account

# mca python imports
from mca.common.paths import paths
from mca.common import log

logger = log.MCA_LOGGER

DCC_TRACKING_SOFTWARE_ID = '1Rr7OdoxlxOEgraF8Ee4d0HvslufZIKvdh6oQ0KyoQ3o'
SERVICE_ACCOUNT_FILE = os.path.join(paths.get_common_path(), 'Google Sheets', 'dcc-gs_key.json')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GSToolsRowData:
	def __init__(self,
					function,
					username,
					classes,
					software,
					modules,
					fullname,
					date,
					pst,
					timezone,
					localtime,
					email,
					team,
					title,
					location,
					country,
					local_username,
					hash):
	
		self.function = function.lower()
		self.username = username.lower()
		self.classes = classes.lower()
		self.software = software.lower()
		self.modules = modules.lower()
		self.fullname = fullname.lower()
		self.date = date
		self.pst = pst
		self.timezone = timezone.lower()
		self.localtime = localtime
		self.email = email.lower()
		self.team = team.lower()
		self.title = title.lower()
		self.location = location.lower()
		self.country = country.lower()
		self.local_username = local_username.lower()
		self.hash = hash
		
		self.data_sources = {}
		self.data_sources['function'] = self.function
		self.data_sources['username'] = self.username
		self.data_sources['classes'] = self.classes
		self.data_sources['software'] = self.software
		self.data_sources['modules'] = self.modules
		self.data_sources['fullname'] = self.fullname
		self.data_sources['date'] = self.date
		self.data_sources['pst'] = self.pst
		self.data_sources['timezone'] = self.timezone
		self.data_sources['localtime'] = self.localtime
		self.data_sources['email'] = self.email
		self.data_sources['team'] = self.team
		self.data_sources['title'] = self.title
		self.data_sources['location'] = self.location
		self.data_sources['country'] = self.country
		self.data_sources['local_username'] = self.local_username
		self.data_sources['hash'] = self.hash
	
	def attr(self, value):
		return self.data_sources.get(value, None)
		
		
class GSData:
	def __init__(self, spreadsheet_id, key_file, default_register=True):
		self._id = spreadsheet_id
		self._key = key_file
		
		if default_register:
			self.register()
		
	def register(self):
		"""
		Registers the credentials for the Google Sheet.  This gives us access to the sheets API.
		"""
		
		self.credentials = service_account.Credentials.from_service_account_file(self.key, scopes=SCOPES)
		# The ID and range of a spreadsheet.
		service = discovery.build('sheets', 'v4', credentials=self.credentials, cache_discovery=False)
		self.spreadsheet = service.spreadsheets()
	
	@property
	def id(self):
		return self._id
	
	@property
	def key(self):
		return self._key
	
	def register_check(self):
		"""
		Checks to see if the spreadsheet and credentials have been registered.

		:return: If True, The spreadsheet and credentials have been registered.
		:rtype: bool
		"""
		
		if not self.credentials or not self.spreadsheet:
			print("The Google SpreadSheets Credentials have not been registered!")
			return False
		return True
	
	def get_all_worksheet_names(self):
		"""
		Returns a list of all the work sheets in the google sheet.

		:return: Returns a list of all the work sheets in the google sheet.
		:rtype: list(str)
		"""
		
		sheet_metadata = self.spreadsheet.get(spreadsheetId=self.id).execute()
		sheets = sheet_metadata.get('sheets', '')
		
		worksheet_names = []
		for wrksht in sheets:
			worksheet_names.append(wrksht.get('properties', {}).get('title', ""))
		return worksheet_names


class GSToolData(GSData):
	def __init__(self, spreadsheet_id, key_file, default_register=True):
		super().__init__(spreadsheet_id=spreadsheet_id, key_file=key_file, default_register=default_register)
		if default_register:
			self._all_data = self.get_all_data()
		else:
			self._all_data = {}
	
	def get_headers(self, sheet):
		"""
		Returns a list of all the headers on a specific worksheet
		
		:param str sheet: name of the worksheet
		:return: Returns a list of all the headers on a specific worksheet
		:rtype: list(str)
		"""
		
		headers = self.get_range_values(sheet, 'A1:Z1')
		if not headers:
			print('No Headers!  Cannot continue.')
			return
		return headers[0]
	
	def get_range_values(self, sheet, gs_range):
		"""
		Returns a list with a list of values for each row requested

		:param str sheet: name of the worksheet
		:param str gs_range: Row and Column data
		:return: Returns a list with a list of values for each row requested
		:rtype: list(list[str])
		"""
		
		_range = f'{sheet}!{gs_range}'
		request = self.spreadsheet.values().get(spreadsheetId=self.id, range=_range)
		response = request.execute()
		_values = response.get('values', [])
		_range = response.get('range', None)
		if not _values or not _range:
			return
		
		data_objs = []
		for x, val in enumerate(_values):
			data_objs.append(GSToolsRowData(val[0],
											val[1],
											val[2],
											val[3],
											val[4],
											val[5],
											val[6],
											val[7],
											val[8],
											val[9],
											val[10],
											val[11],
											val[12],
											val[13],
											val[14],
											val[15],
											val[16]))
		return data_objs
	
	def get_sheet_dict(self, sheet):
		"""
		Returns of all data from a single worksheet from a google sheet

		:param str sheet: Name of the worksheet
		:return: Returns of all data from a single worksheet from a google sheet
		:rtype: dictionary
		"""
		
		values = self.get_range_values(sheet, 'A2:Z1000')
		data = OrderedDict()
		data[sheet] = values
		return data
	
	def get_all_data(self):
		"""
		Returns a dictionary of all the google sheet data.

		:return: Returns a dictionary of all the google sheet data.
		:rtype: dictionary
		"""
		
		all_sheets = self.get_all_worksheet_names()
		all_sheets = [x for x in all_sheets if 'total' not in x.lower() and 'chart' not in x.lower()]
		all_data = {}
		for sheet in all_sheets:
			all_data.update(self.get_sheet_dict(sheet))
		
		return all_data
	
	def get_column_data(self, header, sheets=()):
		
		if not sheets:
			sheets = self.get_all_worksheet_names()
			sheets = [x for x in sheets if 'total' not in x.lower() and 'chart' not in x.lower()]
		if not isinstance(sheets, (tuple, list)):
			sheets = [sheets]

		filter_list = []
		for sheet, data_list in self._all_data.items():
			if sheet in sheets:
				for data in data_list:
					data_entry = data.attr(header.lower())
					if not data_entry:
						continue
					filter_list.append(data)
		return filter_list
		
	def get_specific_data(self, header, entry, sheets=()):
		"""
		Returns a list with the selected criteria
		
		:param str header: The header on the google sheet
		:param str entry: The row data that is entered
		:param list(str) sheets:
		:return: Returns a list with the selected criteria
		:rtype: list(GSToolsRowData)
		"""
		if not sheets:
			sheets = self.get_all_worksheet_names()
			sheets = [x for x in sheets if 'total' not in x.lower() and 'chart' not in x.lower()]
		if not isinstance(sheets, (tuple, list)):
			sheets = [sheets]

		filter_list = []
		for sheet, data_list in self._all_data.items():
			if sheet in sheets:
				for data in data_list:
					data_entry = data.attr(header.lower())
					if not data_entry:
						continue
					if entry.lower() in data_entry.lower():
						filter_list.append(data)
		return filter_list

	def filter_row(self, row_data, header, entry):
		row_entry = row_data.attr(header)
		if entry == row_entry:
			return True
		return False
	
	def filter_rows(self, row_data_list, header, entry):
		row_list = []
		for row_data in row_data_list:
			if self.filter_row(row_data, header, entry):
				row_list.append(row_data)
		return row_list
	
	def get_tools_count(self, dcc=None, class_name=None, total_number=None):
		# get all tool functions, class, and count

		funcs = self.get_column_data(header='function')
		if dcc:
			dcc = dcc.lower()
			funcs = [x for x in funcs if x.software == dcc]
		if class_name:
			funcs = [x for x in funcs if x.classes == dcc]
		if not funcs:
			return
		
		all_func_names = [x.function for x in funcs]
		func_names = list(set(all_func_names))
		names = {}
		for name in func_names:
			names.update({name: all_func_names.count(name)})
		sorted_names = sorted(names.items(), key=lambda x: x[1])
		sorted_names.reverse()
		if not total_number:
			return sorted_names
		tools_list = sorted_names[:int(total_number)]
		return tools_list



























class ReadGSData(GSData):
	def __init__(self, spreadsheet_id, key_file, default_register=True):
		super().__init__(spreadsheet_id=spreadsheet_id, key_file=key_file, default_register=default_register)
		self._all_data = {}
	
	def get_all_worksheet_names(self):
		"""
		Returns a list of all the work sheets in the google sheet.

		:return: Returns a list of all the work sheets in the google sheet.
		:rtype: list(str)
		"""
		
		sheet_metadata = self.spreadsheet.get(spreadsheetId=self.id).execute()
		sheets = sheet_metadata.get('sheets', '')
		
		worksheet_names = []
		for wrksht in sheets:
			worksheet_names.append(wrksht.get('properties', {}).get('title', ""))
		return worksheet_names
	
	def get_row_data(self, sheet, gs_range):
		"""
		
		
		:param gs_range:
		:return:
		"""
		
		_range = f'{sheet}!{gs_range}'
		request = self.spreadsheet.values().get(spreadsheetId=self.id, range=_range)
		response = request.execute()
		
		data = {}
		data[sheet] = {}
		data[sheet].update({'values': response.get('values', [])})
		
		return data
	
	def get_range_values(self, sheet, gs_range):
		"""
		Returns a list with a list of values for each row requested
		
		:param sheet:
		:param gs_range: Row and Column data
		:return: Returns a list with a list of values for each row requested
		:rtype: list(list[str])
		"""
		
		_range = f'{sheet}!{gs_range}'
		request = self.spreadsheet.values().get(spreadsheetId=self.id, range=_range)
		response = request.execute()
		return response.get('values', [])
	
	def get_sheet_dict(self, sheet):
		"""
		Returns of all data from a single worksheet from a google sheet
		
		:param str sheet: Name of the worksheet
		:return: Returns of all data from a single worksheet from a google sheet
		:rtype: dictionary
		"""
		
		values = self.get_range_values(sheet, 'A2:Z1000')
		data = OrderedDict()
		data[sheet] = {}
		headers = self.get_range_values(sheet, 'A1:Z1')
		if not headers:
			print('No Headers!  Cannot continue.')
			return
		headers = headers[0]
		print(headers)
		row = 2
		for val in values:
			data[sheet][f'{row}'] = {}
			for x, header in enumerate(headers):
				data[sheet][f'{row}'].update({header: val[x]})
			row += 1
		
		return data
	
	def get_all_data(self):
		"""
		Returns a dictionary of all the google sheet data.
		
		:return: Returns a dictionary of all the google sheet data.
		:rtype: dictionary
		"""
		
		all_sheets = self.get_all_worksheet_names()
		all_sheets = [x for x in all_sheets if 'total' not in x.lower() and 'chart' not in x.lower()]
		all_data = {}
		for sheet in all_sheets:
			all_data.update(self.get_sheet_dict(sheet))
		
		return all_data

	def get_dcc_numbers(self, sheet_name, dcc):
		if not self._all_data:
			return
		count = 0

		for sheet, data in self._all_data.items():
			if sheet != sheet_name:
				continue
			if data[0] == dcc:
				count += 1
		return count

	def get_dcc_per_person(self, sheet_name, dcc, username):
		if not self._all_data:
			return
		count = 0

		for sheet, data in self._all_data.items():
			if sheet != sheet_name:
				continue
			if data[0] == dcc and data:
				count += 1
		return count

	




























class GoogleSheets:
	def __init__(self, spreadsheet_id, key_file, default_register=True):
		self._id = spreadsheet_id
		self._key = key_file
		self.credentials = None
		self.spreadsheet = None
		
		if default_register:
			self.register()
		
	@property
	def id(self):
		return self._id
	
	@property
	def key(self):
		return self._key
	
	def register(self):
		"""
		Registers the credentials for the Google Sheet.  This gives us access to the sheets API.
		"""
		
		self.credentials = service_account.Credentials.from_service_account_file(self.key, scopes=SCOPES)
		# The ID and range of a spreadsheet.
		service = discovery.build('sheets', 'v4', credentials=self.credentials)
		self.spreadsheet = service.spreadsheets()
	
	def register_check(self):
		"""
		Checks to see if the spreadsheet and credentials have been registered.
		
		:return: If True, The spreadsheet and credentials have been registered.
		:rtype: bool
		"""
		
		if not self.credentials or not self.spreadsheet:
			logger.warning("The Google SpreadSheets Credentials have not been registered!")
			return False
		return True
	
	def format_cell_range(self, sheet_name, start=None, end=None):
		"""
		
		:param str sheet_name: Name of the worksheet.
		:param str start: Starting Row and Column.
		:param str end: Ending Row and Column.
		:return: Returns a properly formatted string to add a cell range.
		:rtype: str
		"""
		
		if not end:
			range = f'{sheet_name}!{start}'
		else:
			range = f'{sheet_name}!{start}:{end}'
		return range
	
	def update_cells(self, sheet_name, start=None, end=None, input_values=()):
		"""
		Adds data to a cell range.
		
		:param str sheet_name: Name of the worksheet.
		:param str start: Starting Row and Column.
		:param str end: Ending Row and Column.
		:param list(str) input_values: List of values that will be inputted into the cells.
		"""
		
		if not self.register_check():
			return
		
		input_data = [input_values]
		range = self.format_cell_range(sheet_name=sheet_name, start=start, end=end)
		request = self.spreadsheet.values().update(spreadsheetId=self.id,
										range=range,
										valueInputOption='USER_ENTERED',
										body={'values': input_data})
		request.execute()
	
	def append_to_cells(self, sheet_name, start=None, end=None, input_values=()):
		"""
		Adds data to the next cell row.
		
		:param str sheet_name: Name of the worksheet.
		:param str start: Starting Row and Column.
		:param str end: Ending Row and Column.
		:param list(str) input_values: List of values that will be inputted into the cells.
		"""
		
		if not self.register_check():
			return
		
		input_data = [input_values]
		range = self.format_cell_range(sheet_name=sheet_name, start=start, end=end)
		request = self.spreadsheet.values().append(spreadsheetId=self.id,
													range=range,
													valueInputOption='USER_ENTERED',
													#insertDataOption='INSERT_ROWS',
													body={'values': input_data})
		request.execute()
	
	def get_all_worksheet_names(self):
		"""
		Returns a list of all the work sheets in the google sheet.
		
		:return: Returns a list of all the work sheets in the google sheet.
		:rtype: list(str)
		"""
		
		sheet_metadata = self.spreadsheet.get(spreadsheetId=self.id).execute()
		sheets = sheet_metadata.get('sheets', '')
		
		worksheet_names = []
		for wrksht in sheets:
			worksheet_names.append(wrksht.get('properties', {}).get('title', ""))
		return worksheet_names
	
	def add_basic_worksheet(self, worksheet_name, frozen_rows=0):
		"""
		Creates a new work sheet with the given name.
		
		:param str worksheet_name: The name of the Spread Sheet
		:param int frozen_rows: number of frozen rows.
		"""
		
		spreadsheet_body = {
			'requests': [{
				'addSheet': {
					'properties': {
						'title': worksheet_name,
						'gridProperties': {'frozenRowCount': frozen_rows}}
				}}]}
		
		request = self.spreadsheet.batchUpdate(body=spreadsheet_body, spreadsheetId=self.id)
		request.execute()
	
	def create_non_existing_worksheet(self, worksheet_name, frozen_rows=0):
		"""
		Checks to see if the worksheet name exists.  If not, it creates a new worksheet.
		
		:param str worksheet_name: name of the worksheet.
		:param int frozen_rows: number of frozen rows.
		:return: If a new sheet is created it will return True.
		:rtype: bool
		"""
		
		worksheets = self.get_all_worksheet_names()
		existing_worksheet = None
		for sheet in worksheets:
			if worksheet_name == sheet:
				return False
		if not existing_worksheet:
			self.add_basic_worksheet(worksheet_name, frozen_rows=frozen_rows)
		return True
		
