
from PySide6 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg
import numpy as np
from func.datareader import DataReader
from func.utils import (
    extract_data
)
from plotters import FitPlotter
import time
from models.linear_regression_model import LinearRegressionModel
from os import path, makedirs
from scipy import optimize as optim


class CentralWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setLayout(QtWidgets.QHBoxLayout(self))

        self.toolbar = QtWidgets.QToolBar("Main Toolbar")
        
        display_window = QtWidgets.QFrame(self)
        display_window_layout = QtWidgets.QVBoxLayout(self)
        display_window.setLayout(display_window_layout)
        
        self.figure_path = "results/images"
        self.max_samples = 100
        
        # self.graph = pg.ScatterPlotItem()
        # self.plot = pg.plot()
        # self.plot.setBackground("w")
        # self.plot.addItem(self.graph)
        # display_window_layout.addWidget(self.plot)
        
        self.plot = QtWidgets.QLabel()
        self.plot.setPixmap(QtGui.QPixmap("assets/image.png"))
        display_window_layout.addWidget(self.plot)

        self.console = QtWidgets.QTextEdit(alignment=QtCore.Qt.AlignLeft,readOnly=True)
        display_window_layout.addWidget(self.console)
        self.button = QtWidgets.QPushButton("Calculate")
        display_window_layout.addWidget(self.button)

        self.file_list = QtWidgets.QListWidget()
        self.file_list_data = None

        
        self.result_list = QtWidgets.QListWidget()
        self.results = None

        self.layout().addWidget(self.file_list)
        self.layout().addWidget(self.result_list)
        self.layout().addWidget(display_window)

        self.button.clicked.connect(self.magic)
        self.result_list.currentRowChanged.connect(self.itemActivated_event)

    def write_message(self, msg):
        self.console.setPlainText(f"{msg}\n"+self.console.toPlainText())


    def itemActivated_event(self, item):
        print(item)
        height, width, channel = self.results[item]['image'].shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(self.results[item]['image'].data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.plot.setPixmap(QtGui.QPixmap.fromImage(qImg))
        

    @QtCore.Slot()
    def magic(self):        
        file_loaders = []
        for file in self.file_list_data:
            file_loaders.append(DataReader(file))
        self.write_message(f"Loaded {len(file_loaders)} files")

        self.results = list()
        self.result_list.clear()
        for i in range(len(file_loaders) - 1):
            for j in range(i + 1, len(file_loaders)):
                dataset_x = file_loaders[i]
                dataset_y = file_loaders[j]
                self.write_message(f"Fitting intensities of {dataset_x} to intensities of {dataset_y}")
                extracted_data = extract_data(dataset_x=dataset_x, dataset_y=dataset_y, max_samples=self.max_samples)
                if extracted_data["x_values"] is None:
                    self.write_message(f"No intersecting hkl values for {dataset_x} and {dataset_y}")
                    continue
                self.write_message(f"Got {len(extracted_data['intersection_total'])} intesecting hkl values")
                self.write_message(f"Using {len(extracted_data['intersection_subsampled'])} intesecting hkl values")
                
                model = LinearRegressionModel(target_values=extracted_data["y_values"], input_values=extracted_data["x_values"], weights=extracted_data["weights"])
                
                tic = time.time()
                result = optim.minimize(method="BFGS", fun=model, x0=np.ones(2))
                toc = time.time()
                self.write_message(f"elapsed time: {toc-tic} s")
                self.write_message(f"Fitting function:\n I_{dataset_y} = {result.x[0]} + {result.x[1]} * I_{dataset_x}")
                plotter = FitPlotter(np.stack([extracted_data["y_values"], extracted_data["x_values"]],axis=1), fitted_function=model.func, weights=extracted_data["weights"])
                self.results.append({
                    "dataset_x": str(dataset_x),
                    "dataset_y": str(dataset_y),
                    "scaling_factor": result.x[1],
                    "offset": result.x[0],
                    "variance": result.fun,
                    "correspondences": len(extracted_data['intersection_total']),
                    "image": plotter.getfig() 
                })
                self.result_list.addItem(f"{self.results[-1]['dataset_x']}_{self.results[-1]['dataset_y']}")