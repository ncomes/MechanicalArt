#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interacting with Google Sheets
"""

# mca python imports
# software specific imports
from googleapiclient import discovery
from google.oauth2 import service_account

# mca python imports
from mca.common import log

logger = log.MCA_LOGGER

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


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
		
