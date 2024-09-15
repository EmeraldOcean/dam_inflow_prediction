"""
Reference : https://github.com/tommyjr1/2023-DSC3028-InflowPrediction
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime as dt
import json
from glob import glob
import urllib.request
from tqdm import tqdm

with open("config.json", "r") as f:
    CONFIG = json.load(f)

class damDataExtract:
    """
    Data extractor for dam data
    """
    def __init__(self):
       """
       :param  
       """
       self.key = CONFIG["dam"]["serviceKey"]  # serviceKey needed to get data from API
       self.start = CONFIG["dam"]["startDate"]
       self.end = CONFIG["dam"]["endDate"]
       self.name = CONFIG["dam"]["damName"]
       self.url = CONFIG["dam"]["url"]
       self.dataPath = CONFIG["dam"]["dataPath"]
    
    def parse(self, item, date, time):
        """
        Data Parsing
        :input item: elements extracted from OpenAI Data
        :output Dictionary for dam data
        """
        datetime = dt.datetime(date.year, date.month, date.day, time, 0,0)
        try:
            damnm = item.find("damnm").get_text()
            dvlpqyacmtlacmslt = item.find("dvlpqyacmtlacmslt").get_text()
            dvlpqyacmtlplan = item.find("dvlpqyacmtlplan").get_text()
            dvlpqyacmtlversus = item.find("dvlpqyacmtlversus").get_text()
            dvlpqyfyerplan = item.find("dvlpqyfyerplan").get_text()
            dvlpqyfyerversus = item.find("dvlpqyfyerversus").get_text()
            inflowqy = item.find("inflowqy").get_text()
            lastlowlevel = item.find("lastlowlevel").get_text()
            lastrsvwtqy = item.find("lastrsvwtqy").get_text()
            nowlowlevel = item.find("nowlowlevel").get_text()
            nowrsvwtqy = item.find("nowrsvwtqy").get_text()
            nyearlowlevel = item.find("nyearlowlevel").get_text()
            nyearrsvwtqy = item.find("nyearrsvwtqy").get_text()
            oyaacurf = item.find("oyaacurf").get_text()
            prcptqy = item.find("prcptqy").get_text()
            pyacurf = item.find("pyacurf").get_text()
            rsvwtrt = item.find("rsvwtrt").get_text()
            suge = item.find("suge").get_text()
            totdcwtrqy = item.find("totdcwtrqy").get_text()
            totdcwtrqyjo = item.find("totdcwtrqyjo").get_text()
            vyacurf = item.find("vyacurf").get_text()
            zerosevenhourprcptqy = item.find("zerosevenhourprcptqy").get_text()

            return {
                "댐이름": damnm,
                "시간": datetime,
                "발전량(실적)": dvlpqyacmtlacmslt,
                "발전량(계획)": dvlpqyacmtlplan,
                "발전량(계획대비)": dvlpqyacmtlversus,
                "연간발전계획": dvlpqyfyerplan,
                "연간계획대비": dvlpqyfyerversus,
                "전일유입량": inflowqy,
                "저수위(전년)": lastlowlevel,
                "저수량(전년)": lastrsvwtqy,
                "저수위(현재)": nowlowlevel,
                "저수량(현재)": nowrsvwtqy,
                "저수위(예년)": nyearlowlevel,
                "저수량(예년)": nyearrsvwtqy,
                "예년누계강우량": oyaacurf,
                "강우량전일": prcptqy,
                "금년누계강우량": pyacurf,
                "현재저수율": rsvwtrt,
                "수계": suge,
                "전일방류량(본댐)": totdcwtrqy,
                "전일방류량(조정지)": totdcwtrqyjo,
                "전년누계강우량": vyacurf,
                "강우량금일": zerosevenhourprcptqy
            }
        except AttributeError as e:
            return {
                "댐이름": None,
                "시간": None,
                "발전량(실적)": None,
                "발전량(계획)": None,
                "발전량(계획대비)": None,
                "연간발전계획": None,
                "연간계획대비": None,
                "전일유입량": None,
                "저수위(전년)": None,
                "저수량(전년)": None,
                "저수위(현재)": None,
                "저수량(현재)": None,
                "저수위(예년)": None,
                "저수량(예년)": None,
                "예년누계강우량": None,
                "강우량전일": None,
                "금년누계강우량": None,
                "현재저수율": None,
                "수계": None,
                "전일방류량(본댐)": None,
                "전일방류량(조정지)": None,
                "전년누계강우량": None,
                "강우량금일": None
            }  

    def extract(self):
        """
        Extract data
        :output csv data
        """
        # Day to start
        date = dt.datetime(self.start["year"], self.start["month"], self.start["day"])
        #Day to end
        while (date < dt.datetime(self.end["year"], self.end["month"], self.end["day"])):
            row = []
            vdate = date
            tdate = date - dt.timedelta(days=1)
            ldate = date - dt.timedelta(days=365)

            for i in range(1, 25):
                str_i = str(i).zfill(2)
                params ={'serviceKey' : self.key, 'tdate' : tdate.strftime("%Y-%m-%d"),
                         'ldate' : ldate.strftime("%Y-%m-%d"), 'vdate' : vdate.strftime("%Y-%m-%d"), 
                         'vtime' : str_i, 'numOfRows':'21'}

                response = requests.get(self.url, params=params)
                soup = bs(response.text, 'lxml-xml')

                items= soup.find_all('item')
                for item in items:
                    row.append(self.parse(item,vdate,i-1))

            df2 = pd.DataFrame(row)
            df2 = df2[df2["댐이름"]==self.name]
            # if(vdate.month!=(vdate+dt.timedelta(days=1)).month):
            df2.to_csv(f"{self.dataPath}/합천다목적댐_"+vdate.strftime("%Y-%m-%d")+".csv", index=False)
            date = date+dt.timedelta(days=1)
    
    def concat(self):
        total = pd.DataFrame()
        file_name = glob(f"{self.dataPath}/*.csv")
        for file in file_name:
            # print(file_name)
            tmp = pd.read_csv(file, encoding="utf-8")
            total = pd.concat([total, tmp], ignore_index=True)
        total.to_csv("합천다목적댐_원본.csv", index=False, encoding="utf-8-sig")


class weatherExtract:
    """
    Data extractor for weather data
    """
    def __init__(self):
       self.key = CONFIG["weather"]["serviceKey"]  # serviceKey needed to get data from API
       self.start = CONFIG["weather"]["startDate"]
       self.end = CONFIG["weather"]["endDate"]
       self.url = CONFIG["weather"]["url"]
       self.lat = CONFIG["weather"]["latitude"]
       self.long = CONFIG["weather"]["longitude"]

    def date_range(self, start, end):
        dates = [date.strftime("%Y%m%d") for date in pd.date_range(start, periods=(end-start).days+1)]
        return dates
    
    def extract(self):
        startDate = dt.datetime(self.start["year"], self.start["month"], self.start["day"])
        endDate = dt.datetime(self.start["year"], self.start["month"], self.start["day"])
        date_list = self.date_range(startDate, endDate)

        df = pd.DataFrame()
        for date in tqdm(date_list):
            try:
                url = self.url.format(date, self.key)
                response = requests.get(url)
                soup = bs(response.text, "lxml-xml")
                tmp = pd.DataFrame({"날짜":[soup.find("locdate").get_text()],
                                    "위치":[soup.find("location").get_text()],
                                    "남중고도":[soup.find("altitudeMeridian").get_text()],
                                    "9시고도":[soup.find("altitude_09").get_text()],
                                    "12시고도":[soup.find("altitude_12").get_text()],
                                    "15시고도":[soup.find("altitude_15").get_text()],
                                    "18시고도":[soup.find("altitude_18").get_text()],
                                    "9시방위각":[soup.find("azimuth_09").get_text()],
                                    "12시방위각":[soup.find("azimuth_12").get_text()],
                                    "15시방위각":[soup.find("azimuth_15").get_text()],
                                    "18시방위각":[soup.find("azimuth_18").get_text()]})
                df = pd.concat([df, tmp])
            except:
                pass
            df.to_csv("태양고도데이터.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    damExtractor = damDataExtract()
    damExtractor.extract()
    damExtractor.concat()

    weatherExtractor = weatherExtract()
    weatherExtractor.extract()