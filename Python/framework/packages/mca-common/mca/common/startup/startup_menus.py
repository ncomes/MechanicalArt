#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
These are the Common menus that get loaded into the dcc software.
"""

# mca python imports
import subprocess
import webbrowser

# software specific imports

# mca python imports
from mca.common.textio import packages
from mca.common.project import project_paths

PACKAGE_MANAGER = packages.ProjectPackageManager()


def project_url_menu():
	"""
	Opens the Confluence page for dcc tools.
	"""
	
	webbrowser.open(PACKAGE_MANAGER.project_url)


def animation_url_menu():
	"""
	Opens the Confluence page for dcc tools.
	"""
	
	webbrowser.open(PACKAGE_MANAGER.animation_url)


def modeling_url_menu():
	"""
	Opens the Confluence page for dcc tools.
	"""
	
	webbrowser.open(PACKAGE_MANAGER.modeling_url)


def rigging_url_menu():
	"""
	Opens the Confluence page for dcc tools.
	"""
	
	webbrowser.open(PACKAGE_MANAGER.rigging_url)


def jira_url_menu():
	"""
	Opens the Confluence page for dcc tools.
	"""
	
	webbrowser.open(PACKAGE_MANAGER.jira_url)


def dcc_setup_url_menu():
	"""
	Opens the Confluence page for dcc tools.
	"""
	
	webbrowser.open(PACKAGE_MANAGER.dcc_setup_url)


def open_plastic_folder():
	"""
	Opens an explorer window to the project
	"""
	
	plastic_path = project_paths.get_plastic_content_path(create_env=False)[0]
	subprocess.Popen(r'explorer ' + plastic_path)

