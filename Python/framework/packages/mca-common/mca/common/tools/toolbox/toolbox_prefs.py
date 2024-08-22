"""
Saving preferences for the toolbox
"""

# mca python imports
import os

# software specific imports
# mca python imports
from mca.common.project import paths
from mca.common.tools import toolbox
from mca.common.textio import yamlio
from mca.common import log

logger = log.MCA_LOGGER

LOCAL_PREFS_FILE = f'toolbox_{toolbox.TOOLBOX_VERSION}.pref'


TOOLBOX_PREFS_DICT = {'All Tools': {'on_dcc_start': 0,
						'start_docked': 1,
						'toolbar_buttons': {}}}

TOOLBOX_PREFERENCES = {}


def get_toolbox_local_prefs_folder(dcc):
	"""
	Returns the folder where the local toolbox prefs lives.
	
	:param str dcc: the dcc software
	:return: Returns the folder where the local toolbox prefs lives.
	:rtype: str
	"""
	
	prefs_folder = paths.get_dcc_prefs_folder(dcc=dcc)
	dcc_folder = os.path.join(prefs_folder, f'Toolbox')
	return os.path.normpath(dcc_folder)


def create_toolbox_local_prefs_folder(dcc):
	"""
	Creates the folder where the local toolbox prefs lives.

	:param str dcc: the dcc software
	:return: Returns the folder where the local toolbox prefs lives.
	:rtype: str
	"""
	
	toolbox_folder = get_toolbox_local_prefs_folder(dcc=dcc)
	if not os.path.exists(toolbox_folder):
		os.makedirs(toolbox_folder)
	return toolbox_folder


def get_toolbox_local_prefs_file(dcc):
	"""
	Creates the File where the local toolbox prefs lives.

	:param str dcc: the dcc software
	:return: Returns the file where the local toolbox prefs lives.
	:rtype: str
	"""
	
	prefs_folder = create_toolbox_local_prefs_folder(dcc=dcc)
	prefs_file = os.path.join(prefs_folder, LOCAL_PREFS_FILE)
	if not os.path.isfile(prefs_file):
		#os.makedirs(os.path.dirname(prefs_file))
		yamlio.write_yaml(prefs_file, TOOLBOX_PREFS_DICT)
	return os.path.normpath(prefs_file)
	
	
def get_toolbox_common_prefs(dcc):
	"""
	
	:param dcc:
	:return: Returns the path to the preferences for the toolbox in the Tools/Common Directory
	:rtype: str
	"""
	
	path = paths.get_common_tools_path()
	toolbox_path = os.path.join(path, dcc, 'Toolbox')
	if not os.path.exists(toolbox_path):
		os.makedirs(toolbox_path)
	return toolbox_path


class AllToolBoxPreferences:
	def __init__(self, data=None, dcc=None):
		self.path = get_toolbox_local_prefs_file(dcc=dcc)
		self.data = data or self.read_file()
		
		if not self.data:
			self.data = TOOLBOX_PREFS_DICT
			
	@property
	def toolbox_list(self):
		return list(self.data.keys())
	
	def read_file(self):
		"""
		Reads the preferences file
		"""
		
		data = yamlio.read_yaml(self.path)
		return data
	
	def write_file(self):
		"""
		Writes the preferences file
		"""
		
		yamlio.write_yaml(self.path, self.data)
	
	def get_all_on_startups(self):
		"""
		Returns a list of toolboxes that should be loaded at startup
		
		:return: Returns a list of toolboxes that should be loaded at startup
		:rtype: list[str]
		"""
		
		start_ups = []
		for tb in self.toolbox_list:
			if self.data[tb].get('on_dcc_start', 0):
				start_ups.append(tb)
		return start_ups


class ToolBoxPreferences(AllToolBoxPreferences):
	def __init__(self, data=None, toolbox='All Tools', dcc=None):
		super().__init__(data=data, dcc=dcc)
		
		self.toolbox = toolbox
		if self.toolbox not in self.data.keys():
			self.data.update(self.default_toolbox_data())
	
	@property
	def tb_data(self):
		return self.data[self.toolbox]
	
	@property
	def on_start(self):
		startup = self.tb_data.get('on_dcc_start', None)
		if startup is None:
			logger.warning('There was an issue getting the "on startup" value.  Please check the yaml data.')
			return 0
		return startup
	
	@on_start.setter
	def on_start(self, value):
		self.tb_data.update({'on_dcc_start': value})
	
	@property
	def start_docked(self):
		docked = self.tb_data.get('start_docked', None)
		if docked is None:
			logger.warning('There was an issue getting the "start docked" value.  Please check the yaml data.')
			return 0
		return docked
	
	@start_docked.setter
	def start_docked(self, value):
		self.tb_data.update({'start_docked': value})
	
	def update_entry(self, entry, value):
		"""
		Updates a toolbox entry
		:param str entry: name of the entry.  Ex: button_name, on_dcc_start
		:param bool/int/str value: value for the entry
		"""
		
		self.tb_data.update({entry: value})
	
	def default_toolbox_data(self):
		"""
		Returns a default dictionary for a toolbox entry.  aka, the start dictionary.
		
		:return: Returns a default dictionary for a toolbox entry.  aka, the start dictionary.
		:rtype: Dictionary
		"""
		
		return {self.toolbox: {'on_dcc_start': 0,
								'start_docked': 1,
								'toolbar_buttons': {}}}
	
	def toolbar_entry_exist(self, toolbar_id):
		"""
		Checks to see if an entry exists.
		:param str toolbar_id: the name or id of the toolbar button.
		:return: Returns if an entry exists
		:rtype: bool
		"""
		if not self.tb_data['toolbar_buttons'].get(toolbar_id, None):
			return False
		return True
	
	def update_toolbar_button(self, toolbar_id, state):
		"""
		Sets whether the toolbar button was opened or not.
		
		:param str toolbar_id: the name or id of the toolbar button.
		:param bool state: Sets whether the toolbar button was opened or not.
		"""
		
		state = {'state': state}
		self.tb_data['toolbar_buttons'].update({toolbar_id: state})
	
	def get_toolbar_button_state(self, toolbar_id):
		
		return self.tb_data['toolbar_buttons'][toolbar_id].get('state', 0)

	def entry_exist(self, entry):
		"""
		Checks to see if an entry exists.
		
		:param str entry: name of the entry.  Ex: button_name, on_dcc_start
		:return: Returns if an entry exists
		:rtype: bool
		"""
		
		if not self.tb_data:
			return False
		return self.tb_data.get(entry, None)

