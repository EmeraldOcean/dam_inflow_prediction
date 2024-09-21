import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt

# # For jupyter Notebook
# !sudo apt-get install -y fonts-nanum
# !sudo fc-cache -fv
# !rm ~/.cache/matplotlib -rf

# # 런타임 재시작 시 적용
# plt.rc('font', family='NanumBarunGothic')
# plt.rc('axes', unicode_minus=False)

plt.rcParams["axes.grid"]=True

class damGraph:
    def __init__(self, dataPath):
        self.data = pd.read_csv(dataPath)
        self.data['시간'] = pd.to_datetime(self.data['시간'])
        self.data.sort_values('시간', inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    def oneRainGraph(self, column):
        plt.plot(self.data['시간'], self.data[column])
        plt.title(column)
        plt.savefig(f"./graph/{column}.png")
        plt.close()

    def yesterdayTodayRain(self):
        plt.plot(self.data['강우량금일'], label='금일')
        plt.plot(self.data['강우량전일'], label='전일')
        plt.title('강우량')
        plt.legend(['강우량금일','강우량전일'])
        plt.savefig("./graph/전일금일강우량비교.png")
        plt.close()

class weatherGraph:
    def __init__(self, dataPath):
        self.data = pd.read_csv(dataPath)
    
    def meanTemp(self):
        plt.figure(figsize=(20,4))

        # # 기간 별로 그래프 그리기
        # dataYear1 = self.data[(self.data.index.year >= 2016) & (self.data.index.year <= 2019)]
        # dataYear2 = self.data[(self.data.index.year >= 2010) & (self.data.index.year <= 2015)]

        sns.lineplot(data=self.data, x=self.data.index, y="평균기온(°C)")
        # sns.lineplot(data=dataYear1, x=dataYear1.index, y="평균기온(°C)", label="2016~2019")
        # sns.lineplot(data=dataYear2, x=dataYear2.index, y="평균기온(°C)", label="2010~2019")

        plt.xlabel("연도")
        plt.title("2000.01.01~2023.04.06 합천군 평균기온(°C)")
        plt.savefig("./graph/2000.01.01~2023.04.06 합천군 평균기온.png")
        plt.close()

        # # 특정 날짜에 대한 평균 기온 그래프
        # plt.figure(figsize=(20,4))
        # sns.lineplot(data=self.data[self.data.index.year == 2020], x=self.data[self.data.index.year == 2020].index, y="평균기온(°C)")
        # plt.xlabel("날짜")
        # plt.title("2020년 합천군 평균기온(°C)")
        # plt.savefig("./graph/2020년 합천군 평균기온.png")
        plt.close()
        
    def meanRain(self):
        plt.figure(figsize=(20,4))
        sns.lineplot(data=self.data, x=self.data.index, y="평균강수량(mm)")
        plt.xlabel("연도")
        plt.title("2000.01.01~2023.04.06 합천군 평균강수량(mm)")
        plt.savefig("./graph/2000.01.01~2023.04.06 합천군 평균강수량.png")
        plt.close()

    def meanHum(self):
        plt.figure(figsize=(20,4))
        sns.lineplot(data=self.data, x=self.data.index, y="평균습도(%)")
        plt.xlabel("연도")
        plt.title("2000.01.01~2023.04.06 합천군 평균습도(%)")
        plt.savefig("./graph/2000.01.01~2023.04.06 합천군 평균습도.png")
        plt.close()

    def correlationMap(self):
        heatmap_data = self.data[self.data.columns[2:]]
        colormap = plt.cm.PuBu
        plt.figure(figsize=(5,5))
        plt.title("2000.01.01~2023.04.06 합천군 기상청 데이터 변수 간 상관관계", size=9)
        sns.heatmap(heatmap_data.astype(float).corr(), linewidths=0.1, vmax=1.0, square=True, cmap=colormap, annot=True)
        plt.savefig("./graph/2000.01.01~2023.04.06 합천군 기상청 데이터 변수 간 상관관계.png")
        plt.close()

class sunGraph:
    def __init__(self, dataPath):
        self.data = pd.read_csv(dataPath)
        self.data.index = pd.to_datetime(self.data["날짜"], format="%Y%m%d")
        self.data.drop(["날짜"], axis=1, inplace=True)

        for col in self.data.columns[1:]:
            self.data[col] = self.data[col].apply(lambda x:int(x[:x.index("˚")].replace(" ", "")))

    def TimeGraph(self):
        plt.figure(figsize=(20,5))
        sns.lineplot(data=self.data, x=self.data.index, y="남중고도", label="남중고도")
        sns.lineplot(data=self.data, x=self.data.index, y="9시고도", label="9시고도")
        sns.lineplot(data=self.data, x=self.data.index, y="12시고도", label="12시고도")
        sns.lineplot(data=self.data, x=self.data.index, y="15시고도", label="15시고도")
        sns.lineplot(data=self.data, x=self.data.index, y="18시고도", label="18시고도")
        plt.legend()
        plt.xlabel("연도")
        plt.title("2016년~2022년 시간별 대구 태양 고도")
        plt.savefig("./graph/2016년~2022년 시간별 대구 태양 고도.png")
        plt.close()

        # 특정 날짜에 대한 남중고도 그래프
        plt.figure(figsize=(20,4))
        sns.lineplot(data=self.data[self.data.index.year==2022], x=self.data[self.data.index.year==2022].index, y="남중고도")
        plt.xlabel("날짜")
        plt.title("2022년 대구 태양 남중고도")
        plt.savefig("./graph/2022년 대구 태양 남중고도.png")
        plt.close()


if __name__ == "__main__":
    dam_graph = damGraph("./data/합천다목적댐_수정.csv")
    dam_graph.oneRainGraph("예년누계강우량")
    dam_graph.oneRainGraph("금년누계강우량")
    dam_graph.oneRainGraph("전년누계강우량")
    dam_graph.oneRainGraph("강우량전일")
    dam_graph.oneRainGraph("강우량금일")

    weather_graph = weatherGraph("./data/일별_합천기상데이터.csv")
    weather_graph.meanTemp()
    weather_graph.meanRain()
    weather_graph.meanHum()

    sun_graph = sunGraph("./data/태양고도데이터.csv")
    sun_graph.TimeGraph()