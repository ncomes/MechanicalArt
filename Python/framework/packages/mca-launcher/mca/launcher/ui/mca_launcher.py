# mca python imports
import os

# PySide2 imports
from PySide2.QtCore import QEvent, Qt, QSize
from PySide2.QtGui import QPalette, QBrush, QPixmap, QIcon
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QLineEdit, QFrame
from PySide2.QtWidgets import QSpacerItem, QSizePolicy
# mca imports
from mca.launcher.utils import path_utils, windows, launcher_utils, config_paths, yamlio, dialogs, launcher_prefs
from mca.launcher.dcc import maya, mobu


LOCAL_PREFS_FILE = f'mca_launcher.pref'
LAUNCHER_PREFS_DICT = {'maya_version': 0,
                        'mobu_version': 0,
                        'unreal_version': 0}

LAUNCHER_STYLE = """
                    QLineEdit
                    {
                    background-color: rgba(38,109,147,255);
                    color: white;
                    border: 1px solid white;
                    }
                    
                    QPushButton
                    {
                        background-color: rgba(33,92,120,0);
                        border: 2px solid rgba(33,92,120,200);
                    
                    }
                    
                    
                    QPushButton::hover
                    {
                        background-color: rgba(33,86,123,100);
                    
                    
                    }
                    
                    QPushButton#path_pushButton
                    {
                        color: white;
                        background-color: rgba(10,10,10,255);
                    
                    }
                    
                    QLabel
                    {
                        color: white;
                    }
                    
                    QComboBox
                    {
                    background-color: rgba(23,83,116,255);
                    color: white;
                    }
                    
                    """



class DCCLauncher(QMainWindow):
    VERSION = '1.0.0'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(f'MCA DCC Launcher v{self.VERSION}')
        mca_icon = os.path.join(config_paths.ICONS_PATH, 'mca.png')
        self.setWindowIcon(QIcon(mca_icon))
        self.setFixedSize(800, 400)

        self.setFocusPolicy(Qt.StrongFocus)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_frame = QLabel(self)
        self.main_frame.setFixedSize(800, 400)
        splash = QPixmap(os.path.join(config_paths.IMAGES_PATH, 'jackalyptic-splash.png'))
        splash.scaled(800, 400, Qt.KeepAspectRatio)
        self.main_frame.setPixmap(splash)
        self.main_layout.addWidget(self.main_frame)

        self.main_v = QVBoxLayout(self.main_frame)
        self.main_frame.setLayout(self.main_v)

        self.path_layout = QHBoxLayout()
        self.main_v.addLayout(self.path_layout)

        self.path_label = QLabel(' Path to Art Depot: ', parent=self.main_frame)
        self.path_layout.addWidget(self.path_label)

        self.path_lineEdit = QLineEdit()
        self.path_lineEdit.setEnabled(False)
        self.path_layout.addWidget(self.path_lineEdit)

        # self.path_pushButton = QPushButton(' Open Folder ')
        # self.path_layout.addWidget(self.path_pushButton)

        # Add the main frame for all the software buttons
        self.software_h_layout = QHBoxLayout(self.main_frame)
        self.main_v.addLayout(self.software_h_layout)

        self.software_layout = QVBoxLayout()
        self.software_h_layout.addLayout(self.software_layout)

        # Add the button setup for Maya
        self.maya_frame = QFrame()
        self.maya_frame.setFixedSize(125, 165)
        self.software_layout.addWidget(self.maya_frame)

        self.maya_layout = QVBoxLayout(self.maya_frame)
        self.maya_frame.setLayout(self.maya_layout)

        maya_icon = QIcon(os.path.join(config_paths.ICONS_PATH, 'maya-2023.png'))
        self.maya_pushButton = QPushButton()
        self.maya_pushButton.setFixedSize(108, 120)
        self.maya_pushButton.setIcon(maya_icon)
        self.maya_pushButton.setIconSize(QSize(106, 118))
        self.maya_layout.addWidget(self.maya_pushButton)

        self.maya_comboBox = QComboBox()
        self.maya_layout.addWidget(self.maya_comboBox)

        # Add the button setup for Mobu
        self.mobu_frame = QFrame()
        self.mobu_frame.setFixedSize(125, 165)
        self.software_layout.addWidget(self.mobu_frame)

        self.mobu_layout = QVBoxLayout(self.mobu_frame)
        self.mobu_frame.setLayout(self.mobu_layout)

        mobu_icon = QIcon(os.path.join(config_paths.ICONS_PATH, 'mobu-2023.png'))
        self.mobu_pushButton = QPushButton()
        self.mobu_pushButton.setFixedSize(108, 120)
        self.mobu_pushButton.setIcon(mobu_icon)
        self.mobu_pushButton.setIconSize(QSize(106, 118))
        self.mobu_layout.addWidget(self.mobu_pushButton)

        self.mobu_comboBox = QComboBox()
        self.mobu_layout.addWidget(self.mobu_comboBox)

        self.h_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.software_layout.addItem(self.h_spacer)

        # Set UI Data
        self.setStyleSheet(LAUNCHER_STYLE)

        self.prefs_check = False
        if self.path_lineEdit.text() == '':
            self.do_prefs_check()
        self.launcher_prefs = launcher_prefs.LauncherPrefs.load()
        self.common_path = path_utils.get_common_path()
        self.maya_versions = launcher_utils.get_maya_versions()
        self.maya_comboBox.addItems(self.maya_versions)
        self.maya_comboBox.setCurrentIndex(self.launcher_prefs.maya_version)

        self.mobu_versions = launcher_utils.get_mobu_versions()
        self.mobu_comboBox.addItems(self.mobu_versions)
        self.mobu_comboBox.setCurrentIndex(self.launcher_prefs.mobu_version)

        self.installEventFilter(self)
        self.show()

        ######################
        # Signals
        ######################
        self.maya_pushButton.clicked.connect(self.launch_maya)
        self.maya_comboBox.currentIndexChanged.connect(self.update_prefs)
        self.mobu_pushButton.clicked.connect(self.launch_mobu)
        self.mobu_comboBox.currentIndexChanged.connect(self.update_prefs)

    ######################
    # Slots
    ######################
    def launch_maya(self):
        """
        Launches Maya
        """

        version = str(self.maya_comboBox.currentText()).strip()
        maya.launch(version, self.common_path, path_utils.get_dependencies_path())

    def launch_mobu(self):
        """
        Launches MoBu
        """

        version = str(self.mobu_comboBox.currentText()).strip()
        mobu.launch(version, self.common_path, path_utils.get_dependencies_path())

    def update_prefs(self):
        self.launcher_prefs.maya_version = self.maya_comboBox.currentIndex()
        self.launcher_prefs.mobu_version = self.mobu_comboBox.currentIndex()

    def do_prefs_check(self):
        if not launcher_utils.prefs_check():
            mca_dir = launcher_utils.get_python_path_dialog()
            if not mca_dir:
                return
            launcher_utils.write_prefs_path_file(mca_dir)
            self.path_lineEdit.setText(mca_dir)
            self.prefs_check = True
            return

        mca_dir = path_utils.get_mca_python_root_path()
        if not mca_dir:
            return
        self.path_lineEdit.setText(mca_dir)
        self.prefs_check = True

    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == QEvent.Close:
                if self.launcher_prefs:
                    self.launcher_prefs.export()
                return True
            else:
                return super().eventFilter(obj, event)


def get_launcher_local_prefs_file():
    """
    Creates the File where the local toolbox prefs lives.
    :return: Returns the file where the local toolbox prefs lives.
    :rtype: str
    """

    prefs_folder = path_utils.create_launcher_local_prefs_folder()
    prefs_file = os.path.join(prefs_folder, LOCAL_PREFS_FILE)
    if not os.path.isfile(prefs_file):
        yamlio.write_yaml(LAUNCHER_PREFS_DICT, prefs_file)
    return os.path.normpath(prefs_file)


def export_launcher_local_prefs(prefs_dict):
    """
    Creates the folder where the local toolbox prefs lives.

    :param str dcc: the dcc software
    :return: Returns the folder where the local toolbox prefs lives.
    :rtype: str
    """

    prefs_file = get_launcher_local_prefs_file()
    if not os.path.exists(prefs_file):
        os.makedirs(prefs_file)
    yamlio.write_yaml(prefs_dict, prefs_file)
    return prefs_file


def read_launcher_file(path):
    """
    Reads the preferences file
    """

    data = yamlio.read_yaml(path)
    return data


class LauncherPrefs:
    def __init__(self, launcher_prefs):
        self.prefs = launcher_prefs

    @property
    def maya_version(self):
        return self.prefs.get('maya_version', 0)

    @maya_version.setter
    def maya_version(self, value):
        self.prefs.update({'maya_version': value})

    @property
    def mobu_version(self):
        return self.prefs.get('mobu_version')

    @mobu_version.setter
    def mobu_version(self, value):
        self.prefs.update({'mobu_version': value})

    @property
    def unreal_version(self):
        return self.prefs.get('unreal_version')

    @unreal_version.setter
    def unreal_version(self, value):
        self.prefs.update({'unreal_version': value})

    @classmethod
    def create(cls, maya_version=0, mobu_version=0, unreal_version=0):
        prefs = {'maya_version': maya_version,
                 'mobu_version': mobu_version,
                 'unreal_version': unreal_version}
        return cls(prefs)

    @classmethod
    def load(cls):
        prefs_file = get_launcher_local_prefs_file()
        prefs = read_launcher_file(prefs_file)
        if not prefs:
            prefs = LAUNCHER_PREFS_DICT
            dialogs.error_message(title='Preferences Error', text='WARNING: Unable to read local prefs file.\n'
                                                                  'Your setting will not be saved')
            print('WARNING: Unable to read local prefs file.  Your setting will not be saved')
        return cls(prefs)

    def export(self):
        export_launcher_local_prefs(self.prefs)
