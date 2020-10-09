import numpy as np
import requests
import pandas as pd
import datetime
import os
import sys
parent_dir = os.path.dirname(sys.path[0])
sys.path.insert(0, parent_dir)
from lib.logwriter import *
from lib.connDB_base import *
import time
from zipfile import ZipFile
from bs4 import BeautifulSoup
import subprocess


def get_data_weather(timing):
    try:
        url = 'http://opendata.cwb.gov.tw/opendataapi?dataid=F-D0047-093&authorizationkey=CWB-3FB0188A-5506-41BE-B42A-3785B42C3823'
        r = requests.get(url, stream=True)
        with open("weather_data/{}.zip".format(timing), 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        logger.debug("weather data: get day data success !!")
    except:
        logger.error("weather data: get day data failed !!")

def handle_zipfile(timing):
    with ZipFile("weather_data/{}.zip".format(timing), 'r') as zip_ref:
        zip_ref.extractall("weather_data/{}".format(timing))
    
    f = open("weather_data/{}/63_72hr_EN.xml".format(timing),"r", encoding= "utf8")
    data = f.read()
    soup = BeautifulSoup(data,"xml")
    city = soup.locationsName.text
    a = soup.find_all("location")

    DAY = []
    TIME = []
    CITY = []
    DISTRICT = []
    GEOCODE = []
    T = [] #溫度
    TD = [] #露點溫度
    WD = [] #風向(Wind direction)
    Wind = [] #風速
    RH = [] #相對濕度
    PoP12h = [] #降雨機率12hr
    Wx = [] #天氣現象
    try:
        for i in range(0,len(a)):
            location = a[i]
            district = location.find_all("locationName")[0].text
            geocode = location.geocode.text
            weather = location.find_all("weatherElement")
            # time 
            time = weather[1].find_all("dataTime")
            for j in range(0,len(time)):
                x = time[j].text.split("T")
                DAY.append(x[0])
                time_1 = x[1].split("+")
                TIME.append(time_1[0])
                CITY.append(city)
                DISTRICT.append(district)
                GEOCODE.append(geocode)
            for t in weather[0].find_all("value"):
                T.append(t.text)
            for td in weather[1].find_all("value"):
                TD.append(td.text)
            for rh in weather[2].find_all("value"):
                RH.append(rh.text)
            for wd in weather[5].find_all("value"):
                WD.append(wd.text)  
            ws = weather[6].find_all("value")
            for k  in range(0,len(ws),2):
                Wind.append(ws[k].text)
  
            wx = weather[9].find_all("value")
            for w in range(0,len(wx),2):
                Wx.append(wx[w].text)

            for l in weather[4].find_all("value"):
                PoP12h.append(l.text)
                PoP12h.append(l.text)
                PoP12h.append(l.text)
                PoP12h.append(l.text)
        logger.debug("weather data: translate data success !!")        
    except:
        logger.error("weather data: translate data failed !!")        

    f.close()

    data = {"CITY":CITY,"DISTRICT":DISTRICT,"GEOCODE":GEOCODE,"DAY" : DAY,"TIME" : TIME,"T":T,"TD" : TD,"RH":RH,
        "WD" : WD,"Wind":Wind, "Wx":Wx, "PoP12h":PoP12h}
    df = pd.DataFrame(data,columns=["CITY","DISTRICT","GEOCODE","DAY","TIME","T","TD","RH","WD", "Wind","Wx", "PoP12h"])
    print(df)
    try:
        db = ConnDB_base(db_weather)
        db.insertFrame(df, "weather_Table")
        logger.debug("weather data: insert weather data to DB success !!")
    except:
        logger.error("weather data: insert weather data to DB failed !!")

if __name__ == '__main__':
    
    today = datetime.date.today()
    d1 = today.strftime("%Y%m%d")
    d2 = today.strftime("%Y-%m-%d")
    db = ConnDB_base(db_weather)
    
    currhour = datetime.datetime.now().hour
    print(currhour)
    closetTiming = closest(currhour, timeList)
    sql = "SELECT * FROM weather_data.weather_table WHERE DISTRICT = 'Xinyi District' AND DAY = '{}' AND TIME = '{}:00:00'".format(d2, str(closetTiming).zfill(2))
    df  = db.showTable(sql)
    if df.empty:
        print('DataFrame is empty!')
        logger.debug("weather data: DataFrame is empty! Try parse the new data")
        # get_data_weather(d1)
        # handle_zipfile(d1)
        # file_del(d1)
    else:
        logger.debug("weather data: DataFrame founded")
        print(df)
    
    





    

    
