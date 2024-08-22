# mca python imports
import os

# PySide6 imports
from PySide6.QtCore import QEvent, Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QLineEdit, QFrame
from PySide6.QtWidgets import QSpacerItem, QSizePolicy
# mca imports
from mca.launcher.utils import path_utils, windows, launcher_utils, config_paths, yamlio, dialogs, launcher_prefs
from mca.launcher.dcc import maya, mobu, ue


LOCAL_PREFS_FILE = f'mca_launcher.pref'
LAUNCHER_PREFS_DICT = {'maya_version': 0,
                        'mobu_version': 0,
                        'unreal_version': 0,
                       'unreal_paths': []}

LAUNCHER_STYLE = """
                    QFrame
                    {
                    background-color: rgba(37,36,37,255);
                    }
                    
                    
                    QPushButton
                    {
                        background-color: rgba(37,36,37,255);
                        color: white
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
                        background-color: rgba(65,65,64,0);
                    }
                    
                    QComboBox
                    {
                    background-color: rgba(65,65,64,255);
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
        self.setFixedSize(680, 440)

        self.setFocusPolicy(Qt.StrongFocus)

        self.setStyleSheet(LAUNCHER_STYLE)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_frame = QLabel(self)
        self.main_frame.setObjectName('main_frame')
        self.main_frame.setStyleSheet("""QLabel#main_frame{border: 6px solid rgba(128,129,129,255);background-color: rgba(37,36,37,255);}""")
        self.main_frame.setFixedSize(680, 440)
        self.main_layout.addWidget(self.main_frame)

        self.main_v = QVBoxLayout(self.main_frame)
        self.main_frame.setLayout(self.main_v)

        self.path_layout = QHBoxLayout()
        self.main_v.addLayout(self.path_layout)

        # Line Edit Spacer
        self.path_h_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.path_layout.addItem(self.path_h_spacer)

        path_label_pixmap = QPixmap(os.path.join(config_paths.IMAGES_PATH, 'path_box.png'))
        self.path_main_label = QLabel()
        self.path_main_label.setPixmap(path_label_pixmap)
        self.path_layout.addWidget(self.path_main_label)

        self.path_lbl_layout = QHBoxLayout()
        self.path_main_label.setLayout(self.path_lbl_layout)

        self.path_label = QLabel(' Path to Art Depot: ', parent=self.main_frame)
        self.path_label.setFixedSize(120, 25)
        self.path_label.setStyleSheet("""background-color: rgba(100,101,100,0);""")
        self.path_lbl_layout.addWidget(self.path_label)

        self.path_lineEdit = QLineEdit()
        self.path_lineEdit.setStyleSheet("""color: white;
                                            border: 2px solid black;
                                            border-radius: 6px;
                                            background-color: rgba(100,101,100,255);""")
        self.path_lineEdit.setEnabled(False)
        self.path_lineEdit.setFixedSize(350, 25)
        self.path_lbl_layout.addWidget(self.path_lineEdit)

        self.line_edit_h_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.path_lbl_layout.addItem(self.line_edit_h_spacer)

        # Line Edit Spacer
        self.path2_h_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.path_layout.addItem(self.path2_h_spacer)

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
        self.maya_pushButton.setFixedSize(108, 110)
        self.maya_pushButton.setIcon(maya_icon)
        self.maya_pushButton.setIconSize(QSize(106, 118))
        self.maya_layout.addWidget(self.maya_pushButton)

        self.maya_comboBox = QComboBox()
        self.maya_comboBox.setStyleSheet("""background-color: rgba(65,65,64,255);""")
        self.maya_layout.addWidget(self.maya_comboBox)

        # Add the button setup for Mobu
        self.mobu_frame = QFrame()
        self.mobu_frame.setFixedSize(125, 165)
        self.software_layout.addWidget(self.mobu_frame)

        self.mobu_layout = QVBoxLayout(self.mobu_frame)
        self.mobu_frame.setLayout(self.mobu_layout)

        mobu_icon = QIcon(os.path.join(config_paths.ICONS_PATH, 'mobu-2023.png'))
        self.mobu_pushButton = QPushButton()
        self.mobu_pushButton.setFixedSize(108, 110)
        self.mobu_pushButton.setIcon(mobu_icon)
        self.mobu_pushButton.setIconSize(QSize(106, 118))
        self.mobu_layout.addWidget(self.mobu_pushButton)

        self.mobu_comboBox = QComboBox()
        self.mobu_comboBox.setStyleSheet("""background-color: rgba(65,65,64,255);""")
        self.mobu_layout.addWidget(self.mobu_comboBox)

        self.v1_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.software_layout.addItem(self.v1_spacer)

        # Next Software V Line

        self.software2_layout = QVBoxLayout()
        self.software_h_layout.addLayout(self.software2_layout)

        # Add the button setup for Unreal
        self.ue_frame = QFrame()
        self.ue_frame.setFixedSize(160, 165)
        self.ue_frame.setContentsMargins(0, 5, 0, 0)
        self.software2_layout.addWidget(self.ue_frame)

        self.ue_layout = QVBoxLayout(self.ue_frame)
        self.ue_frame.setLayout(self.ue_layout)

        self.ue_button_frame = QFrame()
        self.ue_button_frame.setMinimumWidth(100)
        self.ue_button_frame.setContentsMargins(0, 0, 0, 0)
        self.ue_layout.addWidget(self.ue_button_frame)

        self.ue_button_layout = QHBoxLayout()
        self.ue_button_layout.setContentsMargins(0, 0, 0, 0)
        self.ue_button_frame.setLayout(self.ue_button_layout)

        ue_icon = QIcon(os.path.join(config_paths.ICONS_PATH, 'ue-logo.png'))
        self.ue_pushButton = QPushButton()
        self.ue_pushButton.setFixedSize(108, 110)
        # self.ue_pushButton.setContentsMargins(30, 0, 30, 0)
        self.ue_pushButton.setIcon(ue_icon)
        self.ue_pushButton.setIconSize(QSize(106, 118))
        self.ue_button_layout.addWidget(self.ue_pushButton)

        self.options_ue = QFrame()
        self.options_ue.setMinimumWidth(100)
        self.ue_pushButton.setContentsMargins(0, 0, 0, 0)
        self.ue_layout.addWidget(self.options_ue)

        self.ue_h_frame = QHBoxLayout()
        self.ue_h_frame.setContentsMargins(0, 0, 0, 0)
        self.options_ue.setLayout(self.ue_h_frame)

        self.ue_comboBox = QComboBox()
        # self.ue_comboBox.setMinimumWidth(80)
        self.ue_comboBox.setStyleSheet("""background-color: rgba(65,65,64,255);""")
        self.ue_comboBox.setContentsMargins(0, 0, 0, 0)
        self.ue_h_frame.addWidget(self.ue_comboBox)

        self.ue_add_pushButton = QPushButton('+')
        self.ue_add_pushButton.setFixedSize(20, 20)
        self.ue_add_pushButton.setStyleSheet("""background-color: rgba(65,65,64,255);""")
        self.ue_h_frame.addWidget(self.ue_add_pushButton)

        self.ue_remove_pushButton = QPushButton('-')
        self.ue_remove_pushButton.setFixedSize(20, 20)
        self.ue_remove_pushButton.setStyleSheet("""background-color: rgba(65,65,64,255);""")
        self.ue_h_frame.addWidget(self.ue_remove_pushButton)

        self.v_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.software2_layout.addItem(self.v_spacer)

        # Spacer
        self.h_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.software_h_layout.addItem(self.h_spacer)

        # Logo
        self.logo_main_layout = QVBoxLayout()
        self.software_h_layout.addItem(self.logo_main_layout)

        # Spacer
        self.logo_v_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.logo_main_layout.addItem(self.logo_v_spacer)

        logo_icon = QPixmap(os.path.join(config_paths.ICONS_PATH, 'mca_dust_short_orange.png'))
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(logo_icon)
        self.logo_label.setMinimumSize(260, 60)
        self.logo_main_layout.addWidget(self.logo_label)
        self.logo_label.show()


        self.prefs_check = False
        if self.path_lineEdit.text() == '':
            self.do_prefs_check()
        self.launcher_prefs = launcher_prefs.LauncherPrefs.load()
        self.common_path = path_utils.get_common_path()

        self.maya_versions = list(set(launcher_utils.get_maya_versions()))
        self.maya_comboBox.addItems(list(sorted(self.maya_versions)))
        self.maya_comboBox.setCurrentIndex(self.launcher_prefs.maya_version)

        self.mobu_versions = list(set(launcher_utils.get_mobu_versions()))
        self.mobu_comboBox.addItems(list(sorted(self.mobu_versions)))
        self.mobu_comboBox.setCurrentIndex(self.launcher_prefs.mobu_version)

        self.ue_projects = self.get_unreal_projects()
        self.add_ue_projects_to_combobox()
        self.ue_comboBox.setCurrentIndex(self.launcher_prefs.unreal_version)

        self.installEventFilter(self)
        self.show()

        ######################
        # Signals
        ######################
        self.maya_pushButton.clicked.connect(self.launch_maya)
        self.maya_comboBox.currentIndexChanged.connect(self.update_prefs)
        self.mobu_pushButton.clicked.connect(self.launch_mobu)
        self.mobu_comboBox.currentIndexChanged.connect(self.update_prefs)
        self.ue_pushButton.clicked.connect(self.launch_unreal)
        self.ue_add_pushButton.clicked.connect(self.add_ue_project)
        self.ue_remove_pushButton.clicked.connect(self.remove_ue_project)
        self.ue_comboBox.currentIndexChanged.connect(self.update_prefs)

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

    def launch_unreal(self):
        """
        Launches Unreal
        """

        project_name = self.ue_comboBox.currentText()
        project_path = self.unreal_projects.get(project_name, None)
        if not project_path:
            return

        ue.launch(project_path, self.common_path, path_utils.get_dependencies_path())

    def add_ue_project_clicked(self):
        result = dialogs.question_message(title='Add an Unreal Project?',
                                          text='Are you sure you want to add an Unreal Project?',
                                          parent=self)
        if result != 'Yes':
            return

        self.add_ue_project()

    def update_prefs(self):
        self.launcher_prefs.maya_version = self.maya_comboBox.currentIndex()
        self.launcher_prefs.mobu_version = self.mobu_comboBox.currentIndex()
        self.launcher_prefs.unreal_version = self.ue_comboBox.currentIndex()

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

    def get_unreal_projects(self):
        self.unreal_projects = {}
        unreal_paths = self.launcher_prefs.unreal_paths
        if not unreal_paths:
            return
        for project in unreal_paths:
            project_name = os.path.basename(project).split('.')[0]
            self.unreal_projects.update({project_name: project})

    def add_ue_project(self):
        default_path = self.launcher_prefs.unreal_saved_path
        ue_project = launcher_utils.get_ue_project(default_path)
        if not ue_project or not os.path.exists(ue_project):
            dialogs.error_message(title='Path Error',
                                  text='The provided "UProject" is not a valid path!',
                                  parent=self)
            return

        self.launcher_prefs.unreal_saved_path = os.path.dirname(ue_project)
        self.launcher_prefs.add_unreal_path(ue_project)
        project_name = os.path.basename(ue_project).split('.')[0]
        self.ue_comboBox.addItem(project_name)
        self.get_unreal_projects()
        windows.set_combobox_item(self.ue_comboBox, project_name)

    def remove_ue_project(self):
        project_name = self.ue_comboBox.currentText()
        project_path = self.unreal_projects.get(project_name, None)
        if not project_path:
            return

        result = dialogs.question_message(title='Remove an Unreal Project?',
                                          text=f'Are you sure you want to remove the following project?:'
                                               f'\n{project_path}',
                                          parent=self)
        if result != 'Yes':
            return

        self.launcher_prefs.remove_unreal_path(project_path)
        self.get_unreal_projects()
        self.add_ue_projects_to_combobox()

    def add_ue_projects_to_combobox(self):
        self.ue_comboBox.clear()
        if not self.unreal_projects:
            return

        project_names = list(self.unreal_projects.keys())
        self.ue_comboBox.addItems(project_names)

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
