import requests
import pandas as pd
import pymysql

response = requests.get("https://od.cdc.gov.tw/eic/NHI_EnteroviralInfection.json")
data_json = response.json()


enterovirus = []
for i in data_json:
    if i["縣市"] == "桃園市":
        if (i["年"] <= "2021") & (i["年"] > "2018"):
            data = (i["就診類別"], int(i["年"]), i["年齡別"], i["縣市"], int(i["週"]), int(i["腸病毒健保就診人次"]))
            enterovirus.append(data)
            

### 匯出 SQL
def insert_SQL(sql_insert, table, data):

    config = {"host" : "mqtt2.tibame.cloud", "port" : 3306, "user" : "hsuan",
              "passwd" : "hsuan", "db" : "Disease", "charset" : "utf8mb4"
          }

    conn = pymysql.connect(**config) ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    cursor.execute("select * from {}".format(table))
    
    # 將 SQL 批量執行
    cursor.execute("TRUNCATE TABLE {}".format(table))
    cursor.executemany(sql_insert, data)
    
    # Commit 並檢查資料是否存入資料庫
    conn.commit()
    
    print('資料筆數 :',cursor.execute("select * from {}".format(table)))
    
    # 關閉連線
    cursor.close()
    conn.close()
    
    
# 先寫好 SQL 語法
# 並將語法中會不斷改變的部分挖空 ( %s )
sql_insert = """
    INSERT INTO enterovirus (type, year, age, county, week, cases)
    VALUES (%s, %s, %s, %s, %s, %s);
"""
table = "enterovirus"

insert_SQL(sql_insert, table, enterovirus)
