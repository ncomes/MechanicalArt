"""
String Constants
"""

# System global imports
import os
# Software specific imports
# mca python imports
from mca.launcher.utils import path_utils, consts, yamlio, dialogs


LAUNCHER_PREFS_DICT = {'maya_version': 0,
                        'mobu_version': 0,
                        'unreal_version': 0}


def get_launcher_local_prefs_file():
    """
    Creates the File where the local toolbox prefs lives.
    :return: Returns the file where the local toolbox prefs lives.
    :rtype: str
    """

    prefs_folder = path_utils.create_launcher_local_prefs_folder()
    prefs_file = os.path.join(prefs_folder, consts.MCA_LAUNCHER_PREFS)
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

