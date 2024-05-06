#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that sets up the environment variables for MAT
"""

# mca python imports
import os
import sys

# software specific imports
# mca python imports


def add_unreal_system_paths(path_list):
	if not isinstance(path_list, (list, tuple)):
		path_list = [path_list]
		
	for path in path_list:
		if os.path.isdir(path) and os.path.normpath(path) not in sys.path:
			sys.path.append(path)
