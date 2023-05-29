import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import optimize as optim
from argparse import ArgumentParser
from glob import glob
from os import path, makedirs
from datareader import DataReader
from utils import (
    get_intersection,
    find_index_by_hkl,
    subsample_data
)
import time
import json

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

    if not path.exists("results"):
        makedirs("results")
    
    if args.save_figures:
        makedirs(args.save_figures)
    coefficients = list()
    for i in range(len(file_loaders) - 1):
        for j in range(i + 1, len(file_loaders)):
            dataset_a = file_loaders[i]
            dataset_b = file_loaders[j]
            print(f"Fitting intensities of {dataset_a} to intensities of {dataset_b}")
            intersection = get_intersection(dataset_a, dataset_b)
            print(f"Got {len(intersection)} intesecting hkl values")
            if args.max_samples:
                intersection = subsample_data(intersection, args.max_samples)
            print(f"Using {len(intersection)} intesecting hkl values")
            
            intersection_index_a = list()
            intersection_index_b = list()
            for hkl_tuple in intersection:
                intersection_index_a.append(find_index_by_hkl(hkl_tuple=hkl_tuple, dataset=dataset_a.hkl()))
                intersection_index_b.append(find_index_by_hkl(hkl_tuple=hkl_tuple, dataset=dataset_b.hkl()))
            intersection_index_a = np.array(intersection_index_a)
            intersection_index_b = np.array(intersection_index_b)

            X = dataset_a.intensities()[intersection_index_a] 
            y_hat = dataset_b.intensities()[intersection_index_b]



            def func(params):
                return np.sum((y_hat - (params[0] + params[1]*X))**2)
            
            tic = time.time()
            result = optim.minimize(method="BFGS", fun=func, x0=np.ones(2))
            toc = time.time()
            print(f"elapsed time: {toc-tic} s")
            print(f"Fitting function:\n I_{dataset_b} = {result.x[0]} + {result.x[1]} * I_{dataset_a}")
            coefficients.append({
                "dataset_a": str(dataset_a),
                "dataset_b": str(dataset_b),
                "coefficient": result.x[1]
            })

            lin_grid = np.linspace(0,np.max(X),100)

            if args.save_figures:
                plt.figure()
                plt.title(f"Plotted intensities")
                plt.scatter(X, y_hat)
                plt.xlabel(f"Intensities {dataset_a}")
                plt.ylabel(f"Intensities {dataset_b}")
                plt.savefig(path.join(args.save_figures,f"{dataset_a}_{dataset_b}.png"))
                plt.figure()
                plt.title(f"Fitted Line")
                plt.scatter(X, y_hat)
                plt.plot(lin_grid,result.x[0] + result.x[1]*lin_grid)
                plt.xlabel(f"Intensities {dataset_a}")
                plt.ylabel(f"Intensities {dataset_b}")
                plt.savefig(path.join(args.save_figures,f"{dataset_a}_{dataset_b}_fitted.png"))
    json.dump(coefficients, open(path.join("results",f"result_{int(time.time())}.json"), "w+"),indent=4)

        
            

            

if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument("data", help="File path to directory containing .hkl files", default="data", type=str)
    parser.add_argument("--max_samples", help="This arguments defines an upper bound on the number of intersecting hkl indices", default=None, type=int)
    parser.add_argument("--save_figures", help="Set the path to the folder, where images will be stored", default=None)
    main(parser.parse_args())
