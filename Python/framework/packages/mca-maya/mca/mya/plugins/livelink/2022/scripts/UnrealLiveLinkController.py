import weakref
from UnrealLiveLinkWindow import UnrealLiveLinkWindow

class UnrealLiveLinkController():
    def __init__(self, model, windowName, windowTitle, iconPath, parentWidget=None, window=None):
        self._Window = None
        if window:
            self._Window = window
        else:
            self._Window = UnrealLiveLinkWindow(self,
                                                windowName,
                                                windowTitle,
                                                parentWidget)

        self._Model = weakref.proxy(model)
        if model and parentWidget is None:
            tlc, width, height = model.loadUISettings()
            if width > 0 and height > 0:
                self._Window.setWindowRect(tlc, width, height)

        self._Window.setIconPath(iconPath)
        self._Window.initUI()

    def __del__(self):
        self._Model = None
        if self._Window:
            del self._Window
            self._Window = None

    def loadUISettings(self):
        if self._Model:
            return self._Model.loadUISettings()
        return [50, 50], 650, 450

    def setWindowRect(self, tlc, w, h):
        if self._Window:
            self._Window.setWindowRect(tlc, w, h)

    def updateConnectionState(self, connectionText, connectedState):
        if self._Window:
            self._Window.updateConnectionState(connectionText, connectedState)

    def clearUI(self):
        if self._Window:
            self._Window.clearUI()

    def refreshUI(self):
        if self._Window:
            self._Window.refreshUI()

    def refreshSubjects(self):
        if self._Model:
            return self._Model.refreshSubjects()
        return []

    def addSelection(self):
        if self._Model:
            return self._Model.addSelection()
        return False

    def removeSubject(self, dagPath):
        if self._Model:
            self._Model.removeSubject(dagPath)

    def changeSubjectName(self, dagPath, newName):
        if self._Model:
            self._Model.changeSubjectName(dagPath, newName)

    def changeSubjectRole(self, dagPath, newRole):
        if self._Model:
            self._Model.changeSubjectRole(dagPath, newRole)

    def getNetworkEndpoints(self):
        if self._Model:
            return self._Model.getNetworkEndpoints()
        return {}

    def setNetworkEndpoints(self, endpointsDict):
        if self._Model:
            self._Model.setNetworkEndpoints(endpointsDict)

    def setWindowProperty(self, name, value):
        if self._Window:
            self._Window.setWindowProperty(name, value)

    def getDpiScale(self, size):
        if self._Model:
            return self._Model.getDpiScale(size)
        return size

    def isDocked(self):
        if self._Model:
            return self._Model.isDocked()
        return False

    def getPluginVersion(self):
        if self._Model:
            return self._Model.getPluginVersion()
        return ""

    def getApiVersion(self):
        if self._Model:
            return self._Model.getApiVersion()
        return ""

    def getUnrealVersion(self):
        if self._Model:
            return self._Model.getUnrealVersion()
        return ""

    def getAboutText(self):
        if self._Model:
            return self._Model.getAboutText()
        return ""

    def getUpdateURL(self):
        if self._Model:
            return self._Model.getUpdateURL()
        return ""

    def getDocumentationURL(self):
        if self._Model:
            return self._Model.getDocumentationURL()
        return ""

    def notifyNewerUpdate(self):
        if self._Window:
            return self._Window.notifyNewerUpdate()
        return ""

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
# CwUAMA0GCSqGSIb3DQEBAQUABIIBgEfJrt4SloO2dTmy52plNA4wr2axF8EigrKd
# u4VSaKXL2A+/CNUIVYyFUqUqqr4flPmaByYMFnbvS8tcMS755fzBGEx1OpHypu7q
# oy33BTEvwnOFK50WvaIFTQdgevUz1WbRPVCKQRoGh3RsqTdaMclqow5OGT+e47a7
# 6cS4Uk8ihGTG4j4mQx3E2mFGr2NAa1YIed1/4i9/VMsfEXoZKYiO8BtjvOda/Uyj
# dM0afLKtFtxesyFkuTMDdGTbwaty13XgvrsDBQhFgL3Rm/umkVUrO/qXx2y1uOeL
# 8rL4hr8IfK6ElDWF4ZMydmhu+GO/WKu/lDwiurf0gV+eHXVSP/zpakz9N5vAeJun
# FddrLt4f4WLvMD1H1MLEubT8Dcw615QMq3bs8ZVZz70pvBxGOARW9D3JOjxf0p94
# 3Tn/OqXdQAwIUInE6RxjFq8GG4cmzGScbBflxZ7BcJnj+0i4zO3iZS0o1gL/TzjB
# pcyU3rCZpY3XCaqcwPM86wn+9kTfQg==
# -----END-SIGNATURE-----