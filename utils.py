import numpy as np
from datareader import DataReader
from json import JSONEncoder

def subsample_data(l: list, num_samples: int) -> list:
    if len(l) <= num_samples:
        return l
    return np.array(l)[np.random.choice(len(l), size=num_samples, replace=False)].tolist()

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


class NpEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, (np.floating, np.complexfloating)):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.string_):
            return str(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, timedelta):
            return str(obj)
        return super(NpEncoder, self).default(obj)