import matplotlib.pyplot as plt
import pandas as pd
import pymysql
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
from datetime import timedelta
import numpy as np
from sklearn.impute import KNNImputer
import matplotlib.pyplot as plt

# =============================================================================
# 取得資料
# =============================================================================
def get_data(table):
    config = {"host" : "mqtt2.tibame.cloud", "port" : 3306, "user" : "hsuan",
          "passwd" : "hsuan", "db" : "AQI_History", "charset" : "utf8mb4"}

    conn = pymysql.connect(**config) ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    
    SQL = "select * from {}".format(table)
    print('資料筆數 :',cursor.execute(SQL))
    
    results = cursor.fetchall()
    
    if table == "weather_hours_H":
        data = pd.DataFrame(results, columns = ["ID", "Date", "Station", "Humidity", "Temp"])
        data = data.drop("ID", axis=1)
    elif table == "AQI_hour_H":
        data = pd.DataFrame(results).iloc[:, [1,2,9,5,6,7,10,11,12, 13, 14]]
        data.columns = ["Date", "Station", "PM2.5", "SO2", "CO", "O3", "NO2", "NOx", "NO", "windSpeed", "windDirec"]
    # 關閉連線
    cursor.close()
    conn.close()
    
    return data

pm25 = get_data("AQI_hour_H")
weather = get_data("weather_hours_H")

merge_df = pd.merge(pm25, weather, how = "outer")


data = merge_df[merge_df.Date >= datetime.strptime("2019-01-01", "%Y-%m-%d")].sort_values(by = "Date")

data = data[(data["Station"] == "大園") | (data["Station"] == "桃園") | (data["Station"] == "龍潭") |
            (data["Station"] == "觀音") | (data["Station"] == "平鎮") | (data["Station"] == "中壢")]

# =============================================================================
# 將怪異的值全部改成 None
# =============================================================================
Hum = []
count = 0
for i in data["Humidity"]:
    try:
        if len(i) == 2:
            Hum.append(int(i))
        else:
            Hum.append(None)
    except TypeError:
        Hum.append(None)
        
data["Humidity"] = Hum
        
temp = []
for i in data["Temp"]:
    if (i == "...") or (i == "X") or (i == None):
        temp.append(None)
    else:
        temp.append(float(i))
        
data["Temp"] = temp
# data = data.set_index("Date")

### 遺失值比例
na_precrent = data.isnull().sum()/169295 * 100

### 轉變資料型態
for i in data.columns[2:10]:
    data[i] = data[i].astype("float")
            

# =============================================================================
# 將六個測站分開
# =============================================================================
Taoyuan = data[data["Station"] == "桃園"] ; Taoyuan = Taoyuan[Taoyuan.duplicated("Date") == False]
Dayuan = data[data["Station"] == "大園"] ; Dayuan = Dayuan[Dayuan.duplicated("Date") == False]
Guanyin = data[data["Station"] == "觀音"] ; Guanyin = Guanyin[Guanyin.duplicated("Date") == False]
Longtan = data[data["Station"] == "龍潭"] ; Longtan = Longtan[Longtan.duplicated("Date") == False]
Pingzhen = data[data["Station"] == "平鎮"] ; Pingzhen = Pingzhen[Pingzhen.duplicated("Date") == False]
Zhongli = data[data["Station"] == "中壢"]; Zhongli = Zhongli[Zhongli.duplicated("Date") == False]

# =============================================================================
# 複製測站資料 (以便做比較)
# =============================================================================
### LOCF
Tao_LOCF = Taoyuan.copy() ; Da_LOCF = Dayuan.copy() ; Guan_LOCF = Guanyin.copy()
Long_LOCF = Longtan.copy() ; Ping_LOCF = Pingzhen.copy() ; Zhong_LOCF = Zhongli.copy()

### NOCB
Tao_NOCB = Taoyuan.copy() ; Da_NOCB = Dayuan.copy() ; Guan_NOCB = Guanyin.copy()
Long_NOCB = Longtan.copy() ; Ping_NOCB = Pingzhen.copy() ; Zhong_NOCB = Zhongli.copy()

### KNN
Tao_KNN = Taoyuan.copy() ; Da_KNN = Dayuan.copy() ; Guan_KNN = Guanyin.copy()
Long_KNN = Longtan.copy() ; Ping_KNN = Pingzhen.copy() ; Zhong_KNN = Zhongli.copy()

# =============================================================================
# 1. 前推法 LOCF
# =============================================================================
for i in Tao_LOCF.columns[2:13]:
   Tao_LOCF.loc[:, i].fillna(method = 'ffill', inplace = True) 
   
for i in Da_LOCF.columns[2:13]:
   Da_LOCF.loc[:, i].fillna(method = 'ffill', inplace = True) 
   
for i in Guan_LOCF.columns[2:13]:
   Guan_LOCF.loc[:, i].fillna(method = 'ffill', inplace = True) 
   
for i in Long_LOCF.columns[2:13]:
   Long_LOCF.loc[:, i].fillna(method = 'ffill', inplace = True) 
   
for i in Ping_LOCF.columns[2:13]:
   Ping_LOCF.loc[:, i].fillna(method = 'ffill', inplace = True) 
   
for i in Zhong_LOCF.columns[2:13]:
   Zhong_LOCF.loc[:, i].fillna(method = 'ffill', inplace = True) 
   
# =============================================================================
# 2. 後推法 NOCB
# =============================================================================
for i in Tao_NOCB.columns[2:13]:
   Tao_NOCB.loc[:, i].fillna(method = 'bfill', inplace = True) 
   
for i in Da_NOCB.columns[2:13]:
   Da_NOCB.loc[:, i].fillna(method = 'bfill', inplace = True) 
   
for i in Guan_NOCB.columns[2:13]:
   Guan_NOCB.loc[:, i].fillna(method = 'bfill', inplace = True) 
   
for i in Long_NOCB.columns[2:13]:
   Long_NOCB.loc[:, i].fillna(method = 'bfill', inplace = True) 
   
for i in Ping_NOCB.columns[2:13]:
   Ping_NOCB.loc[:, i].fillna(method = 'bfill', inplace = True) 
   
for i in Zhong_NOCB.columns[2:13]:
   Zhong_NOCB.loc[:, i].fillna(method = 'bfill', inplace = True)
   
# =============================================================================
# 3. KNN 補值
# =============================================================================
### ["PM2.5", "SO2", "CO", "O3", "NO2", "NOx", "NO", "windSpeed", "windDirec"]
imputer = KNNImputer(n_neighbors=1)

def KNN_Imputer(data, n_neighbors):
    imputer = KNNImputer(n_neighbors = n_neighbors)
    for i in data.columns[2:13]:
        data[[i]] = imputer.fit_transform(data[[i]])
    return data

Tao_KNN = KNN_Imputer(Tao_KNN, 1)
Da_KNN = KNN_Imputer(Da_KNN, 1)
Guan_KNN = KNN_Imputer(Guan_KNN, 1)
Ping_KNN = KNN_Imputer(Ping_KNN, 1)
Zhong_KNN = KNN_Imputer(Zhong_KNN, 1)
Long_KNN = KNN_Imputer(Long_KNN, 1)

# =============================================================================
# 轉換風度
# =============================================================================
def WindDirec(data):
    direc = []
    for i in data["windDirec"]:
        if (i <= 22.5) or (i > 337.5):
            direc.append("N")
        elif (i > 22.5) and (i <= 67.5):
            direc.append("NE")
        elif (i > 67.5) and (i <= 112.5):
            direc.append("E")
        elif (i > 112.5) and (i <= 157.5):
            direc.append("SE")
        elif (i > 157.5) and (i <= 202.5):
            direc.append("S")
        elif (i > 202.5) and (i <= 247.5):
            direc.append("SW")
        elif (i > 247.5) and (i <= 292.5):
            direc.append("W")
        elif (i > 292.5) and (i <= 337.5):
            direc.append("NW")
    data["Direc"] = direc
    return data
    
WindDirec(Tao_LOCF) ; WindDirec(Da_LOCF) ; WindDirec(Guan_LOCF)
WindDirec(Long_LOCF) ; WindDirec(Ping_LOCF) ; WindDirec(Zhong_LOCF)
WindDirec(Tao_NOCB) ; WindDirec(Da_NOCB) ; WindDirec(Guan_NOCB)
WindDirec(Long_NOCB) ; WindDirec(Ping_NOCB) ; WindDirec(Zhong_NOCB)
WindDirec(Tao_KNN) ; WindDirec(Da_KNN) ; WindDirec(Guan_KNN)
WindDirec(Long_KNN) ; WindDirec(Ping_KNN) ; WindDirec(Zhong_KNN)

### 將空氣品質指標 <0 之值轉變為 0
def negative_to_zero(data):
    num = data._get_numeric_data()
    for i in num:
        num[num < 0] = 0
        
negative_to_zero(Tao_LOCF) ; negative_to_zero(Da_LOCF) ; negative_to_zero(Guan_LOCF)
negative_to_zero(Long_LOCF) ; negative_to_zero(Ping_LOCF) ; negative_to_zero(Zhong_LOCF)
negative_to_zero(Tao_NOCB) ; negative_to_zero(Da_NOCB) ; negative_to_zero(Guan_NOCB)
negative_to_zero(Long_NOCB) ; negative_to_zero(Ping_NOCB) ; negative_to_zero(Zhong_NOCB)
negative_to_zero(Tao_KNN) ; negative_to_zero(Da_KNN) ; negative_to_zero(Guan_KNN)
negative_to_zero(Long_KNN) ; negative_to_zero(Ping_KNN) ; negative_to_zero(Zhong_KNN)

# =============================================================================
# one-hot encoding
# =============================================================================
def one_hot_encoding(data):
    data_dum = pd.get_dummies(data["Direc"])
    newdata = data.join(data_dum)
    return newdata

Tao_LOCF = one_hot_encoding(Tao_LOCF) ; Da_LOCF = one_hot_encoding(Da_LOCF) ; Guan_LOCF = one_hot_encoding(Guan_LOCF)
Long_LOCF = one_hot_encoding(Long_LOCF) ; Ping_LOCF = one_hot_encoding(Ping_LOCF) ; Zhong_LOCF = one_hot_encoding(Zhong_LOCF)
Tao_NOCB = one_hot_encoding(Tao_NOCB) ; Da_NOCB = one_hot_encoding(Da_NOCB) ; Guan_NOCB = one_hot_encoding(Guan_NOCB)
Long_NOCB = one_hot_encoding(Long_NOCB) ; Ping_NOCB = one_hot_encoding(Ping_NOCB) ; Zhong_NOCB = one_hot_encoding(Zhong_NOCB)
Tao_KNN = one_hot_encoding(Tao_KNN) ; Da_KNN = one_hot_encoding(Da_KNN) ; Guan_KNN = one_hot_encoding(Guan_KNN)
Long_KNN = one_hot_encoding(Long_KNN) ; Ping_KNN = one_hot_encoding(Ping_KNN) ; Zhong_KNN = one_hot_encoding(Zhong_KNN)
# =============================================================================
# 畫圖查看遺失值填補狀況
# =============================================================================
def missing_plot(data, LOCF, NOCB, KNN, var, start = "2019-01-01", end = "2021-12-16"):
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定字體
    plt.rcParams['axes.unicode_minus'] = False                # 用來正常顯示負號
    plt.rcParams["figure.figsize"] = (10,6)
    plt.figure(dpi=150)
    plt.subplot(3,1,1)
    plt.plot(LOCF[var], label = "LOCF", color='red', marker='o', linestyle='dotted')
    plt.plot(data[var], marker='o')
    plt.xlim(datetime.strptime(start, "%Y-%m-%d"), datetime.strptime(end, "%Y-%m-%d"))
    plt.subplot(3,1,2)
    plt.plot(NOCB[var], label = "NOCB", color='red', marker='o', linestyle='dotted')
    plt.plot(data[var], marker='o')
    plt.xlim(datetime.strptime(start, "%Y-%m-%d"), datetime.strptime(end, "%Y-%m-%d"))
    plt.subplot(3,1,3)
    plt.plot(KNN[var], label = "KNN", color='red', marker='o', linestyle='dotted')
    plt.plot(data[var], marker='o')
    plt.xlim(datetime.strptime(start, "%Y-%m-%d"), datetime.strptime(end, "%Y-%m-%d"))
    plt.show()
    
missing_plot(Dayuan, Da_LOCF, Da_NOCB, Da_KNN, "PM2.5")


# =============================================================================
# to_sql
# =============================================================================
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format('hsuan', 'hsuan', 'airiot.tibame.cloud:3306', 'model','utf8mb4'))
con = engine.connect()#建立連線
Tao_LOCF.to_sql(name='locf', con=con, if_exists='replace', index=False)
con.close()

engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format('hsuan', 'hsuan', 'airiot.tibame.cloud:3306', 'model','utf8mb4'))
con = engine.connect()#建立連線
Tao_NOCB.to_sql(name='nocb', con=con, if_exists='replace', index=False)
con.close()

engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format('hsuan', 'hsuan', 'airiot.tibame.cloud:3306', 'model','utf8mb4'))
con = engine.connect()#建立連線
Tao_KNN.to_sql(name='knn', con=con, if_exists='replace', index=False)
con.close()

engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format('hsuan', 'hsuan', 'airiot.tibame.cloud:3306', 'model','utf8mb4'))
con = engine.connect()#建立連線
Taoyuan.to_sql(name='Taoyuan', con=con, if_exists='replace', index=False)
con.close()