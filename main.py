from parser_tide import *
from parser_weather import *

def file_del(timing):
    try:
        subprocess.call([r'del_redundant.bat', timing])
        logger.debug("weather data: redundant data delete success !!")
    except:
        logger.error("weather data: redundant data delete failed !!")

def closest(num, arr):
    curr = arr[0]
    for val in arr:
        if abs (num - val) < abs (num - curr):
            curr = val
    return curr

def extractNum(str):
    return [int(s) for s in str.split() if s.isdigit()]

if __name__ == '__main__':
    timeList = [0,3,6,9,12,15,18,21]

    today = datetime.date.today()
    d1 = today.strftime("%Y%m%d")
    d2 = today.strftime("%Y-%m-%d")
    db = ConnDB_base(db_weather)

    currhour = datetime.datetime.now().hour
    print(currhour)
    closetTiming = closest(currhour, timeList)
    sql1 = "SELECT * FROM weather_data.weather_table WHERE DISTRICT = 'Xinyi District' AND DAY = '{}' AND TIME = '{}:00:00'".format(d2, str(closetTiming).zfill(2))
    df_weather  = db.showTable(sql1)
    if df_weather.empty:
        print('DataFrame is empty!')
        logger.debug("weather data: DataFrame is empty! Try parse the new data")
        get_data_weather(d1)
        handle_zipfile(d1)
        file_del(d1)
        df_weather  = db.showTable(sql1)
        print(df_weather)
    else:
        logger.debug("weather data: DataFrame founded")
        print(df_weather)

    sql2 = "SELECT * FROM weather_data.tide_table WHERE DISTRICT = 'PENGJIAYU-KEELUNG INSHORE' AND DAY = '{}' AND TIME = '{}:00:00'".format(d2, str(closetTiming).zfill(2))
    df_tide = db.showTable(sql2)
    if df_tide.empty:
        print('DataFrame is empty!')
        logger.debug("weather data: DataFrame is empty! Try parse the new data")
        get_data_tide(d1)
        handle_xmlfile(d1)
        df_tide = db.showTable(sql2)
        print(df_tide)
    else:
        logger.debug("weather data: DataFrame founded")
        print(df_tide)

    if extractNum(df_tide["WaveHeight"][0])[-1]>=4:
        logger.debug("Result: Not suitable for fishing(large wave)")
    elif extractNum(df_tide["WindSpeed"][0])[-1]>=40:
        logger.debug("Result: Not suitable for fishing(large wind)")
    else:
        logger.debug("Result: Suitable for fishing!!!!")


    
