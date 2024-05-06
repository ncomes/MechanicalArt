import weakref

try:
  from PySide2.QtCore import *
  from PySide2.QtGui import *
  from PySide2.QtWidgets import *
  from PySide2 import __version__
except ImportError:
  from PySide.QtCore import *
  from PySide.QtGui import *
  from PySide import __version__

import UnrealLiveLinkWindow

class SubjectLineEdit(QLineEdit):
    textModified = Signal(str, str) # (before, after)

    def __init__(self, table, contents='', parent=None):
        super(SubjectLineEdit, self).__init__(contents, parent)
        self.editingFinished.connect(self.__handleEditingFinished)
        self._before = contents
        self._table = weakref.proxy(table)

    def __del__(self):
        self._table = None

    def __handleEditingFinished(self):
        before, after = self._before, self.text()
        if len(after) == 0:
            self.setText(before)
        elif before != after and self._table:
            finalName = after
            self._before = finalName
            self.textModified.emit(before, finalName)
        self._table.setFocus()

class RowHighlightDelegate(QStyledItemDelegate):
    onHoverIndexChanged = Signal(int)
    onLeaveTable = Signal()

    def __init__(self, table, parent=None):
        super(RowHighlightDelegate, self).__init__(parent)
        self.hoveredRow = -1
        self.Table = weakref.proxy(table)
        defaultColor = table.palette().color(QPalette.Window)
        self.defaultBrush = QBrush(defaultColor)
        self.hoveredBrush = QBrush(defaultColor.darker(115))

    def __del_(self):
        self.Table = None

    def _onHoverIndexChanged(self, index):
        if index != self.hoveredRow:
            self.hoveredRow = index
            self.Table.viewport().update()

    def _onLeaveTableEvent(self):
        self.hoveredRow = -1

    def paint(self, painter, option, index):
        painter.save()

        self.initStyleOption(option, index)

        isSelected = option.state & QStyle.State_Selected
        if isSelected == False:
            if index.row() == self.hoveredRow:
                painter.fillRect(option.rect, self.hoveredBrush)
            else:
                painter.fillRect(option.rect, self.defaultBrush)

        painter.restore()

class ComboBox(QComboBox):
    def __init__(self, parent):
       super(ComboBox, self).__init__(parent)
       self.icons = []
       self.hoverIcons = []

    def initIcons(self, icons, hoverIcons):
        self.icons = icons
        self.hoverIcons = hoverIcons

    def enterEvent(self, event):
        super(ComboBox, self).enterEvent(event)

        currentIndex = self.currentIndex()
        if currentIndex < 0 or currentIndex >= len(self.hoverIcons):
            return
        self.setItemIcon(currentIndex, self.hoverIcons[currentIndex])

    def leaveEvent(self, event):
        super(ComboBox, self).leaveEvent(event)

        currentIndex = self.currentIndex()
        if currentIndex < 0 or currentIndex >= len(self.icons):
            return
        self.setItemIcon(currentIndex, self.icons[currentIndex])

class UnrealLiveLinkSubjectTable(QTableWidget):
    StreamTypesPerSubjectType = {
        'Prop': 		['Root Only', 'Full Hierarchy'],
        'Character':	['Root Only', 'Full Hierarchy'],
        'Camera':		['Root Only', 'Full Hierarchy', 'Camera'],
        'Light':		['Root Only', 'Full Hierarchy', 'Light'],
    }

    IconsPerSubjectType = {
        'Prop': 		['streamTransform', 'streamAll'],
        'Character':	['streamRoot', 'streamAll'],
        'Camera':		['streamTransform', 'streamAll', 'streamCamera'],
        'Light':		['streamTransform', 'streamAll', 'streamLights'],
    }

    hoverIndexChanged = Signal(int)
    leaveTableEvent = Signal()

    def __init__(self, windowParent):
        super(UnrealLiveLinkSubjectTable, self).__init__(0, 3)

        self.windowParent = weakref.proxy(windowParent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Load the icons used in the table
        self.Icons = dict()
        self.HoverIcons = dict()
        for subject in UnrealLiveLinkSubjectTable.IconsPerSubjectType:
            iconNames = UnrealLiveLinkSubjectTable.IconsPerSubjectType[subject]
            for iconName in iconNames:
                if iconName not in self.Icons:
                    self.Icons[iconName] = self.windowParent.createIcon(iconName)
                    if self.Icons[iconName]:
                        pixmap = self.Icons[iconName].pixmap(32, 32)
                        highlightPixmap = self.windowParent.highlightPixmap(pixmap)
                        self.HoverIcons[iconName] = QIcon(highlightPixmap)

        self.setHorizontalHeaderLabels(['Type', 'Object Name', 'DAG Path'])
        self.horizontalHeader().setDefaultSectionSize(250)
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        dpiScale = windowParent.Controller.getDpiScale(60)
        self.setColumnWidth(0, 60 + max(0, int((dpiScale - 60) * 0.5)))
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.emptyLayout = QHBoxLayout()
        self.emptyLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.emptyLabel = QLabel('To stream a subject to Unreal:<br>1. Select an object in <i>Maya</i>.</pre><br>2. Click <i>Add Selection.</i></pre>')
        self.emptyLabel.setTextFormat(Qt.RichText)
        self.emptyLayout.addWidget(self.emptyLabel)
        self.emptyLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.setLayout(self.emptyLayout)

        self.setStyleSheet('QTableWidget { background-color: ' +
                           windowParent.palette().color(QPalette.Window).darker(125).name() +
                           '; } QTableWidget::item { padding: 3px }')

        self.setMouseTracking(True)
        self.rowDelegate = RowHighlightDelegate(self)

        self.mouseMoveEvent = self._mouseMoveEvent
        self.leaveEvent = self._leaveEvent
        self.hoverIndexChanged.connect(self.rowDelegate._onHoverIndexChanged)
        self.leaveTableEvent.connect(self.rowDelegate._onLeaveTableEvent)
        self.itemSelectionChanged.connect(lambda: self.windowParent.deleteSelectionButton.setEnabled(len(self.selectedIndexes()) > 0))

        self.subjectList = []
        self.subjectTypes = dict()
        self.cellMouseHover = [-1, -1]

    def __del__(self):
        self.windowParent = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self._removeRow()
        else:
            if self.windowParent.Controller.isDocked():
                super(UnrealLiveLinkSubjectTable, self).keyPressEvent(event)

    def _mouseMoveEvent(self, event):
        modelIndex = self.indexAt(event.pos())
        rowIndex = modelIndex.row()
        columnIndex = modelIndex.column()

        if rowIndex != self.cellMouseHover[0]:
            self.hoverIndexChanged.emit(rowIndex)

        self.cellMouseHover = [rowIndex, columnIndex]

        if rowIndex == -1 or columnIndex == -1:
            self._leaveEvent(None)

    def _leaveEvent(self, event):
        self.cellMouseHover = [-1, -1]
        self.leaveTableEvent.emit()
        self.viewport().update()

    def _addRow(self):
        alreadyInList = self.windowParent.Controller.addSelection()
        self._refreshUI()
        if alreadyInList:
            self.windowParent.logMessage('One or more objects you have selected have already been added to the table.')

    def _clearUI(self):
        self.subjectList = []
        self.subjectTypes.clear()
        self.setRowCount(0)

    def _refreshUI(self):
        addedSelections = self.windowParent.Controller.refreshSubjects()

        if len(addedSelections) == 4 and all(addedSelections):
            self.subjectList = list(addedSelections[0])

            for (SubjectName, SubjectPath, SubjectType, SubjectRole) in zip(
                 addedSelections[0], addedSelections[1], addedSelections[2], addedSelections[3]):

                self.subjectTypes[SubjectPath] = SubjectType

                # Make sure not to add back subjects we already have in the list
                subjectAlreadyInList = False
                for rowIndex in range(self.rowCount()):
                    lineEdit = self.cellWidget(rowIndex, 1)
                    pathLineEdit = self.cellWidget(rowIndex, 2)
                    if SubjectName == lineEdit.text() and SubjectPath == pathLineEdit.text():
                        subjectAlreadyInList = True
                        break
                if subjectAlreadyInList:
                    continue

                # Add new row for the subject
                rowCount = self.rowCount()
                self.insertRow(rowCount)
                self.setRowHeight(rowCount, 32)
                self.setItemDelegateForRow(rowCount, self.rowDelegate)

                # Icon dropdown to display the stream type/role
                iconComboBox = ComboBox(self)
                if self.windowParent:
                    iconNames = UnrealLiveLinkSubjectTable.IconsPerSubjectType[SubjectType]
                    normalIcons = []
                    hoverIcons = []
                    for item in UnrealLiveLinkSubjectTable.StreamTypesPerSubjectType[SubjectType]:
                        iconName = iconNames[iconComboBox.count()]
                        iconComboBox.addItem(self.Icons[iconName], '  ' + item)
                        normalIcons.append(self.Icons[iconName])
                        hoverIcons.append(self.HoverIcons[iconName])
                    selectedItem = UnrealLiveLinkSubjectTable.StreamTypesPerSubjectType[SubjectType].index(SubjectRole)
                    iconComboBox.setCurrentIndex(selectedItem)
                    iconComboBox.initIcons(normalIcons, hoverIcons)
                iconComboBox.setIconSize(QSize(24, 24))
                iconComboBox.setStyleSheet('''QComboBox { background-color: transparent; }
                                              QComboBox:item::hover { background-color: #FF0000; }
                                              QComboBox:hover { color: palette(light|text ); }''')
                iconComboBox.setMinimumWidth(60)
                iconComboBox.view().setMinimumWidth(200)
                iconComboBox.currentIndexChanged.connect(lambda x, type=SubjectType, dagPath=SubjectPath: self._changeSubjectRole(x, type, dagPath))
                self.setCellWidget(rowCount, 0, iconComboBox)

                # Subject name
                lineEdit = SubjectLineEdit(self, SubjectName)
                lineEdit.textModified.connect(lambda old, new, dagPath=SubjectPath: self._changeSubjectName(old, new, dagPath))
                self.setCellWidget(rowCount, 1, lineEdit)

                # DAG path
                label = QLabel()
                label.setText(SubjectPath)
                self.setCellWidget(rowCount, 2, label)

            # Hide the instructions when there is at least one subject in the list
            if self.rowCount() > 0:
                self.emptyLabel.hide()

    def _removeRow(self):
        if self.rowCount() > 0:
            # Get the selected rows
            rowIndices = set()
            for index in self.selectedIndexes():
                rowIndices.add(index.row())

            # Remove each subject based on its DAG path
            for rowIndex in rowIndices:
                frame = self.cellWidget(rowIndex, 2)
                dagPath = frame.text()
                del self.subjectTypes[dagPath]
                self.windowParent.Controller.removeSubject(dagPath)

            # Remove the selected rows going in reverse order to make sure that row indices stay valid
            for rowIndex in sorted(rowIndices, reverse=True):
                self.removeRow(rowIndex)

        self._updateSubjectList()

        # Show the instructions when there is no subject in the list
        if self.rowCount() == 0:
            self.emptyLabel.show()

    def _changeSubjectName(self, oldName, newName, dagPath):
        if oldName != newName:
            self.windowParent.Controller.changeSubjectName(dagPath, newName)
            self._clearUI()
            self._refreshUI()

    def _updateSubjectList(self):
        addedSelections = self.windowParent.Controller.refreshSubjects()
        if len(addedSelections) == 4 and all(addedSelections):
            self.subjectList = list(addedSelections[0])

    def _changeSubjectRole(self, roleIndex, subjectRole, dagPath):
        if subjectRole not in UnrealLiveLinkSubjectTable.StreamTypesPerSubjectType:
            return

        streamTypes = UnrealLiveLinkSubjectTable.StreamTypesPerSubjectType[subjectRole]
        if roleIndex < len(streamTypes) and self.windowParent.Controller:
            self.windowParent.Controller.changeSubjectRole(dagPath, streamTypes[roleIndex])

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
# CwUAMA0GCSqGSIb3DQEBAQUABIIBgFa1ZpQcXrVPYxWElrFdq8CIPAPPqwp+gYiU
# 525V+WmOhazOrDcEOpZaesveNhgbYPHu2TZCzaWSs4OpF3+fE1717NyvepViupBF
# 8wNQrBC9fUCts0k64L/QIq6f1RBgyIkb0vYGCaF8dKjRDaIyD9B3rw5jIUmn3lCs
# y65pldnVYlKOXCdzNb/WmMifxJDJyoJq3VjH4smGxkKv53Qw0HUFEtwywfRnkL94
# VkQZmbBAQgwcaNtWq8eKE+/kLYwaGhh/1gpk5jFAojluh0Gwjub3TCtCaTi5w0CD
# KTjHvBlL8kddGeZ6T0fy6HRuum50Lh+f6HARDZvoMPn1VBmIVSxb0NsuQ8H3M26P
# PzAgy2bnKIyb0Ef9oLbf7zJHtYdOO8P32mNDX4e3/wMHB4dnkBQYLZ3ssWYKdjem
# QS2xdl2baupoHNyk3f8qzhi12DP0VfxrcFmvvfmSMydqGBgaPEK6+SDl03hGGjsh
# noKOmJoq1qUdeJ59ISEwQndjP/wn9w==
# -----END-SIGNATURE-----