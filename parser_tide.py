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

# 

def get_data_tide(timing):
    try:
        url = 'http://opendata.cwb.gov.tw/opendataapi?dataid=F-A0012-002&authorizationkey=CWB-3FB0188A-5506-41BE-B42A-3785B42C3823'
        r = requests.get(url, stream=True)
        with open("tide_data/{}.xml".format(timing), 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        logger.debug("weather data: get day data success !!")
    except:
        logger.error("weather data: get day data failed !!")

def handle_xmlfile(timing):
    f = open("tide_data/{}.xml".format(timing),"r", encoding= "utf8")
    data = f.read()
    soup = BeautifulSoup(data,"xml")
    a = soup.find_all("location")

    DAY = []
    TIME = []
    DISTRICT = []

    Wx = [] #天氣現象
    WinDir = [] #風向
    WindSpeed = [] #風速
    WaveHeight = [] #浪高
    WaveType = [] #浪況
    
    try:
        for i in range(0,len(a)):
            location = a[i]
            district = location.find_all("locationName")[0].text
            weather = location.find_all("weatherElement")
            # time 
            time = weather[1].find_all("startTime")
            time2 = weather[1].find_all("time")
            for j in range(0,len(time2)):
                x = time[j].text.split("T")
                DAY.append(x[0])
                time_1 = x[1].split("+")
                TIME.append(time_1[0])
                DISTRICT.append(district)
            for wx in weather[0].find_all("parameterValue"):
                Wx.append(wx.text)
            for windir in weather[1].find_all("parameterName"):
                WinDir.append(windir.text)
            for windspeed in weather[2].find_all("parameterName"):
                WindSpeed.append(windspeed.text)
            for waveheight in weather[3].find_all("parameterName"):
                WaveHeight.append(waveheight.text)  
            for wavetype in weather[4].find_all("parameterName"):
                WaveType.append(wavetype.text)
            
        logger.debug("weather data: translate data success !!")        
    except:
        logger.error("weather data: translate data failed !!")        

    f.close()

    data = {"DISTRICT":DISTRICT,"DAY" : DAY,"TIME" : TIME,"Wx":Wx, "WinDir" : WinDir,"WindSpeed":WindSpeed, "WaveHeight":WaveHeight, "WaveType":WaveType}
    df = pd.DataFrame(data,columns=["DISTRICT","DAY","TIME","Wx","WinDir", "WindSpeed","WaveHeight", "WaveType"])
    print(df)
    try:
        db = ConnDB_base(db_weather)
        db.insertFrame(df, "tide_Table")
        logger.debug("weather data: insert weather data to DB success !!")
    except:
        logger.error("weather data: insert weather data to DB failed !!")

if __name__ == '__main__':
    today = datetime.date.today()
    d1 = today.strftime("%Y%m%d")

    get_data(d1)
    handle_xmlfile(d1)