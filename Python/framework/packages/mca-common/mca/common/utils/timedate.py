#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains utility functions related with time and date
"""

# mca python imports
import time
from datetime import datetime
import pytz
# software specific imports
# mca python imports


def get_current_time(date_and_time=True, reverse_date=False):
	"""
	Returns current time.

	:param bool date_and_time: whether to return only the time or time and data.
	:param bool reverse_date: whether to return date with {year}-{month}-{day} format or {day}-{month}-{year} format.
	:return: current time as a string.
	:rtype: str
	"""
	
	mtime = time.time()
	date_value = datetime.fromtimestamp(mtime)
	hour = str(date_value.hour)
	minute = str(date_value.minute)
	second = str(int(date_value.second))
	
	if len(hour) == 1:
		hour = '0' + hour
	if len(minute) == 1:
		minute = '0' + minute
	if len(second) == 1:
		second += '0'
	
	time_value = '{}:{}:{}'.format(hour, minute, second)
	
	if not date_and_time:
		return time_value
	else:
		year = date_value.year
		month = date_value.month
		day = date_value.day
		
		if reverse_date:
			return '{}-{}-{} {}'.format(year, month, day, time_value)
		else:
			return '{}-{}-{} {}'.format(day, month, year, time_value)


def get_current_date(reverse_date=False, separator=None):
	"""
	Returns current date.

	:param bool reverse_date: whether to return date with {year}-{month}-{day} format or {day}-{month}-{year} format.
	:param str separator: character used to separate the different parts of the date
	:return: current date as a string.
	:rtype: str
	"""
	
	separator = separator or '-'
	mtime = time.time()
	date_value = datetime.fromtimestamp(mtime)
	year = date_value.year
	month = date_value.month
	day = date_value.day
	
	if reverse_date:
		return '{1}{0}{2}{0}{3}'.format(separator, year, month, day)
	else:
		return '{1}{0}{2}{0}{3}'.format(separator, day, month, year)


def get_date_and_time(reverse_date=False, separator=None):
	"""
	Returns current date and time.

	:param bool reverse_date: whether to return date with {year}-{month}-{day} format or {day}-{month}-{year} format.
	:param str separator: character used to separate the different parts of the date
	:return: current date and time as a string.
	:rtype: str
	"""
	
	separator = separator or '-'
	date_value = datetime.now()
	year = date_value.year
	month = date_value.month
	day = date_value.day
	hour = str(date_value.hour)
	minute = str(date_value.minute)
	second = str(int(date_value.second))
	
	if len(hour) == 1:
		hour = '0' + hour
	if len(minute) == 1:
		minute = '0' + minute
	if len(second) == 1:
		second = second + '0'
	
	if reverse_date:
		return '{1}{0}{2}{0}{3} {4}:{5}:{6}'.format(separator, year, month, day, hour, minute, second)
	else:
		return '{1}{0}{2}{0}{3} {4}:{5}:{6}'.format(separator, day, month, year, hour, minute, second)


def get_current_pst_time():
	"""
	Returns the current time in Pacific Standard time

	:return:Returns the current time in Pacific Standard time
	:rtype: str
	"""
	
	pst_time = datetime.now().astimezone(pytz.timezone('America/Los_Angeles')).strftime('%H:%M:%S')
	return pst_time


def get_time_zone():
	"""
	Returns the time zone from the users computer.

	:return: Returns the time zone from the users computer.
	:rtype: str
	"""
	
	time_zone = time.tzname or None
	if not time:
		return
	return time_zone[0]

