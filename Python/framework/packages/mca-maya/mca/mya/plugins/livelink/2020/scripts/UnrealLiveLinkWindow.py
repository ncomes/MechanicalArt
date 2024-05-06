import os

try:
  from PySide2.QtCore import *
  from PySide2.QtGui import *
  from PySide2.QtWidgets import *
  from PySide2 import __version__
except ImportError:
  from PySide.QtCore import *
  from PySide.QtGui import *
  from PySide import __version__

from UnrealLiveLinkSubjectTable import *
from UnrealLiveLinkSettings import *
from UnrealLiveLinkAboutDialog import *

class ButtonHoverWatcher(QObject):
    def __init__(self, iconName, parent=None):
        super(ButtonHoverWatcher, self).__init__(parent)
        self.LeaveIcon = UnrealLiveLinkWindow.createIcon(iconName)
        if self.LeaveIcon:
            hoverIcon = QIcon(UnrealLiveLinkWindow.highlightPixmap(self.LeaveIcon.pixmap(32, 32)))
            self.HoverIcon = hoverIcon
        else:
            self.HoverIcon = None

    def eventFilter(self, watched, event):
        button = watched
        if button is None:
            return False

        if event.type() == QEvent.Enter and self.HoverIcon:
            button.setIcon(self.HoverIcon)
            return True
        elif event.type() == QEvent.Leave and self.LeaveIcon:
            button.setIcon(self.LeaveIcon)
            return True
        return False

class UnrealLiveLinkWindow(QWidget):
    iconPath = ''

    PushButtonStyleSheet = '''QPushButton { border: 1px }
                              QPushButton:hover:pressed { background-color: rgb(48, 48, 48); }'''

    def __init__(self, controller, windowName, windowTitle, parent):
        self.mainLayout = None

        super(UnrealLiveLinkWindow, self).__init__()
        if parent:
            if parent.layout():
                parent.layout().addWidget(self)
        else:
            self.setWindowFlags(Qt.Window)
            self.setObjectName(windowName if windowName else 'UnrealLiveLinkWindow')

        self._properties = dict()
        self.ConnectedState = False
        self.Controller = weakref.proxy(controller)
        self.ConnectedPicture = None
        self.DisconnectedPicture = None

        if parent and windowTitle:
            parent.setWindowTitle(windowTitle)

    def __del__(self):
        self.Controller = None

    @staticmethod
    def setIconPath(path):
        UnrealLiveLinkWindow.iconPath = path

    def openHelpUrl(self):
        docUrl = self.Controller.getDocumentationURL()
        if docUrl and (isinstance(docUrl, str) or isinstance(docUrl, unicode)) and len(docUrl) > 0:
            url = QUrl(docUrl)
            if QDesktopServices.openUrl(url):
                return
        QMessageBox.warning(self, 'Open Url', 'Could not open ' + docUrl)

    def openReportProblemUrl(self):
        url = QUrl('https://www.autodesk.com/company/contact-us/product-feedback')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Url', 'Could not open ' + url.url())

    def openUnrealLiveLinkForumUrl(self):
        url = QUrl('https://forums.autodesk.com/t5/unreal-live-link-for-maya-forum/bd-p/6143')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Url', 'Could not open ' + url.url())

    def openAboutBox(self):
        pluginVersion = self.Controller.getPluginVersion()
        apiVersion = self.Controller.getApiVersion()
        unrealVersion = self.Controller.getUnrealVersion()
        About = UnrealLiveLinkAboutDialog(pluginVersion, apiVersion, unrealVersion, self)
        About.setAboutText(self.Controller.getAboutText())
        About.exec_()

    def initUI(self):
        if self.mainLayout:
            return

        self.ConnectedPicture = UnrealLiveLinkWindow.createIcon('infoConnected')
        self.DisconnectedPicture = UnrealLiveLinkWindow.createIcon('infoDisconnected')
        helpPicture = UnrealLiveLinkWindow.createIcon('help')
        aboutPicture = UnrealLiveLinkWindow.createIcon('about')
        settingsPicture = UnrealLiveLinkWindow.createIcon('settings')

        self.setFocusPolicy(Qt.StrongFocus)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(7, 0, 7, 7)

        # Connection Status
        ## Icon
        self.connectionButton = QPushButton(self.DisconnectedPicture, '')
        self.connectionButton.setStyleSheet("""
            border: none;
            color: palette(window-text);
            background: transparent;
            padding-top: 3px;""")
        self.connectionButton.setIconSize(QSize(20, 20))
        self.connectionButton.setFixedSize(QSize(20, 20))
        self.connectionButton.setContentsMargins(0,0,0,0)
        
        ## Label
        self.connectionFrame = QLabel()
        self.connectionFrame.setTextFormat(Qt.RichText)
        self.connectionFrame.setText('<b>No Connection</b>')
        self.connectionFrame.setMargin(0)
        self.connectionFrame.setContentsMargins(5,3,0,0)

        # Menu bar
        menuBar = QMenuBar(self)

        #Edit Menu
        editMenu = menuBar.addMenu('Edit')
        ## Settings action
        settingsAction = QAction(settingsPicture, 'Settings', self)
        settingsAction.triggered.connect(self.openSettings)
        
        editMenu.addAction(settingsAction)
        
        # Help Menu
        helpMenu = menuBar.addMenu('Help')
        ## Help Action
        helpAction = QAction(helpPicture, 'Help on Unreal Live Link', self)
        helpAction.triggered.connect(self.openHelpUrl)
        helpMenu.addAction(helpAction)

        ## Feedback submenu
        feedbackMenu = helpMenu.addMenu('Feedback')
        ### Report problem Action
        reportProblemAction = feedbackMenu.addAction('Report a Problem')
        reportProblemAction.triggered.connect(self.openReportProblemUrl)
        ### Unreal LiveLink forum Action
        unrealLiveLinkForumAction = feedbackMenu.addAction('Unreal Live Link Forum')
        unrealLiveLinkForumAction.triggered.connect(self.openUnrealLiveLinkForumUrl)

        ## About Action
        aboutAction = QAction(aboutPicture, 'About Unreal Live Link', self)
        aboutAction.triggered.connect(self.openAboutBox)
        helpMenu.addAction(aboutAction)

        # Menu bar layout
        menuBarLayout = QHBoxLayout()
        menuBarLayout.setMargin(0)
        menuBarLayout.setContentsMargins(0,0,0,0)
        menuBarLayout.setSpacing(0)

        # Populate the layout
        menuBarLayout.addWidget(menuBar, 0, Qt.AlignLeft)
        menuBarLayout.addStretch(1)
        menuBarLayout.addWidget(self.connectionButton, 0, Qt.AlignRight)
        menuBarLayout.addWidget(self.connectionFrame, 0, Qt.AlignRight)
        
        # Add menu bar layout to main layout
        self.mainLayout.addLayout(menuBarLayout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet('background-color: rgb(86, 86, 86)')
        separator.setFixedHeight(2)
        self.mainLayout.addWidget(separator)

        # Button layout
        buttonLayout = QHBoxLayout()
        self.table = UnrealLiveLinkSubjectTable(self)

        # Add selection
        buttonHoverWatcher = ButtonHoverWatcher('add', self)
        addSelectionButton = QPushButton(buttonHoverWatcher.LeaveIcon, 'Add Selection')
        addSelectionButton.setIconSize(QSize(20, 20))
        addSelectionButton.setFixedHeight(20)
        addSelectionButton.setStyleSheet(self.PushButtonStyleSheet)
        addSelectionButton.setToolTip('Add selected node')
        addSelectionButton.clicked.connect(self.table._addRow)
        addSelectionButton.installEventFilter(buttonHoverWatcher)
        buttonLayout.addWidget(addSelectionButton)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred)
        buttonLayout.addItem(spacer)

        # Delete selection
        buttonHoverWatcher = ButtonHoverWatcher('delete', self)
        self.deleteSelectionButton = QPushButton(buttonHoverWatcher.LeaveIcon, '')
        self.deleteSelectionButton.setIconSize(QSize(20, 20))
        self.deleteSelectionButton.setFixedSize(QSize(20, 20))
        self.deleteSelectionButton.setStyleSheet(self.PushButtonStyleSheet)
        self.deleteSelectionButton.setToolTip('Delete selection')
        self.deleteSelectionButton.setEnabled(False)
        self.deleteSelectionButton.clicked.connect(self.table._removeRow)
        self.deleteSelectionButton.installEventFilter(buttonHoverWatcher)
        buttonLayout.addWidget(self.deleteSelectionButton, alignment=Qt.AlignTop)

        self.mainLayout.addLayout(buttonLayout)

        self.mainLayout.addWidget(self.table)
        layout = QHBoxLayout()
        self._logLabel = QLabel('')
        self._logLabel.setTextFormat(Qt.RichText)
        layout.addWidget(self._logLabel)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer)
        self.updateLabel = QLabel()
        self.updateLabel.setTextInteractionFlags(Qt.TextBrowserInteraction);
        self.updateLabel.setOpenExternalLinks(True);
        self.updateLabel.setTextFormat(Qt.RichText)
        url = self.Controller.getUpdateURL()
        if url and len(url) > 0:
            self.updateLabel.setText(self._getUpdateText(url))
        else:
            self.updateLabel.hide()
        layout.addWidget(self.updateLabel)
        self.mainLayout.addLayout(layout)

        self.setLayout(self.mainLayout)

    def logMessage(self, message, timeToClear=3000):
        if len(message) > 0:
            self._logLabel.setText(message)

            # Clear the log after some time
            QTimer.singleShot(3000, lambda: self._logLabel.setText(''))

    def updateConnectionState(self, ConnectionText, ConnectedState):
        if ConnectedState != self.ConnectedState:
            self.connectionFrame.setText('<b>' + ConnectionText + '</b>')
            self.ConnectedState = ConnectedState
            connectionPicture = None
            if ConnectedState and self.ConnectedPicture:
                connectionPicture = self.ConnectedPicture
            elif ConnectedState is False and self.DisconnectedPicture:
                connectionPicture = self.DisconnectedPicture
            if connectionPicture:
                self.connectionButton.setIcon(connectionPicture)

    @staticmethod
    def createIcon(iconName):
        icon = QIcon()
        availableSizes = ['1', '2', '3']
        for size in availableSizes:
            path = os.path.join(UnrealLiveLinkWindow.iconPath, iconName + '@' + size + 'x.png')
            if os.path.isfile(path):
                icon.addFile(path)
        return icon

    @staticmethod
    def highlightPixmap(pixmap):
        img = QImage(pixmap.toImage().convertToFormat(QImage.Format_ARGB32))
        imgh = img.height()
        imgw = img.width()

        for y in range (0, imgh, 1):
            for x in range (0, imgw, 1):
                pixel = img.pixel(x, y)
                highLimit = 205 # value above this limit will just max up to 255
                lowLimit = 30 # value below this limit will not be adjusted
                adjustment = 255 - highLimit
                color = QColor(pixel)
                v = color.value()
                s = color.saturation()
                h = color.hue()
                if(v > lowLimit):
                    if (v < highLimit):
                        v = v + adjustment
                    else:
                        v = 255
                v = color.setHsv(h, s, v)
                img.setPixel(x, y, qRgba(color.red(), color.green(), color.blue(), qAlpha(pixel)))
        return QPixmap(img)

    def clearUI(self):
        if self.table:
            self.table._clearUI()

    def refreshUI(self):
        if self.table:
            self.table._refreshUI()

    def setWindowRect(self, tlc, w, h):
        self.setGeometry(0, 0, w, h)
        self.move(tlc[0], tlc[1])

    def openSettings(self):
        Settings = UnrealLiveLinkSettings(self)
        Settings.initUI()
        Settings.showWindow()

    def setWindowProperty(self, name, value):
        self._properties[name] = value
        self.setProperty(name, value)

    def notifyNewerUpdate(self):
        url = self.Controller.getUpdateURL()
        if url and len(url) > 0:
            self.updateLabel.setText('<a href="' + url + '">Update Available</a>')
            self.updateLabel.show()

    def _getUpdateText(self, url):
        return '<a href="' + url + '">Update Available</a>' if url and len('URL') > 0 else ''

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
# CwUAMA0GCSqGSIb3DQEBAQUABIIBgAFo778iuEMbyRq0UC0wmsU8rDW2qTNnfVNW
# TwJjP87VO874Vh0pgEyDZGIepxy/gMftsAMbwdSOZ/LSlm3k/PKj8pcJnXCoNBMz
# /10WyQlyEtd8FFoHk10uKgqMoMFsAWqQs1OQKfMn+QQ2YXhTeFFLQtPRp/0hbaWh
# E+MYE/zMWqaA2l/jYCIy+1nK7hfeX7qQ5sBEB10dHGOzSidlPTLPT81+pRF/yYO/
# T0dRcwX+hAcnEPHMQnrj1fCSpiQT5QiLNUezzoPwTBgwyfgDJcQrrcUg2/6rbOKl
# YHRC7t+XF4IR4Mw/lj8JCOPMRJ8jHB2fVVTbOMPpE5nusrJoyDL7PZsLOwhT1Mud
# 8VWLKPXfyC2DYUj4Nfqy/09r8+UnSDYS/7mRCSzTbldtYUtTa+dt57v//WdnRXJA
# EuL/8+ZwStvgHiOsurvQy3nBbabA91RHjUwVKf4sN33zmOhv6f1WYk4KnvRdvRsk
# XjVQLhpohowoPJsKviFYHPACheFdsg==
# -----END-SIGNATURE-----