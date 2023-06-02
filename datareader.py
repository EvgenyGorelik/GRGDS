import numpy as np
from os import path
import pandas as pd
import re

class DataReader():
    def __init__(self, file):
        assert path.exists(file), f"File {file} doesn't exist"
        self.file = file
        self.file_name, self.ext = path.splitext(file)
        self._name = path.basename(self.file_name)
        if self.ext == ".hkl":
            self.data = self.read_hkl()
        elif self.ext == ".csv":
            self.data = pd.load_csv(file)
        else:
            raise NotImplementedError(f"File format {self.ext} unknown")
        np_data = np.array(self.data)
        self._hkl = np_data[:,:3].astype(np.int16)
        self._intensities = np_data[:,3]
        if np_data.shape[1] > 4:
            self.error = np_data[:,4]
    
    def __str__(self):
        return self._name
        
    
    def hkl(self):
        return self._hkl

    def intensities(self):
        return self._intensities

    def read_hkl(self):
        data = []
        with open(self.file) as f:
            lines = f.readlines()
            for line in lines:
                if line != "":
                    h = float(line[0:4])
                    k = float(line[4:8])
                    l = float(line[8:12])
                    intensity = float(line[12:20])
                    error = 0
                    try: 
                        error = float(line[20:28])
                    except IndexError as e:
                        pass
                    data.append([h, k, l, intensity, error])
        return data


if __name__== "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    data_reader = DataReader(args.file)
    print(data_reader.hkl)