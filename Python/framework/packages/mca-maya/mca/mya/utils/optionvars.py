# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Maya code related with option vars
"""

# System global imports
# software specific imports
import pymel.core as pm

#  python imports
from mca.common import log
from mca.common.modifiers import decorators, singleton
from mca.common.textio import jsonio

logger = log.MCA_LOGGER


@decorators.add_metaclass(singleton.Singleton)
class OptionVarsHelperRegistry(object):
	"""
	Singleton used to register OptionVarsHelper instances in an instance of <DCC>. Don't register directly :)
	"""
	
	def __init__(self):
		self._option_var_instances = {}
	
	def reset_all(self):
		"""
		Resets all registered optionvars back to default values
		"""
		for option_var in self._option_var_instances:
			self._option_var_instances[option_var].reset()
	
	def inspect_all(self):
		"""
		Logs all the option vars currently registered & active in <DCC>.
		Checks for duplicates
		:return: True/False if duplicate detected.
		"""
		all_registered_variable_names = set()
		errors = []
		
		for option_var in self._option_var_instances:
			self._option_var_instances[option_var].inspect()
			used_option_vars = self._option_var_instances[option_var]._option_var_names
			errors.extend([var for var in used_option_vars if var in all_registered_variable_names])
			all_registered_variable_names.union(set(used_option_vars))
		
		if errors:
			error_string = '\n\t'.join(errors)
			logger.info('Option vars that exist between data structures:\n\t' + error_string)
			return False
		return True
	
	def register_mca_option_var(self, mca_option_var):
		"""
		Register a DCCOptionVars object
		:param OptionVarsHelper mca_option_var: option var data struct to register
		:return: True
		"""
		# Can't register non  option vars type object in this object
		if not isinstance(mca_option_var, OptionVarsHelper):
			raise TypeError("Cannot register {0}: not of type {1}".format(mca_option_var, OptionVarsHelper.__name__))
		self._option_var_instances[mca_option_var.__class__.__name__] = mca_option_var
		return True
	
	def __getattr__(self, item):
		"""
		Override getattr functionality for this class to default to returning instances of OptionVar structures
		:param str item: attr name to get
		:return: Returns the attribute
		:rtype: attribute
		"""
		if item in self._option_var_instances:
			return self._option_var_instances[item]
		return object.__getattribute__(self, item)


class OptionVarsHelper(object):
	"""
	Base data structure storing, accessing & resetting optionvars in DCC's
	Each DCC will need an override of the _get_option_var() function for this to operate properly

	Note - OptionVarsHelper is not a singleton and thus new instances do retain values set by other instances. This behavior
	is achieved by overriding the self._get_option_var func. Reference OptionVars() class for an example.
	"""
	_names_to_skip = ['reset', 'inspect', 'save_to_file', 'load_from_file']
	_option_var_names = []
	_option_var_params = {}
	_option_var_defaults = {}
	_option_var_docs = {}
	
	def __new__(cls):
		cls._option_var_names = list(filter(lambda a: not a.startswith('_') and a not in cls._names_to_skip, dir(cls)))
		cls._option_var_params = {name: getattr(cls, name, None) for name in cls._option_var_names}
		
		for option_var_name in cls._option_var_names:
			parameters = cls._option_var_params[option_var_name]
			if not isinstance(parameters, dict):
				continue
			
			# Handle names
			if 'name' in parameters:
				name = parameters['name']
			else:
				name = option_var_name
			
			if not 'default_value' in parameters:
				raise KeyError("A default value is required for OptionVar {0}.{1}".format(cls.__name__, name))
			
			# Handle default value
			default_value = parameters['default_value']
			cls._option_var_defaults[name] = default_value
			
			# Handle docstrings
			if 'docstring' in parameters:
				doc_string = parameters['docstring']
			else:
				doc_string = 'None'
			cls._option_var_docs[name] = doc_string
			
			# Perform overrides
			prop = cls._get_option_var(name, default_value, doc_string)
			setattr(cls, name, prop)
		option_var = super(OptionVarsHelper, cls).__new__(cls)
		
		# Add to registry
		OptionVarsHelperRegistry().register_mca_option_var(option_var)
		return option_var
	
	@classmethod
	def _get_option_var(cls, name, default_value, doc_string):
		"""
		Method to override; create the representation of the option var here

		Example:
			Maya option var override will reference the option_var_wrapper here.
			Standalone python instance will reference nothing other than creating a dictionary.
		:param str name: name of the option var
		:param any default_value: default value of the option var
		:param str doc_string: docstring associated with the option var
		:return: default value
		:rtype: any
		"""
		return default_value
	
	def __init__(self):
		super(OptionVarsHelper, self).__init__()
	
	def reset(self, name=''):
		"""
		Reset options vars to default state.
		:param str name: name of optionvar to reset to default value
		:return: If Success, Returns True.
		:rtype: bool
		"""
		for option_var_name in self._option_var_names:
			if name and option_var_name != name:
				continue
			default_value = self._option_var_defaults[option_var_name]
			setattr(self, option_var_name, default_value)
		return True
	
	def inspect(self):
		"""
		Prints options and all their values, names, docstring
		"""
		logger.debug('Printing option vars for: {0}'.format(self.__class__.__name__))
		for option_var_name in self._option_var_names:
			attr = getattr(self, option_var_name, 'NO VALUE')
			logger.debug('\t{0} | {1} | {2}'.format(option_var_name, attr,
													self._option_var_docs.get(option_var_name, 'No docstring defined')))
	
	def save_to_file(self, path):
		"""
		Save option vars tracked by this class into a JSON file.

		:param str path : Full path to the JSON file
		"""
		json_data = {}
		
		for option_var_name in self._option_var_names:
			json_data[option_var_name] = getattr(self, option_var_name, 'NO VALUE')
		
		jsonio.write_to_json_file(json_data, path)
	
	def load_from_file(self, path, filter_option_vars=None):
		"""
		Load a file containing option var settings into option vars that are tracked by this
		class. Skip option var settings that aren't tracked by this class.

		:param str path : Full path to the JSON file
		:param str or list[str] filter_option_vars: Only allow loading values to the listed option vars
		"""
		
		if filter_option_vars:
			filter_option_vars = set(filter_option_vars) if isinstance(filter_option_vars, list) else set([filter_option_vars])
		
		json_data = jsonio.read_json_file(path)
		
		option_var_name_set = set(self._option_var_names)
		for option_var_name, option_var_value in json_data.iteritems():
			if (option_var_name in option_var_name_set and
					(not filter_option_vars or option_var_name in filter_option_vars)):
				setattr(self, option_var_name, option_var_value)


def option_var_wrapper(variable_name, default_value, docstring=''):
	"""
	Generates a python property object that automatically updates pm.optionVar (mya internal option var storage)

	:param variable_name: name of the key to store
	:param default_value: value of the var to store if not already set
	:param docstring: docstring for the property to hold for dir/help/etc.
	:return: returns the property for the optionvar
	:rtype: property
	"""
	doc = docstring
	
	def fget(self):
		if variable_name in pm.optionVar.keys():
			# Finds the optionVar and returns the value
			result = pm.optionVar[variable_name]
		else:
			# If it doesn't find the name in the optionVar, set name to the default value.
			pm.optionVar[variable_name] = default_value
			result = default_value
		return result
	
	def fset(self, value):
		if variable_name in pm.optionVar.keys():
			pm.optionVar[variable_name] = value
		else:
			# make sure the default value is set to something in case value fails
			pm.optionVar[variable_name] = default_value
			pm.optionVar[variable_name] = value
	
	return property(fget=fget, fset=fset, doc=doc)


class MCAOptionVars(OptionVarsHelper):
	@classmethod
	def _get_option_var(cls, name, default_value, doc_string):
		"""
		Override: generate a option_var_wrapper object and return for DCCOptionVarRegistry tracking
		:param str name: name of the option var
		:param any default_value: default value of the option var
		:param str doc_string: docstring associated with the option var
		:return: returns the property for the optionvar
		:rtype: property
		"""
		return option_var_wrapper(name, default_value, docstring=doc_string)


"""
Example of how to use:
Have a separate class that will manage your optionvars.

class RiggingOptions(OptionVars):
	### Example OptionVars setup ###

	# String - OptionVar Name
	ContentPath      = {'default_value': 'base_head_name', 'docstring': 'Name of the base Character'}
	# Bool
	TurnOnSymmetry   = {'default_value': True, 'docstring': 'Set the Symmetry selection.'}
	# Int\Float
	UISettingsTab    = {'default_value': 2.358, 'docstring': 'Asset ID used to create the rig.'}
"""