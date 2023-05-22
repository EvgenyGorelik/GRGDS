import sys
import numpy as np
import random
from PySide6 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")

        self.toolbar = QtWidgets.QToolBar("Main Toolbar")
        

        self.layout = QtWidgets.QVBoxLayout(self)
        
        
        self.graph = pg.ScatterPlotItem()
        self.plot = pg.plot()
        self.plot.setBackground("w")
        self.plot.addItem(self.graph)
        self.layout.addWidget(self.plot)
        self.console = QtWidgets.QLineEdit(alignment=QtCore.Qt.AlignLeft,readOnly=True)

        self.layout.addWidget(self.console)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.graph.clear()
        self.graph.addPoints(np.random.rand(100),np.random.rand(100))
        self.console.setText(self.console.text()+"\nScatter Plot with 100 points")
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())