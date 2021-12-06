import requests
import pandas as pd
import pymysql
# from datetime import datetime, timedelta, timezone


response = requests.get("https://od.cdc.gov.tw/eic/NHI_Influenza_like_illness.json")
data_json = response.json()

influenza = []
influenza_sql = []
for i in data_json:
    if (i["年"] == "2021") & (i["縣市"] == "桃園市"):
        data = (i["健保就診總人次"], i["就診類別"], i["年"], i["年齡別"], i["縣市"], i["週"], i["類流感健保就診人次"])
        sqldata = (i["年"], i["年齡別"], i["週"], i["類流感健保就診人次"])
        influenza.append(data)
        influenza_sql.append(sqldata)
        
df = pd.DataFrame(influenza, columns = ["健保就診總人次", "就診類別", "年", "年齡", "縣市", "週", "類流感健保就診人次"])
df["健保就診總人次"] = df["健保就診總人次"].astype(int)
df["類流感健保就診人次"] = df["類流感健保就診人次"].astype(int)

df["類流感健保就診人次比"] = round(df.iloc[:,6] / df.iloc[:,0], 4)
df

df.to_csv("歷年健保門診類流感就診人次.csv", encoding = 'utf_8_sig',index = False)


### 匯出 SQL
def insert_SQL(sql_insert, table, data):

    config = {
        "host" : "127.0.0.1", "port" : 3306, "user" : "root",
        "passwd" : "012276", "db" : "project", "charset" : "utf8mb4"
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
    INSERT INTO influenza (year, age, week, influenza)
    VALUES (%s, %s, %s, %s);
"""
table = "influenza"

insert_SQL(sql_insert, table, influenza_sql)