#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains internal API to interact with Plastic SCM server v1
"""
# mca python imports
from __future__ import print_function, division, absolute_import
import os
import uuid
# software specific imports

# mca python imports
from mca.common.plasticscm.core import rest
from mca.common.plasticscm.v1 import model


class API(object):

    def __new__(cls, url="http://localhost:9090", http_username=None, http_password=None,
                ssl_verify=True, timeout=None):
        """
        Instantiates a new PlasticSCM API wrapper.

        :param str url: API endpoint in format http://host:port (defaults to "http://localhost:9090").
        :param str http_username: optional username.
        :param str http_password: optional password.
        :param bool ssl_verify: whether SSL verification will be executed.
        :param int or float timeout: timeout to use for requests to the PlasticSCM server.
        """

        self = super(API, cls).__new__(cls)
        self._api_url = "{}/api/v1".format(url)
        self._http_username = http_username
        self._http_username = http_password
        self._ssl_verify = ssl_verify   # Whether SSL certificates should be validated
        self._timeout = float(timeout) if timeout is not None else None

        return self

    # ============================================================================================================
    # REPOSITORIES
    # ============================================================================================================

    @rest.REST.GET("/repos")
    def get_repositories(self):
        """
        Returns all available repositories of a server, along with their information.

        :return: repositories of a server.
        :rtype: tuple(Repository)
        """

        url, action = self.get_repositories.REST
        response = action(self._api_url + url, verify=self._ssl_verify, timeout=self._timeout)
        return tuple(self._json_to_repository(repo) for repo in response.json())

    # ============================================================================================================
    # WORKSPACES
    # ============================================================================================================

    @rest.REST.GET("/wkspaces")
    def get_workspaces(self):
        """
        Returns all registered workspaces, along with their information.

        :return: registered workspaces.
        :rtype: tuple(Workspace)
        """

        url, action = self.get_workspaces.REST
        response = action(self._api_url + url, verify=self._ssl_verify, timeout=self._timeout)
        return tuple(self._json_to_workspace(wkspace) for wkspace in response.json())

    @rest.REST.GET("/wkspaces/{wkspace_name}")
    def get_workspace(self, wkspace_name: str):
        """
        Returns the information concerning  a single workspace.

        :param str wkspace_name: name of the workspace whose info we want to retrieve.
        :return: workspace model instance.
        :rtype: Workspace or None.
        """

        url, action = self.get_workspace.REST
        url = url.format(wkspace_name=wkspace_name)
        response = action(self._api_url + url, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_workspace(response.json())

    @rest.REST.GET("/wkspaces/{wkspace_name}/update")
    def get_workspace_update_status(self, wkspace_name):
        """
        Returns whether workspace with given name is updated.

        :param str wkspace_name: name of the workspace whose status we want to retrieve.
        :return: True if workspace is updated; False otherwise.
        :rtype: bool
        """

        url, action = self.get_workspace_update_status.REST
        url = url.format(wkspace_name=wkspace_name)
        response = action(self._api_url + url, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_operation_status(response.json())

    @rest.REST.POST("/wkspaces/{wkspace_name}/update")
    def update_workspace(self, wkspace_name):
        """
        Updates workspace with given name.

        :param str wkspace_name: name of the workspace we want to update.
        :return: operation status model instance.
        :rtype: OperationStatus or None
        """

        url, action = self.update_workspace.REST
        url = url.format(wkspace_name=wkspace_name)
        response = action(self._api_url + url, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_operation_status(response.json())

    @rest.REST.GET("/wkspaces/{wkspace_name}/fileinfo/{file_path}")
    def get_file_info(self, wkspace_name, file_path):
        """
        Returns the info of the given file path within workspace.

        :param str wkspace_name: name of the workspace where the item we want to revert is located.
        :param str file_path: file path of the file we want to retrieve info for.
        :return: file info.
        :rtype: FileInfo
        """

        url, action = self.get_file_info.REST
        url = url.format(wkspace_name=wkspace_name, file_path=file_path.strip('/'))
        response = action(self._api_url + url, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_file_info(response.json())

    @rest.REST.POST("/wkspaces/{wkspace_name}/content/{item_path}")
    def add_workspace_item(self, wkspace_name, item_path, add_parents=True, checkout_parent=True, recurse=True):
        """
        Adds an item to version control.

        :param str wkspace_name: name of the workspace.
        :param str item_path: path of the item to be added.
        :param bool add_parents: whether to add any parent directories which are not under version control.
        :param bool checkout_parent: whether parent node of the item will be checked out as a result.
        :param bool recurse: whether all the children items should be recursively added.
        :return: paths that were affected by the addition operation.
        """

        url, action = self.add_workspace_item.REST
        params = {
            'addPrivateParents': add_parents,
            'checkoutParent': checkout_parent,
            'recurse': recurse
        }
        url = url.format(wkspace_name=wkspace_name, item_path=item_path.strip('/'))
        response = action(self._api_url + url, json=params, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_affected_paths(response.json())

    @rest.REST.PUT("/wkspaces/{wkspace_name}/content/{item_path}")
    def checkout_workspace_item(self, wkspace_name, item_path):
        """
        Marks workspace item as ready to modify.

        :param str wkspace_name: name of the workspace.
        :param str item_path: path of the item to checkout.
        :return: paths that were affected by the checkout operation.
        :rtype: AffectedPaths
        """

        url, action = self.checkout_workspace_item.REST
        url = url.format(wkspace_name=wkspace_name, item_path=item_path.strip('/'))
        response = action(self._api_url + url, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_affected_paths(response.json())

    @rest.REST.PATCH("/wkspaces/{wkspace_name}/content/{item_path}")
    def move_workspace_item(self, wkspace_name, item_path, dest_item_path):
        """
        Moves or renames a file or directory within a workspace.

        :param str wkspace_name: name of the workspace.
        :param str item_path: path of the item to move/rename.
        :param str dest_item_path: target path of the item.
        :return: paths that were affected by the checkout operation.
        :rtype: AffectedPaths
        """

        url, action = self.checkout_workspace_item.REST
        params = {
            'destination': dest_item_path
        }
        url = url.format(wkspace_name=wkspace_name, item_path=item_path.strip('/'))
        response = action(self._api_url + url, json=params, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_affected_paths(response.json())

    @rest.REST.PUT("/wkspaces/{wkspace_name}/revert/{item_path}")
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

        url, action = self.revert_item.REST
        params = {
            'changeset': int(changeset)
        }
        url = url.format(wkspace_name=wkspace_name, item_path=item_path)
        response = action(self._api_url + url, json=params, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_affected_paths(response.json())

    @rest.REST.POST("/wkspaces/{wkspace_name}/partialconfigure")
    def load_items(self, wkspace_name, items):
        """
        Loads all the given items.

        :param str wkspace_name: workspace name we want to load files to.
        :param list(str) items: list of absolute item paths to load.

        ..note:: the following items are supported:
            - file paths (to load specific files).
            - directories (directories will be loaded recursively).
        """

        # TODO: Check why this is not working
        url, action = self.load_items.REST
        params = {'instructions': list()}
        for item in items:
            params['instructions'].append({'path': item, 'action': 'load'})
        url = url.format(wkspace_name=wkspace_name)
        response = action(self._api_url + url, json=params, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_operation_status(response.json())

    @rest.REST.POST("/wkspaces/{wkspace_name}/partialconfigure")
    def unload_items(self, wkspace_name, items):
        """
        Unloads all the given items.

        :param str wkspace_name: workspace name we want to unload files from.
        :param list(str) items: list of items to unload.

        ..note:: the following items are supported:
            - file paths (to unload specific files).
            - directories (directories will be uloaded recursively).
        """

        # TODO: Check why this is not working
        url, action = self.unload_items.REST
        params = {'instructions': list()}
        for item in items:
            params['instructions'].append({'path': item, 'action': 'unload'})
        url = url.format(wkspace_name=wkspace_name)
        response = action(self._api_url + url, json=params, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_operation_status(response.json())

    # ============================================================================================================
    # ITEMS / CONTENTS
    # ============================================================================================================

    @rest.REST.GET("/repos/{repo_name}/branches/{branch_name}/contents/{item_path}")
    def get_item_in_branch(self, repo_name, branch_name, item_path):
        """
        Returns information about a single item in a branch within a repository.

        :param str repo_name: name of the repository where the item we want to retrieve info from is located.
        :param str branch_name: name of the branch we want to retrieve info item is located.
        :param str item_path: absolute path of the item we want to retrieve info for.
        :return: item model instance.
        :rtype: Item
        """

        url, action = self.get_item_in_branch.REST
        url = url.format(repo_name=repo_name, branch_name=branch_name.strip('/'), item_path=item_path.strip('/'))
        response = action(self._api_url + url, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_item(response.json())

    @rest.REST.GET("/repos/{repo_name}/revisions/{revision_id}")
    def get_item_revision(self, repo_name, revision_id):
        """
        Loads a single item's revision within the workspace and gets information about it.

        :param str repo_name: name of the repository where the item we want to retrieve info from is located.
        :param str revision_id: ID of the revision we want to retrieve info of.
        :return: desired item's revision will be returned.
        :rtype: Item
        """

        url, action = self.get_item_in_branch.REST
        url = url.format(repo_name=repo_name, revision_id=revision_id.strip('/'))
        response = action(self._api_url + url, verify=self._ssl_verify, timeout=self._timeout)
        return self._json_to_item(response.json())

    # ============================================================================================================
    # INTERNAL
    # ============================================================================================================

    def _json_to_repository(self, data):
        """
        Internal function that converts given repository data into a Repository model object.

        :param dict data: repository data retrieved from PlasticSCM REST API.
        :return: Repository model instance.
        :rtype: Repository
        """

        return model.Repository(
            name=data['name'], server=data['server'],
            owner=model.Owner(
                name=data['owner']['name'], is_group=data['owner']['isGroup']) if 'owner' in data else None,
            rep_id=model.RepId(
                id=data['repId']['id'], module_id=data['repId']['moduleId']) if 'repId' in data else None,
            guid=uuid.UUID('{' + data['guid'] + '}') if 'guid' in data else None
        )

    def _json_to_workspace(self, data):
        """
        Internal function that converts given workspace data into a Workspace model object.
         
        :param dict data: workspace data retrieved from PlasticSCM REST API. 
        :return: Workspace model instance.
        :rtype: Workspace
        """

        return model.Workspace(
            name=data['name'], path=os.path.normpath((data['path'])),
            machine_name=data['machineName'], guid=uuid.UUID('{' + data['guid'] + '}'))

    def _json_to_operation_status(self, data):
        """
        Internal function that converts given operation data into an Operation Status model object.

        :param dict data: operation status retrieved from PlasticSCM REST API.
        :return: Operation Status model instance.
        :rtype: OperationStatus
        """

        return model.OperationStatus(
            status=data.get('status'), message=data.get('message'), total_files=data.get('totalFiles'),
            total_bytes=data.get('totalBytes'), updated_files=data.get('updatedFiles'),
            updated_bytes=data.get('updatedBytes'))

    def _json_to_affected_paths(self, data):
        """
        Internal function that converts given revert info data into an Affected Paths model object.

        :param dict data: revert info retrieved from PlasticSCM REST API.
        :return: Revert Info model instance.
        :rtype: RevertInfo
        """

        return model.AffectedPaths(affected_paths=data.get('affectedPaths', list()))

    def _json_to_item(self, data):
        """
        Internal function that converts given item data into an Item model object.

        :param dict data: item retrieved from PlasticSCM REST API.
        :return: item model instance.
        :rtype: Item
        """

        return model.Item(
            type=next(item_type for item_type in model.Item.Type if item_type.value == data['type']), name=data['name'],
            path=data['path'], revision_id=data.get('revisionId'), size=data['size'],
            is_under_xlink=data.get('isUnderXlink'), content=data.get('content'), hash=data.get('hash'),
            items=[self._json_to_item(elem) for elem in data['items']] if 'items' in data else None,
            xlink_targets=model.XLink(
                changeset_id=data.get('xlinkTarget', dict()).get('changesetId'),
                changeset_guid=data.get('xlinkTarget', dict()).get('changesetGuid'),
                repo_name=data.get('xlinkTarget', dict()).get('repository'),
                server=data.get('xlinkTarget', dict()).get('server')),
            repository=self._json_to_repository(data['repository']) if 'repository' in data else None)

    def _json_to_file_info(self, data):
        """
        Internal function that converts given file info data into a FileInfo model object.

        :param dict data: file info retrieved from PlasticSCM REST API.
        :return: file info model instance.
        :rtype: FIleInfo
        """

        return model.FileInfo(client_path=data.get('clientPath', ''), relative_path=data.get('relativePath', ''),
                              server_path=data.get('serverPath', ''), rep_spec=data.get('repSpec', ''),
                              size=data.get('size'), hash=data.get('hash'), owner=data.get('owner', ''),
                              revision_head_changeset=data.get('revisionHeadChangeset'),
                              revision_changeset=data.get('revisionChangeset'), status=data.get('status'),
                              type=data.get('type'), changelist=data.get('changelist'))
