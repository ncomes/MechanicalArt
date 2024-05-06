try:
  from PySide2.QtCore import *
  from PySide2.QtGui import *
  from PySide2.QtWidgets import *
  from PySide2 import __version__
except ImportError:
  from PySide.QtCore import *
  from PySide.QtGui import *
  from PySide import __version__

from UnrealLiveLinkSettingsNetwork import UnrealLiveLinkSettingsNetwork

class UnrealLiveLinkSettings(QDialog):
    class TreeWidgetItem(QTreeWidgetItem):
        def __init__(self, name = ''):
            super(UnrealLiveLinkSettings.TreeWidgetItem, self).__init__([name])

        def name(self):
            return self.text(0)

        def fullpath(self):
            fullpath = [self.name()]
            parent = self.parent()
            while parent:
                fullpath.append(parent.name())
                parent = parent.parent()
            fullpath.reverse()
            return '/'.join(fullpath)

    _windowName = 'UnrealLiveLinkSettings'

    def __init__(self, parent=None):
        super(UnrealLiveLinkSettings, self).__init__(parent)
        self._parentWindow = parent

    def showWindow(self):
        self.exec_()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.setWindowFlags(Qt.Window)
        self.setObjectName(UnrealLiveLinkSettings._windowName)
        self.setWindowTitle('Unreal Live Link settings')

        self.labelStyle = 'QLabel { background-color : ' + self.palette().color(QPalette.Button).name() + '; }'

        # Content layout
        categoryLayout = QVBoxLayout()
        label = QLabel()
        label.setLineWidth(0)
        label.setTextFormat(Qt.RichText)
        label.setText('<b>Categories</b>')
        label.setStyleSheet(self.labelStyle)
        label.setMargin(4)
        categoryLayout.addWidget(label)
        self.categoryTreeWidget = QTreeWidget()
        self.categoryTreeWidget.setHeaderHidden(True)
        self.categoryTreeWidget.setRootIsDecorated(False);
        self.categoryTreeWidget.setMinimumWidth(120)
        self.categoryTreeWidget.setMaximumWidth(120)
        self.categoryTreeWidget.setSortingEnabled(False)
        self.categoryTreeWidget.setItemsExpandable(False)
        self.categoryTreeWidget.itemClicked.connect(self._categoryTreeItemClicked)
        categoryLayout.addWidget(self.categoryTreeWidget)
        categoryLayout.setSpacing(0)
        categoryLayout.setContentsMargins(0,0,0,0)

        # Preference layout
        self.preferenceLayout = QVBoxLayout()
        self.preferencesLabel = QLabel('')
        self.preferencesLabel.setTextFormat(Qt.RichText)
        self.preferencesLabel.setStyleSheet(self.labelStyle)
        self.preferencesLabel.setMargin(4)
        self.preferencesLabel.setMinimumWidth(350)
        self.preferenceLayout.addWidget(self.preferencesLabel)
        self.preferencesFrame = QFrame()
        self.preferencesFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.preferenceLayout.addWidget(self.preferencesFrame)
        self.preferenceLayout.setSpacing(0)
        self.preferenceLayout.setContentsMargins(0,0,0,0)

        self.contentLayout = QHBoxLayout()
        self.contentLayout.addLayout(categoryLayout)
        self.contentLayout.addLayout(self.preferenceLayout)
        self.contentLayout.setSpacing(5)
        self.contentLayout.setContentsMargins(0,0,0,3)
        self.mainLayout.addLayout(self.contentLayout)
        self.mainLayout.setSpacing(3)

        # Save/Cancel layout
        saveLayout = QHBoxLayout()
        saveButton = QPushButton()
        saveButton.setText('Save')
        saveButton.clicked.connect(self._onSaveClicked)
        saveLayout.addWidget(saveButton)

        cancelButton = QPushButton()
        cancelButton.setText('Cancel')
        cancelButton.clicked.connect(self._onCancelClicked)
        saveLayout.addWidget(cancelButton)

        self.mainLayout.addLayout(saveLayout)
        self.setLayout(self.mainLayout)

        self.closeEvent = self.closeEvent

        self._fillTreeWidget()

    def _fillTreeWidget(self):
        self.contentLayoutTable = dict()

        networkTreeWidget = UnrealLiveLinkSettings.TreeWidgetItem('Network')
        widget = UnrealLiveLinkSettingsNetwork(self._parentWindow.Controller)
        self.contentLayoutTable[networkTreeWidget.fullpath()] = widget

        self.categoryTreeWidget.addTopLevelItem(networkTreeWidget)
        topLevelItem = self.categoryTreeWidget.topLevelItem(0)
        topLevelItem.setSelected(True)
        self._categoryTreeItemClicked(topLevelItem, 0)

        self.categoryTreeWidget.expandAll()

    def _categoryTreeItemClicked(self, item, col):
        prevWidget = self.preferenceLayout.itemAt(1).widget()

        fullpath = item.fullpath()
        newWidget = None
        if fullpath in self.contentLayoutTable:
            newWidget = self.contentLayoutTable[fullpath]
        else:
            newWidget = self.preferencesFrame

        if newWidget != prevWidget:
            self.preferenceLayout.replaceWidget(prevWidget, newWidget)
            prevWidget.hide()
            newWidget.show()
            self.preferencesLabel.setText('<b>' + item.name() + ': General ' + item.name() + ' Preferences</b>')

    def _onSaveClicked(self):
        for key in self.contentLayoutTable:
            widget = self.contentLayoutTable[key]
            if isinstance(widget, QWidget):
                widget.saveContent(self._parentWindow.Controller)
        self.accept()

    def _onCancelClicked(self):
        self.reject()

    def closeEvent(self, event):
        super(UnrealLiveLinkSettings, self).closeEvent(event)
        event.accept()

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
# CwUAMA0GCSqGSIb3DQEBAQUABIIBgHmcwdNPiaArQx+thxu6pWT2un8lcnubh77l
# zf2ywtdaKbtu0uZA5cwNefT6Z1gLb3tWXvaCKEu6t9ohFRFi3ZVm1+DjGIJcFxRW
# OD7dUVeWCQEpvM970DwyZET2S1igJA0oVnLVcVmcnfQn0K84JfhVY6wMD5ILvBGV
# 5fPVMrTM9ksJh2C4ZCdixOPR/CmHvFLx5SnVQaYh4j5DoODD4iMIYAGbETGPga5b
# 9is/uw0ZVs2ddh+wTtPHCqfwQ2MgC7ny91h/RePyW6Hazv9nj/2y3TDOF6ph0X8S
# WrjdTWoJyhSUWVu5GDQOqCuqCosxwJX5bjHlwURAWCUp2XtCORmpxlT7msIoFe58
# sU+PUTRSc7Eg9a6f5YFqF03UCmoKIlGHqpuuexI6lB3r2rpkC89Y2I0hoXq62FpF
# /7XKTcqm/d0V22RdrcP9KKQWxE8YOSiKSmb0BLVw58w7TZdGGCPmS0m1iFWKd4N1
# 71i3gtdlh0YtPHA1cLqkfjUdOiV/OQ==
# -----END-SIGNATURE-----