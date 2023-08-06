'''
Plotter for overlapping hkl values in datasets
'''
import matplotlib.pyplot as plt
from numpy import ndarray

class HKLPlotter():
    def __init__(self, hkl_values: ndarray , save_path: str, weights: ndarray = None):
        self.hkl_values = hkl_values
        self.weights = weights

    def savefig(self, save_path):
        ax = plt.axes(projection="3d")
        plt.title(f"hkl Overlap")
        ax.scatter(self.hkl_values[:,0], self.hkl_values[:,1], self.hkl_values[:,2], alpha=self.weights)
        ax.set_xlabel("h")
        ax.set_ylabel("k")
        ax.set_zlabel("l")
        plt.savefig(save_path)
        plt.close()
    