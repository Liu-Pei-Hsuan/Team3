import requests
import pymysql
import pandas as pd
from sqlalchemy import create_engine

def covid19_Taiwan():
    url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=5001&limited=全部縣市'
    res = requests.get(url)
    date = res.json()[0]['a02']
    tw = []
    twCount = 0
    others = 0
    x = 1
    while x == 1:
        for i in range(0, len(res.json())):
            if res.json()[i]['a02'] == date:
                if res.json()[i]['a03'] == '境外移入':
                    others += 1
                else:
                    twCount += 1
                    city = res.json()[i]['a03']
                    tw.append(city)
            else:
                x = 0
                break
    data = (date, twCount, others)
    return data

# =============================================================================
def covid19CountryCity():
    TW = []
    TW.clear()
    url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=5001&limited=全部縣市'
    res = requests.get(url)
    date = res.json()[0]['a02']
    for i in range(0, len(res.json())):
        if res.json()[i]['a02'] == date:
            loc = res.json()[i]['a03']
            TW.append(loc)
        else:
            break

    KEL = TW.count('基隆市') ; NTPC = TW.count('新北市') ; TPE = TW.count('台北市') ; TYN = TW.count('桃園市')
    HSZC = TW.count('新竹市') ; HSZ = TW.count('新竹縣') ; ZMIC = TW.count('苗栗市') ; ZMI = TW.count('苗栗縣')
    TXG = TW.count('台中市') ; CHWC = TW.count('彰化市') ; CHW = TW.count('彰化縣') ; NTCC = TW.count('南投市')
    NTC = TW.count('南投縣') ; YUN = TW.count('雲林縣') ; CYIC = TW.count('嘉義市'); CYI = TW.count('嘉義縣')
    TNN = TW.count('台南市'); KHH = TW.count('高雄市') ; PIF = TW.count('屏東縣') ; PIFC = TW.count('屏東市')
    ILAC = TW.count('宜蘭市') ; ILA = TW.count('宜蘭縣') ; HUNC = TW.count('花蓮市') ; HUN = TW.count('花蓮縣')
    TTTC = TW.count('台東市') ; TTT = TW.count('台東縣') ; PEH = TW.count('澎湖縣')
    
    county = ["基隆市", "新北市", "台北市", "桃園市", "新竹市", "新竹縣", "苗栗市", "苗栗縣", "台中市",
              "彰化市", "彰化縣", "南投市", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "台南市", "高雄市",
              "屏東縣", "屏東市", "宜蘭市", "宜蘭縣", "花蓮市", "花蓮縣", "台東市", "台東縣", "澎湖縣"]
    number = [KEL, NTPC, TPE, TYN, HSZC, HSZ, ZMIC, ZMI, TXG, CHWC, CHW, NTCC, NTC, YUN,
              CYIC, CYI, TNN, KHH, PIF, PIFC, ILAC, ILA, HUNC, HUN, TTTC, TTT, PEH]
    
    return county, number

county_data = covid19CountryCity()

county_covid19 = pd.DataFrame(list(zip(county_data[0], county_data[1])), columns=["county", "number"])

# =============================================================================

### 匯出 SQL
def insert_SQL(sql_insert, table, data):

    config = {
        "host" : "airiot.tibame.cloud", "port" : 3306, "user" : "hsuan",
        "passwd" : "hsuan", "db" : "linebot", "charset" : "utf8mb4"
    }

    conn = pymysql.connect(**config) ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    cursor.execute("select * from {}".format(table))
    
    # 將 SQL 批量執行
    cursor.execute("delete from {}".format(table))
    cursor.execute(sql_insert, data)
    
    # Commit 並檢查資料是否存入資料庫
    conn.commit()
    
    print('資料筆數 :',cursor.execute("select * from {}".format(table)))
    
    # 關閉連線
    cursor.close()
    conn.close()

 
# 先寫好 SQL 語法
# 並將語法中會不斷改變的部分挖空 ( %s )
sql_insert = """
    INSERT INTO taiwan (Date, local, foreigner)
    VALUES (%s, %s, %s);
"""
table = "taiwan"

insert_SQL(sql_insert, table, covid19_Taiwan())

### 匯出資料庫
engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format('hsuan', 'hsuan', 'airiot.tibame.cloud:3306', 'linebot','utf8mb4'))
con = engine.connect()#建立連線
county_covid19.to_sql(name='county', con=con, if_exists='replace', index=False)
con.close()

