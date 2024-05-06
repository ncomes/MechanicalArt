import inspect
import io
import os
import sys
import weakref

from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui
import maya.api.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

from mca.core import dcc

sys.dont_write_bytecode = True

IsAutomatedTest = os.environ.get('MAYA_UNREAL_LIVELINK_AUTOMATED_TESTS')
if IsAutomatedTest is None and dcc.is_maya() and dcc.get_version() == 2018:
    # To be able to add a script subfolder, we need to import this module to have __file__ be defined
    # We can then get the current path for this script, remove the filename and add the subfolder script name instead
    import MayaUnrealLiveLinkPluginUI
    def getBasePath():
        basePath = __file__
        basePath = basePath.replace('\\', '/')
        scriptPathIndex = basePath.rfind('/')
        if scriptPathIndex >= 0:
            basePath = basePath[:scriptPathIndex]
        return basePath
    def addPath(path):
        if (path in sys.path) is False:
            print('Adding ' + path + ' to system path')
            sys.path.append(path)
    basePath = MayaUnrealLiveLinkPluginUI.getBasePath()
    addPath(basePath)
    iconPath = basePath + '/icons'
    scriptPath = basePath + '/scripts'
    addPath(scriptPath)
    from UnrealLiveLinkController import UnrealLiveLinkController
    from UnrealLiveLinkWindow import UnrealLiveLinkWindow
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
    try:
      from shiboken2 import wrapInstance
    except ImportError:
      from shiboken import wrapInstance
    from PySide2.QtWidgets import QWidget, QVBoxLayout
    from PySide2.QtCore import QUrl, QJsonDocument, QJsonArray
    from PySide2.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkSession, QNetworkConfigurationManager, QNetworkReply
else:
    # Create dummy classes when running automated tests
    class MayaQWidgetDockableMixin():
        def __init__(self):
            pass
    class QWidget():
        def __init__(self):
            pass

MayaDockableWindow = None
MayaLiveLinkModel = None
NetworkAccessManager = None

# Base class for command (common creator method + allows for automatic
# register/unregister)
class LiveLinkCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    @classmethod
    def Creator(Cls):
        return OpenMayaMPx.asMPxPtr(Cls())


# Is supplied object a live link command
def IsLiveLinkCommand(InCls):
    return (
        inspect.isclass(InCls) and
        issubclass(InCls, LiveLinkCommand) and
        InCls != LiveLinkCommand)

# Given a list of strings of names return all the live link commands listed
def GetLiveLinkCommandsFromModule(ModuleItems):
    EvalItems = (eval(Item) for Item in ModuleItems)
    return [Command for Command in EvalItems if IsLiveLinkCommand(Command)]

class MayaUnrealLiveLinkDockableWindow(MayaQWidgetDockableMixin, QWidget):
    WindowName = 'MayaUnrealLiveLinkDockableWindow'
    WorkspaceControlName = WindowName + 'WorkspaceControl'

    def __init__(self, parent=None):
        super(MayaUnrealLiveLinkDockableWindow, self).__init__(parent=parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

class MayaUnrealLiveLinkModel():
    DefaultWidth = 650
    DefaultHeight = 450
    DefaultTopLeftCorner = [50, 50]
    UpdateURL = ""

    def __init__(self):
        self.Controller = None
        self.UnicastEndpoint = ''
        self.StaticEndpoints = []

    def __del__(self):
        if self.Controller:
            del self.Controller
            self.Controller = None

    def createController(self, dockableWindow=None, uiWindow=None):
        if self.Controller is None:
            self.Controller = UnrealLiveLinkController(self,
                                                       MayaUnrealLiveLinkDockableWindow.WindowName,
                                                       'Unreal Live Link',
                                                       iconPath,
                                                       dockableWindow if dockableWindow else MayaDockableWindow,
                                                       uiWindow)
        self.Controller.clearUI()

    def loadUISettings(self):
        w = MayaUnrealLiveLinkModel.DefaultWidth
        h = MayaUnrealLiveLinkModel.DefaultHeight
        tlc = MayaUnrealLiveLinkModel.DefaultTopLeftCorner
        windowName = MayaUnrealLiveLinkDockableWindow.WindowName

        if len(windowName) == 0:
            return tlc, w, h

        ## Check if the window settings already exist
        windowSettingsFound = cmds.windowPref(windowName, q=True, ex=True)

        if windowSettingsFound:
            # Read the window settings
            _w = cmds.windowPref(windowName, q=True, w=True)
            _h = cmds.windowPref(windowName, q=True, h=True)
            tlc = cmds.windowPref(windowName, q=True, tlc=True)
            if _w > 0:
                w = _w
            if _h > 0:
                h = _h
        else:
            cmds.windowPref(windowName)
            cmds.windowPref(windowName, e=True, w=w)
            cmds.windowPref(windowName, e=True, h=h)
            cmds.windowPref(windowName, e=True, tlc=tlc)
            cmds.windowPref(windowName, e=True, max=False)

        # We expect to receive [left, top] corners
        return [tlc[1], tlc[0]], w, h

    @staticmethod
    def addSelection():
        alreadyInList = cmds.LiveLinkAddSelection()
        return alreadyInList[0] if len(alreadyInList) > 0 else False

    @staticmethod
    def refreshSubjects():
        SubjectNames = cmds.LiveLinkSubjectNames()
        SubjectPaths = cmds.LiveLinkSubjectPaths()
        SubjectTypes = cmds.LiveLinkSubjectTypes()
        SubjectRoles = cmds.LiveLinkSubjectRoles()
        return [SubjectNames, SubjectPaths, SubjectTypes, SubjectRoles]

    @staticmethod
    def removeSubject(dagPath):
        cmds.LiveLinkRemoveSubject(dagPath)

    @staticmethod
    def changeSubjectName(dagPath, newName):
        cmds.LiveLinkChangeSubjectName(dagPath, newName)

    @staticmethod
    def changeSubjectRole(dagPath, newRole):
        cmds.LiveLinkChangeSubjectStreamType(dagPath, newRole)

    def getNetworkEndpoints(self):
        # Store the current endpoint settings.
        self.UnicastEndpoint = cmds.LiveLinkMessagingSettings(
            q=True, unicastEndpoint=True)
        self.StaticEndpoints = cmds.LiveLinkMessagingSettings(
            q=True, staticEndpoints=True)
        return { 'unicast' : self.UnicastEndpoint,
                 'static' : list(self.StaticEndpoints) }
    
    def setNetworkEndpoints(self, endpointsDict):
        # Apply new endpoint settings if they differ from the current
        # settings.
        NewUnicastEndpoint = endpointsDict['unicast']
        NewStaticEndpoints = endpointsDict['static']

        if NewUnicastEndpoint != self.UnicastEndpoint:
            cmds.LiveLinkMessagingSettings(
                NewUnicastEndpoint, unicastEndpoint=True)
            self.UnicastEndpoint = NewUnicastEndpoint

        if NewStaticEndpoints != self.StaticEndpoints:
            RemovedStaticEndpoints = list(
                set(self.StaticEndpoints) - set(NewStaticEndpoints))
            AddedStaticEndpoints = list(
                set(NewStaticEndpoints) - set(self.StaticEndpoints))

            if RemovedStaticEndpoints:
                cmds.LiveLinkMessagingSettings(
                    *RemovedStaticEndpoints, staticEndpoints=True,
                    removeEndpoint=True)
            if AddedStaticEndpoints:
                cmds.LiveLinkMessagingSettings(
                    *AddedStaticEndpoints, staticEndpoints=True,
                    addEndpoint=True)
            self.StaticEndpoints = NewStaticEndpoints

    @staticmethod
    def getDpiScale(size):
        return omui.MQtUtil.dpiScale(size)

    @staticmethod
    def isDocked():
        if cmds.workspaceControl(MayaUnrealLiveLinkDockableWindow.WorkspaceControlName, q=True, exists=True) and \
            (not cmds.workspaceControl(MayaUnrealLiveLinkDockableWindow.WorkspaceControlName, q=True, floating=True)):
            return True
        return False

    def getUpdateURL(self):
        return MayaUnrealLiveLinkModel.UpdateURL

    @staticmethod
    def getDocumentationURL():
        url = cmds.LiveLinkGetPluginDocumentationUrl()
        if url and isinstance(url, list) and len(url) > 0:
            return url[0]
        return ''

    @staticmethod
    def getPluginVersion():
        version = cmds.LiveLinkGetPluginVersion()
        app_version = ''
        if version and len(version) > 0:
            app_version = version[0]
        return app_version

    @staticmethod
    def getApiVersion():
        return str(cmds.about(apiVersion=True))

    @staticmethod
    def getUnrealVersion():
        version = cmds.LiveLinkGetUnrealVersion()
        app_version = ''
        if version and len(version) > 0:
            app_version = version[0]
        return app_version

    @staticmethod
    def getAboutText():
        filePath = basePath + '/../../docs/copyright.txt'
        if not os.path.exists(filePath):
            filePath = basePath + '/../../../resource/copyright.txt'
            if not os.path.exists(filePath):
                return ''
        try:
            with io.open(filePath, 'r', encoding='cp1252') as fr:
                text = fr.read()
                fr.close()
                if text and len(text) > 0:
                    return text
        except:
            print('Unable to read ' + filePath)
        return ''

    @staticmethod
    def handleVersionResponse(reply):
        er = reply.error()
        if er == QNetworkReply.NoError:
            # Get the plugin version
            app_version = MayaUnrealLiveLinkModel.getPluginVersion()

            # Get the plugin appstore id
            id = cmds.LiveLinkGetPluginAppId()
            app_id = ''
            if id and len(id) > 0:
                app_id = id[0]

            if len(app_version) == 0 or len(app_id) == 0:
                return

            # Read the network request and convert it to json for easier decoding
            bytes_string = reply.readAll()
            jsonResponse = QJsonDocument.fromJson(bytes_string)
            apps = jsonResponse.array()
            for i in range(apps.size()):
                app = apps.at(i).toObject()
                if 'app_id' in app:
                    # Check if the app id is our plugin's id
                    if app['app_id'] == app_id and 'app_version' in app:
                        version = app['app_version']
                        if not isinstance(version, str):
                            version = str(version)
                        versionSplit = version.split('.')
                        app_versionSplit = app_version.split('.')
                        minLen = min(len(versionSplit), len(app_versionSplit))

                        # Compare the versions to determine if the plugin from the appstore is newer
                        newer = False
                        for i in range(minLen):
                            try:
                                versionSplit[i] = int(versionSplit[i])
                                app_versionSplit[i] = int(app_versionSplit[i])
                                if versionSplit[i] != app_versionSplit[i]:
                                    if versionSplit[i] > app_versionSplit[i]:
                                        newer = True
                                    break
                            except:
                                pass

                        if newer or len(versionSplit) > len(app_versionSplit):
                            # If newer, get the plugin url on the appstore
                            url = cmds.LiveLinkGetPluginUpdateUrl()
                            if url and len(url) > 0:
                                MayaUnrealLiveLinkModel.UpdateURL = url[0]
                                if MayaLiveLinkModel and MayaLiveLinkModel.Controller:
                                    # Notify the UI there's an update
                                    MayaLiveLinkModel.Controller.notifyNewerUpdate()
                        break
        else:
            print("Error occured: ", er)
            print(reply.errorString())


def ShowUI(restore=False):
    if IsAutomatedTest:
        return

    global MayaDockableWindow

    # When the control is restoring, the workspace control has already been created and
    # all that needs to be done is restoring its UI.
    restoredControl = None
    if restore == True:
        # Grab the created workspace control with the following.
        restoredControl = omui.MQtUtil.getCurrentParent()
  
    if MayaDockableWindow is None:
        # Create a custom mixin widget for the first time
        MayaDockableWindow = MayaUnrealLiveLinkDockableWindow()
        MayaDockableWindow.setObjectName(MayaUnrealLiveLinkDockableWindow.WindowName)

        global MayaLiveLinkModel
        if not MayaLiveLinkModel:
            MayaLiveLinkModel = MayaUnrealLiveLinkModel()
            MayaLiveLinkModel.createController()

    if restore == True:
        # Add custom mixin widget to the workspace control
        mixinPtr = omui.MQtUtil.findControl(MayaDockableWindow.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(int(mixinPtr), int(restoredControl))
    else:
        # Create a workspace control for the mixin widget by passing all the needed parameters. See workspaceControl command documentation for all available flags.
        script = '''
import sys
sys.dont_write_bytecode = True
if ("{0}" in sys.path) is False:
    sys.path.append("{0}")
import MayaUnrealLiveLinkPluginUI
MayaUnrealLiveLinkPluginUI.ShowUI(restore=True)'''.format(basePath)
        MayaDockableWindow.setGeometry(0, 0, MayaUnrealLiveLinkModel.DefaultWidth, MayaUnrealLiveLinkModel.DefaultHeight)
        MayaDockableWindow.move(MayaUnrealLiveLinkModel.DefaultTopLeftCorner[0], MayaUnrealLiveLinkModel.DefaultTopLeftCorner[1])
        MayaDockableWindow.show(dockable=True, rp='MayaUnrealLiveLinkPluginUI', cp=True, uiScript=script)

def restoreModelFromWorkspaceControl():
    if IsAutomatedTest:
        return

    if cmds.workspaceControl(MayaUnrealLiveLinkDockableWindow.WorkspaceControlName, q=True, exists=True):
        deleteControl(MayaUnrealLiveLinkDockableWindow.WorkspaceControlName)
        cmd = MayaUnrealLiveLinkUI()
        cmd.doIt([])

# Command to create the Live Link UI
class MayaUnrealLiveLinkUI(LiveLinkCommand):
    def __init__(self):
        LiveLinkCommand.__init__(self)

    # Invoked when the command is run.
    def doIt(self, argList):
        if IsAutomatedTest:
            return

        if cmds.workspaceControl(MayaUnrealLiveLinkDockableWindow.WorkspaceControlName, q=True, exists=True) and \
           (not MayaDockableWindow):
            deleteControl(MayaUnrealLiveLinkDockableWindow.WorkspaceControlName)

        if not cmds.workspaceControl(MayaUnrealLiveLinkDockableWindow.WorkspaceControlName, q=True, exists=True):
            ShowUI()

        if MayaDockableWindow:
            if not cmds.workspaceControl(MayaUnrealLiveLinkDockableWindow.WorkspaceControlName, q=True, visible=True):
                MayaDockableWindow.show(dockable=True)

        if MayaLiveLinkModel and MayaLiveLinkModel.Controller:
            MayaLiveLinkModel.Controller.refreshUI()

# Command to Refresh the subject UI
class MayaUnrealLiveLinkRefreshUI(LiveLinkCommand):
    def __init__(self):
        LiveLinkCommand.__init__(self)

    # Invoked when the command is run.
    def doIt(self, argList):
        if MayaLiveLinkModel and MayaLiveLinkModel.Controller:
            MayaLiveLinkModel.Controller.clearUI()
            MayaLiveLinkModel.Controller.refreshUI()

# Command to Refresh the connection UI
class MayaUnrealLiveLinkRefreshConnectionUI(LiveLinkCommand):
    def __init__(self):
        LiveLinkCommand.__init__(self)

    # Invoked when the command is run.
    def doIt(self, argList):
        if MayaLiveLinkModel and MayaLiveLinkModel.Controller:
            # Get current connection status
            ConnectionText, ConnectedState = cmds.LiveLinkConnectionStatus()
            MayaLiveLinkModel.Controller.updateConnectionState(ConnectionText, ConnectedState)

# Grab commands declared
Commands = GetLiveLinkCommandsFromModule(dir())

AfterPluginUnloadCallbackId = None

def AfterPluginUnloadCallback(stringArray, clientData):
    for stringVal in stringArray:
        if MayaLiveLinkModel and MayaLiveLinkModel.Controller and stringVal.startswith('MayaUnrealLiveLinkPlugin'):
            MayaLiveLinkModel.Controller.clearSubjects()
            MayaLiveLinkModel.Controller.refreshSubjects()
            return

def deleteControl(control):
    if cmds.workspaceControl(control, q=True, exists=True):
        cmds.workspaceControl(control,e=True, close=True)
        cmds.deleteUI(control, control=True)

    global MayaLiveLinkModel
    if MayaLiveLinkModel:
        del MayaLiveLinkModel
        MayaLiveLinkModel = None

    global MayaDockableWindow
    if MayaDockableWindow:
        del MayaDockableWindow
        MayaDockableWindow = None

# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    print("LiveLink:")
    for Command in Commands:
        try:
            print("\tRegistering Command '%s'" % Command.__name__)
            mplugin.registerCommand(Command.__name__, Command.Creator)

        except Exception:
            sys.stderr.write(
                "Failed to register command: %s\n" % Command.__name__)
            raise

    if not cmds.about(batch=True):
       mel.eval("eval(\"source MayaUnrealLiveLinkPluginMenu.mel;\")")
       mel.eval('callbacks -addCallback \"AddMayaUnrealLiveLinkMenuItems\" -hook \"addItemToFileMenu\" -owner \"MayaUnrealLiveLinkPluginUI\"');

    restoreModelFromWorkspaceControl()

    global AfterPluginUnloadCallbackId
    AfterPluginUnloadCallbackId = \
        OpenMaya.MSceneMessage.addStringArrayCallback(
            OpenMaya.MSceneMessage.kAfterPluginUnload,
            AfterPluginUnloadCallback)

    if not IsAutomatedTest:
        id = cmds.LiveLinkGetPluginAppId()
        if id and len(id) > 0 and len(id[0]) > 0:
            global NetworkAccessManager
            NetworkAccessManager = QNetworkAccessManager()
            NetworkAccessManager.finished[QNetworkReply].connect(MayaUnrealLiveLinkModel.handleVersionResponse)
            url = cmds.LiveLinkGetPluginRequestUrl()
            if url and len(url) > 0:
                NetworkAccessManager.get(QNetworkRequest(QUrl(url[0])))

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    global AfterPluginUnloadCallbackId
    if AfterPluginUnloadCallbackId is not None:
        OpenMaya.MSceneMessage.removeCallback(AfterPluginUnloadCallbackId)
        AfterPluginUnloadCallbackId = None

    if not cmds.about(batch=True):
        mel.eval('callbacks -removeCallback \"AddMayaUnrealLiveLinkMenuItems\" -hook \"addItemToFileMenu\" -owner \"MayaUnrealLiveLinkPluginUI\"');
        mel.eval("eval(\"source MayaUnrealLiveLinkPluginMenu.mel; RemoveMayaUnrealLiveLinkMenuItems;\")")
 
    for Command in Commands:
        try:
            mplugin.deregisterCommand(Command.__name__)
        except Exception:
            sys.stderr.write(
                "Failed to unregister command: %s\n" % Command.__name__)

    if cmds.workspaceControl(MayaUnrealLiveLinkDockableWindow.WorkspaceControlName, q=True, ex=True):
        deleteControl(MayaUnrealLiveLinkDockableWindow.WorkspaceControlName)

    NetworkAccessManager = None

#-----BEGIN-SIGNATURE-----
# cgkAADCCCW4GCSqGSIb3DQEHAqCCCV8wgglbAgEBMQ8wDQYJKoZIhvcNAQELBQAw
# CwYJKoZIhvcNAQcBoIIHCjCCBwYwggTuoAMCAQICEA7/N6RkuCK7HKE4Q5jYf0Aw
# DQYJKoZIhvcNAQELBQAwaTELMAkGA1UEBhMCVVMxFzAVBgNVBAoTDkRpZ2lDZXJ0
# LCBJbmMuMUEwPwYDVQQDEzhEaWdpQ2VydCBUcnVzdGVkIEc0IENvZGUgU2lnbmlu
# ZyBSU0E0MDk2IFNIQTM4NCAyMDIxIENBMTAeFw0yMTA4MTgwMDAwMDBaFw0yMjA4
# MTgyMzU5NTlaMIGKMQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTET
# MBEGA1UEBxMKU2FuIFJhZmFlbDEXMBUGA1UEChMOQXV0b2Rlc2ssIEluYy4xHzAd
# BgNVBAsTFkRlc2lnbiBTb2x1dGlvbnMgR3JvdXAxFzAVBgNVBAMTDkF1dG9kZXNr
# LCBJbmMuMIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAuAzqArC2+9vr
# xjAsi3/l9j5OMdehHwuowSa3HED56fUQUcm7hWA9ymZqA1uoMNTzUMFOuY//9ZJz
# bkwpVnbZ/P5mRtTkhWejwdTr8h+NN8b27/Wqi/OTK3wSUsjzqIAqqTA7MweluNIe
# RNP6cGASMRIYWXVc1aEc0TqR9+hVDLGEaeK7eBirqsZW9mpoHxEC8QY6TMTAYify
# ynE/j8haEd0hsl/JP93vi5CXpMcHuwRJHucbzpEoM+xtNRn3hXXf8Rhb6iimoMgr
# wdAn47cOaSARsEzH058odyj4jDjWRiStSfuoa8gQaIkcsDw9r9+HTF69Nlk+GFCb
# nf3mWFAwy8oLElRl7CRDhj2aJesu+eeCM+YaxkI8nYZ9FWAAylo8rOwGgtK9ji8P
# WXckvOCsMynCynmudV0pJcSnnlgzIXueblCUp6haRhwMoyWrVVukhFO7gxd/Ti2/
# ibUF3S1aaxMpB0jhs9jaj52aCjb0SIyfo8ePlhsQ5GOQrCDf1rj1AgMBAAGjggIG
# MIICAjAfBgNVHSMEGDAWgBRoN+Drtjv4XxGG+/5hewiIZfROQjAdBgNVHQ4EFgQU
# 14TPWwN/dEdUdTlczmk/joQs8okwDgYDVR0PAQH/BAQDAgeAMBMGA1UdJQQMMAoG
# CCsGAQUFBwMDMIG1BgNVHR8Ega0wgaowU6BRoE+GTWh0dHA6Ly9jcmwzLmRpZ2lj
# ZXJ0LmNvbS9EaWdpQ2VydFRydXN0ZWRHNENvZGVTaWduaW5nUlNBNDA5NlNIQTM4
# NDIwMjFDQTEuY3JsMFOgUaBPhk1odHRwOi8vY3JsNC5kaWdpY2VydC5jb20vRGln
# aUNlcnRUcnVzdGVkRzRDb2RlU2lnbmluZ1JTQTQwOTZTSEEzODQyMDIxQ0ExLmNy
# bDA+BgNVHSAENzA1MDMGBmeBDAEEATApMCcGCCsGAQUFBwIBFhtodHRwOi8vd3d3
# LmRpZ2ljZXJ0LmNvbS9DUFMwgZQGCCsGAQUFBwEBBIGHMIGEMCQGCCsGAQUFBzAB
# hhhodHRwOi8vb2NzcC5kaWdpY2VydC5jb20wXAYIKwYBBQUHMAKGUGh0dHA6Ly9j
# YWNlcnRzLmRpZ2ljZXJ0LmNvbS9EaWdpQ2VydFRydXN0ZWRHNENvZGVTaWduaW5n
# UlNBNDA5NlNIQTM4NDIwMjFDQTEuY3J0MAwGA1UdEwEB/wQCMAAwDQYJKoZIhvcN
# AQELBQADggIBAKTucYhaf0sXqcTZOpbrbYwCQUKdWwX+8V2NeRSGPh2gk29TL0MP
# +/k8qgs9B5wC5nq2KPXL8hdz183rpO72/gED0XK5r7DJgB9eTGa+BxuMfsE97LFZ
# tIqDXJWCDoS/G+ZVHYKEGDdT43nuk0K+ra5rjxZy4jDnnkIASD+MH1y8ud10c7kw
# xYfl4ysWV1JnvCer9VDPdXEoh2okR7X4rtpQqi/AJA/SKoYf5pbijQNaSbD8LrUk
# 8j7Z8taN6dzMbLNg4gavAvy/6neKbegOSmC2JQPb2veesIB6MBwXFU/8abmj2AEC
# lcPibrSUn1vUM6rTesFC9SqSMJi+W/63WpCRMHy6/8Jsff6ObiWH9w65qrMWPHL/
# HNGIRFDxhlrE56H0Y/7uTyxsTDVfJ3ja3SWx+Azw8K4recSSu4mm0+FheZl3vWCG
# hu29bqt1V0VFe2QYG4gfmQ+XkR1ixNU6yCCKycZAQc1yIR/uwYKA0VSm5GCzgGMZ
# 3dlHKPULN6pTbWSO+7QxEEhApKxkrnhhM+xY7gTHoG9eqXChRugs/BOhnStk37H1
# e50pVBwQCheEhcqD3NP6T/5VonYXpXbGxo4tWBMd94BXDFmTzbLWzNXDRPpXaJ30
# nItudoFjc+KvLntsqh6Vu2vZbp4UybkzrBMEAq+MyuwC3cMH0HDVhVgBMYICKDCC
# AiQCAQEwfTBpMQswCQYDVQQGEwJVUzEXMBUGA1UEChMORGlnaUNlcnQsIEluYy4x
# QTA/BgNVBAMTOERpZ2lDZXJ0IFRydXN0ZWQgRzQgQ29kZSBTaWduaW5nIFJTQTQw
# OTYgU0hBMzg0IDIwMjEgQ0ExAhAO/zekZLgiuxyhOEOY2H9AMA0GCSqGSIb3DQEB
# CwUAMA0GCSqGSIb3DQEBAQUABIIBgKB+0jR/icjEPzokfpzcCiL07auPmd3Sb+x/
# o7K5EOauOM2uiylCQA6zaQrhUphggeGSUWei/9wapbtENojZEb7mA+1JVfwd7evQ
# utqu9OYO4HPwcRydLwVVAsVFmEqYmLqcg8k1ntrVOsb8jTpOrHG950SRCD83TWMi
# DS+LNey2g4Dn6h9yrTE56BTOYSgOZu55Vt+wAUQujNyiIca8Vfy9w2q5ZCBmC8Kn
# moaVHDtX6utc+7jDO4hSErHRyPDGPnHYArCS7Th3tolXGBdOeNQZrK52e40F6277
# 7JfXdQ9jM9ULomuS2mfUxjoVC8b41SReZaXonxADwUh/CW5mT3rKYutUpDk/tnx4
# aEW3Sx85JM/QzBDMyBvJwTbFlgAs4vYYMZa5XVcQJ2mz9BbL/cxaNWZLeBZCmz+S
# TokRPElMZgrVgSAnp3ngQU/A6EGtdVyfBsgX4J5jLGYLNi6+pCOsPwHPHzway9Z/
# qoj3VlxUZHmDqLXjN+mb/jbME3AwsQ==
# -----END-SIGNATURE-----