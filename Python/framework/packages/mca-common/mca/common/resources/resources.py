#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains mca-common-resources library API
"""

# mca python imports
import os
import pathlib
# Qt imports
from mca.common.pyqt.pygui import qtgui
# software specific imports
# mca python imports
from mca.common.project import paths
from mca.common.modifiers import singleton
from mca.common.startup.configs import consts
from mca.common import log
from mca.common.utils import path_utils

logger = log.MCA_LOGGER


class ResourceTypes:
    ICON = 'icon'
    PIXMAP = 'pixmap'
    IMAGE = 'image'


RESOURCE_IMAGE_TYPES = ['.png', '.bmp', '.svg', '.jpg', '.JPEG', '.JPG']


class MATResources(singleton.SimpleSingleton):
    """
    Handlers for icons, pixmaps, and images
    """

    def __init__(self):
        super().__init__()
        self.mat_resources = {'icon': {}, 'image': {}, 'pixmap': {}}

        self.register_icons()
        self.register_images()

    def register_icons(self):
        """
        Registers all icons and pixmaps in the icons folder
        """

        icon_paths = paths.get_icons_path()

        sub_dirs = path_utils.all_folders_in_directory(icon_paths)
        sub_dirs.append(icon_paths)

        for full_sub_dir in sub_dirs:
            sub_dir = os.path.relpath(full_sub_dir, icon_paths)
            images = [os.path.join(full_sub_dir, x) for x in os.listdir(full_sub_dir) if pathlib.Path(x).suffix in RESOURCE_IMAGE_TYPES]
            if not images:
                continue

            for image in images:
                # Build Dictionary
                image_name = f'{sub_dir}\\{os.path.basename(image)}'
                if sub_dir == '.':
                    image_name = os.path.basename(image)
                self.mat_resources[ResourceTypes.ICON][image_name] = {}
                self.mat_resources[ResourceTypes.ICON][image_name][ResourceTypes.ICON] = qtgui.QIcon(image)
                self.mat_resources[ResourceTypes.ICON][image_name][ResourceTypes.PIXMAP] = qtgui.QPixmap(image)

    def register_images(self):
        """
        Registers all images in the images folder
        """

        image_paths = paths.get_images_path()

        sub_dirs = path_utils.all_folders_in_directory(image_paths)

        for full_sub_dir in sub_dirs:
            sub_dir = os.path.relpath(full_sub_dir, image_paths)
            images = [os.path.join(full_sub_dir, x) for x in os.listdir(full_sub_dir) if
                      pathlib.Path(x).suffix in RESOURCE_IMAGE_TYPES]
            if not images:
                continue

            for image in images:
                # Build Dictionary
                image_name = os.path.normpath(f'{sub_dir}\\{os.path.basename(image)}')
                if sub_dir == '.':
                    image_name = os.path.basename(image)
                self.mat_resources[ResourceTypes.IMAGE][image_name] = {}
                self.mat_resources[ResourceTypes.IMAGE][image_name][ResourceTypes.IMAGE] = qtgui.QPixmap(image)


    def reset(self):
        """
        Resets all icons, images, and pixmaps
        """

        self.mat_resources = {'icon': {}, 'image': {}, 'pixmap': {}}
        self.register_icons()
        self.register_images()


def get_movies_path():
    """
    Returns the path to the movies folder

    :return:Returns the path to the movies folder
    :rtype: str
    """

    root_path = os.getenv(consts.MCA_RESOURCES_PATH)
    movie_path = os.path.join(root_path, 'movies')
    return movie_path


def icon(image_path, typ=ResourceTypes.ICON):
    """
    Returns the qtgui.QIcon for the given path

    :param image_path: the relative path to the image
    :return: Returns the qtgui.QIcon for the given path
    :rtype: qtgui.QIcon
    """

    mat_resources = MATResources()
    image_name = os.path.normpath(image_path)
    if image_name not in mat_resources.mat_resources[ResourceTypes.ICON]:
        logger.warning(f'Icon is not registered: {image_name}')
        return

    _icon = mat_resources.mat_resources[ResourceTypes.ICON][image_name].get(typ)
    if not _icon:
        logger.warning(f'Icon is not registered: Name: {image_name}: Type:{typ}')
        return icon(r'software\mat')
    return mat_resources.mat_resources[ResourceTypes.ICON][image_name].get(typ)


def pixmap(image_path, typ=ResourceTypes.PIXMAP):
    """
    Returns the qtgui.QPixmap for the given path

    :param image_path: the relative path to the image
    :return: Returns the qtgui.QPixmap for the given path
    :rtype: qtgui.QPixmap
    """

    mat_resources = MATResources()
    image_name = os.path.normpath(image_path)
    if image_name not in mat_resources.mat_resources[ResourceTypes.ICON]:
        logger.warning(f'Icon is not registered: {image_name}')
        return

    _icon = mat_resources.mat_resources[ResourceTypes.ICON][image_name].get(typ)
    if not _icon:
        logger.warning(f'Icon is not registered: Name: {image_name}: Type:{typ}')
        return icon(r'software\mat')
    return mat_resources.mat_resources[ResourceTypes.ICON][image_name].get(typ)


def image(image_path):
    """
    Returns the qtgui.QPixmap for the given path

    :param image_path: the relative path to the image
    :return: Returns the qtgui.QPixmap for the given path
    :rtype: qtgui.QPixmap
    """

    mat_resources = MATResources()
    image_name = os.path.normpath(image_path)
    if image_name not in mat_resources.mat_resources[ResourceTypes.IMAGE]:
        logger.warning(f'Icon is not registered: {image_name}')
        return
    return mat_resources.mat_resources[ResourceTypes.IMAGE][image_name][ResourceTypes.IMAGE]


def movie(name):
    if not '.gif' in name:
        name = f'{name}.gif'
    return os.path.join(get_movies_path(), name)


def register_resources():
    """
    Registers current resources paths.
    """

    MATResources()


def read_stylesheet(stylesheet):
    """
    Reads and Returns the stylesheet.
    
    :return: Returns the stylesheet.
    :rtype: str
    """
    
    stylesheet = stylesheet.split('.')[0]
    style_path = os.path.join(paths.get_stylesheet_path(), f'{stylesheet}.css')
    if os.path.isfile(style_path):
        with open(style_path, 'r') as f:
            return f.read()
    logger.warning('Unable to read style sheet {stylesheet}.  Path not found!')
    return


