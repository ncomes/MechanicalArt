# -*- coding: utf-8 -*-

"""
this startup code is used to add a script editor button to the unreal tool bar.
ignore this file when using this script editor widget outside Unreal
"""

# mca python imports
# Qt imports
# software specific imports
import unreal
# mca python imports


def create_script_editor_button():
    """
    Start up script to add script editor button to tool bar
    """

    section_name = 'Plugins'
    se_command = (
        'from mca.ue.tools.scripteditor import script_editor_ui;'
        'global editor;'
        'editor = script_editor_ui.script_editor_cmd()'
    )

    menus = unreal.ToolMenus.get()
    level_menu_bar = menus.find_menu('LevelEditor.LevelEditorToolBar.PlayToolBar')
    level_menu_bar.add_section(section_name=section_name, label=section_name)

    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label('Script Editor')
    entry.set_tool_tip('MAT Unreal Python Script Editor')
    #entry.set_icon('EditorStyle', 'ContentBrowser.AssetActions.Edit')
    entry.set_icon('EditorStyle', 'FontEditor.FontBackgroundColor')
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),
        string=se_command
    )
    level_menu_bar.add_menu_entry(section_name, entry)
    menus.refresh_all_widgets()


def create_script_editor_button_cmd():
    create_script_editor_button()
