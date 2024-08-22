"""
These are the Maya menus that get loaded
"""

# python imports
# software specific imports
from mca.common.pyqt.pygui import qtwidgets, qtcore
# mca python imports
from mca.mya.pyqt.utils import ma_main_window
from mca.common.startup import startup_menus
from mca.common.pyqt.qt_utils import qt_menus
from mca.common.resources import resources
from mca.common.tools.toolbox import toolbox_data

from mca.mya.tools.toolbox import ma_toolbox_ui
#from mca.mya.tools.helios import helios_ui
from mca.mya.tools.summoner import summoner
from mca.mya.tools.reanimator import reanimator
from mca.mya.tools.animationexporter import animationexporter_ui
from mca.mya.utils import ma_fileio

resources.register_resources()


ACTION_PROJ_DOCS = 'ProjectDocuments'
MENU_HELP_DOCS = 'HelpDocuments'
ACTION_ANIM_DOCS = 'Animation Help'
ACTION_MODEL_DOCS = 'Modeling Help'
ACTION_RIG_DOCS = 'Rigging Help'
ACTION_JIRA_DOCS = 'Jira URL'

MENU_MCA_TOOLS = 'MechArt'
MENU_MCA_TOOLBOX = 'Toolbox'


def action_proj_docs(maya_menu_bar, maya_window):
    """
    Adds the help docs to Maya's main window.

    :param QMainWindow maya_window: Maya's main window
    """
    
    menu_inst = qt_menus.MainWindowsMenus(maya_menu_bar, maya_window)
    
    # Add Project Documents Action
    menu_inst.add_action(ACTION_PROJ_DOCS, startup_menus.project_url_menu, icon=resources.icon(r'logos\mech-art-logo_blue.png'))


def menu_help_urls(maya_window):
    """
    Adds the Help docs to Maya's main window.

    :param QMainWindow maya_window: Maya's main window
    """
    
    menu_inst = qt_menus.MainWindowsMenus.create(MENU_HELP_DOCS, maya_window, icon=resources.icon(r'logos\mech-art-white.png'))
    menu_inst.add_action(ACTION_ANIM_DOCS, startup_menus.animation_url_menu, icon=resources.icon(r'white\animation.png'))
    menu_inst.add_action(ACTION_MODEL_DOCS, startup_menus.modeling_url_menu, icon=resources.icon(r'white\art.png'))
    menu_inst.add_action(ACTION_RIG_DOCS, startup_menus.rigging_url_menu, icon=resources.icon(r'white\puppet.png'))
    menu_inst.add_separator()
    menu_inst.add_action(ACTION_JIRA_DOCS, startup_menus.jira_url_menu, icon=resources.icon(r'color\jira.png'))


def menu_mca_tools(maya_window):
    """
    Adds the toolbox to Maya's main window.
    
    :param QMainWindow maya_window: Maya's main window
    """
    
    menu_tools_inst = qt_menus.MainWindowsMenus.create(MENU_MCA_TOOLBOX, maya_window)
    menu_tools_inst.add_action('Toolbox Editor',
                             lambda sacrificial=False, maya_window=maya_window: ma_toolbox_ui.MayaToolboxEditor(),
                             icon=resources.icon(r'logos\mca.png'))
    menu_toolbars = qt_menus.MainWindowsMenus(menu_tools_inst.menu, maya_window)
    menu_toolbars.add_menu('ToolBox')
    for toolbox_name, toolbox_class in toolbox_data.ToolboxRegistry().TOOLBOX_NAME_DICT.items():
        menu_toolbars.add_action(toolbox_name,
                             lambda sacrificial=False, toolbox_class=toolbox_class: ma_toolbox_ui.MayaToolBox(toolbox_class=toolbox_class),
                             icon=resources.icon(r'logos\mca.png'))


def menu_mca_quick_tools(maya_window):
    """
    Adds the toolbox to Maya's main window.

    :param QMainWindow maya_window: Maya's main window
    """
    
    menu_tools_inst = qt_menus.MainWindowsMenus.create(MENU_MCA_TOOLS, maya_window, icon=resources.icon(r'logos\mca.png'))
    menu_toolbars = qt_menus.MainWindowsMenus(menu_tools_inst.menu, maya_window)
    menu_toolbars.add_menu('General')
    menu_toolbars.add_action('Plastic Check Out', ma_fileio.touch_and_checkout_cmd, icon=resources.icon(r'software\plasticscm_logo.png'))
    menu_tools_inst = qt_menus.MainWindowsMenus.create(MENU_MCA_TOOLS, maya_window)
    menu_toolbars = qt_menus.MainWindowsMenus(menu_tools_inst.menu, maya_window)
    menu_toolbars.add_menu('Modeling')
    #menu_toolbars.add_action('Helios', helios_ui.Helios, icon=resources.icon(r'logos\mech-art-white.png'))
    menu_tools_inst = qt_menus.MainWindowsMenus.create(MENU_MCA_TOOLS, maya_window)
    menu_toolbars = qt_menus.MainWindowsMenus(menu_tools_inst.menu, maya_window)
    menu_toolbars.add_menu('Animation')
    menu_toolbars.add_action('Summoner', summoner.Summoner, icon=resources.icon(r'logos\mca.png'))
    menu_toolbars.add_action('Re-Animator', reanimator.Reanimator, icon=resources.icon(r'logos\mca.png'))
    menu_toolbars.add_action('Export Animations', animationexporter_ui.AnimationExporter, icon=resources.icon(r'logos\mca.png'))
    menu_toolbars = qt_menus.MainWindowsMenus(menu_tools_inst.menu, maya_window)
    menu_toolbars.add_menu('ToolBox')
    menu_toolbars.add_action('Toolbox Editor',
                               lambda sacrificial=False, maya_window=maya_window: ma_toolbox_ui.MayaToolboxEditor(),
                               icon=resources.icon(r'logos\mca.png'))
    for toolbox_name, toolbox_class in toolbox_data.ToolboxRegistry().TOOLBOX_NAME_DICT.items():
        menu_toolbars.add_action(toolbox_name,
                                 lambda sacrificial=False, toolbox_class=toolbox_class: ma_toolbox_ui.MayaToolBox(
                                     toolbox_class=toolbox_class),
                                 icon=resources.icon(r'logos\mca.png'))


def create_menus():
    """
    Creates the Maya menus at the top of Maya
    """
    
    # This is here because, if the menus are already open the actions don't close properly.
    menu_bars = ma_main_window.get_main_menu_menubar()
    for menu_bar in menu_bars.children():
        if ACTION_PROJ_DOCS in menu_bar.objectName():
            force_remove_actions()
            break
    # Give the UI a second to think
    qtcore.QTimer.singleShot(1000, lambda: qtwidgets.QApplication.activeWindow())
    
    # Get the main window and menu bar.
    maya_window = ma_main_window.get_maya_window()
    maya_menu_bar = ma_main_window.get_main_menu_menubar()
    
    # Add Project URL Documents Action
    #action_proj_docs(maya_menu_bar, maya_window)
    # Help URLs
    #menu_help_urls(maya_window)
    # Tools
    menu_mca_quick_tools(maya_window)
    # Toolbox
    #menu_mca_tools(maya_window)
    

def remove_menus():
    """
    Removes the menus at the top of Maya
    """
    
    maya_window = ma_main_window.get_maya_window()
    maya_menu_bar = ma_main_window.get_main_menu_menubar()
    
    # Remove Help URLs
    menu_inst = qt_menus.MainWindowsMenus.create(MENU_HELP_DOCS, maya_window)
    menu_inst.remove_menu()
    
    # Remove the Tools Menu
    menu_tools_inst = qt_menus.MainWindowsMenus.create(MENU_MCA_TOOLS, maya_window)
    menu_tools_inst.remove_menu()

    # Remove the Quick Tools Menu
    menu_tools_inst = qt_menus.MainWindowsMenus.create(MENU_MCA_TOOLBOX, maya_window)
    menu_tools_inst.remove_menu()
    
    # Remove URL
    main_menu_inst = qt_menus.MainWindowsMenus(maya_menu_bar, maya_window)
    main_menu_inst.remove_action(ACTION_PROJ_DOCS)
    
    force_remove_actions()


def force_remove_actions():
    # force remove all mca actions
    menu_bars = ma_main_window.get_main_menu_menubar()
    action_list = [ACTION_PROJ_DOCS]
    for menu_bar in menu_bars.children():
        for act in action_list:
            if act in menu_bar.objectName():
                menu_bar.deleteLater()

