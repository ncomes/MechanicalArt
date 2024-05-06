"""
Initialization module for mca-package
"""


# mca python imports
import os
import sys
# software specific imports

# mca python imports

from mca.common.startup.configs import common_env, consts, config
from mca.common.textio import packages
from mca.common.paths import project_paths, path_utils
from mca.common.pyqt.qt_utils import windows

PACKAGE_LOADED = False
CONFIG_FILE = None

from mca.common import log
logger = log.MCA_LOGGER


def startup_init(dcc, config_file=None, skip_dialog=False, hide_envs=True):
    """
    Initializes MCA Packages.
    
    :param str config_file: full path to the config file that will be loaded for a specific software.
    :param str dcc: Name of the specific software being loaded.
    :param bool skip_dialog: if true, the info will not be displayed in the console.
    :param bool hide_envs: if true, the info will not be displayed in the console.
    """
    
    global PACKAGE_LOADED
    global CONFIG_FILE
    
    if PACKAGE_LOADED:
        if not skip_dialog:
            logger.info(f'Project is already registered')
            return
    
    # Set up common and project environment variables
    if not skip_dialog:
        logger.info('Creating MCA Python Common framework environment ...')
        print('\n' + '=' * 118 + '\n')
        print("""\
        
 __      __  ____    ___     ____  							      _____                                            _
|  \    /  |/ ___|  / _ \   |  _ \ __   __ _   _      ___  __  _ |  ___| __ __ _ _ __ ___   _____      _____  _ __| | __
| \ \  / / | |     / /_\ \  | |_) |\ \ / /| | | |___ / _ \|  \| || |_ | '__/ _` | '_ ` _ \ / _ \ \ /\ / / _ \| '__| |/ /
| |\ \/ /| | |___ / /___\ \ |  __/  \ V /|_ _|| |_  | (_) | | \ ||  _|| | | (_| | | | | | |  __/\ V  V / (_) | |  |   <
|_| \__/ |_|\____/_/     \_\|_|      |_|  |_| |_| |_|\___/|_|\__||_|  |_|  \__,_|_| |_| |_|\___| \_/\_/ \___/|_|  |_|\_\
        """)
        print('\n' + '=' * 118 + '\n')
    if not skip_dialog:
        logger.info(f'Registering Environment Variables...')
    common_env.create_path_envs()
    if not project_paths.get_mca_root_path():
        logger.warning(f'\tProject Root Path was not set.  Cannot continue!')
        return

    common_env.create_project_envs(skip_dialog=hide_envs)
    if not skip_dialog:
        logger.info(f'\tProject Environment Variables have been registered')
    common_env.create_tools_envs(skip_dialog=hide_envs)
    if not skip_dialog:
        logger.info(f'\tTools Environment Variables have been registered')
    common_env.create_common_envs(skip_dialog=hide_envs)
    if not skip_dialog:
        logger.info(f'\tCommon Depot Environment Variables have been registered')
    
    deps_path = os.getenv(consts.MCA_DEPEND_PATH, None)
    
    if deps_path and os.path.isdir(deps_path):
        if not deps_path in sys.path:
            sys.path.insert(0, deps_path)
        if not skip_dialog:
            logger.info(f'Dependencies Path registered: {path_utils.to_relative_path(deps_path)}')
    else:
        if not skip_dialog:
            logger.info(f'Dependencies Path was NOT registered: {path_utils.to_relative_path(deps_path)}\n'
                        f'Could not Find the Dependencies path!')
    
    # import here to make sure that bootstrapping vendor paths are already included within sys.path
    
    root_path = os.getenv('MCA_FRAMEWORK_ROOT', None)
    if not skip_dialog:
        logger.info(f'\tRoot Path registered: {path_utils.to_relative_path(root_path)}')
    
    # Set the sys paths
    if not config_file:
        config_file = project_paths.get_package_python_config_path()
    config.create_sys_packages(config_file, dcc=dcc)
    
    CONFIG_FILE = config_file

    if not skip_dialog:
        logger.info(f'Common Depot setup was successful...')
        logger.info('\n' + '=' * 118 + '\n')
    
    config.reload_modules()
    run_packages_startups(config_file, dcc=dcc)
    
    PACKAGE_LOADED = True


def shutdown(dcc, config_file=None, skip_dialog=False):
    """
    Shuts down and unregisters the loaded MAT Packages
    
    :param str config_file: full path to the config file that will be loaded for a specific software.
    :param str dcc: specific software.
    :param bool skip_dialog: If True, nothing will be written to the console.
    """
    
    if not config_file:
        config_file = CONFIG_FILE
    
    # Close all Windows
    windows.close_all_mca_windows()
    run_packages_startups(config_file=config_file, dcc=dcc, do_shutdown=True)
    
    # Remove all of the paths in the sys.path
    config.remove_sys_packages(config_file=config_file, dcc=dcc, skip_dialog=skip_dialog)
    if not skip_dialog:
        logger.info('Shutting down MCA Common framework environment')
    # Remove all of the environment variables
    common_env.remove_all_mca_envs()
    # Reloads the sys.path
    config.reload_modules()
    
    if not skip_dialog:
        logger.info('Common framework environment shutdown successfully')
        logger.info('\n' + '=' * 160 + '\n')
    
    global PACKAGE_LOADED
    PACKAGE_LOADED = False


def run_packages_startups(config_file=None, dcc='maya', do_shutdown=False, skip_dialog=False):
    """
    Runs any startup/shutdown scripts in the other startup depots
    
    :param str config_file: full path to the config file that will be loaded for a specific software.
    :param str dcc: specific software.
    :param bool do_shutdown: If True, will run the shutdown instead of the startups.
    :param bool skip_dialog: If True, nothing will be written to the console.
    """

    dir_path, load = config.get_config_packages(dcc=dcc, config_file=config_file, skip_dialog=True)

    if not dir_path:
        if not skip_dialog:
            logger.info('No other packages were loaded.  Cannot find the startup functions.')
            return
    for x, path in enumerate(dir_path):
        depot_name = load[x]
        if not depot_name or depot_name == 'common':
            continue

        mod = 'startup_init'
        if do_shutdown:
            mod = 'shutdown'

        string_command = f'from mca.{depot_name}.startup import startup as stup; stup.{mod}()'
        exec(string_command)


def init(dcc, config_file=None, skip_dialog=False, hide_envs=True):
    """
    This is a temporary fix.  We will need to change all the call to the startup init.
    # ToDo @comes Change all the call to the startup init.

    :param str config_file: full path to the config file that will be loaded for a specific software.
    :param str dcc: Name of the specific software being loaded.
    :param bool skip_dialog: if true, the info will not be displayed in the console.
    :param bool hide_envs: if true, the info will not be displayed in the console.
    """
    
    startup_init(dcc, config_file=config_file, skip_dialog=skip_dialog, hide_envs=hide_envs)

    
# Todo: ncomes - Get the log generater up and working.  This is a start below.

# def create_logger():
# 	"""
# 	Creates tool logger.
#
# 	:return: tool logger
# 	:rtype: logging.logger
# 	"""
#
# 	logger_directory = os.path.normpath(os.path.join(os.path.expanduser('~'), 'mca', 'logs'))
# 	if not os.path.isdir(logger_directory):
# 		os.makedirs(logger_directory)
#
# 	logging_config = os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))
#
# 	logging.config.fileConfig(logging_config, disable_existing_loggers=True)
# 	logger = logging.getLogger('mca-bootstrap')
# 	dev = bool(strtobool(os.getenv('# mca python importsDEV', 'False')))
# 	if dev:
# 		logger.setLevel(logging.DEBUG)
# 		for handler in logger.handlers:
# 			handler.setLevel(logging.DEBUG)
#
# 	return logger
#
#
# # force logger creation during module import
# logger = create_logger()
