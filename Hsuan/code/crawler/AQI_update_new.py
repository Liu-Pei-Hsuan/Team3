import requests
import csv
import pymysql


userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
headers = {"User-Agent" : userAgent}

# 空氣品質指標 (每小時更新)
update_url = "https://data.epa.gov.tw/api/v1/aqx_p_432?format=json&api_key=84d3f5d7-6629-4967-9218-f0a6dae7be37"

# 檢查網頁是否正常回傳，並取得資料
def get_AQI(url):
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        aqi = response.json()['records']
        print("正常回傳，已取得資料")
        return aqi
    else:
        print("回傳錯誤")

AQI_hour_update = get_AQI(update_url)

def update_hourAQI(AQIData):
    update_hour = []

    for col in AQIData:
        if (col["County"] == "桃園市"):
            data = [col["SiteName"], col["County"], col["AQI"], col["SO2"], col["CO"], col["O3"], col["PM10"], col["PM2.5"], 
                    col["NO2"], col["NOx"], col["NO"], col["WindSpeed"], col["WindDirec"], col["PublishTime"]]
            data = tuple([None if ((i == "-") or (i == " ") or (i == "")) else i for i in data])
            update_hour.append(data)
    

    return update_hour

AQI_update_data = update_hourAQI(AQI_hour_update)




### 匯出 SQL
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
    INSERT INTO AQI_hour (SiteName, County, AQI, SO2, CO, O3, PM10, PM25, NO2,
                          NOx, NO, WindSpeed, WindDirec, DataCreationDate)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""
table = "AQI_hour"

# insert_SQL(sql_insert, table, AQI_hist_data)
insert_SQL(sql_insert, table, AQI_update_data)
