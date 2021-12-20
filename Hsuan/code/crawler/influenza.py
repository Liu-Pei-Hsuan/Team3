import requests
import pandas as pd
import pymysql


response = requests.get("https://od.cdc.gov.tw/eic/NHI_Influenza_like_illness.json")
data_json = response.json()

influenza = []
for i in data_json:
    if i["縣市"] == "桃園市":
        if (i["年"] <= "2021") & (i["年"] > "2018"):
            data = (i["就診類別"], int(i["年"]), i["年齡別"], i["縣市"], int(i["週"]), int(i["類流感健保就診人次"]))
            influenza.append(data)
        
# df = pd.DataFrame(influenza, columns = ["就診類別", "年", "年齡", "縣市", "週", "類流感健保就診人次"])
# df["健保就診總人次"] = df["健保就診總人次"].astype(int)
# df["類流感健保就診人次"] = df["類流感健保就診人次"].astype(int)

# df["類流感健保就診人次比"] = round(df.iloc[:,6] / df.iloc[:,0], 4)
# df

# df.to_csv("歷年健保門診類流感就診人次.csv", encoding = 'utf_8_sig',index = False)


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
    INSERT INTO influenza (type, year, age, county, week, cases)
    VALUES (%s, %s, %s, %s, %s, %s);
"""
table = "influenza"

insert_SQL(sql_insert, table, influenza)
