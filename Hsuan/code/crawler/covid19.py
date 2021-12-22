import requests
from datetime import datetime
import pymysql
import pandas as pd

url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=5002&limited=全部縣市'
res = requests.get(url)
# =============================================================================
### 變數介紹
# "id":"ID", "a01":"個案研判日", "a02":"個案公佈日", "a03":"縣市別"
#            "a04":"區域", "a05":"新增確診人數","a06":"累計確診人數"}
# =============================================================================
### 境外移入
covid19_Foreign = []
for i in res.json():
    if (i["a03"] == "境外移入") & (i["a04"] == "全區") & (i["a01"] >= "2021-01-01"):
        data = (i["a01"], int(i["a05"]))
        covid19_Foreign.append(data)
        
### 國內
covid19_Taiwan = []
for i in res.json():
    if (i["a03"] != "境外移入") & (i["a01"] >= "2021-01-01"):
        data = [i["a01"], i["a03"], int(i["a05"])]
        covid19_Taiwan.append(data)

# =============================================================================
# 將同天同縣市資料整合
# =============================================================================
Taiwan = pd.DataFrame(covid19_Taiwan, columns = ["date", "city", "number"])
# Taiwan.city.unique()

df = Taiwan.groupby(["date", "city"], as_index=False).sum()
df = df.sort_values(by = "date")

covid19_data = []
for i in range(len(df)):
    lst = tuple(df.iloc[i,:])
    covid19_data.append(lst)
    
    
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
    
    
# =============================================================================
# 國內 COVID-19 資料
# =============================================================================
sql_insert = """
    INSERT INTO COVID19 (date, city, number)
    VALUES (%s, %s, %s);
"""
table = "COVID19"

insert_SQL(sql_insert, table, covid19_data)

# =============================================================================
# 境外 COVID-19 資料
# =============================================================================
sql_insert_foreign = """
    INSERT INTO COVID19_foreign (date, number)
    VALUES (%s, %s);
"""
table_foreign = "COVID19_foreign"

insert_SQL(sql_insert_foreign, table_foreign, covid19_Foreign)
