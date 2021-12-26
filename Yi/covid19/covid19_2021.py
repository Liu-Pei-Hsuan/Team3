import requests
from datetime import datetime
import pymysql

url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=5002&limited=全部縣市'
res = requests.get(url)
first_date = "2021-01-01"
covid19data = []
for i in range(0, len(res.json())):
    if datetime.strptime(res.json()[i]['a02'], "%Y-%m-%d") > first_date:
        date = res.json()[i]['a02']
        cType = res.json()[i]['a03']
        covid2tuple = tuple([date, cType])
        covid19data.append(covid2tuple)


def insert_SQL(sql_insert, table, data):
    config = {
        "host": "mqtt2.tibame.cloud", "port": 3306, "user": "yi",
        "passwd": "yi", "db": "Disease", "charset": "utf8mb4"
    }

    conn = pymysql.connect(**config)  ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    cursor.execute("select * from {}".format(table))
    cursor.execute('delete from {}'.format(table))
    cursor.executemany(sql_insert, data)
    conn.commit()
    print('資料筆數 :', cursor.execute("select * from {}".format(table)))

    # 關閉連線
    cursor.close()
    conn.close()


table = "coviddata"
sql_insert = f'insert into {table} (date, cType) values (%s,%s)'
insert_SQL(sql_insert, table, covid19data)