try:
  from PySide2.QtCore import *
  from PySide2.QtGui import *
  from PySide2.QtWidgets import *
  from PySide2 import __version__
except ImportError:
  from PySide.QtCore import *
  from PySide.QtGui import *
  from PySide import __version__

class IPAddressLineEdit(QLineEdit):
    class IPAddressRegExpValidator(QRegExpValidator):
        validationChanged = Signal(QValidator.State)

        def validate(self, input, pos):
            state, input, pos = super().validate(input, pos)
            self.validationChanged.emit(state)
            return state, input, pos

    textModified = Signal(str, str) # (before, after)
    validationError = Signal()

    _ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"   # Part of the regular expression
    _portRange = "([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"
    _ipRegex = QRegExp("^" + _ipRange + "\\." + _ipRange + "\\." + _ipRange + "\\." + _ipRange + ":" + _portRange + "$|0.0.0.0:0")

    def __init__(self, contents='', parent=None):
        super(IPAddressLineEdit, self).__init__(contents, parent)
        self.editingFinished.connect(self.__handleEditingFinished)
        self._before = contents
        self._validationState = self.hasAcceptableInput()
        self._skipValidation = False
        self.defaultIPAddress = ''

        # Install a validator to make the IP address is always well formed
        ipValidator = IPAddressLineEdit.IPAddressRegExpValidator(IPAddressLineEdit._ipRegex, self)
        ipValidator.validationChanged.connect(self.handleValidationChange)
        self.setValidator(ipValidator)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        textLength = len(self.text())

        # validate the IP address
        if textLength == 0:
            if len(self.defaultIPAddress) > 0:
                # Replace an empty line edit by the default address
                self.setText(self.defaultIPAddress)
        elif self.hasAcceptableInput() is False:
            # Stay on the line edit until the user finishes typing the address
            self.setFocus()
            self.validationError.emit()

    @staticmethod
    def trim(address):
        # Remove any leading 0
        after = address.replace(':', '.')
        trimmedIP = after.split('.')
        trimmedIP = [x.lstrip('0') for x in trimmedIP]
        trimmedIPSize = len(trimmedIP)
        if trimmedIPSize == 5:
            for i in range(trimmedIPSize):
                if len(trimmedIP[i]) == 0:
                       trimmedIP[i] = '0'
            after = ".".join(trimmedIP[:4]) + ':' + trimmedIP[4]
            return after
        return ""

    def __handleEditingFinished(self):
        before, after = self._before, self.text()
        if before != after:
            trimmed = IPAddressLineEdit.trim(after)
            if len(trimmed) > 0:
                after = trimmed
            self.setText(after)
            self._before = after
            self.textModified.emit(before, after)

    def handleValidationChange(self, state):
        validState = False
        if state == QValidator.Invalid:
            colour = 'red'
        elif state == QValidator.Intermediate:
            colour = 'gold'
        elif state == QValidator.Acceptable:
            colour = 'lime'
            validState = True
        if validState or len(self.text()) == 0:
            # Clear the border if valid or empty
            QTimer.singleShot(1000, lambda: self.setStyleSheet(''))

        # Add a colored border to let the user know that the IP address is valid or not
        self.setStyleSheet('border: 2px solid %s' % colour)
        if validState != self._validationState:
            self_validationState = validState

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
# CwUAMA0GCSqGSIb3DQEBAQUABIIBgI/gu/G0YTwrIZYb/DvLjmYSh2Ar2/f2ni+8
# Ay9lptQQ65sSj3ir3Gfh5ZhpuAp2naGKqAlR/2y1dAe5keoXNXVUkdjrhqXp3z80
# Hw3k9cxNkhZgacP8ci7FDZMVhIRd7jrDQQ97iPVnHyVLXF6E/2CEaXMRqIdPB394
# NJ/wCYLUWEHJJnveWRFgA3zp2OxSdk1oRpLBbpP6/PQCwGQEjFhfD/X0clbzmkP9
# kXfEKM+EdW7EUCqL/bVVyAoMINAg3Zq86XcrwlxnTu3CCB7ovG3bO1JSN6LJufl4
# QJG564UUm9+Z5vLxgTmSKzdpQsrBJvI1FJ+FNPIhgDnz1QcN/g8PoXoU4k4rpbdD
# IUUmvHxUg1uObozXRDY980Je5qN2iY6sV8Pi02BdMwKnTlUTWgNrlZskSywYP5cr
# OkMB2UscvNYmwyjnfdEuqzwM95aRTXvWhaLpvmFzCMunkaqhLJDiGUx5OitYTJcb
# Q6xsHA6pM7b+F7did3XFJLPaply2jg==
# -----END-SIGNATURE-----