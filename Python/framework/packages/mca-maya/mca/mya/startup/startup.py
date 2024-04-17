"""
Initializes all the  Packages needed to run the python codebase in Maya.
"""

# python imports
import os
# software specific imports
import pymel.core as pm
#  python imports
from mca.mya.startup import start_menus
from mca import mya as mca_maya
from mca.common import log
from mca.common.startup.configs import consts, config
from mca.common.pyqt.qt_utils import windows
from mca.common.paths import project_paths
from mca.mya.pyqt.utils import ma_main_window
from mca.common.tools.toolbox import toolbox_prefs, toolbox_data
from mca.mya.tools.toolbox import ma_toolbox_ui
from mca.mya.startup.configs import ma_envs, ma_configs, ma_consts
from mca.mya.utils import plugins
from mca.common.resources import resources


logger = log.MCA_LOGGER


def startup_init(skip_dialog=False):
    """
    Initializes  Packages.
    """

    if not skip_dialog:
        logger.info('Creating  Python Maya framework environment ...')
        print("""
         __      __  ____    ___      __      __
        |  \    /  |/ ___|  / _ \    |  \    /  | __ _ __   __ __ _
        | \ \  / / | |     / /_\ \   | \ \  / / |/ _` |\ \ / // _` |
        | |\ \/ /| | |___ / /___\ \  | |\ \/ /| | (_| | \ V /| (_| |
        |_| \__/ |_|\____/_/     \_\ |_| \__/ |_|\__,_|  |_|  \__,_|""")
        print('\n' + '=' * 118 + '\n')
    
    ma_envs.create_maya_envs()
    if not skip_dialog:
        logger.info('Maya Environment Variables Created...')

    resources.register_resources()
    logger.info('Registered Resources...')
    print('\n' + '=' * 118 + '\n')

    start_menus.create_menus()
    if not skip_dialog:
        logger.info('Maya Main Window Menus Created...')
        print('\n' + '=' * 118 + '\n')

    # make sure there are no old windows open
    maya_main_window = ma_main_window.get_maya_window()
    maya_main_window.setWindowIcon(resources.icon(r'company_logos\jkg.png'))
    windows.close_all_mca_docked_windows(maya_main_window)
    if not skip_dialog:
        logger.info('Double Checked to make sure all windows are closed...')

    studiolibrary_paths = os.getenv(ma_consts.STUDIOLIBRARY, None)
    if studiolibrary_paths:
        ma_configs.add_maya_system_paths(studiolibrary_paths)
        if not skip_dialog:
            logger.info('Maya Studio Library path added...')

    pose_wrangler_paths = os.getenv(ma_consts.POSE_WRANGLER, None)
    if pose_wrangler_paths:
        ma_configs.add_maya_system_paths(pose_wrangler_paths)
        load_plugins()
        if not skip_dialog:
            logger.info('Maya Epic Pose Wrangler path added...')

    third_party_paths = os.getenv(ma_consts.THRIDPARTY, None)
    if third_party_paths:
        ma_configs.add_maya_system_paths(third_party_paths)
        if not skip_dialog:
            logger.info('Maya Third Party Tools path added...')
    #
    # Maya Dependencies paths
    depend_paths = os.getenv(ma_consts.DEPS_ROOT, None)
    if depend_paths:
        ma_configs.add_maya_system_paths(depend_paths)
        if not skip_dialog:
            logger.info('Maya Dependencies paths added...')

    # Check to see if any Toolboxes need to be opened.
    TOOLBOX_P = toolbox_prefs.ToolBoxPreferences(dcc=consts.MAYA)
    all_on_start = TOOLBOX_P.get_all_on_startups()
    if all_on_start:
        for toolbox_name in all_on_start:
            toolbox_class = toolbox_data.ToolboxRegistry().TOOLBOX_NAME_DICT.get(toolbox_name)
            if toolbox_class:
                ma_toolbox_ui.MayaToolBox(toolbox_class)
                if not skip_dialog:
                    logger.info(f'Opened Toolbox: {toolbox_name}')

    # Set Project path
    pm.workspace(project_paths.MCA_PROJECT_ROOT, openWorkspace=True)

    # set default settings #################################
    new_prefs = ma_configs.MayaDefaultStartOptions.load()
    new_prefs.apply_maya_defaults()

    print('THIS IS DEPOT 1.0.0')
    print('\n' + '=' * 118 + '\n')


def shutdown(skip_dialog=False):
    """

    :param bool skip_dialog: If True, nothing will be written to the console.
    """

    start_menus.remove_menus()

    maya_main_window = ma_main_window.get_maya_window()
    windows.close_all_mca_docked_windows(maya_main_window)

    # Remove Maya's paths from sys.path
    depend_paths = os.getenv(ma_consts.DEPS_ROOT, None)
    maya_root_path = mca_maya.MAYA_TOP_ROOT
    if depend_paths:
        config.remove_sys_path([depend_paths, maya_root_path])

    if not skip_dialog:
        logger.info('Maya menus removed successfully')
        logger.info('Maya docked windows closed successfully')
        logger.info('Maya framework shutdown successfully')
        logger.info('\n' + '=' * 160 + '\n')


def init(skip_dialog=False):
    """
    This is a temporary fix.  We will need to change all the init calls to the startup init.
    So we can remove this function.
    # ToDo @comes Change all the init calls to the startup_init.

    :param bool skip_dialog: If True, will not print any dialogs
    """

    startup_init(skip_dialog=skip_dialog)


def load_plugins():
    pose_wrangler_paths = os.getenv(ma_consts.POSE_WRANGLER, None)
    version = pm.about(version=True)
    plugin_path = f'plug-ins\\windows\\{version}\\MayaUERBFPlugin.mll'
    if pose_wrangler_paths:
        path = os.path.join(os.path.dirname(os.getenv(ma_consts.POSE_WRANGLER)), plugin_path)
        loaded = plugins.load_plugin(os.path.normpath(path))
        if loaded:
            logger.info('Epic Pose Wrangler Plug-in loaded successfully')
