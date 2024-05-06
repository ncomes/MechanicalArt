#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
These are the Maya menus that get loaded
"""

# mca python imports

# PySide2 imports
# software specific imports
import unreal

# mca python imports
from mca.common import log
from mca.common.tools.toolbox import toolbox_data

logger = log.MCA_LOGGER

ACTION_PROJ_DOCS = 'ProjectDocuments'
MENU_HELP_DOCS = 'HelpDocuments'
ACTION_ANIM_DOCS = 'Animation Help'
ACTION_MODEL_DOCS = 'Modeling Help'
ACTION_RIG_DOCS = 'Rigging Help'
ACTION_JIRA_DOCS = 'Jira URL'

MENU_MCA_TOOLS = 'MAT Tools'


def create_menus():
    """
    Creates the Maya menus at the top of Maya
    """

    menus = unreal.ToolMenus.get()
    main_menu = menus.find_menu("LevelEditor.MainMenu")
    if not main_menu:
      logger.error("Failed to find the 'Main' menu. Something is wrong in the force!")
    
    custom_menu = main_menu.add_sub_menu('Custom Menu', 'Python Tools', 'MATTOOLS', 'MAT Tools')

    # Add ToolBox Editor
    tools_editor_entry = unreal.ToolMenuEntry(name=f'mat_toolbox_editor',
                                           type=unreal.MultiBlockType.MENU_ENTRY,
                                           insert_position=unreal.ToolMenuInsert("",
                                                                                 unreal.ToolMenuInsertType.FIRST))

    string_command = f'from mca.ue.tools.toolbox import ue_toolbox;win=ue_toolbox.UnrealToolBoxEditor()'

    tools_editor_entry.set_label('ToolBox Editor')
    tools_editor_entry.set_tool_tip("MAT an editor the for ToolBox")
    tools_editor_entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON,
                                       '',
                                       string=(string_command))

    custom_menu.add_menu_entry("Scripts", tools_editor_entry)

    # ToolBoxes
    sub_menu = custom_menu.add_sub_menu('ToolBoxMenu',
                                        'PythonToolBox',
                                        'MATTOOLBOX',
                                        'MAT ToolBox',
                                        'All MAT Tools for Unreal Editor')

    for toolbox_name, toolbox_class in toolbox_data.ToolboxRegistry().TOOLBOX_NAME_DICT.items():
        all_tools_entry = unreal.ToolMenuEntry(name=f'mat_{toolbox_name}',
                                               type=unreal.MultiBlockType.MENU_ENTRY,
                                               insert_position=unreal.ToolMenuInsert("",
                                                                                     unreal.ToolMenuInsertType.FIRST))

        string_command = f'from mca.ue.tools.toolbox import ue_toolbox;win=ue_toolbox.UnrealToolBox("{toolbox_name}")'

        all_tools_entry.set_label(toolbox_name)
        all_tools_entry.set_tool_tip("MAT Toolbox that is dedicated to all existing tools")
        all_tools_entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON,
                                '',
                                string=(string_command))

        sub_menu.add_menu_entry("Scripts", all_tools_entry)

    # refresh the UI
    menus.refresh_all_widgets()


def remove_menus():
    return
