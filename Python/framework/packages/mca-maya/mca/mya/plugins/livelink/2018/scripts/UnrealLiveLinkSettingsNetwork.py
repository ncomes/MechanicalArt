try:
  from PySide2.QtCore import *
  from PySide2.QtGui import *
  from PySide2.QtWidgets import *
  from PySide2 import __version__
except ImportError:
  from PySide.QtCore import *
  from PySide.QtGui import *
  from PySide import __version__

from IPAddressLineEdit import IPAddressLineEdit

class UnrealLiveLinkSettingsNetwork(QWidget):
    class ListWidget(QListWidget):
        def __init__(self, button, parent=None):
            super(UnrealLiveLinkSettingsNetwork.ListWidget, self).__init__(parent)
            self.removeButton = button

        def focusOutEvent(self, event):
            super().focusOutEvent(event)
            self.selectionModel().clear()
            self.removeButton.setEnabled(False)

    def __init__(self, controller, parent=None):
        super(UnrealLiveLinkSettingsNetwork, self).__init__(parent)
        self.labelStyle = 'QLabel { background-color : ' + self.palette().color(QPalette.Button).name() + '; }'
        self.setWindowTitle('Endpoints')

        mainLayout = QVBoxLayout()

        self.unicastEndpoint = '0.0.0.0:0'
        self.staticEndpoints = []
        if controller:
            endpointsDict = controller.getNetworkEndpoints()
            if endpointsDict:
                if 'unicast' in endpointsDict:
                    self.unicastEndpoint = endpointsDict['unicast']
                if 'static' in endpointsDict:
                    self.staticEndpoints = endpointsDict['static']

        vboxLayout = QVBoxLayout()
        gridLayout = QGridLayout()

        #########
        # Row 0 #
        #########
        rowNumber = 0

        # Unicast endpoint
        label = QLabel('Unicast Endpoint')
        gridLayout.addWidget(label, rowNumber, 0, 1, 1, Qt.AlignRight)

        # Unicast endpoint line edit
        self.unicastLineEdit = IPAddressLineEdit(self.unicastEndpoint)
        self.unicastLineEdit.defaultIPAddress = '0.0.0.0:0'
        self.unicastLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.unicastLineEdit.setPlaceholderText('X.X.X.X:X')
        self.unicastLineEdit.textModified.connect(self._unicastEndpointChanged)
        gridLayout.addWidget(self.unicastLineEdit, rowNumber, 1)

        #########
        # Row 1 #
        #########
        rowNumber += 1

        # Static endpoints
        label = QLabel('Static Endpoints')
        gridLayout.addWidget(label, rowNumber, 0, 1, 1, Qt.AlignRight)

        # Static endpoint line edit
        self.staticEndpointLineEdit = IPAddressLineEdit('')
        self.staticEndpointLineEdit.setPlaceholderText('X.X.X.X:X')
        self.staticEndpointLineEdit.textChanged.connect(lambda x, le=self.staticEndpointLineEdit: self._validateEndpoint(x, le))
        gridLayout.addWidget(self.staticEndpointLineEdit, rowNumber, 1)

        # Static endpoint add button
        self.addButton = QPushButton('+')
        self.addButton.setStyleSheet("text-align:center;");
        self.addButton.clicked.connect(self._addStaticEndpointToListWidget)
        textSize = self.addButton.fontMetrics().size(Qt.TextShowMnemonic, self.addButton.text())
        opt = QStyleOptionButton();
        opt.initFrom(self.addButton);
        opt.rect.setSize(textSize);
        size = self.addButton.style().sizeFromContents(QStyle.CT_PushButton,
                                                       opt,
                                                       textSize,
                                                       self.addButton)
        size = QSize(size.width(), size.width())
        self.addButton.setMaximumSize(size);
        self.addButton.setEnabled(False)
        gridLayout.addWidget(self.addButton, rowNumber, 2, Qt.AlignRight | Qt.AlignTop)

        #########
        # Row 2 #
        #########
        rowNumber += 1

        # Static endpoint remove button
        self.removeButton = QPushButton('-')
        self.removeButton.setStyleSheet("text-align:center;");
        self.removeButton.setMaximumSize(size)
        self.removeButton.setEnabled(False)
        self.removeButton.clicked.connect(self.removeStaticEndpointFromListWidget)

        # Static endpoint list widget
        self.staticEndpointListWidget = UnrealLiveLinkSettingsNetwork.ListWidget(self.removeButton)
        for staticEndpoint in self.staticEndpoints:
            self.staticEndpointListWidget.addItem(staticEndpoint)
        self.staticEndpointListWidget.itemClicked.connect(self._staticEndpointItemClicked)
        gridLayout.addWidget(self.staticEndpointListWidget, rowNumber, 1)
        gridLayout.addWidget(self.removeButton, rowNumber, 2, Qt.AlignRight | Qt.AlignTop)

        #########
        # Row 3 #
        #########
        rowNumber += 1

        # Horizontal spacer
        gridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), rowNumber, 0, 1, 3)

        # Vertical spacer
        gridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), 0, 3, rowNumber, 1)

        gridLayout.setColumnMinimumWidth(0, 150)

        label = QLabel()
        label.setTextFormat(Qt.RichText)
        label.setText('<b>Endpoints</b>')
        label.setStyleSheet(self.labelStyle)
        label.setContentsMargins(7, 2, 7, 2)
        vboxLayout.addWidget(label)

        vboxLayout.addLayout(gridLayout)
        mainLayout.addLayout(vboxLayout)

        self.setLayout(mainLayout)

    def saveContent(self, controller):
        if controller:
            controller.setNetworkEndpoints({
                'unicast' : self.unicastEndpoint,
                'static' : self.staticEndpoints})

    def _validateEndpoint(self, endpoint, lineEdit):
        if lineEdit:
            self.addButton.setEnabled(lineEdit.hasAcceptableInput())
            self.removeButton.setEnabled(False)

    def _unicastEndpointChanged(self, oldIP, newIP):
        if oldIP != newIP:
            self._validateEndpoint(newIP, None)
            self.unicastEndpoint = newIP

    def _addStaticEndpointToListWidget(self, checked):
        endpoint = self.staticEndpointLineEdit.text()
        trimmed = IPAddressLineEdit.trim(endpoint)
        if len(trimmed) > 0:
            endpoint = trimmed

        if endpoint not in self.staticEndpoints:
            self.staticEndpointListWidget.addItem(endpoint)
            self.staticEndpoints.append(endpoint)
        self.staticEndpointLineEdit.clear()

    def _staticEndpointItemClicked(self, item):
        self.removeButton.setEnabled(True)

    def removeStaticEndpointFromListWidget(self, checked):
        items = self.staticEndpointListWidget.selectedItems()
        for item in items:
            self.staticEndpoints.remove(item.text())
            self.staticEndpointListWidget.takeItem(self.staticEndpointListWidget.row(item))
        if len(self.staticEndpoints) == 0:
            self.removeButton.setEnabled(False)

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
# CwUAMA0GCSqGSIb3DQEBAQUABIIBgFfWr1r6wzMQqS+6DKFDPsc3MPofiAg4+pAg
# APmXmu3b9A+K61xow7EUSR3wFFSEwnFM5kKjPCpYLJqiO4iOcnupHqLbnCs5gqPU
# ttA41XDk+bogfNrlYnu0odrFxtCOEmVdvFRl8QdYemiyLW1jf65FTCTdK6yhQk+0
# Eorfu0ok+Y7ekZ04Gy7u/H0V09+DbpGfL9WwZXOaREebq/QMxqZQc9rYJV3u7WI3
# ClAQhGF3H2n0iwHbiqnk55YSGEnUEh1P+XmoBMsSRC5Rz6cmnLVkU4cGrU5uXFj8
# ZrrmzaEr+gbBySRnvlNCfSKVfqZsv8a7ePX6e43X3pxMDfc4OHmZ4+8eftFfERl2
# be0TC9dMwj6C27WJo74m/2dbDmsAcq+wpR/ZubQEVO4xNoUNWCD3qLYj4/n374Wh
# 5JmzVaR0MTByeDTrWJ57Uu4I1n/jS1o+uPl69EoSd4sb+Wu6Tm7U3o8H1IB0BJ23
# V5d3Wz7A2beU2Glj64WDXWvkIzBXxA==
# -----END-SIGNATURE-----