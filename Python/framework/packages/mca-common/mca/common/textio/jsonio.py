"""
Module that contains utility methods related to write/read JSON files
"""

# System global imports
from __future__ import print_function, division, absolute_import
import os
import json
# mca python imports
from mca.common.utils import fileio
# mca logger
from mca.common import log
logger = log.MCA_LOGGER


def read_json(file_path):
    """
    Read data from a given JSON and return it.

    :param str file_path: The absolute file path to a given json file.
    """
    if not os.path.isfile(file_path):
        raise IOError(f'{file_path} does not exist.')

    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except:
            print('JSON load failed.')
            return None


def write_json(file_path, json_data):
    """
    Write data to a json file.

    :param str file_path:
    :param list|dict json_data: A list or dictionary
    """
    json_str = json.dumps(json_data, indent=4)
    fileio.touch_path(file_path)

    with open(file_path, 'w') as f:
        f.write(json_str)