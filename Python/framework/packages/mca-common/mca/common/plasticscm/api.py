#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains API to interact with Plastic SCM server
"""
# mca python imports
import os.path
import shutil
import importlib
import subprocess
# software specific imports
# mca python imports
from mca.common import log
from mca.common.paths import project_paths, path_utils
from mca.common.utils import process
from mca.common.utils import lists

#from mca.common.plasticscm.widgets import dialogs

logger = log.MCA_LOGGER


def verify_workspace():
    current_project = project_paths.MCA_PLASTIC_ROOT
    if not current_project:
        logger.warning('Impossible to get workspace update status because no MAT project is defined!')
        return False
    return True


def get_workspace_update_status():
    """
    Returns whether workspace with given name is updated.

    :return: operation status model instance.
    :rtype: OperationStatus or None
    """

    if not verify_workspace():
        return False
    
    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning(
            'Impossible to get workspace update status because current MAT project does not defines a Plastic '
            'workspace')
        return False

    return Plastic().get_workspace_update_status(plastic_workspace_name)


def update_workspace():
    """
    Updates current project workspace.

    :return: operation status model instance.
    :rtype: OperationStatus or None
    """

    if not verify_workspace():
        return False

    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning(
            'Impossible to update workspace because current MAT project does not defines a Plastic workspace')
        return False

    return Plastic().update_workspace(plastic_workspace_name)


def get_file_info(file_path):
    """
    Returns the info of the given file path within workspace.

    :param str file_path: file path of the file we want to retrieve info for.
    :return: file info.
    :rtype: FileInfo
    """

    if not verify_workspace():
        return False

    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning(
            'Impossible to get file info because current MAT project does not defines a Plastic workspace')
        return False

    return Plastic().get_file_info(plastic_workspace_name, file_path)


def add_item(item_path, add_parents=True, checkout_parent=True, recurse=True):
    """
    Adds an item to version control.

    :param str item_path: path of the item to be added.
    :param bool add_parents: whether to add any parent directories which are not under version control.
    :param bool checkout_parent: whether parent node of the item will be checked out as a result.
    :param bool recurse: whether all the children items should be recursively added.
    :return: paths that were affected by the addition operation.
    :rtype: AffectedPaths
    """

    if not verify_workspace():
        return False

    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning('Impossible to add item because current MAT project does not defines a Plastic workspace')
        return False

    return Plastic().add_workspace_item(
        plastic_workspace_name, item_path, add_parents=add_parents, checkout_parent=checkout_parent, recurse=recurse)


def checkout_item(item_path):
    """
    Marks workspace item as ready to modify.

    :param str item_path: path of the item to checkout.
    :return: paths that were affected by the checkout operation.
    :rtype: AffectedPaths
    """

    if not verify_workspace():
        return False

    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning('Impossible to checkout item because current MAT project does not defines a Plastic workspace')
        return False

    return Plastic().checkout_workspace_item(plastic_workspace_name, item_path)


def move_item(item_path, dest_item_path):
    """
    Moves or renames a file or directory within a workspace.

    :param str item_path: path of the item to move/rename.
    :param str dest_item_path: target path of the item.
    :return: paths that were affected by the checkout operation.
    :rtype: AffectedPaths
    """

    if not verify_workspace():
        return False

    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning('Impossible to move/rename item because current MAT project does not defines a Plastic workspace')
        return False

    return Plastic().move_workspace_item(plastic_workspace_name, item_path, dest_item_path)


def revert_item(item_path, changeset):
    """
    Reverts locally given item to the contents of the item in the given changset

    :param str item_path: absolute path of the item we want to revert.
    :param int changeset: number of the changeset that contains the revision which content we want to load in the
        workspace.
    :return: revert info.
    :rtype: RevertInfo
    """

    if not verify_workspace():
        return False

    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning('Impossible to revert item because current MAT project does not defines a Plastic workspace')
        return False

    return Plastic().revert_workspace_item(plastic_workspace_name, item_path, changeset)


def get_item(item_path):
    """
    Returns information about a single item within a repository.

    :param str item_path: absolute path of the item we want to retrieve info for.
    :return: item model instance.
    :rtype: Item
    """

    return get_item_from_branch('main', item_path)


def get_item_from_branch(branch_name, item_path):
    """
    Returns information about a single item within a repository.

    :param str branch_name: name of the branch we want to retrieve item from.
    :param str item_path: absolute path of the item we want to retrieve info for.
    :return: item model instance.
    :rtype: Item
    """

    if not verify_workspace():
        return False

    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning(
            'Impossible to retrieve item information because current MAT project does not defines a Plastic workspace')
        return False

    return Plastic().get_item_in_branch(plastic_workspace_name, branch_name, item_path)


def get_item_revision(revision_id):
    """
    Loads a single item's revision within the workspace and gets information about it.

    :param str revision_id: ID of the revision we want to retrieve info of.
    :return: desired item's revision will be returned.
    :rtype: Item
    """

    if not verify_workspace():
        return False

    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning(
            'Impossible to retrieve item revision information because current MAT project does not defines a Plastic'
            ' workspace')
        return False

    return Plastic().get_item_revision(plastic_workspace_name, revision_id)


def load_items(items, ui=False):
    """
    Loads all the given items in MAT project Plastic workspace.

    :param list(str) items: list of items
    :param bool ui: whether to show UI or not.
    """
    return
    # if ui:
    #     dlg = dialogs.PlasticLoadItemsDialog(files_to_sync=items, enable_templates=True)
    #     dlg.exec_()
    #     return dlg.result
    #
    # if not verify_workspace():
    #     return False
    #
    # # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    # plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    # plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    # if not plastic_workspace:
    #     logger.warning('Impossible to load items because current MAT project does not defines a Plastic workspace')
    #     return False
    #
    # return Plastic().load_items(plastic_workspace, items)


def unload_items(items, ui=False):
    """
    Unloads all the given items from the MAT project Plastic workspace.

    :param list(str) items: list of items to unload.
    :param bool ui: whether to show UI or not.
    """
    return
    # if ui:
    #     dlg = dialogs.PlasticUnloadItemsDialog(files_to_sync=items)
    #     dlg.exec_()
    #     return dlg.result
    #
    # if not verify_workspace():
    #     return False
    #
    # # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    # plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    # plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    # if not plastic_workspace:
    #     logger.warning('Impossible to unload items because current MAT project does not defines a Plastic workspace')
    #     return False
    #
    # return Plastic().unload_items(plastic_workspace, items)


def is_item_updated(item_path):
    """
    Returns whether given item path is updated.

    :param str item_path: path to an item.
    :return: True if item is updated; False otherwise.
    :rtype: bool
    """

    if not verify_workspace():
        return False

    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning(
            'Impossible to check whether item is updated because current MAT project does not defines a Plastic '
            'workspace')
        return False

    item_info = Plastic().get_file_info(plastic_workspace_name, item_path)
    if not item_info:
        return False

    return item_info.revision_head_changeset == item_info.revision_changeset


def update_items(items):
    """
    Updates all given items.

    :param list(str) items: list of items to update.
    """

    if not verify_workspace():
        return False

    # Ex: 'DarkWinterArt'  The name of the depot the user set which should be the same as the folder name.
    plastic_workspace_name = project_paths.MCA_PROJECT_FOLDER_NAME
    plastic_workspace = Plastic().get_workspace(plastic_workspace_name)
    if not plastic_workspace:
        logger.warning('Impossible to update items because current MAT project does not defines a Plastic workspace')
        return list()

    return Plastic().update_items(plastic_workspace_name, items)


class Plastic(object):

    _PROCESS = None

    def __new__(cls, url="http://localhost:9090", http_username=None, http_password=None,
                ssl_verify=True, timeout=None, api_version='1'):
        """
        Instantiates a new PlasticSCM API wrapper.

        :param str url: API endpoint in format http://host:port (defaults to "http://localhost:9090").
        :param str http_username: optional username.
        :param str http_password: optional password.
        :param bool ssl_verify: whether SSL verification will be executed.
        :param int or float timeout: timeout to use for requests to the PlasticSCM server.
        :param str api_version: PlasticSCM API version to use.
        """

        self = super(Plastic, cls).__new__(cls)
        self._api_version = api_version = str(api_version)
        api = importlib.import_module('.v{}.api'.format(api_version),   __package__)
        model = importlib.import_module('.v{}.model'.format(api_version), __package__)
        self._api = api.API(
            url, http_username=http_username, http_password=http_password, ssl_verify=ssl_verify, timeout=timeout)
        self._model = model
        self._workspace = None
        self._workspace_name = None

        # first we check whether a cm.exe process is already running, if that is not the case we open a new one
        if not cls._PROCESS:
            cls._PROCESS = lists.get_first_in_list(process.get_processes_by_name('cm.exe'))
            if not cls._PROCESS:
                cls._PROCESS = subprocess.Popen(['cm', 'api'], shell=True)

        return self

    # ============================================================================================================
    # PROPERTIES
    # ============================================================================================================

    @property
    def api_version(self):
        """
        Returns API version used by PlasticSCM.

        :return: PlasticSCM version.
        :rtype: str
        """

        return self._api_version

    @property
    def model(self):
        """
        Returns classes of objects provided by the API.

        :return: model module.
        :rtype: Module
        """

        return self._model

    # ============================================================================================================
    # UTILS
    # ============================================================================================================

    def get_cm_location(self):
        """
        Returns path where Plastic CLI (cm) is located.

        :return: absolute path to plastic CLI.
        :rtype: str
        """

        cm_path = shutil.which('cm')
        if cm_path is None:
            raise FileNotFoundError('"cm" executable was not found!')

        return os.path.normpath(cm_path)

    # ============================================================================================================
    # REPOSITORIES
    # ============================================================================================================

    def get_repositories(self):
        """
        Returns all available repositories of a server, along with their information.

        :return: repositories of a server.
        :rtype: tuple(Repository)
        """

        return self._api.get_repositories()

    # ============================================================================================================
    # WORKSPACES
    # ============================================================================================================

    def get_workspaces(self):
        """
        Returns all registered workspaces, along with their information.

        :return: registered workspaces.
        :rtype: tuple(Workspace)
        """

        return self._api.get_workspaces()

    def get_workspace(self, wkspace_name):
        """
        Returns the information concerning a single workspace.

        :param str wkspace_name: name of the workspace whose info we want to retrieve.
        :return: workspace model instance.
        :rtype: Workspace or None.
        """

        if self._workspace and self._workspace_name == wkspace_name:
            return self._workspace

        self._workspace_name = wkspace_name
        self._workspace = self._api.get_workspace(wkspace_name)

        return self._workspace

    def get_workspace_update_status(self, wkspace_name):
        """
        Returns whether workspace with given name is updated.

        :param str wkspace_name: name of the workspace whose status we want to retrieve.
        :return: operation status model instance.
        :rtype: OperationStatus or None
        """

        return self._api.get_workspace_update_status(wkspace_name)

    def update_workspace(self, wkspace_name):
        """
        Updates workspace with given name.

        :param str wkspace_name: name of the workspace we want to update.
        :return: operation status model instance.
        :rtype: OperationStatus or None
        """

        return self._api.update_workspace(wkspace_name)

    def get_file_info(self, wkspace_name, file_path):
        """
        Returns the info of the given file path within workspace.

        :param str wkspace_name: name of the workspace where the item we want to revert is located.
        :param str file_path: file path of the file we want to retrieve info for.
        :return: file info.
        :rtype: FileInfo
        """

        relative_path = lists.get_first_in_list(self._get_item_relative_paths(wkspace_name, file_path))
        return self._api.get_file_info(wkspace_name, relative_path)

    def add_workspace_item(self, wkspace_name, item_path, add_parents=True, checkout_parent=True, recurse=True):
        """
        Adds an item to version control.

        :param str wkspace_name: name of the workspace.
        :param str item_path: path of the item to be added.
        :param bool add_parents: whether to add any parent directories which are not under version control.
        :param bool checkout_parent: whether parent node of the item will be checked out as a result.
        :param bool recurse: whether all the children items should be recursively added.
        :return: paths that were affected by the addition operation.
        :rtype: AffectedPaths
        """

        relative_path = lists.get_first_in_list(self._get_item_relative_paths(wkspace_name, item_path))
        return self._api.add_workspace_item(wkspace_name, relative_path, add_parents, checkout_parent, recurse)

    def checkout_workspace_item(self, wkspace_name, item_path):
        """
        Marks workspace item as ready to modify.

        :param str wkspace_name: name of the workspace.
        :param str item_path: path of the item to checkout.
        :return: paths that were affected by the checkout operation.
        :rtype: AffectedPaths
        """

        relative_path = lists.get_first_in_list(self._get_item_relative_paths(wkspace_name, item_path))
        return self._api.checkout_workspace_item(wkspace_name, relative_path)

    def move_workspace_item(self, wkspace_name, item_path, dest_item_path):
        """
        Moves or renames a file or directory within a workspace.

        :param str wkspace_name: name of the workspace.
        :param str item_path: path of the item to move/rename.
        :param str dest_item_path: target path of the item.
        :return: paths that were affected by the checkout operation.
        :rtype: AffectedPaths
        """

        relative_path = lists.get_first_in_list(self._get_item_relative_paths(wkspace_name, item_path))
        source_relative_path = lists.get_first_in_list(self._get_item_relative_paths(wkspace_name, item_path))
        return self._api.move_workspace_item(wkspace_name, relative_path, source_relative_path)

    def revert_workspace_item(self, wkspace_name, item_path, changeset):
        """
        Reverts locally given item to the contents of the item in the given changset

        :param str wkspace_name: name of the workspace where the item we want to revert is located.
        :param str item_path: absolute path of the item we want to revert.
        :param int changeset: number of the changeset that contains the revision which content we want to load in the
            workspace.
        :return: revert info.
        :rtype: RevertInfo
        """

        relative_path = lists.get_first_in_list(self._get_item_relative_paths(wkspace_name, item_path))
        return self._api.revert_workspace_item(wkspace_name, relative_path, changeset)

    # ============================================================================================================
    # ITEMS / CONTENTS
    # ============================================================================================================

    def get_item_in_branch(self, repo_name, branch_name, item_path):
        """
        Returns information about a single item in a branch within a repository.

        :param str repo_name: name of the repository where the item we want to retrieve info from is located.
        :param str branch_name: name of the branch we want to retrieve info item is located.
        :param str item_path: absolute path of the item we want to retrieve info for.
        :return: item model instance.
        :rtype: Item
        """

        relative_path = lists.get_first_in_list(self._get_item_relative_paths(repo_name, item_path))
        return self._api.get_item_in_branch(repo_name, branch_name, relative_path)

    def get_item_revision(self, repo_name, revision_id):
        """
        Loads a single item's revision within the workspace and gets information about it.

        :param str repo_name: name of the repository where the item we want to retrieve info from is located.
        :param str revision_id: ID of the revision we want to retrieve info of.
        :return: desired item's revision will be returned.
        :rtype: Item
        """

        return self._api.get_item_revision(repo_name, revision_id)

    # ============================================================================================================
    # PARTIAL / SELECTIVE SYNC
    # ============================================================================================================

    def update_items(self, workspace, items):
        """
        Updates all given items.

        :param str or Workspace workspace: Workspace model instance or workspace name we want to load files to.
        :param list(str) items: list of items to update.

        ..note:: the following items are supported:
            - file paths (to load specific files).
            - directories (directories will be loaded recursively).
        """

        if isinstance(workspace, str):
            workspace = self.get_workspace(workspace)
        workspace_path = os.path.normpath(workspace.path)
        relative_paths = self._get_item_relative_paths(workspace, items)
        relative_paths = ['./{}'.format(pth) if not pth.startswith('/') else pth for pth in relative_paths]

        command = '"{}" partial update'.format(self.get_cm_location())
        for relative_path in relative_paths:
            command += ' "{}"'.format(relative_path)

        logger.info('Updating Plastic paths: {}'.format(items))
        process = subprocess.Popen(command, cwd=workspace_path, stdout=subprocess.PIPE, creationflags=0x08000000)
        out, err = process.communicate()
        if err:
            logger.error('Error happened while updating item from Plastic: {}'.format(err))

    def load_items(self, workspace, items):
        """
        Loads all the given items.

        :param str or Workspace workspace: Workspace model instance or workspace name we want to load files to.
        :param list(str) items: list of items to load.

        ..note:: the following items are supported:
            - file paths (to load specific files).
            - directories (directories will be loaded recursively).
        """

        if isinstance(workspace, str):
            workspace = self.get_workspace(workspace)
        workspace_path = os.path.normpath(workspace.path)
        relative_paths = self._get_item_relative_paths(workspace, items)
        relative_paths = ['/{}'.format(pth) if not pth.startswith('/') else pth for pth in relative_paths]
        paths_to_add = ' '.join(['+"{}"'.format(relative_path) for relative_path in relative_paths])

        command = '"{}" partial configure {} --ignorecase'.format(self.get_cm_location(), paths_to_add)

        logger.info('Loading Plastic paths: {}'.format(paths_to_add))
        process = subprocess.Popen(command, cwd=workspace_path, stdout=subprocess.PIPE, creationflags=0x08000000)
        out, err = process.communicate()

        if err:
            logger.error('Error happened while loading items from Plastic: {}'.format(err))
            return False

        return True

    def unload_items(self, workspace, items):
        """
        Unloads all the given items.

        :param str or Workspace workspace: Workspace model instance or workspace name we want to unload files from.
        :param list(str) items: list of items to unload.

        ..note:: the following items are supported:
            - file paths (to unload specific files).
            - directories (directories will be uloaded recursively).
        """

        if isinstance(workspace, str):
            workspace = self.get_workspace(workspace)
        workspace_path = os.path.normpath(workspace.path)
        relative_paths = self._get_item_relative_paths(workspace, items)
        relative_paths = ['/{}'.format(pth) if not pth.startswith('/') else pth for pth in relative_paths]
        path_to_remove = ' '.join(['-"{}"'.format(relative_path) for relative_path in relative_paths])

        command = '"{}" partial configure {} --ignorecase'.format(self.get_cm_location(), path_to_remove)

        logger.info('Unloading Plastic paths: {}'.format(path_to_remove))
        process = subprocess.Popen(command, cwd=workspace_path, stdout=subprocess.PIPE, creationflags=0x08000000)
        out, err = process.communicate()

        if err:
            logger.error('Error happened while unloading items from Plastic: {}'.format(err))
            return False

        return True

    def _get_item_relative_paths(self, workspace, item_paths):
        """
        Internal function that converts an absolute path pointing within a Plastic workspace into a relative path
        to that Plastic workspace. For example:
            D:\wkspaces\DarkWinterArt\DarkWinter\Characters\ ==> DarkWinter\Characters\

        :param Workspace or str workspace: workspace items are located.
        :param list(str) item_paths: absolute item paths.
        :return: relative item paths.
        :rtype: list(str)
        """

        if isinstance(workspace, str):
            workspace = self.get_workspace(workspace)
        workspace_path = os.path.normpath(workspace.path)

        item_paths = lists.force_list(item_paths)
        item_paths = [os.path.normpath(item_path) for item_path in item_paths]

        relative_paths = [path_utils.to_relative_path(item_path) for item_path in item_paths]

        return relative_paths
