"""
Initializes all the MAT Packages needed to run the python codebase in MotionBuilder.
"""


# mca python imports
import os
# software specific imports
# mca python imports
from mca import mobu as mca_mobu
from mca.common.modifiers import decorators
from mca.mobu.startup import start_menus
from mca.common import log
from mca.mobu.startup.configs import mo_consts, mo_configs
from mca.mobu.startup.configs import mo_envs
from mca.common.startup.configs import consts, config
from mca.common.pyqt.qt_utils import windows
from mca.mobu.pyqt.utils import mo_main_windows
from mca.common.tools.toolbox import toolbox_prefs, toolbox_data
from mca.mobu.tools.toolbox import mo_toolbox_ui
from mca.common.resources import resources

logger = log.MCA_LOGGER


@decorators.track_fnc
def startup_init(skip_dialog=False):
    """
    Initializes MAT Packages.
    """

    if not skip_dialog:
        logger.info('Creating MAT Python Maya framework environment ...')
        print("""
     __      __  ____    ___     __      __       _
    |  \    /  |/ ___|  / _ \   |  \    /  | ___ | |__  _   _
    | \ \  / / | |     / /_\ \  | \ \  / / |/ _ \| |_ \| | | |
    | |\ \/ /| | |___ / /___\ \ | |\ \/ /| | |_| | |_| | \_/ |
    |_| \__/ |_|\____/_/     \_\|_| \__/ |_|\___/|_|__/ \___/
         
         """)
        print('\n' + '=' * 118 + '\n')

    mo_envs.create_mobu_envs()
    resources.register_resources()
    logger.info('Registered Resources...')
    print('\n' + '=' * 118 + '\n')

    start_menus.create_menus()
    if not skip_dialog:
        logger.info('Motion Builder Main Window Environment Variables Created...')
        logger.info('Motion Builder Main Window Menus Created...')
        print('\n' + '=' * 118 + '\n')

    mobu_main_window = mo_main_windows.get_mobu_window()
    mobu_main_window.setWindowIcon(resources.icon(r'software\mca.png'))
    windows.close_all_mca_docked_windows(mobu_main_window)
    if not skip_dialog:
        logger.info('Double Checked to make sure all windows are closed...')

    # Check to see if any Toolboxes need to be opened.
    TOOLBOX_P = toolbox_prefs.ToolBoxPreferences(dcc=consts.MOBU)
    all_on_start = TOOLBOX_P.get_all_on_startups()

    if all_on_start:
        for toolbox_name in all_on_start:
            toolbox_class = toolbox_data.ToolboxRegistry().TOOLBOX_NAME_DICT.get(toolbox_name)
            if toolbox_class:
                mo_toolbox_ui.MobuToolBox(toolbox_class)
                if not skip_dialog:
                    logger.info(f'Opened Toolbox: {toolbox_name}')

    # Maya Dependencies paths
    depend_paths = os.getenv(mo_consts.DEPS_ROOT, None)
    if depend_paths:
        mo_configs.add_mobu_system_paths(depend_paths)
        if not skip_dialog:
            logger.info('Motion Builder Dependencies paths added...')


def shutdown(skip_dialog=False):
    """
    Shuts down the MAT Depots for Motion Builder

    :param bool skip_dialog: If True, nothing will be written to the console.
    """

    start_menus.remove_menus()

    mobu_main_window = mo_main_windows.get_mobu_window()
    windows.close_all_mca_docked_windows(mobu_main_window)

    # Remove Mobu's paths from sys.path
    depend_paths = os.getenv(mo_consts.DEPS_ROOT, None)
    mobu_root_path = mca_mobu.MOBU_TOP_ROOT
    if depend_paths:
        config.remove_sys_path([depend_paths, mobu_root_path])

    if not skip_dialog:
        logger.info('Motion Builder menus removed successfully')
        logger.info('Motion Builder docked windows closed successfully')
        logger.info('Motion Builder framework shutdown successfully')
        logger.info('\n' + '=' * 160 + '\n')


def init(skip_dialog=False):
    """
    This is a temporary fix.  We will need to change all the init calls to the startup init.
    So we can remove this function.
    # ToDo @comes Change all the init calls to the startup_init.

    :param bool skip_dialog: If True, will not print any dialogs
    """
    
    startup_init(skip_dialog=skip_dialog)
