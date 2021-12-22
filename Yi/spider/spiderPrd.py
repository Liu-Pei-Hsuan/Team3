import requests
import time
from bs4 import BeautifulSoup
import pymysql

searchPrd_list = ['漂白水', '瓦斯警報器', '一氧化碳偵測儀', '3M 6200防毒面具', '酒精濕紙巾', '乾洗手', '活性碳口罩', '不織布口罩', '活性碳空氣清淨機', 'PM2.5 空氣清淨機',
                  '酒精', '肥皂', '安全護目鏡']
prdData = []
for searchPrd in searchPrd_list:
    url = f" https://m.momoshop.com.tw/search.momo?searchKeyword={searchPrd}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    print(f'=====  Search satr {searchPrd}  =====')
    for prd in soup.select('.goodsItemLi'):
        prdClass = str(searchPrd)
        prdName = prd.select_one('.prdName').text.strip()
        prdPrice = prd.select_one('.price').text
        prdImg = prd.select_one('.goodsImg')['src']
        prdUrl = 'https://m.momoshop.com.tw/' + prd.select_one('a')['href']
        prd2tuple = tuple([prdClass, prdName, prdPrice, prdImg, prdUrl])
        prdData.append(prd2tuple)
        print(f'類別:{searchPrd}')
        print(prdName)
        print(prdPrice)
        print(prdImg)
        print(prdUrl)
        print('-' * 100)
    time.sleep(2)
prdData.pop(0)


def insert_SQL(sql_insert, table, data):
    config = {
        "host": "mqtt2.tibame.cloud", "port": 3306, "user": "yi",
        "passwd": "yi", "db": "prd", "charset": "utf8mb4"
    }

    conn = pymysql.connect(**config)  ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    cursor.execute("select * from {}".format(table))

    # 先將舊的table刪除，在批量執行新增
    cursor.execute('delete from {}'.format(table))
    cursor.executemany(sql_insert, data)
    # cursor.execute("delete from aqi_day")
    # Commit 並檢查資料是否存入資料庫
    conn.commit()
    print('資料筆數 :', cursor.execute("select * from {}".format(table)))

    # 關閉連線
    cursor.close()
    conn.close()


table = "prdinfo"
sql_insert = f'insert into {table} (prdClass,prdName,prdPrice,prdImg,prdUrl) values (%s,%s,%s,%s,%s)'
insert_SQL(sql_insert, table, prdData)