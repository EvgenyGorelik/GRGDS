import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import optimize as optim
from argparse import ArgumentParser
from glob import glob
from os import path
from datareader import DataReader
from utils import (
    get_intersection,
    find_index_by_hkl
)
import time

def main(args):
    assert path.exists(args.data), f"Directory {path.abspath(args.data)} not available"
    file_list = glob(args.data + "/*")
    print(f"Found {len(file_list)} files in {path.abspath(args.data)}")
    if len(file_list) < 2:
        print("ERROR: Not enough files")
        exit()
    
    file_loaders = []
    for file in file_list:
        file_loaders.append(DataReader(file))
    print(f"Loaded {len(file_loaders)} files")

    for i in range(len(file_loaders) - 1):
        for j in range(i + 1, len(file_loaders)):
            dataset_a = file_loaders[i]
            dataset_b = file_loaders[j]
            print(f"Fitting intensities of {dataset_a} to intensities of {dataset_b}")
            intersection = get_intersection(dataset_a, dataset_b)
            print(f"Got {len(intersection)} intesecting hkl values")
            intersection_index_a = list()
            intersection_index_b = list()
            for hkl_tuple in intersection:
                intersection_index_a.append(find_index_by_hkl(hkl_tuple=hkl_tuple, dataset=dataset_a.hkl()))
                intersection_index_b.append(find_index_by_hkl(hkl_tuple=hkl_tuple, dataset=dataset_b.hkl()))
            intersection_index_a = np.array(intersection_index_a)
            intersection_index_b = np.array(intersection_index_b)

            X = dataset_a.intensities()[intersection_index_a] 
            y_hat = dataset_b.intensities()[intersection_index_b]

            plt.figure()
            plt.scatter(X, y_hat)
            plt.xlabel(f"Intensities {dataset_a}")
            plt.ylabel(f"Intensities {dataset_b}")
            plt.waitforbuttonpress(2)


            def func(params):
                return np.sum((y_hat - (params[0] + params[1]*X))**2)
            
            result = optim.minimize(method="BFGS", fun=func, x0=np.array([np.min(y_hat), np.mean(y_hat / X)]))
            print(f"Fitting function:\n I_{dataset_b} = {result.x[0]} + {result.x[1]} * I_{dataset_a}")

            lin_grid = np.linspace(0,np.max(X),100)

            plt.figure()
            plt.scatter(X, y_hat)
            plt.plot(lin_grid,result.x[0] + result.x[1]*lin_grid)
            plt.xlabel(f"Intensities {dataset_a}")
            plt.ylabel(f"Intensities {dataset_b}")
            plt.waitforbuttonpress(2)

        
if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument("data", help="File path to directory containing .hkl files", default="data")
    main(parser.parse_args())