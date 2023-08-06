from typing import Callable
from numpy import ndarray, ones
import matplotlib.pyplot as plt
import numpy as np

class FitPlotter():
    def __init__(self, data_points: ndarray, fitted_function: Callable = None, weights: ndarray  = None, xlabel: str = "x", ylabel: str = "y"):
        self.data_points = data_points
        if weights is not None:
            self.weights = weights
        else:
            self.weights = ones(data_points.shape[0])
        self.fitted_function = fitted_function
        self.xlabel = xlabel
        self.ylabel = ylabel
        
    def plot(self):
        fig = plt.figure()
        plt.title(f"Fitted Line")
        plt.scatter(self.data_points[:,0],self.data_points[:,1], alpha=self.weights)
        lin_grid = np.linspace(0, np.max(self.data_points[:, 0]), 100)
        plt.plot(lin_grid, self.fitted_function(lin_grid))
        plt.xlabel(f"Intensities {self.xlabel}")
        plt.ylabel(f"Intensities {self.ylabel}")
        return fig

    def savefig(self, save_path):
        fig = self.plot()
        fig.savefig(save_path)
        plt.close()

    def getfig(self):
        fig = self.plot()
        canvas = fig.canvas
        canvas.draw()  # Draw the canvas, cache the renderer
        image_flat = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
        image = image_flat.reshape(*reversed(canvas.get_width_height()), 3)
        plt.close()
        return image