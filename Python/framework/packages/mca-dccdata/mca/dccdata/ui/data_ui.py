# -*- coding: utf-8 -*-

# mca python imports
import os
import logging
# PySide2 imports
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QPainter, QPen
from PySide2.QtCharts import QtCharts

from PySide2.QtCore import QFile, QSettings, Qt
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide2 import QtUiTools

# mca imports
from mca.dccdata.gscore import gs

logger = logging.getLogger('MCA_DCC_DATA')


class MCAMainWindow(QMainWindow):
    INITIAL_WIDTH_FALLBACK = 150
    INITIAL_HEIGHT_FALLBACK = 100

    def __init__(self, title, ui_path=None, version='1.0.0', parent=None):
        super().__init__(parent=parent)
        self.title = f'MAT {title}'
        self.single_window_instance()

        self.setWindowTitle(f'{self.title} {version}')

        self.ui = None

        self.setMinimumHeight(MCAMainWindow.INITIAL_HEIGHT_FALLBACK)
        self.setMinimumWidth(MCAMainWindow.INITIAL_WIDTH_FALLBACK)
        self.setContentsMargins(0,0,0,0)
        if ui_path:
            loader = QtUiTools.QUiLoader()
            file = QFile(os.path.abspath(ui_path))
            if file.open(QFile.ReadOnly):
                self.ui = loader.load(file, parent)
                file.close()
                self.setCentralWidget(self.ui)
        else:
            self.central_widget = QWidget(self)
            self.main_layout = QVBoxLayout(self.central_widget)
            self.setCentralWidget(self.central_widget)
            self.main_layout.setContentsMargins(0, 0, 0, 0)

        username = os.getlogin()
        self.settings = QSettings(username, self.title)
        geometry = self.settings.value('geometry', bytes('', 'utf-8'))
        self.restoreGeometry(geometry)
        self.show()

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)
        super().closeEvent(event)


class DCCData(MCAMainWindow):
    VERSION = '1.0.0'
    
    def __init__(self, parent=None):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'dcc_data.ui')
        print(ui_path)
        super().__init__(title='DCC Data',
                         ui_path=ui_path,
                         version=DCCData.VERSION,
                         parent=parent)
        self.setMinimumSize(600, 750)
        self.gs_data = gs.GSToolData(gs.DCC_TRACKING_SOFTWARE_ID, gs.SERVICE_ACCOUNT_FILE)
        self.create_bar_chart()

        QApplication.activeWindow()
        # raise RuntimeError('Not an Error!')
        
    def create_bar_chart(self):
        tools_list = self.gs_data.get_tools_count(total_number=25)
        series = QtCharts.QHorizontalBarSeries()
        categories = []
        bar_list = []
        bar_set = QtCharts.QBarSet('tool')
        tools_list.reverse()
        for tool, num in tools_list:
            bar_list.append(float(num))
            categories.append(str(tool))
        bar_set.append(bar_list)
        series.append(bar_set)
        
        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        chart.setTitle('Test Chart')

        axis = QtCharts.QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisY(axis, series)
        #axis.setLabelsAngle(-90)

        chart.legend().setVisible(False)
        #chart.legend().setAlignment(Qt.AlignBottom)
        
        chartview = QtCharts.QChartView(chart)
        #chartview.setRenderHint(QPainter.Antialiasing)
        
        #self.chart_v_box = QVBoxLayout(self.ui.chart_frame)
        self.ui.chart_v_layout.addWidget(chartview)
        
    def create_piechart(self):
        tools_dict = self.gs_data.get_tools_count(total_number=25)
        series = QtCharts.QPieSeries()
        tools_dict.reverse()
        for x, (tool, num) in enumerate(tools_dict.items()):
            series.append(str(tool), int(num))
            slice = series.slices()[x]
            slice.setExploded(False)
            slice.setLabelVisible(True)

        #series = QPieSeries()
        # series.append('Python', 80)
        # series.append('C++', 70)
        # series.append('Java', 50)
        # series.append('C#', 80)
        # series.append('PHP', 30)
        
        # adding slice
        #slice = QPieSlice()
        slice = series.slices()[2]
        slice.setExploded(True)
        slice.setLabelVisible(True)
        slice.setPen(QPen(Qt.darkGreen, 2))
        slice.setBrush(Qt.green)
        
        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        chart.setTitle('Test Chart')
        
        
        chartview =QtCharts.QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.main_layout.addWidget(chartview)
