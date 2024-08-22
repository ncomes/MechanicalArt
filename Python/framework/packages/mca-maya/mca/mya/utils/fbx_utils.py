#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related with Maya FBX library
"""

from __future__ import print_function, division, absolute_import

import os

import maya.mel as mel
import pymel.core as pm

from mca.common import log

from mca.common.utils import fileio
from mca.mya.animation import time_utils
from mca.mya.modifiers import ma_decorators
from mca.mya.utils import namespace_utils

logger = log.MCA_LOGGER


@ma_decorators.keep_namespace_decorator
def import_fbx(fbx_path, import_namespace=None):
    """
    Import a given FBX file. If it contains several animation clips it will only import the last.

    :param str fbx_path: A path to a given FBX file.
    :param str import_namespace: If the imported data should be organized under a namespace.
    :return: A list of all imported files. If an import namespace was given it will only return the new subset of nodes.
    :rtype: list[PyNode]
    """

    # $HACK HUGE FUCKING HACK.
    # Improting an FBX will overwrite attr values sometimes. Notable occurs on the root joint.
    # I shouldn't have to put this here but fucking Autodesk can't keep their shit together.
    root_path_list = []
    for root_joint in pm.ls('*.skel_path', o=True):
        root_path_list.append([root_joint, root_joint.skel_path.get()])

    if not os.path.exists(fbx_path):
        raise f'File not found at: {fbx_path}'
    # Note path conversion for FBX calls, for whatever reason this needs to be the style.
    formatted_path = os.path.normpath(fbx_path).replace('\\', '/')
    # need to make sure we're in the root namespace or we'll have problems on import.
    pm.namespace(set=':')
    original_node_list = set(pm.ls('*'))
    FBXImportMode(v="add")
    FBXImportShapes(v=True)
    FBXImportSkins(v=True)
    FBXImportCacheFile(v=True)
    FBXImportGenerateLog(v=False)
    FBXImport(f=formatted_path, t=-1)
    imported_node_list = set(pm.ls('*'))
    return_list = list(imported_node_list-original_node_list)
    if import_namespace:
        for x in return_list:
            namespace_utils.move_node_to_namespace(x, import_namespace)
    
    # $HACK HUGE FUCKING HACK.
    for root_joint, skel_path in root_path_list:
        root_joint.skel_path.set(skel_path)
    return return_list


def export_fbx(fbx_path, node_list, clip_name=None, start_frame=None, end_frame=None):
    """
    Export the passed nodes to an FBX file.

    :param str fbx_path: A path to a given FBX file.
    :param list[PyNode] node_list: A list of nodes to be exported.
    :param str clip_name: If we're exporting animation what we should call the clip associated with this file.
        NOTE: The FBX format can support multiple clips per FBX. We will not be supporting that here.
    :param int start_frame: The starting frame of the animation if we're slicing the file.
    :param int end_frame: The last frame of the animation if we're slicing the file.
        NOTE: If either a start or end frame are not passed we'll use our best guess.
    """

    fileio.touch_path(fbx_path)
    formatted_path = os.path.normpath(fbx_path).replace('\\', '/')
    FBXExportGenerateLog(v=False)
    FBXExportAnimationOnly(v=False)
    FBXExportShapes(v=True)
    FBXExportSkins(v=True)
    FBXExportSmoothingGroups(v=True)
    FBXExportSplitAnimationIntoTakes(clear=True)
    FBXExportDeleteOriginalTakeOnSplitAnimation(v=True)
    if clip_name:
        if not start_frame or not end_frame:
            time_range = time_utils.get_times()
            start_frame = time_range[0] if start_frame is None else start_frame
            end_frame = time_range[1] if end_frame is None else end_frame
        FBXExportBakeComplexStart(v=start_frame)
        FBXExportBakeComplexEnd(v=end_frame)
        FBXExportSplitAnimationIntoTakes(start_frame, end_frame, v=clip_name)
    pm.select(node_list)
    FBXExport(f=formatted_path, s=True)
    FBXExportSplitAnimationIntoTakes(clear=True)


def load_fbx(version_string):
    """
    Loads FBX plugin.

    :param str version_string: FBX plugin string version.
    :return: True if FBX plugin was loaded successfully; False otherwise.
    :rtype: bool
    """

    pm.loadPlugin('fbxmaya.mll', quiet=True),
    plugin_is_loaded = pm.pluginInfo('fbxmaya.mll', q=True, v=True) == version_string

    assert plugin_is_loaded


def assert_property(prop_name, value):
    """
    Quickly FBX property asset.

    :param str prop_name: FBX property name.
    :param any value: FBX property value.
    """

    assert FBXProperty(prop_name, q=True) == value


def _FBXCmd(_CMD, *args, **kwargs):
    """
    Internal command that parses the FBX command arguments into MEL strings.

    :param _CMD:
    :param args:
    :param kwargs:
    :return:
    """

    # format strings with quotes
    arg_string = ''
    for value in args:
        local_str = f'"{value}" ' if isinstance(value, str) else f'{value} '
        arg_string += local_str

    # special case -q for compatibility with python API
    kwargs_string = ''
    for key, value in kwargs.items():
        value = f'"{value}"' if isinstance(value, str) else value
        local_str = f'-{key} ' if key in ['q', 'clear'] else f'-{key} {value} '
        kwargs_string += local_str

    kwargs_string = kwargs_string.replace('True', 'true').replace('False', 'false')
    arg_string = arg_string.replace('True', 'true').replace('False', 'false')

    command = f'{_CMD} {kwargs_string} {arg_string};'
    return mel.eval(command)


def FBXImport(*args, **kwargs):
    return _FBXCmd("FBXImport", *args, **kwargs)


def FBXExport(*args, **kwargs):
    return _FBXCmd("FBXExport", *args, **kwargs)


def FBXExportTriangulate(*args, **kwargs):
    return _FBXCmd("FBXExportTriangulate", *args, **kwargs)


def FBXResetImport(*args, **kwargs):
    return _FBXCmd("FBXResetImport", *args, **kwargs)


def FBXResetExport(*args, **kwargs):
    return _FBXCmd("FBXResetExport", *args, **kwargs)


def FBXLoadImportPresetFile(*args, **kwargs):
    return _FBXCmd("FBXLoadImportPresetFile", *args, **kwargs)


def FBXLoadExportPresetFile(*args, **kwargs):
    return _FBXCmd("FBXLoadExportPresetFile", *args, **kwargs)


def FBXImportShowUI(*args, **kwargs):
    return _FBXCmd("FBXImportShowUI", *args, **kwargs)


def FBXImportGenerateLog(*args, **kwargs):
    return _FBXCmd("FBXImportGenerateLog", *args, **kwargs)


def FBXImportMode(*args, **kwargs):
    return _FBXCmd("FBXImportMode", *args, **kwargs)


def FBXImportMergeBackNullPivots(*args, **kwargs):
    return _FBXCmd("FBXImportMergeBackNullPivots", *args, **kwargs)


def FBXImportConvertDeformingNullsToJoint(*args, **kwargs):
    return _FBXCmd("FBXImportConvertDeformingNullsToJoint", *args, **kwargs)


def FBXImportHardEdges(*args, **kwargs):
    return _FBXCmd("FBXImportHardEdges", *args, **kwargs)


def FBXImportUnlockNormals(*args, **kwargs):
    return _FBXCmd("FBXImportUnlockNormals", *args, **kwargs)


def FBXImportProtectDrivenKeys(*args, **kwargs):
    return _FBXCmd("FBXImportProtectDrivenKeys", *args, **kwargs)


def FBXImportMergeAnimationLayers(*args, **kwargs):
    return _FBXCmd("FBXImportMergeAnimationLayers", *args, **kwargs)


def FBXImportResamplingRateSource(*args, **kwargs):
    return _FBXCmd("FBXImportResamplingRateSource", *args, **kwargs)


def FBXImportSetMayaFrameRate(*args, **kwargs):
    return _FBXCmd("FBXImportSetMayaFrameRate", *args, **kwargs)


def FBXImportQuaternion(*args, **kwargs):
    return _FBXCmd("FBXImportQuaternion", *args, **kwargs)


def FBXImportSetLockedAttribute(*args, **kwargs):
    return _FBXCmd("FBXImportSetLockedAttribute", *args, **kwargs)


def FBXImportAxisConversionEnable(*args, **kwargs):
    return _FBXCmd("FBXImportAxisConversionEnable", *args, **kwargs)


def FBXImportScaleFactorEnable(*args, **kwargs):
    return _FBXCmd("FBXImportScaleFactorEnable", *args, **kwargs)


def FBXImportScaleFactor(*args, **kwargs):
    return _FBXCmd("FBXImportScaleFactor", *args, **kwargs)


def FBXImportUpAxis(*args, **kwargs):
    return _FBXCmd("FBXImportUpAxis", *args, **kwargs)


def FBXImportAutoAxisEnable(*args, **kwargs):
    return _FBXCmd("FBXImportAutoAxisEnable", *args, **kwargs)


def FBXImportForcedFileAxis(*args, **kwargs):
    return _FBXCmd("FBXImportForcedFileAxis", *args, **kwargs)


def FBXImportCacheFile(*args, **kwargs):
    return _FBXCmd("FBXImportCacheFile", *args, **kwargs)


def FBXImportSkins(*args, **kwargs):
    return _FBXCmd("FBXImportSkins", *args, **kwargs)


def FBXImportShapes(*args, **kwargs):
    return _FBXCmd("FBXImportShapes", *args, **kwargs)


def FBXImportCameras(*args, **kwargs):
    return _FBXCmd("FBXImportCameras", *args, **kwargs)


def FBXImportLights(*args, **kwargs):
    return _FBXCmd("FBXImportLights", *args, **kwargs)


def FBXImportFillTimeline(*args, **kwargs):
    return _FBXCmd("FBXImportFillTimeline", *args, **kwargs)


def FBXImportConstraints(*args, **kwargs):
    return _FBXCmd("FBXImportConstraints", *args, **kwargs)


def FBXImportCharacter(*args, **kwargs):
    return _FBXCmd("FBXImportCharacter", *args, **kwargs)


def FBXExportShowUI(*args, **kwargs):
    return _FBXCmd("FBXExportShowUI", *args, **kwargs)

def FBXExportSplitAnimationIntoTakes(*args, **kwargs):
    return _FBXCmd("FBXExportSplitAnimationIntoTakes", *args, **kwargs)

def FBXExportDeleteOriginalTakeOnSplitAnimation(*args, **kwargs):
    return _FBXCmd("FBXExportDeleteOriginalTakeOnSplitAnimation", *args, **kwargs)

def FBXExportGenerateLog(*args, **kwargs):
    return _FBXCmd("FBXExportGenerateLog", *args, **kwargs)


def FBXExportFileVersion(*args, **kwargs):
    return _FBXCmd("FBXExportFileVersion", *args, **kwargs)


def FBXExportApplyConstantKeyReducer(*args, **kwargs):
    return _FBXCmd("FBXExportApplyConstantKeyReducer", *args, **kwargs)


def FBXExportQuaternion(*args, **kwargs):
    return _FBXCmd("FBXExportQuaternion", *args, **kwargs)


def FBXExportSkins(*args, **kwargs):
    return _FBXCmd("FBXExportSkins", *args, **kwargs)


def FBXExportShapes(*args, **kwargs):
    return _FBXCmd("FBXExportShapes", *args, **kwargs)


def FBXExportCameras(*args, **kwargs):
    return _FBXCmd("FBXExportCameras", *args, **kwargs)


def FBXExportLights(*args, **kwargs):
    return _FBXCmd("FBXExportLights", *args, **kwargs)


def FBXExportInstances(*args, **kwargs):
    return _FBXCmd("FBXExportInstances", *args, **kwargs)


def FBXExportReferencedContainersContent(*args, **kwargs):
    return _FBXCmd("FBXExportReferencedContainersContent", *args, **kwargs)


def FBXExportBakeComplexStart(*args, **kwargs):
    return _FBXCmd("FBXExportBakeComplexStart", *args, **kwargs)


def FBXExportBakeComplexEnd(*args, **kwargs):
    return _FBXCmd("FBXExportBakeComplexEnd", *args, **kwargs)


def FBXExportBakeComplexStep(*args, **kwargs):
    return _FBXCmd("FBXExportBakeComplexStep", *args, **kwargs)


def FBXExportEmbeddedTextures(*args, **kwargs):
    return _FBXCmd("FBXExportEmbeddedTextures", *args, **kwargs)


def FBXExportConvert2Tif(*args, **kwargs):
    return _FBXCmd("FBXExportConvert2Tif", *args, **kwargs)


def FBXExportInAscii(*args, **kwargs):
    return _FBXCmd("FBXExportInAscii", *args, **kwargs)


def FBXExportBakeComplexAnimation(*args, **kwargs):
    return _FBXCmd("FBXExportBakeComplexAnimation", *args, **kwargs)


def FBXExportBakeResampleAnimation(*args, **kwargs):
    return _FBXCmd("FBXExportBakeResampleAnimation", *args, **kwargs)


def FBXExportUseSceneName(*args, **kwargs):
    return _FBXCmd("FBXExportUseSceneName", *args, **kwargs)


def FBXExportAnimationOnly(*args, **kwargs):
    return _FBXCmd("FBXExportAnimationOnly", *args, **kwargs)


def FBXExportHardEdges(*args, **kwargs):
    return _FBXCmd("FBXExportHardEdges", *args, **kwargs)


def FBXExportTangents(*args, **kwargs):
    return _FBXCmd("FBXExportTangents", *args, **kwargs)


def FBXExportSmoothMesh(*args, **kwargs):
    return _FBXCmd("FBXExportSmoothMesh", *args, **kwargs)


def FBXExportSmoothingGroups(*args, **kwargs):
    return _FBXCmd("FBXExportSmoothingGroups", *args, **kwargs)


def FBXExportFinestSubdivLevel(*args, **kwargs):
    return _FBXCmd("FBXExportFinestSubdivLevel", *args, **kwargs)


def FBXExportInputConnections(*args, **kwargs):
    return _FBXCmd("FBXExportInputConnections", *args, **kwargs)


def FBXExportConstraints(*args, **kwargs):
    return _FBXCmd("FBXExportConstraints", *args, **kwargs)


def FBXExportCharacter(*args, **kwargs):
    return _FBXCmd("FBXExportCharacter", *args, **kwargs)


def FBXExportCacheFile(*args, **kwargs):
    return _FBXCmd("FBXExportCacheFile", *args, **kwargs)


def FBXExportQuickSelectSetAsCache(*args, **kwargs):
    return _FBXCmd("FBXExportQuickSelectSetAsCache", *args, **kwargs)


def FBXExportColladaTriangulate(*args, **kwargs):
    return _FBXCmd("FBXExportColladaTriangulate", *args, **kwargs)


def FBXExportColladaSingleMatrix(*args, **kwargs):
    return _FBXCmd("FBXExportColladaSingleMatrix", *args, **kwargs)


def FBXExportColladaFrameRate(*args, **kwargs):
    return _FBXCmd("FBXExportColladaFrameRate", *args, **kwargs)


def FBXResamplingRate(*args, **kwargs):
    return _FBXCmd("FBXResamplingRate", *args, **kwargs)


def FBXRead(*args, **kwargs):
    return _FBXCmd("FBXRead", *args, **kwargs)


def FBXGetTakeCount(*args, **kwargs):
    return _FBXCmd("FBXGetTakeCount", *args, **kwargs)


def FBXGetTakeIndex(*args, **kwargs):
    return _FBXCmd("FBXGetTakeIndex", *args, **kwargs)


def FBXGetTakeName(*args, **kwargs):
    return _FBXCmd("FBXGetTakeName", *args, **kwargs)


def FBXGetTakeComment(*args, **kwargs):
    return _FBXCmd("FBXGetTakeComment", *args, **kwargs)


def FBXGetTakeLocalTimeSpan(*args, **kwargs):
    return _FBXCmd("FBXGetTakeLocalTimeSpan", *args, **kwargs)


def FBXGetTakeReferenceTimeSpan(*args, **kwargs):
    return _FBXCmd("FBXGetTakeReferenceTimeSpan", *args, **kwargs)


def FBXConvertUnitString(*args, **kwargs):
    return _FBXCmd("FBXConvertUnitString", *args, **kwargs)


def FBXImportConvertUnitString(*args, **kwargs):
    return _FBXCmd("FBXImportConvertUnitString", *args, **kwargs)


def FBXExportConvertUnitString(*args, **kwargs):
    return _FBXCmd("FBXExportConvertUnitString", *args, **kwargs)


def FBXExportAxisConversionMethod(*args, **kwargs):
    return _FBXCmd("FBXExportAxisConversionMethod", *args, **kwargs)


def FBXExportUpAxis(*args, **kwargs):
    return _FBXCmd("FBXExportUpAxis", *args, **kwargs)


def FBXExportScaleFactor(*args, **kwargs):
    return _FBXCmd("FBXExportScaleFactor", *args, **kwargs)


def FBXProperties(*args, **kwargs):
    return _FBXCmd("FBXProperties", *args, **kwargs)


def FBXProperty(*args, **kwargs):
    '''
    Wraps the FBXProperty command, which is unusually useful but needs special argument formatting
    '''
    if kwargs.get('q', False):
        # special case query here because FBX is stupid
        args = (args[0], "-q")
        return _FBXCmd("FBXProperty", *args)
    elif not kwargs.get("v", None) is None:
        quoted = lambda p: '"%s"' % p if str(p) == p else str(p)  # format strings with quotes
        # args = (quoted(args[0]) +  (" -v %s" % quoted(kwargs.get('v')) ), )
        #kwargs[''] = quoted(args[0])

        return _FBXCmd('FBXProperty  "%s"' % args[0], **kwargs)


def FBXExportUseTmpFilePeripheral(*args, **kwargs):
    return _FBXCmd("FBXExportUseTmpFilePeripheral", *args, **kwargs)


def FBXUICallBack(*args, **kwargs):
    return _FBXCmd("FBXUICallBack", *args, **kwargs)


def FBXUIShowOptions(*args, **kwargs):
    return _FBXCmd("FBXUIShowOptions", *args, **kwargs)