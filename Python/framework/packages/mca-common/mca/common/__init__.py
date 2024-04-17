
"""
Common Init
"""

# mca python imports
from datetime import datetime
import os
import inspect
import platform
import pytz
# software specific imports
# mca python imports
from mca.common.textio import yamlio


COMMON_INIT_PATH = os.path.normpath(os.path.join(os.path.abspath(inspect.getfile(inspect.currentframe()))))
COMMON_PATH = os.path.dirname(COMMON_INIT_PATH)
TOP_ROOT = os.path.dirname(COMMON_INIT_PATH)
MCA_PACKAGE = os.path.join(TOP_ROOT, 'mca_package.yaml')
MCA_CONFIGS_PATH = os.path.join(TOP_ROOT, 'startup', 'configs')
MCA_LOGGING_LEVEL_FILE = os.path.join(MCA_CONFIGS_PATH, 'logging_level_users.yaml')
MCA_DCC_USER_DATA_FILE = os.path.join(MCA_CONFIGS_PATH, 'dcc_user_data.yaml')
LOCAL_USER_NAME = username = os.getlogin() or None


# Placing this here because this has to happen before logging starts up
# To set the logging level
# - The Logging Level always defaults to INFO
# - We need to use the user data we have been collecting to get the MAT Username
# - Then we compare the MAT Userename to the devs list and see if the user is a dev.
#       If so, logging level is set to DEBUG

def generate_unique_tracking_name():
    '''
    Returns a Unique tracking name.

    :return: Returns a Unique tracking name.
    :rtype: str
    '''

    username = os.getlogin()
    time_zone = datetime.now().astimezone(pytz.timezone('America/Los_Angeles')).strftime('%H:%M:%S') or 'NoTimeZone'
    pc_name = platform.node() or 'NoPCName'

    user_name = f'{username}{time_zone}{pc_name}'

    unique_uuid = 't' + str(int.from_bytes(user_name.encode(), 'little'))
    unique_uuid = unique_uuid[:len(unique_uuid) // 4]

    return unique_uuid


def set_logging_level():
    os.environ['MCA_LOGGING_LEVEL'] = 'INFO'
    user_log_level_file = yamlio.read_yaml_file(MCA_LOGGING_LEVEL_FILE)
    raw_user_data = yamlio.read_yaml_file(MCA_DCC_USER_DATA_FILE)
    hash_name = generate_unique_tracking_name()
    all_user_data = DCCUsernameData(raw_user_data, hash_name)
    print(hash_name)
    print(all_user_data)
    mat_username = all_user_data.mat_username
    if not mat_username:
        return
    if mat_username in user_log_level_file.get('devs'):
        os.environ['MCA_LOGGING_LEVEL'] = 'DEBUG'

class DCCUserData:
    def __init__(self, user_data):
        self._user_data = user_data

    @property
    def user_data(self):
        return self._user_data

    @property
    def usernames(self):
        return list(self.user_data.keys())

    def get_user_name_data(self, user_name):
        return self.user_data.get(user_name, None)

    def export(self, file_name):
        yamlio.write_to_yaml_file(self.user_data, file_name)


class DCCUsernameData(DCCUserData):
    def __init__(self, user_data, username):
        super(DCCUsernameData, self).__init__(user_data)
        self._user_data = user_data
        self._username = username

    @property
    def username(self):
        return self._username

    @property
    def user_data(self):
        return self._user_data

    @property
    def username_data(self):
        self.user_data.setdefault(self.username, {})
        return self.user_data[self.username]

    @property
    def country(self):
        return self.username_data.get('country', None)

    @country.setter
    def country(self, value):
        self.username_data.update({'country': value})

    @property
    def email(self):
        return self.username_data.get('email', None)

    @email.setter
    def email(self, value):
        self.username_data.update({'email': value})

    @property
    def full_name(self):
        return self.username_data.get('full_name', None)

    @full_name.setter
    def full_name(self, value):
        self.username_data.update({'full_name': value})

    @property
    def location(self):
        """
        ie: the state or providence in which they live or similar.

        :return: ie: the state or providence in which they live or similar.
        :rtype: str
        """

        return self.username_data.get('location', None)

    @location.setter
    def location(self, value):
        """
        ie: the state or providence in which they live or similar.
        :param str value: ie: the state or providence in which they live or similar.
        """

        self.username_data.update({'location': value})

    @property
    def team(self):
        return self.username_data.get('team', None)

    @team.setter
    def team(self, value):
        self.username_data.update({'team': value})

    @property
    def title(self):
        return self.username_data.get('title', None)

    @title.setter
    def title(self, value):
        self.username_data.update({'title': value})

    @property
    def mat_username(self):
        return self.username_data.get('mat_username', None)

    @mat_username.setter
    def mat_username(self, value):
        self.username_data.update({'mat_username': value})


set_logging_level()