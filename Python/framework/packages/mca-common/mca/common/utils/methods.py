#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Saving preferences for the toolbox
"""

# mca python imports
import inspect

# software specific imports

# mca python imports


def get_properties(cls_inst, filter_out=None):
	"""
	Returns a list of properties for a class.  This automatically filters out properties with '__'.
	
	:param class instance cls_inst: Instance of a class
	:param list[str] filter_out: a list of properties to filter out
	:return: Returns a list of properties for a class
	:rtype: list[str]
	"""
	
	property_list = []
	
	all_properties = inspect.getmembers(cls_inst)
	for i in all_properties:
		# to remove private and protected
		# functions
		if not i[0].startswith('_'):
			# To remove other methods that
			# does not start with a underscore
			if not inspect.ismethod(i[1]):
				if filter_out:
					filtered = [x for x in filter_out if x in i]
					if not filtered:
						property_list.append(i)
	return property_list

