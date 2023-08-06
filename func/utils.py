import numpy as np
from func.datareader import DataReader
from json import JSONEncoder

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

def extract_data(dataset_x: DataReader, dataset_y: DataReader, max_samples: int = None):
    result = {}
    result["intersection_total"] = get_intersection(dataset_x, dataset_y)
    if max_samples is not None:
        intersection = subsample_data(result["intersection_total"], max_samples)
        result["intersection_subsampled"] = intersection
    else:
        intersection = result["intersection_total"]
        result["intersection_subsampled"] = None
    if len(intersection) == 0:
        result["x_values"] = None
        result["y_values"] = None
        return result
    
    intersection_index_a = list()
    intersection_index_b = list()
    for hkl_tuple in intersection:
        intersection_index_a.append(find_index_by_hkl(hkl_tuple=hkl_tuple, dataset=dataset_x.hkl()))
        intersection_index_b.append(find_index_by_hkl(hkl_tuple=hkl_tuple, dataset=dataset_y.hkl()))
    intersection_index_a = np.array(intersection_index_a)
    intersection_index_b = np.array(intersection_index_b)
    result["x_values"] = dataset_x.intensities()[intersection_index_a] 
    result["y_values"] = dataset_y.intensities()[intersection_index_b]
    result["weights"] = np.ones(len(intersection_index_a)) \
                        - dataset_y.errors()[intersection_index_b]/np.max(dataset_y.errors())\
                        * dataset_x.errors()[intersection_index_a]/np.max(dataset_x.errors())
    return result

def subsample_data(l: list, num_samples: int) -> list:
    if len(l) <= num_samples:
        return l
    return np.array(l)[np.random.choice(len(l), size=num_samples, replace=False)].tolist()

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