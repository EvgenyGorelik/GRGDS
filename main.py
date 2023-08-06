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
    subsample_data,
    NpEncoder
)
from models import LinearRegressionModel
import time
import json

from plotters import HKLPlotter, FitPlotter

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
        makedirs("results",exist_ok=True)
    
    if args.save_figures:
        makedirs(args.save_figures,exist_ok=True)

    #TernaryPlot(TernaryPlot.extract_hkl_from_datasets(file_loaders))

    
    results = list()
    for i in range(len(file_loaders) - 1):
        for j in range(i + 1, len(file_loaders)):
            dataset_x = file_loaders[i]
            dataset_y = file_loaders[j]
            print(f"Fitting intensities of {dataset_x} to intensities of {dataset_y}")
            intersection = get_intersection(dataset_x, dataset_y)
            print(f"Got {len(intersection)} intesecting hkl values")
            if args.max_samples:
                intersection = subsample_data(intersection, args.max_samples)
            print(f"Using {len(intersection)} intesecting hkl values")
            if len(intersection) == 0:
                print(f"No intersecting hkl values for {dataset_x} and {dataset_y}")
                continue
            
            intersection_index_a = list()
            intersection_index_b = list()
            for hkl_tuple in intersection:
                intersection_index_a.append(find_index_by_hkl(hkl_tuple=hkl_tuple, dataset=dataset_x.hkl()))
                intersection_index_b.append(find_index_by_hkl(hkl_tuple=hkl_tuple, dataset=dataset_y.hkl()))
            intersection_index_a = np.array(intersection_index_a)
            intersection_index_b = np.array(intersection_index_b)

            X = dataset_x.intensities()[intersection_index_a] 
            y_hat = dataset_y.intensities()[intersection_index_b]
            weights = np.ones(len(intersection_index_a)) \
                        - dataset_y.errors()[intersection_index_b]/np.max(dataset_y.errors())\
                        * dataset_x.errors()[intersection_index_a]/np.max(dataset_x.errors())

            model = LinearRegressionModel(target_values=y_hat, input_values=X, weights=weights)

            
            tic = time.time()
            result = optim.minimize(method="BFGS", fun=model, x0=np.ones(2))
            toc = time.time()
            print(f"elapsed time: {toc-tic} s")
            print(f"Fitting function:\n I_{dataset_y} = {result.x[0]} + {result.x[1]} * I_{dataset_x}")
            results.append({
                "dataset_x": str(dataset_x),
                "dataset_y": str(dataset_y),
                "scaling_factor": result.x[1],
                "offset": result.x[0],
                "variance": result.fun,
                "correspondences": len(intersection)
            })

            if args.save_figures:
                plt.figure()
                plt.title(f"Plotted intensities")
                plt.scatter(X, y_hat)
                plt.xlabel(f"Intensities {dataset_x}")
                plt.ylabel(f"Intensities {dataset_y}")
                plt.savefig(path.join(args.save_figures,f"{dataset_x}_{dataset_y}.png"))
                plt.close()
                
                fit_plotter = FitPlotter(np.stack([X, y_hat],axis=1), fitted_function=model.func, weights=weights, xlabel=str(dataset_x), ylabel=str(dataset_y))
                fit_plotter.savefig(path.join(args.save_figures,f"{dataset_x}_{dataset_y}_fitted.png"))
                #HKLPlotter(dataset_y.hkl()[intersection_index_b]).save_figure(path.join(args.save_figures,f"{dataset_x}_{dataset_y}_hkl_overlap.png"))
                
                
    json.dump(results, open(path.join("results",f"result_{int(time.time())}.json"), "w+"),indent=4,cls=NpEncoder)

if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument("data", help="File path to directory containing .hkl files", default="data", type=str)
    parser.add_argument("--max_samples", help="This arguments defines an upper bound on the number of intersecting hkl indices", default=None, type=int)
    parser.add_argument("--save_figures", help="Set the path to the folder, where images will be stored", default=None)
    main(parser.parse_args())
