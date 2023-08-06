
from PySide6 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg
import numpy as np


class CentralWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setLayout(QtWidgets.QHBoxLayout(self))

        self.toolbar = QtWidgets.QToolBar("Main Toolbar")
        
        display_window = QtWidgets.QFrame(self)
        display_window_layout = QtWidgets.QVBoxLayout(self)
        display_window.setLayout(display_window_layout)
        
        
        self.graph = pg.ScatterPlotItem()
        self.plot = pg.plot()
        self.plot.setBackground("w")
        self.plot.addItem(self.graph)
        display_window_layout.addWidget(self.plot)
        self.console = QtWidgets.QTextEdit(alignment=QtCore.Qt.AlignLeft,readOnly=True)
        display_window_layout.addWidget(self.console)
        self.button = QtWidgets.QPushButton("Calculate")
        display_window_layout.addWidget(self.button)

        self.file_list = QtWidgets.QListWidget()
        self.layout().addWidget(self.file_list)
        self.layout().addWidget(display_window)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.graph.clear()
        self.graph.addPoints(np.random.rand(100), np.random.rand(100))
        self.console.setPlainText("Scatter Plot with 100 points\n"+self.console.toPlainText())
        