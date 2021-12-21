import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import pymysql

'''
loc1 = 大園區
loc2 = 桃園區
loc3 = 觀音區
loc4 = 平鎮區
loc5 = 龍潭區
loc6 = 中壢區
'''
# 各站點資訊
loc_dict = {'loc1': 'e8fcf1233159a2bf6d5628d7242379b2d102ae9f7ab86c5af10e9754d2043955',
            'loc2': '2063dc93d721d794396441c2473f2d3e6e5b335903034198829e1e86eb9e83e0',
            'loc3': '31db554b69ded55ded416d34f7f8e9845f60a4a7c139f73b2e65b1592a13988b',
            'loc4': '3c45ef1549c42db5a6908f760ceab0619d21487c88a133ffe6e4332bff1588a1',
            'loc5': 'adff3d6961c3ca9833a8b72fdf2587b20a0efa40b22b5ce1134f98982cf13dcc',
            'loc6': '0005d4c25ae305606e1095778b12d1224780ea0bed47dd95e90983daf35cac1e'}

###############################每小時資料################################
weatherDataHours = []
weatherAQIHours = []
for locs in loc_dict.values():
    url = f'https://weather.com/zh-TW/weather/hourbyhour/l/{locs}'
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')

    locAQI = soup.select_one('.LocationPageTitle--PresentationName--1QYny').text.split(', ')[0]
    # dateTime = soup.select_one('.DetailsSummary--daypartName--2FBp2').text
    # times = time.strftime("%Y/%m/%d %H:00", time.localtime())
    pTime = soup.select('h2[data-testid="daypartName"]')[0].text
    timesAQI = time.strftime(f"%Y-%m-%d {pTime}:00", time.localtime())
    tempAQI = soup.select('span[data-testid="TemperatureValue"]')[0].text.split('°')[0]
    humAQI = soup.select('li[data-testid="HumiditySection"] span[data-testid="PercentageValue"]')[0].text.split('%')[0]
    rainAQI = soup.select('span[data-testid="PercentageValue"]')[0].text.split('Rain')[0].split('%')[0]
    weatherAQI2tuple = tuple([locAQI.split('區')[0], timesAQI, tempAQI, humAQI, rainAQI])
    weatherAQIHours.append(weatherAQI2tuple)

    for i in range(0, 8):
        loc = soup.select_one('.LocationPageTitle--PresentationName--1QYny').text.split(', ')[0]
        # dateTime = soup.select_one('.DetailsSummary--daypartName--2FBp2').text
        # times = time.strftime("%Y/%m/%d %H:00", time.localtime())
        pTime = soup.select('h2[data-testid="daypartName"]')[i].text
        times = time.strftime(f"%Y-%m-%d {pTime}:00", time.localtime())
        temp = soup.select('span[data-testid="TemperatureValue"]')[i].text.split('°')[0]
        hum = soup.select('li[data-testid="HumiditySection"] span[data-testid="PercentageValue"]')[i].text.split('%')[0]
        rain = soup.select('span[data-testid="PercentageValue"]')[i].text.split('Rain')[0].split('%')[0]
        wType = soup.select('p[data-testid="hourlyWxPhrase"]')[i].text  # 資料型態（大小雨或陣雨）
        print(f'地區：{loc} , 時間：{times} , 溫度：{temp} , 濕度：{hum} , 降雨機率：{rain} , 氣候型態：{wType}')
        weather2tuple = tuple([loc, times, temp, hum, rain, wType])
        weatherDataHours.append(weather2tuple)
    print(f'{loc}資料更新成功' + '=' * 40)
    time.sleep(1)

    ###############################資料庫存取flask################################

    insert = 'insert into weatherHour_flask (loc,date,temp,hum,rain,wType) values (%s,%s,%s,%s,%s,%s)'
    table = 'weatherHour_flask'


    def Mysql_insert(sql_insert, table, data):
        import pymysql
        config = {
            "host": "mqtt2.tibame.cloud",
            "port": 3306,
            "user": "yi",
            "passwd": "yi",
            "db": "weather",
            "charset": "utf8mb4"
        }

        conn = pymysql.connect(**config)  ## **會將字典型態轉變(kwargs)
        cursor = conn.cursor()
        cursor.execute("delete from {}".format(table))
        cursor.execute("select * from {}".format(table))
        cursor.executemany(sql_insert, data)
        conn.commit()
        print('資料筆數 :', cursor.execute("select * from {}".format(table)))
        print('每小時flask資料庫推送完畢')

        # 關閉連線
        cursor.close()
        conn.close()


    Mysql_insert(insert, table, weatherDataHours)
    ###############################資料庫存取AQISQL###########################

    insert = 'insert into weather_hours (loc,date,temp,hum,rain) values (%s,%s,%s,%s,%s)'
    table = 'weather_hours'


    def Mysql_insert(sql_insert, table, data):
        import pymysql
        config = {
            "host": "mqtt2.tibame.cloud",
            "port": 3306,
            "user": "yi",
            "passwd": "yi",
            "db": "weather",
            "charset": "utf8mb4"
        }

        conn = pymysql.connect(**config)  ## **會將字典型態轉變(kwargs)
        cursor = conn.cursor()
        # cursor.execute("delete from {}".format(table)) # 刪除數據
        cursor.execute("select * from {}".format(table))
        cursor.executemany(sql_insert, data)
        conn.commit()
        print('資料筆數 :', cursor.execute("select * from {}".format(table)))
        print('每小時AQI資料庫推送完畢')

        # 關閉連線
        cursor.close()
        conn.close()


    Mysql_insert(insert, table, weatherAQIHours)

    ###############################每三日資料################################

weatherData3D = []
for locs in loc_dict.values():
    url = f'https://weather.com/zh-TW/weather/tenday/l/{locs}'
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    for i in range(0, 4):
        loc = soup.select_one('span[class="LocationPageTitle--PresentationName--1QYny"]').text.split(',')[0]
        try:
            date = soup.select('h2[class="DetailsSummary--daypartName--2FBp2"]')[i].text.split(' ')[1]  # 獲取當日日期
            times = time.strftime(f"%Y-%m-{date}", time.localtime())  # 結合日期
        except:
            times = '今日'
        tempH = soup.select('span[class="DetailsSummary--highTempValue--3Oteu"]')[i].text.split('°')[0]
        tempL = soup.select('span[class="DetailsSummary--lowTempValue--3H-7I"]')[i].text.split('°')[0]
        hum = soup.select('span[data-testid="PercentageValue"][class="DetailsTable--value--1q_qD"]')[i].text.split('%')[
            0]
        rain = soup.select('span[data-testid="PercentageValue"]')[i].text.split('%')[0]
        wType = \
        soup.select('p[data-testid="wxPhrase"][class="DailyContent--narrative--hplRl"]')[i + 2].text.split('。 ')[0]
        print(f'地區：{loc} , 時間：{times} , 最高溫：{tempH} , 最低溫：{tempL} , 濕度：{hum} , 降雨機率：{rain} , 氣候型態：{wType}')
        weather2tuple = tuple([loc, times, tempH, tempL, hum, rain, wType])
        weatherData3D.append(weather2tuple)
    print(f'{loc}資料更新成功' + '=' * 40)
    time.sleep(1)
    ###############################資料庫存取################################

    insert = 'insert into weather3Dflask (loc,date,tempH,tempL,hum,rain,wType) values (%s,%s,%s,%s,%s,%s,%s)'
    table = 'weather3Dflask'


    def Mysql_insert(sql_insert, table, data):
        import pymysql
        config = {
            "host": "mqtt2.tibame.cloud",
            "port": 3306,
            "user": "yi",
            "passwd": "yi",
            "db": "weather",
            "charset": "utf8mb4"
        }

        conn = pymysql.connect(**config)  ## **會將字典型態轉變(kwargs)
        cursor = conn.cursor()
        cursor.execute("delete from {}".format(table))
        cursor.execute("select * from {}".format(table))
        cursor.executemany(sql_insert, data)
        conn.commit()
        print('資料筆數 :', cursor.execute("select * from {}".format(table)))
        print('三日氣象資料推送完畢')

        # 關閉連線
        cursor.close()
        conn.close()


    Mysql_insert(insert, table, weatherData3D)