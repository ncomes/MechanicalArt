#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interacting with Google Sheets
"""

# mca python imports
from __future__ import print_function, division, absolute_import
import os
from datetime import datetime
import inspect
import platform

# software specific imports

# mca python imports
from mca import common
from mca.common.paths import paths
from mca.common.utils import pyutils, dcc_util, timedate, process
from mca.common.textio import yamlio
from mca.common.tools.dcctracking import dcc_user_data
from mca.common.googlesheets import google_sheets
from mca.common.pyqt.qt_utils import checkbox_utils
from mca.common import log

logger = log.MCA_LOGGER

DCC_TRACKING_SPREADSHEET_ID = '1Rr7OdoxlxOEgraF8Ee4d0HvslufZIKvdh6oQ0KyoQ3o'  # Deprecated
DCC_TRACKING_SOFTWARE_ID = '1BLHgKD0wElRZTII7uWb0mQWbSfU3ztV_WqcyTru2yCQ'  # Deprecated
DCC_DATA_SHEET_ID = '1hFunLlvj2j4wxKYzE-gvE8d_XLHbBVJxKMXru1qg6Wc'


def ddc_tool_entry(fn, **kwargs):
    '''
    Adds data about a function that is being loaded in a DCC app.

    :param callable fn: a function that is being loaded in a DCC app.
    '''
    return
    username = os.getlogin() or None
    if not username:
        logger.warning('No Username was found.  Cannot post data to Google Sheets.')
        return

    # Generate a unique has that is consistant.  This way we can always have a unique number per user.
    hash_name = common.generate_unique_tracking_name()
    # Grab the user data from the yaml file.  Ex: full name, team, title, etc...
    user_dict = get_user_info(hash_name)

    # Local Username is the PC username.   Ex: C:\Users\USERNAME
    local_username = username
    if user_dict['mat_username']:
        username = user_dict['mat_username']

    # Check the lists to see if the user is included to move forward.
    ignore_users = dcc_user_data.DCCTrackingIgnoreUsers.load()
    if username in ignore_users.usernames:
        return

    # Starting with checks to make sure we can communicate with Google.  If not, lets bale so the user
    # Does not get errors
    service_account_file = None
    try:
        service_account_file = os.path.join(paths.get_common_path(), 'Google Sheets', 'dcc-gs_key.json')
    except Exception as e:
        logger.error('Cannot communicate with Google Sheets.  Skipping.')
        logger.error(f'{e}')
        return

    ggs = None
    try:
        ggs = google_sheets.GoogleSheets(DCC_DATA_SHEET_ID, service_account_file)
    except Exception as e:
        logger.error('Cannot communicate with Google Sheets.  Skipping.')
        logger.error(f'{e}')
        return

    # Start collecting and formatting the data
    # From Keywords
    fn_name = kwargs.get('fn_name', None)
    data_entry = kwargs.get('data_entry', None)
    extra_entry = kwargs.get('extra_entry', None)
    ui_type = kwargs.get('ui_type', 'default')
    notes = kwargs.get('notes', None)
    asset_id = kwargs.get('asset_id', None)
    checkboxes = kwargs.get('checkboxes', None)
    radio_buttons = kwargs.get('radio_buttons', None)
    comboboxes = kwargs.get('comboboxes', None)
    if checkboxes:
        if not isinstance(checkboxes, (tuple, list)):
            checkboxes = [checkboxes]
        checkboxes = checkbox_utils.get_checkbox_text(checkboxes)
        if not checkboxes:
            checkboxes = None
        else:
            if len(checkboxes) == 1:
                checkboxes = checkboxes[0]
            else:
                checkboxes = ','.join(checkboxes)
        
    # DCC Software and version
    dcc_software = f'{dcc_util.application()}' or None
    dcc_software_version = f'{dcc_util.application_version()}' or None
    # path of the function
    module_name = fn.__module__
    # The tab name uses the month and year.  Ex: 07/2023
    tab_name = user_dict['year_month']

    if not inspect.isclass(fn):
        if not fn_name:
            fn_name = fn.__name__
        class_list = fn.__qualname__.split('.')
        class_name = class_list[0]
    else:
        class_name = fn.__name__

    input_values = [fn_name,
                    class_name,
                    ui_type,
                    asset_id,
                    username,
                    user_dict['full_name'],
                    dcc_software,
                    dcc_software_version,
                    user_dict['team'],
                    user_dict['email'],
                    user_dict['month'],
                    user_dict['day'],
                    user_dict['year'],
                    user_dict['pst'],
                    user_dict['time_zone'],
                    user_dict['local_time'],
                    user_dict['title'],
                    user_dict['location'],
                    user_dict['country'],
                    checkboxes,
                    data_entry,
                    extra_entry,
                    notes,
                    local_username,
                    module_name,
                    hash_name,
                    radio_buttons,
                    comboboxes]

    worksheet_created = ggs.create_non_existing_worksheet(tab_name, frozen_rows=1)
    if worksheet_created:
        a1_values = ['Function',
                     'Class',
                     'UI Type',
                     'Asset ID',
                     'Username',
                     'Full Name',
                     'Software',
                     'Software Version',
                     'Team',
                     'MAT Email',
                     'Month',
                     'Day',
                     'Year',
                     'PST Time',
                     'Time Zone',
                     'Local Time',
                     'Title',
                     'Location',
                     'Country',
                     'Checkboxes',
                     'data_entry',
                     'Extra Entry',
                     'Notes',
                     'Local Username',
                     'Modules',
                     'Hash',
                     'Radio Buttons',
                     'Combo Boxes']
        ggs.append_to_cells(tab_name, start='A1', input_values=a1_values)

    try:
        ggs.append_to_cells(tab_name, start='A1', input_values=input_values)
    except Exception as e:
        logger.warning('Unable to post to Google Sheets')
        logger.warning(f'{e}')


# Todo ncomes:  This should be moved to a common place.
def ddc_tool_entry_thead(fn, **kwargs):
    """
    Runs the dcc tool in a thread.
    
    :param callable fn: a function that is being loaded in a DCC app.
    """

    #process.cpu_threading(ddc_tool_entry(fn, **kwargs))
    return


def get_user_info(username):
    '''
    Returns a dictionary of user data.

    :param str/int username: hashed number representing a user.
    :return: Returns a dictionary of user data.
    :rtype: dictionary
    '''

    raw_user_data = yamlio.read_yaml_file(dcc_user_data.DCC_TRACKING_DATA)
    all_user_data = common.DCCUsernameData(raw_user_data, username)
    user_dict = {}

    user_dict['full_name'] = pyutils.get_user_display_name() or None
    user_dict['pst'] = timedate.get_current_pst_time() or None
    user_dict['time_zone'] = timedate.get_time_zone() or 'NoTimeZone'
    user_dict['capture_date'] = datetime.now().strftime('%m/%d/%Y') or None
    user_dict['local_time'] = datetime.now().strftime('%H:%M:%S') or None
    user_dict['dcc_software'] = dcc_util.application() or None
    user_dict['year_month'] = datetime.now().strftime("%Y/%m") or None
    user_dict['month'] = datetime.now().strftime("%m") or None
    user_dict['day'] = datetime.now().strftime("%d") or None
    user_dict['year'] = datetime.now().strftime("%Y") or None
    user_dict['email'] = all_user_data.email
    user_dict['team'] = all_user_data.team
    user_dict['title'] = all_user_data.title
    user_dict['location'] = all_user_data.location
    user_dict['country'] = all_user_data.country
    user_dict['mat_username'] = all_user_data.mat_username
    if all_user_data.full_name:
        user_dict['full_name'] = all_user_data.full_name

    return user_dict

