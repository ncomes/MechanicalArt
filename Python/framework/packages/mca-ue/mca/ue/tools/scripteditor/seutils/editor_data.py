# -*- coding: utf-8 -*-

"""
this startup code is used to add a script editor button to the unreal tool bar.
ignore this file when using this script editor widget outside Unreal
"""

# mca python imports
import os
import pathlib
# Qt imports
# software specific imports
# mca python imports
from mca.common import log
from mca.common.textio import yamlio
from mca.common.utils import strings, dcc_util
from ue.tools.scripteditor.seutils import script_editor_utils


logger = log.MCA_LOGGER


SCRIPT_EDITOR_DATA_DICT = {strings.generate_guid(): {'name': 'Python',
                                                     'entries': '',
                                                     'index': 0}}


def script_editor_extentions(dcc):
    """
    Returns the file extension of the yaml file for a specific dcc

    :param str dcc: dcc name
    :return: Returns the file extension of the yaml file for a specific dcc
    :rtype: str
    """

    dcc = dcc.lower()
    if dcc == 'unreal':
        return '.uese'  # unreal engine script editor
    else:
        return '.sse'  # standalone script editor


class ScriptEditorData:
    _guid = ''
    _children = []

    def __init__(self, data):
        self._data_dict = data

    @classmethod
    def create(cls, name, idx, string_data):
        data_dict = {}
        guid = strings.generate_guid()
        data_dict[guid] = {}
        data_dict[guid]['name'] = name
        data_dict[guid]['entries'] = string_data
        data_dict[guid]['index'] = idx

        return cls(data_dict)

    @property
    def data_dict(self):
        return self._data_dict

    @property
    def ids(self):
        return list(self.data_dict.keys())

    @property
    def ext(self):
        return script_editor_extentions(self.app)

    @ext.setter
    def ext(self, value):
        self.ext = value

    @property
    def folder(self):
        return script_editor_utils.create_local_prefs_folder(self.app.lower())

    @property
    def app(self):
        return dcc_util.application()

    def export_all(self, ext=None):
        if not ext:
            ext = self.ext
        for guid in self.ids:
            file_name = os.path.join(self.folder, f'{guid}{ext}')
            data = self.data_dict.get(guid, None)
            if not data:
                continue
            yamlio.write_to_yaml_file(data, file_name)

    @classmethod
    def load(cls):
        app = dcc_util.application()
        ext = script_editor_extentions(app)

        path = script_editor_utils.create_local_prefs_folder(app.lower())
        files = os.listdir(path=path)
        tab_files = [os.path.join(path, x) for x in files if pathlib.Path(x).suffix == ext]
        if not tab_files:
            return

        data_dict = {}
        for tab_file in tab_files:
            file_dict = yamlio.read_yaml_file(tab_file)
            guid = pathlib.Path(tab_file).stem
            data_dict.update({guid: file_dict})

        return cls(data_dict)


class ScriptEditorTab(ScriptEditorData):

    def __init__(self, guid_id, data):
        super().__init__(data=data)
        self._guid = guid_id
        
    @property
    def guid(self):
        return self._guid
    
    @property
    def tab_dict(self):
        _dict = self._data_dict.get(self.guid, None)
        print(_dict)
        if not _dict:
            logger.error('Guid does not exist in the dictionary.  Cannot load Script Editor Tab Data.')
            #raise AttributeError('Guid does not exist in the dictionary.  Cannot load Script Editor Tab Data.')
        return _dict

    @property
    def code(self):
        entry = self.tab_dict.get('entries', None)
        if not entry:
            return
        return '\n'.join(entry.splitlines())

    @property
    def name(self):
        return self.tab_dict.get('name', None)

    @property
    def idx(self):
        return self.tab_dict.get('index', None)

    def export(self):
        file_name = os.path.join(self.folder, f'{self.guid}{self.ext}')
        yamlio.write_to_yaml_file(self.tab_dict, file_name)


class ScriptEditorTabsManager:

    def __init__(self):
        self.tab_list = []
        self.unsorted_tab_list = []
        self.tab_data = ScriptEditorData.load()
        self.get_lists()

    def get_lists(self):
        self.unsorted_tab_list = []
        for guid in self.tab_data.ids:
            tab_data = ScriptEditorTab(guid_id=guid, data=self.tab_data.data_dict)
            self.unsorted_tab_list.append([tab_data.idx, tab_data])
            tab_list = sorted(self.unsorted_tab_list)
            for tab, data in tab_list:
                self.tab_list.append(data)











