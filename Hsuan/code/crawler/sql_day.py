import requests
import csv
from datetime import datetime, timedelta
import pymysql


userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
headers = {"User-Agent" : userAgent}
url='https://data.epa.gov.tw/api/v1/aqx_p_434?offset=0&limit=1000&api_key=84d3f5d7-6629-4967-9218-f0a6dae7be37'

# 檢查網頁是否正常回傳，並取得資料
def get_AQI(url):
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        aqi = response.json()['records']
        print("正常回傳，已取得資料")
        return aqi
    else:
        print("回傳錯誤")

AQI = get_AQI(url)

### 桃園所有測站
sitenum = ['17', '18', '19', '20', '21', '68']

### 當月所有資料
# def MonthAQI_CSV(AQIData):
#     SQL_month = []
#     filename = '日空氣品質指標.csv'
#     columns_name=['測站名稱','監測日期','空氣品質指標']   # 變數名稱
#     with open(filename,'w',newline='',encoding="utf-8-sig") as csvFile:     # 建立一個 CSV
#         csv_writer = csv.writer(csvFile)
#         csv_writer.writerow(columns_name)

#     with open(filename,'a',newline='',encoding="utf-8-sig") as csvFile:     # append csv
#         csv_writer = csv.writer(csvFile)

#         for col in AQIData:
#             if (col["SiteId"] in sitenum):
#                 #print(col)
#                 data = [col["SiteName"], col["MonitorDate"], col["AQI"]]
#                 data = tuple([None if i == "-" else i for i in data])
#                 SQL_month.append(data)

#                 csv_writer.writerow(data)
#     return SQL_month

### 每天更新資料
# def DailyAQI_CSV(AQIData):
#     SQL_daily = []
#     filename = '日空氣品質指標.csv'
#     yesterday = str(datetime.today().date() - timedelta(days=1)) 
#     with open(filename,'a',newline='',encoding="utf-8-sig") as csvFile:     # append csv
#         csv_writer = csv.writer(csvFile)

#         for col in AQIData:
#             if (col["MonitorDate"] == yesterday) & (col["SiteId"] in sitenum):
#                 data = [col["SiteName"], col["MonitorDate"], col["AQI"]]
#                 data = tuple([None if i == "-" else i for i in data])
#                 SQL_daily.append(data)

#                 csv_writer.writerow(data)
#     return SQL_daily


def DailyAQI_CSV(AQIData):
    SQL_daily = []
    
    yesterday = str(datetime.today().date() - timedelta(days=1)) 
    
    for col in AQIData:
        if (col["MonitorDate"] == yesterday) & (col["SiteId"] in sitenum):
            data = [col["SiteName"], col["MonitorDate"], col["AQI"]]
            data = tuple([None if i == "-" else i for i in data])
            SQL_daily.append(data)

    return SQL_daily

# AQI_month = MonthAQI_CSV(AQI)
AQI_day = DailyAQI_CSV(AQI)
AQI_day


def insert_SQL(sql_insert, table, data):

    config = {
        "host" : "104.155.221.250", "port" : 3306, "user" : "sikei",
        "passwd" : "zxcv1234", "db" : "AQI", "charset" : "utf8mb4"
    }

    conn = pymysql.connect(**config) ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    cursor.execute("select * from {}".format(table))
    
    # 將 SQL 批量執行
    cursor.executemany(sql_insert, data)
    # cursor.execute("delete from aqi_day")
    
    # Commit 並檢查資料是否存入資料庫
    conn.commit()
    
    print('資料筆數 :',cursor.execute("select * from {}".format(table)))
    
    # 關閉連線
    cursor.close()
    conn.close()
    
    
# 先寫好 SQL 語法
# 並將語法中會不斷改變的部分挖空 ( %s )
sql_insert = """
    INSERT INTO AQI_day (SiteName, MonitorDate, AQI)
    VALUES (%s, %s, %s);
"""
table = "AQI_day"
# insert_SQL(sql_insert, table, AQI_month)
insert_SQL(sql_insert, table, AQI_day)
