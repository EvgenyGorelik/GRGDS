import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

class TernaryPlot():
    def __init__(self, datasets: np.ndarray):
        '''
        Description
        -----------
        Plots ternary plots of hkl values
        
        :param datasets: data in [h,k,l,dataset_num]
        '''
        makeAxis = lambda title, tickangle: {
            'title': title,
            'titlefont': { 'size': 20 },
            'tickangle': tickangle,
            'tickfont': { 'size': 15 },
            'tickcolor': 'rgba(0,0,0,0)',
            'ticklen': 5,
            'showline': True,
            'showgrid': True
            }
        fig = go.Figure(go.Scatterternary({
                'mode': 'markers',
                'a': datasets[:,0],
                'b': datasets[:,1],
                'c': datasets[:,2],
                'text': datasets[:,3],
                'marker': {
                'symbol': 0,
                'color': datasets[:,3],
                'size': 5,
                'line': { 'width': 1 },
                'opacity': 0.3
                }
            }))
        fig.update_layout({
                'ternary': {
                'sum': np.max(datasets[:,:3]),
                'aaxis': makeAxis('h', 0),
                'baxis': makeAxis('k', 45),
                'caxis': makeAxis('l', -45)
                },
                'annotations': [{
                'showarrow': False,
                'text': 'hkl-distribution',
                'x': 0.5,
                'y': 1.3,
                'font': { 'size': 15 }
                }]
            })
        fig.show()



    @staticmethod
    def get_color(n):
        return np.mod((np.ones((len(n),3))*n.reshape(-1,1)*5.4)**3.3, 1) 

    @staticmethod
    def extract_hkl_from_datasets(file_loaders: list):
        hkl = []
        for i, loader in enumerate(file_loaders):
            loader_hkl = loader.hkl()
            hkl.extend(np.hstack([np.array(loader_hkl), np.ones((len(loader_hkl),1))*(i*10)]))
        data = np.array(hkl, dtype=np.int32)
        data[:,:3] -= np.min(data[:,:3], axis=0)
        return data