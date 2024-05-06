"""
Initializes all the MAT Packages needed to run the python codebase in Unreal.
"""

# mca python imports
import os
# software specific imports
import unreal
# mca python imports
from mca.common.startup.configs import config
from mca.common.modifiers import decorators
from mca.ue.startup.configs import ue_envs, ue_configs, ue_consts
from mca.ue.startup import start_menus
from mca.ue.tools.scripteditor import editor_start
from mca.ue.assettypes import py_material_instance
from mca import ue


###################################################################################################
# WARNING!  On Unreal Startup, if any Qt code is running, it will crash Unreal!
###################################################################################################


@decorators.track_fnc
def startup_init(skip_dialog=False):
    """
    Initializes MAT Packages.
    """
    
    if not skip_dialog:
        unreal.log('Creating MAT Python Maya framework environment ...')
        
        print("""   
         __      __  ____    ___     _   _		          _   ____
        |  \    /  |/ ___|  / _ \   | | | |____ ___  __ _| | |  _ \ __   __ _   _      ___  __  _
        | \ \  / / | |     / /_\ \  | | | | '__/ _ \/ _` | | | |_) |\ \ / /| | | |___ / _ \|  \| |
        | |\ \/ /| | |___ / /___\ \ | |_| | |  | __/|(_| | | |  __/  \ V /|_ _|| |_  | (_) | | \ |
        |_| \__/ |_|\____/_/     \_\ \___/|_|  \___|\__,_|_| |_|      |_|  |_| |_| |_|\___/|_|\__|""")
        print('\n' + '=' * 118 + '\n')

    ue_envs.create_unreal_envs()
    if not skip_dialog:
        unreal.log('Maya Environment Variables Created...')

    print('\n' + '=' * 118 + '\n')

    start_menus.create_menus()
    if not skip_dialog:
        unreal.log('Maya Main Window Menus Created...')
        print('\n' + '=' * 118 + '\n')

    if not skip_dialog:
        unreal.log('Double Checked to make sure all windows are closed...')
    
    # Maya Dependencies paths
    depend_paths = os.getenv(ue_consts.DEPS_ROOT, None)
    if depend_paths:
        ue_configs.add_unreal_system_paths(depend_paths)
        if not skip_dialog:
            unreal.log('Maya Dependencies paths added...')

    default_materials = py_material_instance.PlainMaterialInstances()
    print(f'Registering default materials\n{default_materials}')
    print('\n' + '=' * 118 + '\n')

    print('\n' + '=' * 118 + '\n')
    editor_start.create_script_editor_button_cmd()
    if not skip_dialog:
        unreal.log('Script Editor Button Added to Menu')
    print('\n' + '=' * 118 + '\n')


def shutdown(skip_dialog=False):
    """
    Shuts down the MAT Depots for Unreal

    :param bool skip_dialog: If True, nothing will be written to the console.
    """

    ###################################
    # Currently this is not hooked up!
    ###################################

    start_menus.remove_menus()

    depend_paths = os.getenv(ue_consts.DEPS_ROOT, None)
    root_path = ue.UNREAL_TOP_ROOT
    if depend_paths:
        config.remove_sys_path([depend_paths, root_path])
    
    if not skip_dialog:
        unreal.log('Unreal menus removed successfully')
        unreal.log('Unreal docked windows closed successfully')
        unreal.log('Unreal framework shutdown successfully')
        unreal.log('\n' + '=' * 160 + '\n')


def init(skip_dialog=False):
    """
    This is a temporary fix.  We will need to change all the init calls to the startup init.
    So we can remove this function.
    # ToDo @comes Change all the init calls to the startup_init.

    :param bool skip_dialog: If True, will not print any dialogs
    """

    startup_init(skip_dialog=skip_dialog)
