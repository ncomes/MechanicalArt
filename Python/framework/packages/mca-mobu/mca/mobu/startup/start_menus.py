#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
These are the Maya menus that get loaded
"""

# mca python imports

# software specific imports

# mca python imports
from mca.mobu.pyqt.utils import mo_main_windows
from mca.common.startup import startup_menus
from mca.common.pyqt.qt_utils import qt_menus
from mca.common.resources import resources
from mca.common.tools.toolbox import toolbox_data
from mca.mobu.tools.toolbox import mo_toolbox_ui
from mca.mobu.utils import mo_plastic
resources.register_resources()


ACTION_PROJ_DOCS = 'ProjectDocuments'
MENU_HELP_DOCS = 'HelpDocuments'
ACTION_ANIM_DOCS = 'Animation Help'
ACTION_MODEL_DOCS = 'Modeling Help'
ACTION_RIG_DOCS = 'Rigging Help'
ACTION_JIRA_DOCS = 'Jira URL'

MENU_MCA_TOOLS = 'MCA Tools'


def action_proj_docs(maya_menu_bar, mobu_window):
    menu_inst = qt_menus.MainWindowsMenus(maya_menu_bar, mobu_window)

    # Add Project Documents Action
    menu_inst.add_action(ACTION_PROJ_DOCS, startup_menus.project_url_menu, icon=resources.icon(r'white\darkwinter.png'))


def menu_help_urls(mobu_window):
    menu_inst = qt_menus.MainWindowsMenus.create(MENU_HELP_DOCS, mobu_window, icon=resources.icon(r'white\mat.png'))
    menu_inst.add_action(ACTION_ANIM_DOCS, startup_menus.animation_url_menu, icon=resources.icon(r'color\animation.png'))
    menu_inst.add_action(ACTION_MODEL_DOCS, startup_menus.modeling_url_menu, icon=resources.icon(r'color\art.png'))
    menu_inst.add_action(ACTION_RIG_DOCS, startup_menus.rigging_url_menu, icon=resources.icon(r'color\puppet.png'))
    menu_inst.add_separator()
    menu_inst.add_action(ACTION_JIRA_DOCS, startup_menus.jira_url_menu, icon=resources.icon(r'color\jira.png'))


def menu_mca_tools(mobu_window):
    menu_tools_inst = qt_menus.MainWindowsMenus.create(MENU_MCA_TOOLS, mobu_window)
    menu_toolbars = qt_menus.MainWindowsMenus(menu_tools_inst.menu, mobu_window)
    tool_bar_menu = menu_toolbars.add_menu('ToolBox')

    all_tools_toolbox = toolbox_data.get_toolbox_by_name('All Tools')
    menu_toolbars.add_action('All Tools',
                             lambda: mo_toolbox_ui.MobuToolBox(all_tools_toolbox,
                                                               is_floating=False,
                                                               area='right'),
                             icon=resources.icon(r'white\mca.png'))


def mca_menus(mobu_window):
    menu_tools_inst = qt_menus.MainWindowsMenus.create(MENU_MCA_TOOLS,
                                                       mobu_window,
                                                       icon=resources.icon(r'logos\mech-art-white.png'))
    menu_toolbars = qt_menus.MainWindowsMenus(menu_tools_inst.menu, mobu_window)
    menu_toolbars.add_menu('General')
    menu_toolbars.add_action('Plastic Check Out', mo_plastic.checkout_scene,
                             icon=resources.icon(r'software\plasticscm_logo.png'))

    menu_toolbars = qt_menus.MainWindowsMenus(menu_tools_inst.menu, mobu_window)
    tool_bar_menu = menu_toolbars.add_menu('ToolBox')

    all_tools_toolbox = toolbox_data.get_toolbox_by_name('All Tools')
    menu_toolbars.add_action('All Tools',
                             lambda: mo_toolbox_ui.MobuToolBox(all_tools_toolbox,
                                                               is_floating=False,
                                                               area='right'),
                             icon=resources.icon(r'white\mca.png'))


def create_menus():
    mobu_window = mo_main_windows.get_mobu_window()
    mobu_menu_bar = mo_main_windows.get_main_menubar()

    # Add Project URL Documents Action
    # action_proj_docs(mobu_menu_bar, mobu_window)
    # Help URLs
    # menu_help_urls(mobu_window)
    # Toolbox
    mca_menus(mobu_window)


def remove_menus():
    mobu_window = mo_main_windows.get_mobu_window()
    mobu_menu_bar = mo_main_windows.get_main_menubar()

    # Remove Help URLs
    menu_inst = qt_menus.MainWindowsMenus.create(MENU_HELP_DOCS, mobu_window)
    menu_inst.remove_menu()

    # Remove the Tools Menu
    menu_tools_inst = qt_menus.MainWindowsMenus.create(MENU_MAT_TOOLS, mobu_window)
    menu_tools_inst.remove_menu()

    # Remove URL
    main_menu_inst = qt_menus.MainWindowsMenus(mobu_menu_bar, mobu_window)
    main_menu_inst.remove_action(ACTION_PROJ_DOCS)

