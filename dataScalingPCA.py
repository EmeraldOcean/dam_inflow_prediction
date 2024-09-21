import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler


class Scaler:
    def __init__(self, method):
        if method == 'robust':
            self.scaler = RobustScaler()
        elif method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            print('Select method')
            self.scaler = None
    def get(self):
        return self.scaler
    
class PcaTsne:
    def __init__(self, method, **kwargs):
        if method == "PCA":
            self.scaler = PCA(**kwargs)
        elif method == "TSNE":
            self.scaler = TSNE(**kwargs)
        else:
            print('Select method')
            self.scaler = None
    def get(self):
        return self.scaler


if __name__ == '__main__':
    data = pd.read_csv('./data/합천댐_기상종합_전처리_scaled_flood.csv')
    data.rename(columns = {'Unnamed: 0':'date'}, inplace=True)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    y = data['당일유입량']
    x = data.drop('당일유입량', axis=1)

    scaler = Scaler("minmax").get()
    x_scaled = scaler.fit_transform(x)

    pca = PcaTsne("PCA", n_components=3).get()
    x_pca = pca.fit_transform(x_scaled)
    # print(pca.explained_variance_ratio_)
    pd.DataFrame(x_pca).to_csv("./data/pca_result_flood.csv", index=False)