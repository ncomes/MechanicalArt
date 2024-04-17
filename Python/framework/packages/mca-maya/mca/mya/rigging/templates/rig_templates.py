#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
import os.path
import time
import logging
import tempfile
from datetime import datetime
# mca python imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.common.paths import paths

from mca.mya.rigging import rig_utils

logger = log.MCA_LOGGER


class RigTemplates(object):

    VERSION = 1
    ASSET_ID = ''
    ASSET_TYPE = ''
    LOG_NAME = 'TEK.build.{}'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE, debug=False, log_directory=None):
        self._asset_id = asset_id
        self._asset_type = asset_type
        self._debug = debug
        self._errors = list()
        self._start_time = 0
        self._end_time = 0
        self._elapsed_time = 0
        self._log, self._file_handler = self._setup_file_logger(log_directory)

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    @property
    def asset_id(self):
        return self._asset_id

    @asset_id.setter
    def asset_id(self, value):
        self._asset_id = value

    @property
    def asset_type(self):
        return self._asset_type

    @asset_type.setter
    def asset_type(self, value):
        self._asset_type = value

    @property
    def log(self):
        return self._log

    # =================================================================================================================
    # ABSTRACT METHODS
    # =================================================================================================================

    def build(self):
        """
        Main build function for the rig template.
        """

        pass

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def rig(self, asset_id=None):
        """
        Main function that handles the rig building process.
        This function is abstract, so it must be overridden by child classes.
        """
        if asset_id:
            self.ASSET_ID = asset_id

        self._setup_file_logger()

        self._start_time = time.time()
        start_msg = self._get_start_build_log_message()
        #self._log.info(start_msg)

        tek_rig = self.build()
        if tek_rig:
            rig_utils.setup_twist_components(tek_rig)

        pm.select(clear=True)
        self._end_time = time.time()
        self._elapsed_time = self._end_time - self._start_time
        #finish_log_msg = self._get_finish_build_log_message()
        error_count = len(self._errors)
        log_level = logging.WARNING if error_count else logging.INFO
        #finish_log_msg = logger.warning(finish_log_msg) if error_count else logger.info(finish_log_msg)
        #self._log.log(log_level, finish_log_msg, extra=dict(duration=self._elapsed_time))
        #self._close_file_logger()

    def update(self):
        current_version = self.get_version()
        latest_version = self.VERSION
        while current_version < latest_version:
            update_method_name = "_update_version_{0}_to_version_{1}".format(current_version, current_version + 1)
            update_method = getattr(self, update_method_name)
            update_method()
            later_version = self.get_version()
            print("#updated {0} to version {1}".format(str(self), later_version))
            if later_version == current_version:
                raise AttributeError(
                    "Forgot to set the version in your update script: {0}".format(update_method))
            current_version = later_version

    def get_version(self):
        """
        Returns the current rig template version.

        :return: rig template version.
        :rtype: int
        """

        return self.VERSION

    def get_source_directory(self):
        raise NotImplementedError

    def get_flags_path(self):
        """
        Return the path where the rig asset flags are located.

        :return: absolute directory path for the rig asset flags.
        :rtype: str
        """

        project_path = paths.get_asset_rig_path(self._asset_id)
        if project_path:
            return os.path.join(project_path, 'Flags')


    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _setup_file_logger(self, log_directory=None):
        """
        Internal function that creates sequencer builder logger.

        :param str log_directory: optional directory where log file will be generated.
        """
        return None, None

        build_log = logging.getLogger(self.LOG_NAME.format(self.asset_id))
        build_log.setLevel(logging.DEBUG if self._debug else logging.INFO)

        if not log_directory or not os.path.exists(log_directory):
            asset_rig_path = paths.get_asset_rig_path(self.asset_id)
            if not asset_rig_path:
                logger.warning('Was not possible to retrieve asset rig path for asset: "{}"'.format(self.asset_id))
                log_directory = None
            else:
                log_directory = os.path.join(asset_rig_path, '__log__')
                if not os.path.exists(log_directory):
                    os.makedirs(log_directory)
        log_directory = log_directory or tempfile.gettempdir()
        logger.info('Setting up builder log: {}'.format(log_directory))

        date_str = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        log_file_name = 'tek_build_{}_{}.log'.format(self.asset_id.lower(), date_str)
        log_file = os.path.join(log_directory, log_file_name)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
        file_handler.setFormatter(log_formatter)

        build_log.handlers = [file_handler]

        return build_log, file_handler

    def _close_file_logger(self):
        """
        Internal function that closes log build file logger.
        """

        self._file_handler.close()

    def _get_start_build_log_message(self):
        """
        Internal function that returns the message that should be logged before starting the building.

        :return: start log message.
        :rtype; str
        """

        return 'Started building rig: {} (debug={})'.format(self.ASSET_ID, self._debug)

    def _get_finish_build_log_message(self):
        """
        Internal function that returns the message that should be logged when the building process finishes.

        :return: end log message.
        :rtype: str
        """

        return 'Built Rig "{0}", {1:.3f} seconds, {2} error(s)'.format(
            self.ASSET_ID, self._elapsed_time, len(self._errors))
