# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import ast
import contextlib
from collections import namedtuple
import os
import pathlib
import sys
import traceback
from io import StringIO
# Qt imports
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QSplitter, QMessageBox, QFileDialog
from PySide2.QtGui import QIcon
# software specific imports
# mca python imports
from mca.common.pyqt import common_windows
from mca.common.utils import dcc_util, strings
from mca.common.pyqt import syntax_highlighter
from mca.ue.tools.scripteditor import output_text
from mca.ue.tools.scripteditor.seutils import script_editor_utils
from mca.ue.tools.scripteditor.codeeditor import code_editor
# from mca.ue.tools.scripteditor.codeeditor.highlighter import py_highlight

try:
    import unreal
    RUNNING_IN_UNREAL = True
except:
    RUNNING_IN_UNREAL = False
WINDOW = None

CONFIG_PATH = script_editor_utils.get_local_prefs_file('unreal')


class MATScriptEditor(common_windows.MCAMainWindow):
    VERSION = '1.0.0'

    def __init__(self, parent=None):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'script_editor.ui')
        super().__init__(title='Script Editor',
                         ui_path=ui_path,
                         version=MATScriptEditor.VERSION,
                         style='incrypt',
                         parent=parent)

        ICONS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'icons')
        CLEAR_ALL_ICON = QIcon(os.path.join(ICONS_PATH, 'clearAll'))
        CLEAR_HISTORY_ICON = QIcon(os.path.join(ICONS_PATH, 'clearHistory'))
        CLEAR_INPUT_ICON = QIcon(os.path.join(ICONS_PATH, 'clearInput'))
        EXECUTE_ICON = QIcon(os.path.join(ICONS_PATH, 'execute'))
        EXECUTE_ALL_ICON = QIcon(os.path.join(ICONS_PATH, 'executeAll'))

        self.ui.ui_run_all_btn.setIcon(EXECUTE_ALL_ICON)
        self.ui.ui_run_sel_btn.setIcon(EXECUTE_ICON)
        self.ui.ui_clear_script_btn.setIcon(CLEAR_INPUT_ICON)
        self.ui.ui_clear_log_btn.setIcon(CLEAR_HISTORY_ICON)
        self.ui.ui_clear_both_btn.setIcon(CLEAR_ALL_ICON)

        self.output_log = output_text.OutputTextWidget(self)

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.ui.output_vl.addWidget(self.splitter)

        self.splitter.addWidget(self.output_log)
        self.splitter.addWidget(self.ui.ui_tab_widget)

        self.ui_tabs = list()
        self.ui_tab_highlighters = list()

        self.register_traceback()
        self.load_tabs()

        QApplication.activeWindow()

        ####################################
        # Signals
        ####################################
        self.ui.ui_run_all_btn.clicked.connect(self.execute)
        self.ui.ui_run_sel_btn.clicked.connect(self.execute_sel)
        #self.ui.ui_tab_widget.returnPressed.connect(self.execute_sel)
        self.ui.ui_clear_log_btn.clicked.connect(self.clear_log)
        self.ui.ui_clear_script_btn.clicked.connect(self.clear_script)
        self.ui.ui_clear_both_btn.clicked.connect(self.clear_all)

        # self.ui.ui_save_action.triggered.connect(self.save_script)
        # self.ui.ui_open_action.triggered.connect(self.open_script)
        self.ui.actionTabs_to_Spaces.triggered.connect(self.convert_all_to_spaces)
        self.ui.actionSpaces_to_Tabs.triggered.connect(self.convert_all_to_tabs)

        self.ui.ui_tab_widget.tabBarClicked.connect(self.add_tab)
        self.ui.ui_tab_widget.tabCloseRequested.connect(self.remove_tab)

    ####################################
    # Slots
    ####################################
    def register_traceback(self):
        """
        Link Unreal traceback
        """
        def custom_traceback(exc_type, exc_value, exc_traceback=None):
            message = 'Error: {}: {}\n'.format(exc_type, exc_value)
            if exc_traceback:
                format_exception = traceback.format_tb(exc_traceback)
                for line in format_exception:
                    message += line
            self.output_log.update_logger(message, 'error')

        sys.excepthook = custom_traceback

    def load_configs(self):
        """
        During startup, load python script config file and initialize tab gui
        """
        if not os.path.exists(CONFIG_PATH):
            self.load_tabs()
            return

        with open(CONFIG_PATH, 'r') as f:
            tab_configs = list()
            tab_config_dicts = ast.literal_eval(f.read())
            for tab_config_dict in tab_config_dicts:
                tab_config = TabConfig(**tab_config_dict)
                tab_configs.append(tab_config)

        self.load_tabs(tab_configs)

    def load_tabs(self, tab_configs=None):
        """
        Initialize python script tab gui from config object

        :param tab_configs: TabConfig. dataclass object storing python tab info
        """

        folder = self.get_local_folder()
        files = os.listdir(path=folder)
        tabs = [os.path.join(folder, x) for x in files if pathlib.Path(x).suffix == '.py']

        if not tabs:
            self.insert_tab(0, '', 'Python')
            #tab_configs = [TabConfig(0, 'Python', True, '')]
            return

        active_index = 0
        for x, tab in enumerate(tabs):
            with open(tab, 'r') as f:
                file_name = os.path.basename(tab).split('.')[0]
                output = f.read()
                index = self.ui.ui_tab_widget.count() - 1
                self.insert_tab(index, output, 'Python')
                self.ui_tabs.insert(index, file_name)


        self.ui.ui_tab_widget.setCurrentIndex(active_index)

    def insert_tab(self, index, command, label, guid=None):
        """
        Insert a python tab into the tab widget

        :param index: int. tab index to insert
        :param command: str. python script command to add to the inserted tab
        :param label: str. title/label of the tab inserted
        """
        script_edit = code_editor.CodeEditor()
        if not guid:
            guid = strings.generate_guid()
        script_edit.setObjectName(guid)
        self.ui_tabs.insert(index, guid)
        script_edit.setPlainText(command)
        highlight = syntax_highlighter.PythonHighlighter(script_edit.document())

        self.ui.ui_tab_widget.insertTab(index, script_edit, label)
        self.ui_tab_highlighters.append(highlight)
        self.ui_tabs.append(script_edit)

        self.ui.ui_tab_widget.setCurrentIndex(index)

    def convert_all_to_spaces(self):
        """
        Converts all the PlainTextWidget's tabs to spaces
        """

        self.ui.ui_tab_widget.currentWidget().convert_all_to_spaces()

    def convert_all_to_tabs(self):
        """
        Converts all the PlainTextWidget's spaces to tabs
        """
        self.ui.ui_tab_widget.currentWidget().convert_all_to_tabs()

    def execute(self):
        """
        Send all command in script area for mya to execute
        """

        self.save_script()

        command = self.ui.ui_tab_widget.currentWidget().toPlainText()
        if RUNNING_IN_UNREAL:
            output = unreal.PythonScriptLibrary.execute_python_command_ex(
                python_command=command,
                execution_mode=unreal.PythonCommandExecutionMode.EXECUTE_FILE,
                file_execution_scope=unreal.PythonFileExecutionScope.PUBLIC
            )
            self.output_log.update_logger(f"{command}")
            if not output:
                self.output_log.update_logger(f'print({command})')
                return
            self.send_formatted_output(output)
            
        else:
            with stdoutIO() as s:
                exec(command)
            output = s.getvalue()
            self.output_log.update_logger(f"{command}")
            self.send_basic_formatted_output(output)

    def execute_sel(self):
        """
        Send selected command in script area for mya to execute
        """

        self.save_script()
        command = self.ui.ui_tab_widget.currentWidget().textCursor().selection().toPlainText()
        if RUNNING_IN_UNREAL:
            output = unreal.PythonScriptLibrary.execute_python_command_ex(
                python_command=command,
                execution_mode=unreal.PythonCommandExecutionMode.EXECUTE_FILE,
                file_execution_scope=unreal.PythonFileExecutionScope.PUBLIC
            )
            self.output_log.update_logger(f"{command}")
            # self.output_log.update_logger(f"{output}")
            # if not output or not output[1]:
            #     output = unreal.PythonScriptLibrary.execute_python_command_ex(
            #         python_command=f'print({command})',
            #         execution_mode=unreal.PythonCommandExecutionMode.EXECUTE_FILE,
            #         file_execution_scope=unreal.PythonFileExecutionScope.PUBLIC
            #     )
            self.send_formatted_output(output)

        else:
            with stdoutIO() as s:
                exec(command)
            output = s.getvalue()
            self.output_log.update_logger(f"{command}")
            self.send_basic_formatted_output(output)

    def send_formatted_output(self, output):
        """
        Update ui field with messages
        """
        if not output:
            return

        result, log_entries = output
        for entry in log_entries:
            if entry.type != unreal.PythonLogOutputType.INFO:
                self.output_log.update_logger(entry.output, 'error')
            else:
                self.output_log.update_logger(entry.output, 'info')

    def send_basic_formatted_output(self, output):
        """
        Update ui field with messages
        """
        if not output:
            return

        self.output_log.update_logger(output, 'info')

    def clear_log(self):
        """
        Clear history logging area
        """
        self.output_log.clear()

    def clear_script(self):
        self.ui.ui_tab_widget.currentWidget().setPlainText('')

    def clear_all(self):
        self.clear_script()
        self.clear_log()
    # endregion

    # region Tab Operation
    def add_tab(self, index):
        """
        Add a python tab when 'Add' tab button is clicked
        """
        if index == self.ui.ui_tab_widget.count() - 1:
            self.insert_tab(index, '', 'Python')

    def remove_tab(self, index):
        """
        Remove a python tab

        :param index: int. removal tab index
        """
        msg_box = QMessageBox(QMessageBox.Question,
            '',
            'Delete the Current Tab?',
            QMessageBox.Yes | QMessageBox.No)

        usr_choice = msg_box.exec()
        if usr_choice == QMessageBox.Yes:
            if index != self.ui.ui_tab_widget.count() - 1:
                self.ui.ui_tab_widget.removeTab(index)
                self.ui.ui_tab_widget.setCurrentIndex(index-1)
                self.ui_tabs.remove(index)
    
    def open_script_dialog(self):
        """
        Open python file to script edit area
        """
        path = QFileDialog.getOpenFileName(
            parent=None,
            caption="Open Script",
            dir='',
            filter="*.py")[0]

        if not path:
            return

        with open(path, 'r') as f:
            file_name = os.path.basename(path)
            output = f.read()
            index = self.ui.ui_tab_widget.count() - 1
            self.insert_tab(index, output, file_name)

    def save_script_dialog(self):
        """
        Save script edit area as a python file
        """
        path = QFileDialog.getSaveFileName(
            parent=None,
            caption="Save Script As...",
            dir='',
            filter="*.py")[0]

        if not path:
            return

        command = self.ui.ui_tab_widget.currentWidget().toPlainText()
        with open(path, 'w') as f:
            f.write(command)

    def save_script(self):
        folder = self.get_local_folder()
        idx = self.ui.ui_tab_widget.currentIndex()
        command = self.ui.ui_tab_widget.currentWidget().toPlainText()
        guid = self.ui_tabs[idx]
        file_name = os.path.join(folder, f'{guid}.py')

        with open(file_name, 'w') as f:
            f.write(command)

    def get_local_folder(self):
        app = dcc_util.application()
        folder = script_editor_utils.create_local_prefs_folder(app.lower())
        return folder

class TabConfig(namedtuple('TabConfig', ['index', 'label', 'active', 'command'])):
    """
    Dataclass to store python script information in the tabs

    :param index: int. script tab index within the tab widget
    :param label: str. script tab title label
    :param active: bool. whether this tab is set to active (current)
                   only one tab is allowed to be active
    :param command: str. script in the tab
    """
    __slots__ = ()


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def script_editor_cmd():
    global WINDOW
    app = None
    if not QApplication.instance():
        app = QApplication(sys.argv)
    try:
        window = WINDOW or MATScriptEditor()
        if RUNNING_IN_UNREAL:
            unreal.parent_external_window_to_slate(int(window.winId()))
        #if app:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
