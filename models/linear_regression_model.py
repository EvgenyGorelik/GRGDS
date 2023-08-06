import numpy as np

class LinearRegressionModel():
    def __init__(self, target_values: np.ndarray, input_values: np.ndarray, weights: np.ndarray = None):
        self.target_values = target_values
        self.input_values = input_values
        self.params = np.ones(2)
        if weights is not None:
            self.weights = weights
        else:
            self.weights = np.ones_like(target_values)
        
    def __call__(self, params):
        self.params = params
        return np.sum(self.weights * (self.target_values - self.func(self.input_values))**2)

    def func(self, input_values):
        return self.params[0] + self.params[1]*input_values