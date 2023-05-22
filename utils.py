import numpy as np
from datareader import DataReader

def get_intersection(dataset_a: DataReader, dataset_b: DataReader) -> list:
    a_hkl = set([tuple(item) for item in dataset_a.hkl()])
    b_hkl = set([tuple(item) for item in dataset_b.hkl()])
    intersection = list(a_hkl.intersection(b_hkl))
    return intersection

def find_index_by_hkl(hkl_tuple: tuple, dataset: np.ndarray):
    for i in range(dataset.shape[0]):
        if (dataset[i,:3].astype(int) == hkl_tuple).all():
            return i
    return None