#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import string
import random
import re

# software specific imports

# mca python imports
from mca.common import log


logger = log.MCA_LOGGER


def generate_random_string(length=5, alpha_only=False, alpha_safe=True):
    """
    Returns a string of random alphanumeric characters.

    :param in length: The length of the string to be generated.
    :param bool alpha_only: If only letters should be used.
    :param bool alpha_safe: If the string should be mya valid name.
    :return: The newly generated string.
    :rtype: str
    """

    if not length or not isinstance(length, int):
        logger.warning(f'{length}, must be a non zero int.')
        return
    choice_string = string.ascii_lowercase if alpha_only else string.ascii_lowercase + string.digits
    return_string = ''
    for index in range(length):
        if not index and alpha_safe:
            return_string += random.choice(string.ascii_lowercase)
        else:
            return_string += random.choice(choice_string)
    return return_string


def generate_guid():
    """
    Generate a unique alphanumeric string seperated by dashes. In orders of 4, 5, 5, 4 characters.
    We'll use this to assign unique entries for every asset in our asset list.

    :return: A unique identifier string.
    :rtype: str
    """

    return '-'.join([generate_random_string(n, alpha_safe=False) for n in [4, 5, 5, 4]])


def clean_file_string(string_to_clean):
    """
    Replaces all / and \\ characters by _.

    :param str string_to_clean: string to clean.
    :return: cleaned string.
    :rtype: str
    """

    if string_to_clean == '/':
        return '_'

    string_to_clean = string_to_clean.replace('\\', '_')

    return string_to_clean


def get_trailing_numbers(text):
    """
    Return any numeric characters at the end of a string.

    :param str text: String to check against
    :return: The value converted into an int if found ele None
    :rtype: int or None
    """

    if text and isinstance(text, str):
        m = re.search(r'\d+$', text)
        return int(m.group()) if m else None


def get_numbers_from_string(_string, as_string=False):
    """
    Extracts numbers from a string.

    :param _string: sting with numbers
    :param bool as_string: True returns as a string.  False returns as an int.
    :return: Returns a list of vertex numbers.
    :rtype: list(int) or list(str)
    """

    string_number = [i for i in _string if i.isdigit()]
    if not as_string:
        string_number = map(lambda x: int(x), string_number)
    return string_number


def append_extension(input_string, extension):
    """
    Adds the given extension at the end of the string if the input string does not already ends with that extension

    :param str input_string: string to append extension
    :param str extension: extension to append into the input string.
    :return: string with the extension appended.
    :rtype: str
    """

    if not extension.startswith('.'):
        extension = '.{}'.format(extension)
    if input_string.endswith('.'):
        input_string = input_string[:-1]
    if not input_string.endswith(extension):
        input_string = '{}{}'.format(input_string, extension)

    return input_string


def debug_object_string(obj, msg):
    """
    Returns a debug string depending on the type of the object.

    :param object obj: Python object.
    :param str  msg: message to log.
    :return: debug string
    :rtype: str
    """

    import inspect
    # debug a module
    if inspect.ismodule(obj):
        return '[%s module] :: %s' % (obj.__name__, msg)

    # debug a class
    elif inspect.isclass(obj):
        return '[%s.%s class] :: %s' % (obj.__module__, obj.__name__, msg)

    # debug an instance method
    elif inspect.ismethod(obj):
        return '[%s.%s.%s method] :: %s' % (obj.im_class.__module__, obj.im_class.__name__, obj.__name__, msg)

    # debug a function
    elif inspect.isfunction(obj):
        return '[%s.%s function] :: %s' % (obj.__module__, obj.__name__, msg)