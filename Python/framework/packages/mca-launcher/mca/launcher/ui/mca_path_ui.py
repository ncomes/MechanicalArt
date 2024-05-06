"""
A window that sets the default preferences for the launcher.
"""

# System global imports
import os.path
# mca python imports
# PySide2 imports
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PySide2.QtWidgets import QSpacerItem, QSizePolicy, QFrame
# mca imports
from mca.launcher.utils import launcher_utils, path_utils, dialogs


class DCCPathLauncher(QMainWindow):
    """
    This window pops up if the preferences in the documents folder doesn't exist or in it contains the wrong path.
    """

    VERSION = '1.0.0'

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle(f'MCA Launcher {DCCPathLauncher.VERSION}')
        self.setMinimumSize(645, 405)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.central_widget = QWidget(self)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        self.main_layout.setContentsMargins(4, 4, 4, 4)

        self.launcher_prefs = path_utils.MCAProjectPrefs()

        # Required Header
        self.required_layout = QHBoxLayout()
        self.main_layout.addLayout(self.required_layout)
        self.required_layout.setContentsMargins(0, 9, 0, 15)
        self.required_label = QLabel()
        self.required_label.setText(' *Required ')
        self.req_label_font = QFont()
        self.req_label_font.setFamily(u"Arial Black")
        self.req_label_font.setPointSize(10)
        self.req_label_font.setBold(True)
        self.req_label_font.setWeight(75)
        self.required_label.setFont(self.req_label_font)
        self.required_layout.addWidget(self.required_label)

        # Main python path layout
        self.info_layout = QHBoxLayout()
        self.main_layout.addLayout(self.info_layout)
        self.info_layout.setContentsMargins(0, 9, 0, 15)
        self.info_label = QLabel()
        ex_path = r'D:\YOUR_PROJECT_PATH'
        self.info_label.setText(f'Select the Root Workspace for the art depot.\n '
                                f'Example: {ex_path} - '
                                f'You should see a file named: "mca_python.config" in that directory.')

        self.path_layout = QHBoxLayout()
        self.main_layout.addLayout(self.path_layout)
        self.path_label = QLabel()
        self.path_label.setText(' Project Art Depot: ')
        self.path_label_font = QFont()
        self.path_label_font.setBold(True)
        self.path_label.setFont(self.path_label_font)
        self.path_layout.addWidget(self.path_label)

        self.info_layout.addWidget(self.info_label)
        self.project_valid = QLabel()
        self.project_valid.setFixedSize(60, 20)
        self.project_valid_font = QFont()
        self.project_valid_font.setFamily(u"Mulish ExtraBold")
        self.project_valid_font.setBold(True)
        self.project_valid_font.setWeight(75)
        self.project_valid.setFont(self.project_valid_font)
        self.path_layout.addWidget(self.project_valid)

        self.path_edit = QLineEdit()
        self.path_edit.setEnabled(False)
        self.path_layout.addWidget(self.path_edit)
        self.dialog_button = QPushButton(' Open Folder ')
        self.path_layout.addWidget(self.dialog_button)

        self.set_project_valid(self.project_valid, self.path_edit, 1)

        # Separation lines
        self.info_layout = QVBoxLayout()
        self.main_layout.addLayout(self.info_layout)
        self.line_01 = QFrame()
        self.line_01.setFrameShape(QFrame.HLine)
        self.line_01.setFrameShadow(QFrame.Sunken)
        self.line_01.setContentsMargins(3, 9, 3, 9)
        self.info_layout.addWidget(self.line_01)

        # Save the project paths
        self.save_main_frame = QVBoxLayout()
        self.main_layout.addLayout(self.save_main_frame)
        self.save_main_frame.setContentsMargins(9,9,9,9)
        self.save_button = QPushButton(' Save Paths ')
        self.save_main_frame.addWidget(self.save_button)

        self.vertical_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(self.vertical_spacer)

        self.show()

        self.new_win = []

        ##########################################
        # Signals
        ##########################################
        self.dialog_button.clicked.connect(self.dialog_button_clicked)
        self.save_button.clicked.connect(self.save_path_clicked)

    ##########################################
    # Slots
    ##########################################
    def dialog_button_clicked(self):
        """
        Opens a dialog to select the path to the python folder.
        """

        path = launcher_utils.get_python_path_dialog()
        self.path_edit.setText(path)
        verify = launcher_utils.verify_mca_project_path(path)
        if not verify:
            dialogs.error_message(title='Path Error',
                                  text='The provided path is not a valid MCA project path!',
                                  parent=self)
            self.set_project_valid(self.project_valid, self.path_edit, 3)
            return

        self.set_project_valid(self.project_valid, self.path_edit, 2)

    def set_project_valid(self, qlabel, qlineedit, valid=1):
        if valid is 1:
            qlabel.setText(' Not Set ')
            qlabel.setStyleSheet("""border-width: 2px;
                                                border-color: black;
                                                border-style: solid;
                                                color: black;""")
            qlineedit.setStyleSheet("""color: black""")
        if valid is 2:
            qlabel.setText(' Valid! ')
            qlabel.setStyleSheet("""border-width: 2px;
                                                border-color: green;
                                                border-style: solid;
                                                color: green;""")
            qlineedit.setStyleSheet("""color: green""")

        if valid is 3:
            qlabel.setText(' Invalid! ')
            qlabel.setStyleSheet("""border-width: 2px;
                                                border-color: red;
                                                border-style: solid;
                                                color: red;""")
            qlineedit.setStyleSheet("""color: red""")

    def save_path_clicked(self):
        """
        Saves the path to the preferences folder.
        """
        result = dialogs.question_message(title='Save Paths?', text='Are you sure you want to save?', parent=self)
        if result != 'Yes':
            return
        path = str(self.path_edit.text()).strip()
        verify = launcher_utils.verify_mca_project_path(path)
        if not verify:
            dialogs.error_message(title='Path Error',
                                  text='The provided "Project" path is not a valid path!',
                                  parent=self)
            return

        path = os.path.normpath(path)
        self.launcher_prefs.project_path = path
        self.launcher_prefs.save()

        root_path = path_utils.get_mca_python_root_path()
        if not root_path or not os.path.exists(root_path):
            dialogs.error_message(title='Preferences Error',
                                  text='Error:  Preferences were not set.\n'
                                        'Unable to open Launcher\n'
                                        'Error - 1603',
                                  parent=self)
            return
        self.launch_launcher()
        self.close()

    def launch_launcher(self):
        """
        Launches the main launcher UI.
        """

        from mca.launcher.ui import mca_launcher
        win = mca_launcher.DCCLauncher()
        win.show()
        self.new_win.append(win)

