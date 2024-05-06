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


class UnrealLiveLinkAboutDialog(QDialog):
    def __init__(self, pluginVersion, apiVersion, unrealVersion, parent=None):
        super(UnrealLiveLinkAboutDialog, self).__init__(parent=parent)

        self.mainLayout = QVBoxLayout()
        self.setMinimumSize(QSize(600, 450))

        self.setWindowFlags(Qt.Window)
        self.setObjectName("UnrealLiveLinkAboutDialog")
        self.setWindowTitle('About Unreal Live Link')

        if pluginVersion and len(pluginVersion) > 0:
            self.pluginVersionLabel = QLabel()
            self.pluginVersionLabel.setText("Plugin version: " + pluginVersion)
            self.mainLayout.addWidget(self.pluginVersionLabel)

        if apiVersion and len(apiVersion) > 0:
            self.apiVersionLabel = QLabel()
            self.apiVersionLabel.setText("API version: " + apiVersion)
            self.mainLayout.addWidget(self.apiVersionLabel)

        if unrealVersion and len(unrealVersion) > 0:
            self.unrealVersionLabel = QLabel()
            self.unrealVersionLabel.setText("Unreal version: " + unrealVersion)
            self.mainLayout.addWidget(self.unrealVersionLabel)

        self.aboutTextEdit = QTextEdit()
        self.aboutTextEdit.setReadOnly(True)
        self.mainLayout.addWidget(self.aboutTextEdit)

        layout = QHBoxLayout()
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addItem(spacer)

        button = QPushButton()
        button.setText("OK")
        button.clicked.connect(lambda: self.accept())
        layout.addWidget(button)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addItem(spacer)
        self.mainLayout.addLayout(layout)

        self.setLayout(self.mainLayout)

    def setAboutText(self, text):
        if text and (isinstance(text, str) or isinstance(text, unicode)):
            self.aboutTextEdit.setText(text)

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
# CwUAMA0GCSqGSIb3DQEBAQUABIIBgEhkIZs/68aEkjGuv8T1TOZRENE7YGCmJTWl
# emfK3y5maYjnN8y+mnibvBHuDAjBIJdbCtuASRHgl29p9WJIxEXcWCjRBB1qEco9
# U8rFX9zFZbMI6f3T44gVm8Tlea2WmeEM1NTlhP+vMUVy5lWF9V1ykAkkyI29HVo0
# kGH36Ix4BybfJRq9II9+xGmBYjIGc0BDBtZzfrOJJmHpoaoMmnTWzuM82JLWikvd
# EvCHsbQ36ZGkFWuyd1a12jygxmMU6Dn2JiFWpPIT5I5EHg/MsiykRx4l7KwyJZpk
# jwux62QRMFcnLawtFUzp3S+a6vYicDOouqbPWpprfaiM6nCQGbiupuWN4rMoC768
# 354DtvTFeStk8OjIydUIhRpyLFkGNwZsXv+PqeYWyH+anOUwlgi2L2mdsPadNkdH
# IijUlT+zGXIagAwqXpcc4ccNIJt0jJ6vTjSomwKCtc770evnplF0MoRN51awq8CC
# qLLFvpBThB4XvBHHvzaH/cjNI+Pnhw==
# -----END-SIGNATURE-----