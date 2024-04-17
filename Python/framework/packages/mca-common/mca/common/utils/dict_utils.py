#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains utility functions related to dictionaries
"""

# mca python imports

# software specific imports

# mca python imports


def get_dict_slice(starting_dict, index, default_value=None):
    """
    For each value list in a dictionary return the index value with the corresponding key.

    :param dict starting_dict: A dictionary of keys with list values.
    :param int index: The slice value to return from each list.
    :param Any default_value: If the length of the value isn't long enough, return a default value.
    :return: The modified dictionary of sliced values.
    :rtype: dict
    """
    return_dict = {}
    for key, values in starting_dict.items():
        return_dict[key] = values[index] if len(values) >= index+1 else default_value

    return return_dict