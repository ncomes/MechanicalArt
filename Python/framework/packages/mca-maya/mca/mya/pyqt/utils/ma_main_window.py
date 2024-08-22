"""
Module that contains functions and classes related with Maya GUI
"""

import sys
# Qt imports
from mca.common.pyqt.pygui import qtwidgets, qtcore, qtgui, shiboken

import maya.mel as mel
import pymel.core as pm
import maya.OpenMayaUI as OpenMayaUI

if sys.version_info >= (3,):
    long = int


def get_main_window():
    """
    Returns Maya main window through MEL
    """

    return mel.eval("$tempVar = $gMainWindow")


def to_qt_object(maya_name, qobj=None):
    """
    Returns an instance of the Maya UI element as a qtwidgets.QWidget
    """

    if not qobj:
        qobj = qtwidgets.QWidget
    ptr = OpenMayaUI.MQtUtil.findControl(maya_name)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout(maya_name)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findMenuItem(maya_name)
    if ptr is not None:
        return wrapinstance(long(ptr), qobj)
    return None


def to_maya_object(qobj):
    """
    Converts given Qt object to a Maya object.

    :param qtcore.QObject qobj: Qt object to convert.
    :return: Maya object name.
    :rtype: str
    """

    return OpenMayaUI.MQtUtil.fullName(long(shiboken.getCppPointer(qobj)[0]))


def get_maya_window(window_name=None, wrap_instance=True):
    """
    Return the Maya main window widget as a Python object
    :return: Maya Window
    """

    if wrap_instance:
        if window_name is not None:
            if '|' in str(window_name):
                # qt_obj = pm.uitypes.toQtObject(window_id)
                qt_obj = to_qt_object(window_name)
                if qt_obj is not None:
                    return qt_obj
            ptr = OpenMayaUI.MQtUtil.findControl(window_name)
            if ptr is not None:
                return wrapinstance(ptr, qtwidgets.QMainWindow)
        else:
            ptr = OpenMayaUI.MQtUtil.mainWindow()
            if ptr is not None:
                return wrapinstance(ptr, qtwidgets.QMainWindow)

    if isinstance(window_name, (qtwidgets.QWidget, qtwidgets.QMainWindow)):
        return window_name
    search = window_name or 'MayaWindow'
    for obj in qtwidgets.QApplication.topLevelWidgets():
        if obj.objectName() == search:
            return obj


def get_main_menu_menubar():
    """
    Returns Maya main menu bar object.

    :return: found Maya menu bar Qt widget.
    :rtype: qtwidgets.QMenuBar
    """

    win = get_maya_window()
    main_menu_bar = None
    for child in win.children():
        if isinstance(child, qtwidgets.QMenuBar):
            main_menu_bar = child

    return main_menu_bar


def wrapinstance(ptr, base=None):
    if ptr is None:
        return None
    try:
        ptr = int(ptr)
        if 'shiboken' in globals():
            if base is None:
                qobj = shiboken.wrapInstance(int(ptr), qtcore.QObject)
                meta_obj = qobj.metaObject()
                cls = meta_obj.className()
                super_cls = meta_obj.superClass().className()
                if hasattr(qtgui, cls):
                    base = getattr(qtgui, cls)
                elif hasattr(qtgui, super_cls):
                    base = getattr(qtgui, super_cls)
                else:
                    base = qtwidgets.QWidget
            try:
                return shiboken.wrapInstance(int(ptr), base)
            except Exception:
                from shiboken import wrapInstance
                return wrapInstance(int(ptr), base)
        elif 'sip' in globals():
            base = qtcore.QObject
            return shiboken.wrapinstance(int(ptr), base)
        else:
            print('Failed to wrap object ...')
            return None
    except:
        pass

def delete_window(window_name):
    """
    Deletes Maya window with given name.

    :param str window_name: name of the Maya window to delete.
    :return: True if the window deletion operation was successful; False otherwise.
    :rtype: bool
    """

    if pm.window(window_name, q=True, ex=True):
        pm.deleteUI(window_name)
        return True

    return False


def is_enable_workspace_control():
    """
    Returns whether or not workspace functionality is enabled.

    :return: True if workspace functionality is enabled; False otherwise.
    :rtype: bool
    """

    return int(pm.about(v=True)[:4]) > 2016


def delete_workspace_control(workspace_control):
    """
    Delets workspace control with given name.

    :param str workspace_control: name of the workspace control.
    :return: True if the workspace control deletion operation was successful; False otherwise.
    """

    if is_enable_workspace_control():
        if pm.workspaceControl(workspace_control, ex=True):
            pm.deleteUI(workspace_control)
            return True

    return False


def isolate_current_panel(add=False, *args):
    """
    Isolates current Maya gui panel.

    :param bool add:
    :param args:
    """

    panel = pm.paneLayout('viewPanes', query=True, pane1=True)
    state = pm.isolateSelect(panel, q=1, state=1)
    pm.editor(panel, e=1, mainListConnection="activeList")
    pm.isolateSelect(panel, loadSelected=1)
    pm.isolateSelect(panel, state=not state)
    if add:
        pm.editor(panel, e=1, unlockMainConnection=1)
    else:
        pm.editor(panel, e=1, lockMainConnection=1)


def refresh_outliner():
    """
    Force the refresh of the Maya outliner UI.
    """

    mel.eval('AEdagNodeCommonRefreshOutliners();')


def show_time_slider():
    """
    Shows Maya UI time slider.
    """

    mel.eval('setTimeSliderVisible 1;')


def hide_time_slider():
    """
    Hides Maya UI time slider.
    """

    mel.eval('setTimeSliderVisible 0;')


def is_time_slider_visible():
    """
    Returns whether or not time slider is visible within UI.

    :return: True if time slider is visible; False otherwise.
    :rtype: bool
    """

    playback_slider = mel.eval('$tmpVar=$gPlayBackSlider')
    is_visible = pm.timeControl(playback_slider, visible=True, query=True)
    is_obscured = pm.timeControl(playback_slider, isObscured=True, query=True)

    return True if is_visible and not is_obscured else False


def get_progress_bar():
    """
    Returns Maya progress bar object.

    :return: Maya progress bar object name.
    :rtype: str
    """

    main_progress_bar = mel.eval('$tmp = $gMainProgressBar')
    return main_progress_bar


def switch_xray_joints(state=True, panel=4, *args):
    """
    Switches xray joints.

    :param bool state: xray joints status.
    :param int panel: panel index.
    :param args:
    """

    if state:
        pm.modelEditor("modelPanel{}".format(panel), e=1, jx=state)
    else:
        currentState = pm.modelEditor("modelPanel{}".format(panel), q=1, jx=1)
        pm.modelEditor("modelPanel{}".format(panel), e=1, jx=not currentState)


def setup_axis(axis):
    """
    Updates all the model panels to match the correct view along axis
    axis: x or y

    Return: None
    """

    if axis not in ('y', 'z'):
        "{} is not a valid up axis. Please choose 'y' or 'z'".format(axis)
        return

    pm.upAxis(axis=axis, rv=True)
    model_panels = pm.getPanel(type='modelPanel')
    cameras = [pm.modelPanel(model_panel, q=True, camera=True) for model_panel in model_panels]
    for model_panel, camera in zip(model_panels, cameras):
        if camera == 'top':
            pm.viewSet(camera, viewNegativeY=True) if axis == 'y' else pm.viewSet(camera, viewNegativeZ=True)
        if camera == 'front':
            pm.viewSet(camera, viewNegativeZ=True) if axis == 'y' else pm.viewSet(camera, viewY=True)
        if camera == 'left' or camera == 'side':
            pm.viewSet(camera, viewNegativeX=True) if axis == 'y' else pm.viewSet(camera, viewNegativeX=True)
        if camera == 'right':
            pm.viewSet(camera, viewX=True) if axis == 'y' else pm.viewSet(camera, viewX=True)
        pm.viewLookAt(camera)
        pm.viewFit(camera, panel=model_panel, animate=False)


def get_node_editors():
    """
    Returns all node editors panels opened in Maya.

    :return: list of opened Maya node editor panels.
    :rtype: list(str)
    """

    found = list()
    for panel in pm.getPanel(type='scriptedPanel'):
        if pm.scriptedPanel(panel, query=True, type=True) == 'nodeEditorPanel':
            node_editor = panel + 'NodeEditorEd'
            found.append(node_editor)

    return found


def is_ui_suspended():
    """
    Returns whether UI is being suspended.

    :return: True if UI is suspended; False otherwise.
    :rtype: bool
    """

    if pm.about(batch=True):
        return True

    return pm.waitCursor(query=True, state=True)


def is_view_isolated(model_panel):
    """
    Returns whether given model panel is isolated.

    :param str model_panel: model panel name.
    :return: True if panel is isolated; False otherwise.
    :rtype: bool
    """

    state = False
    try:
        state = pm.isolateSelect(model_panel, query=True, state=True)
    except Exception:
        pass

    return state


def get_isolated_objects_for_model_panel(model_panel):
    """
    Returns all nodes that are being isolated in given model panel.

    :param str model_panel: model panel name.
    :return: list of isolated nodes in given model panel.
    :rtype: list(pm.nt.DagNode)
    """

    members = list()
    try:
        state = pm.isolateSelect(model_panel, query=True, state=True)
        view_objects = pm.isolateSelect(model_panel, query=True, viewObjects=True)
        if state and view_objects:
            members = pm.sets(view_objects, query=True)
    except Exception:
        pass

    return members


def add_isolated_objects_for_model_panel(model_panel, nodes):
    """
    Adds given nodes as isolated nodes into the given model panel.

    :param str model_panel: model panel name.
    :param list(DagNode) nodes: nodes to isolate.
    """

    selected = pm.ls(sl=True)
    pm.select(clear=True)
    if model_panel and nodes:
        pm.isolateSelect(model_panel, state=True)
        for n in nodes:
            if pm.objExists(n):
                pm.isolateSelect(model_panel, addDagObject=n)

    pm.isolateSelect(model_panel, update=True)
    if selected:
        pm.select(selected)


class ManageNodeEditors(object):
    """
    Class that allows to temporary turn off node editor panels and restore them when needed.
    """

    def __init__(self):
        self._node_editors = get_node_editors()
        self._additive_state_dict = dict()
        for editor in self._node_editors:
            current_value = pm.nodeEditor(editor, query=True, ann=True)
            self._additive_state_dict[editor] = current_value

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    @property
    def node_editors(self):
        return self._node_editors

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def turn_off_add_new_nodes(self):
        """
        Disables all currently opened node editors. This disables the possibility to add new nodes into them.
        """

        for editor in self._node_editors:
            pm.nodeEditor(editor, e=True, ann=False)

    def restore_add_new_nodes(self):
        """
        Restore opened node editor additive statuses.
        """

        for editor in self._node_editors:
            pm.nodeEditor(editor, e=True, ann=self._additive_state_dict[editor])


class SuspendUI(object):
    """
    Class that allow to handle the suspension of Maya UI.
    """

    AUTO_KEY_FRAME_STATE = False
    BATCH_MODE = None

    @classmethod
    def check_batch_mode(cls):
        """
        Returns whether batch mode is enabled.

        :return: True if batch mode is enabled; False otherwise.
        :rtype: bool
        """

        if cls.BATCH_MODE == None:
            cls.BATCH_MODE = pm.about(batch=True)

        return cls.BATCH_MODE

    @classmethod
    def set_batch_mode(cls, flag):
        """
        Sets whether batch mode is enabled.

        :param flag: True if batch mode is enabled; False otherwise.
        :rtype: bool
        """

        cls.BATCH_MODE = flag

    @classmethod
    def get_state(cls):
        """
        Returns whether UI is being suspended.

        :return: True if UI is suspended; False otherwise.
        :rtype: bool
        """

        return is_ui_suspended()

    @classmethod
    def set_state(cls, flag):
        """
        Sets whether UI should be suspended.

        :param flag: True to suspend Maya UI. False otherwise.
        """

        if cls.check_batch_mode():
            return
        if flag:
            cls.AUTO_KEY_FRAME_STATE = pm.autoKeyframe(query=True, state=True)
            pm.autoKeyframe(state=False)
            pm.waitCursor(state=True)
            pm.refresh(suspend=True)
        else:
            pm.autoKeyframe(state=cls.AUTO_KEY_FRAME_STATE)
            pm.waitCursor(state=False)
            pm.refresh(suspend=False)
