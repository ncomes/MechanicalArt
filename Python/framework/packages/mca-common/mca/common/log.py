#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca logger
"""

# mca python imports
import os
import sys
import logging
# software specific imports
# MCA python imports

MCA_LOGGER_NAME = 'MCA'
JSON_FORMCATER = "%(asctime) %(name) %(processName) %(pathname)  %(funcName) " \
                 "%(levelname) %(lineno) %(" "module) %(threadName) %(message)"
ROTATE_FORMCATER = "%(asctime)s: [%(process)d - %(name)s] %(levelname)s: %(message)s"
SHELL_FORMCATER = "[%(name)s - Module: %(module)s - Function: %(funcName)s] %(levelname)s: %(message)s"
DETAIL_FORMCATER = "[%(name)s - Path: %(pathname)s - Function: %(funcName)s]\n%(levelname)s: %(message)s\n"
GUI_FORMCATER = "[%(name)s]: %(message)s"
CRIT_FORMCATER = "[%(name)s - Path: %(pathname)s - Line: %(lineno)s Function: %(funcName)s]\n%(levelname)s: %(message)s\n"


def add_metaclass(metaclass):
    """
    Decorators that allows to create a class using a metaclass
    https://github.com/benjaminp/six/blob/master/six.py
    """

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        if hasattr(cls, '__qualname__'):
            orig_vars['__qualname__'] = cls.__qualname__
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


class Singleton(type):
    """
    Singleton decorator as metaclass. Should be used in conjunction with add_metaclass function of this module

    @add_metaclass(Singleton)
    class MyClass(BaseClass, object):
    """

    def __new__(meta, name, bases, clsdict):
        if any(isinstance(cls, meta) for cls in bases):
            raise TypeError('Cannot inherit from singleton class')
        clsdict['_instance'] = None
        return super(Singleton, meta).__new__(meta, name, bases, clsdict)

    def __call__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


def get_logger(name=None, formatter=None, file_path=None):
    """
    Returns the logger with name.

    :param str name: logger name.
    :return: logger found.
    :rtype: logging.Logger
    """

    name = name or MCA_LOGGER_NAME
    logger = logging.getLogger(name)
    LogsManager(logger=logger, formatter=formatter, file_path=file_path)

    return logger


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMCAS = {
            logging.DEBUG: SHELL_FORMCATER,
            logging.INFO: SHELL_FORMCATER,
            logging.WARNING: DETAIL_FORMCATER,
            logging.ERROR: CRIT_FORMCATER,
            logging.CRITICAL: CRIT_FORMCATER
        }

    def format(self, record):
        log_fmt = self.FORMCAS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


@add_metaclass(Singleton)
class LogsManager:
    def __init__(self, logger, formatter=None, file_path=None):
        self.logger = self.set_logger(logger)
        self.formatter = SHELL_FORMCATER
        if formatter:
            self.formatter = formatter
        self.file_path = file_path

        self._logs = dict()
        self.add_log()

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def set_logger(self, logger):
        if isinstance(logger, logging.Logger):
            self.logger = logger
        elif isinstance(logger, str):
            self.logger = logging.getLogger(logger)
        else:
            raise TypeError('Must add a logger or a string name of a logger!')
        return logger

    def set_handler(self):
        # MCA_LOGGER.propagate = False
        # handlers = self.logger.handlers
        # if not handlers:
        logging_handler = logging.StreamHandler(stream=sys.stdout)
        if self.file_path:
            logging_handler = logging.FileHandler(self.file_path)
        logging_handler.setFormatter(CustomFormatter(self.formatter))
        self.logger.addHandler(logging_handler)

    def add_log(self):
        """
        Adds a new logger to the manager.

        :param logging.Logger logger: Python logger instance.
        """

        if self.logger.name not in self._logs:
            self._logs[self.logger.name] = self.logger
        log_level = os.getenv('MCA_LOGGING_LEVEL', None)
        if log_level:
            self.logger.setLevel(log_level)
        else:
            self.logger.setLevel(logging.INFO)


MCA_LOGGER = get_logger(MCA_LOGGER_NAME)

# Make sure that child logger does not propagate its message to the root logger.
MCA_LOGGER.propagate = False
# This helps make sure we do not get duplicate logging
handlers = MCA_LOGGER.handlers
if not handlers:
    LogsManager(MCA_LOGGER).set_handler()
