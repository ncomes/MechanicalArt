try:
    from PySide6 import QtWidgets as qtwidgets
    from PySide6 import QtCore as qtcore
    from PySide6 import QtGui as qtgui
    import shiboken6 as shiboken
    from PySide6 import QtUiTools as qtuitools
except:
    from PySide2 import QtWidgets as qtwidgets
    from PySide2 import QtCore as qtcore
    from PySide2 import QtGui as qtgui
    import shiboken2 as shiboken
    from PySide2 import QtUiTools as qtuitools


