import pandas as pd
import numpy as np
import os

class dataConcator:
    def __init__(self, weatherPath, damPath):
        self.weatherData = pd.read_csv(weatherPath)
        self.damData = pd.read_csv(damPath)
        self.weatherData.index = pd.to_datetime(self.weatherData["년월일"])
        self.weatherData.drop(["지점", "지점명", "년월일"], axis=1, inplace=True)
        
        self.damData.index = pd.to_datetime(self.damData["시간"])
        self.damData.drop(["시간"], axis=1, inplace=True)
        
    def concat(self):
        totalData = pd.merge(self.weatherData, self.damData, left_index=True, right_index=True, how="left")
        return totalData

if __name__ == "__main__":
    data_concator = dataConcator("./data/일별_합천기상데이터(전데이터수정최종).csv", "./data/합천다목적댐_일별_0511.csv")
    total_data = data_concator.concat()
    total_data.to_csv("./data/합천댐_기상종합데이터.csv", index=False, encoding="utf-8-sig")