import pandas as pd
import numpy as np
import os

class weatherPreprocess:
    def __init__(self, dataPath, startYear, endYear):
        # startYear : 1990
        # endYear : 2024
        self.dataPath = dataPath
        self.dataFiles = os.listdir(self.dataPath)
        self.dataFiles.sort()

        self.yearRange = range(startYear, endYear)

        self.categoricalColumns = ["전운량(10분위)", "중하층운량(10분위)", "풍향(16방위)"]

    def dataConcat(self):
        data = pd.DataFrame()
        for name in self.yearRange:
            if name != 1990:
                df = pd.read_csv(f"{self.dataPath}/기상청데이터_{name}.csv", encoding="cp949")
                data = pd.concat([data, df], ignore_index=True)
            else:
                data1990 = pd.read_csv(f"{self.dataPath}/기상청데이터_{name}.csv", encoding="cp949")
        data.reset_index(drop=True, inplace=True)
        data1990.reset_index(drop=True, inplace=True)
        return data, data1990
    
    def DropColumns(self):
        data, _ = self.dataConcat()
        dropColList = ["지면상태(지면상태코드)", "index", "현상번호(국내식)", "운형(운형약어)", "일사(MJ/m2)",
                       "3시간신적설(cm)","5cm 지중온도(°C)", "10cm 지중온도(°C)", "20cm 지중온도(°C)",
                       "30cm 지중온도(°C)"]
        data.drop(dropColList, axis=1, inplace=True)
        anotherDropColList = list(data.columns[data.columns.str.contains("QC플래그")])
        data.drop(anotherDropColList, axis=1, inplace=True)
        return data
    
    def makeDateIndex(self):
        data = self.DropColumns()
        data['일시'] = pd.to_datetime(data["일시"])
        data["년월일"] = data["일시"].dt.strftime("%Y-%m-%d")
        data.index = pd.to_datetime(data["년월일"])
        data.drop(["년월일"], axis=1, inplace=True)
        return data
    
    def fillNa(self):
        data = self.makeDateIndex()

        # For Numerical Data
        numericalColumns = list(data.columns)
        for col in self.categoricalColumns:
            if col in numericalColumns:
                numericalColumns.remove(col)
        for col in list(numericalColumns):
            data[col].interpolate(inplace=True)
        
        # For Categorical Data
        for col in self.categoricalColumns:
            data[col] = data[col].fillna(method='ffill')
        data = data[data.index.year > 1990]
        return data
    
    def getAverage(self):
        data = self.fillNa()
        if "Unnamed: 0" in data.columns:
            data.drop(["Unnamed: 0"], axis=1, inplace=True)
        dataColumns = list(data.columns)[2:]
        
        for col in self.categoricalColumns:
            dataColumns.remove(col)
        
        for name in dataColumns:
            colName = "평균"+str(name)
            data[colName] = data[name].groupby(level=0).mean()

        for name in self.categoricalColumns:
            colName = "평균"+str(name)
            data[colName] = round(data[name].groupby(level=0).mean())
        
        return data
    
    def finalProcess(self):
        data = self.getAverage()
        data = data[["지점", "지점명", "평균기온(°C)", "평균강수량(mm)", "평균습도(%)"]]

        for col in data.columns[2:]:
            for i in range(1,8):
                name = f"{i}일전{col}"
                data[name] = 0
        # 이후 도중에 수동으로 데이터 수정 ->> 후에 코드 제작 #
        data = data[data.index.year >= 2000]
        data = data.drop_duplicates()
        return data
    

class sunPreprocess:
    def __init__(self, dataPath):
        self.dataPath = dataPath

    def makeDateIndex(self):
        data = pd.read_csv(self.dataPath)
        if "Unnamed: 0" in data.columns:
            data.drop(["Unnamed: 0"], axis=1, inplace=True)
        data.index = pd.to_datetime(data["날짜"], format="%Y%m%d")
        data.drop(["날짜"], axis=1, inplace=True)
        return data

    def finalPreprocess(self):
        data = self.makeDateIndex(self)
        for col in data.columns[1:]:
            data[col] = data[col].apply(lambda x:int(x[:x.index("˚")].replace(" ", "")))
        return data


if __name__ == "__main__":
    weatherProcessor = weatherPreprocess("./weather_dataset", 1990, 2024)
    weatherData = weatherProcessor.finalPreprocess()
    weatherData.to_csv("일별_합천기상데이터.csv", index=False, encoding="utf-8-sig")

    sunProcessor = sunPreprocess("태양고도데이터.csv")
    sunData = sunProcessor.finalPreprocess()
    sunData["남중고도"].to_csv("태양남중고도데이터.csv", encoding="utf-8-sig", index=False)