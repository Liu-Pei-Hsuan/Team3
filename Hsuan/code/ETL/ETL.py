import matplotlib.pyplot as plt
import pandas as pd
import pymysql
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
from datetime import timedelta
import numpy as np
from sklearn.impute import KNNImputer
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# 取得資料
# =============================================================================
def get_data(table):
    config = {"host" : "airiot.tibame.cloud", "port" : 3306, "user" : "hsuan",
          "passwd" : "hsuan", "db" : "opensource_data", "charset" : "utf8mb4"}

    conn = pymysql.connect(**config) ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    
    SQL = "select * from {}".format(table)
    print('資料筆數 :',cursor.execute(SQL))
    
    results = cursor.fetchall()
    
    data = pd.DataFrame(results, columns = ["Station", "AQI", "SO2", "CO", "O3", "PM2.5", "NO2",
                                            "NO", "NOx", "Date", "WindSpeed", "WindDirec", "Temp", "Humidity"])
    data = data.drop("AQI", axis=1)
   
    # 關閉連線
    cursor.close()
    conn.close()
    
    return data

data = get_data("summary_data")
data = data[["Station", "Date", "PM2.5", "SO2", "CO", "O3", "NO2",
             "NO", "NOx", "WindSpeed", "WindDirec", "Temp", "Humidity"]]
# data = data.set_index("Date")
### 遺失值比例
na_precrent = round(data.isnull().sum()/len(data) * 100, 2)
na_precrent

### 轉變資料型態
for i in data.columns[2:13]:
    data[i] = data[i].astype("float")
    
data = data.sort_values(by = "Date")

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
    for i in data["WindDirec"]:
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
# 遺失比率
# =============================================================================
column = ['PM2.5', 'SO2', 'CO', 'O3', 'NO2', '風速', '風向', '溫度', '濕度']
nan = round(Taoyuan.isnull().sum(), 2)
na = [nan[2], nan[3], nan[4], nan[5], nan[6], nan[9], nan[10], nan[11], nan[12]]

naplot = pd.DataFrame(list(zip(column, na)), columns =["column", "nan"]) 

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定字體
plt.rcParams['axes.unicode_minus'] = False                # 用來正常顯示負號
plt.rcParams["figure.figsize"] = (13,6)
fig = plt.figure(dpi=150)
plt.bar(naplot.column, naplot.nan, label = "遺失比例 (%)", color = "seagreen")
plt.ylabel("遺失比例 (%)", fontsize=16)  # 設定 y 軸標題及粗體
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
#plt.ylim(0,5)
# plt.legend(loc='best', fontsize=13)
plt.show()


# =============================================================================
# 遺失值填補狀況
# =============================================================================
Taoyuan1 = Taoyuan[["Date", "PM2.5", "SO2", "CO", "O3", "NO2", "WindSpeed", "WindDirec", "Temp", "Humidity"]]
data1 = data[["Date", "PM2.5", "SO2", "CO", "O3", "NO2", "WindSpeed", "WindDirec", "Temp", "Humidity"]]

LOCF_desc = round(Tao_LOCF.describe(), 3)
NOCB_desc = round(Tao_NOCB.describe(), 3)
KNN_desc = round(Tao_KNN.describe(), 3)
Taoyuan_desc = round(Taoyuan.describe(), 3)


plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定字體
plt.rcParams['axes.unicode_minus'] = False                # 用來正常顯示負號
plt.rcParams["figure.figsize"] = (15,10)
plt.rcParams.update({'font.size': 12})
fig,axes=plt.subplots(3,3)
p1 = sns.boxplot(y = Taoyuan1["PM2.5"].dropna(), showfliers = False, ax = axes[0,0])
sns.pointplot(y="PM2.5", data=Tao_LOCF, linestyles='', scale=1, 
              color='r', errwidth=1.5, capsize=0.2, markers='x', ax=axes[0,0])
p1.set(xlabel=None)
p2 = sns.boxplot(y = Taoyuan1["SO2"].dropna(), showfliers = False, ax = axes[0,1])
p2.set(xlabel=None)
p3 = sns.boxplot(y = Taoyuan1["CO"].dropna(), showfliers = False, ax = axes[0,2])
p3.set(xlabel=None)
p4 = sns.boxplot(y = Taoyuan1["O3"].dropna(), showfliers = False, ax = axes[1,0])
p4.set(xlabel=None)
p5 = sns.boxplot(y = Taoyuan1["NO2"].dropna(), showfliers = False, ax = axes[1,1])
p5.set(xlabel=None)
p6 = sns.boxplot(y = Taoyuan1["WindSpeed"].dropna(), showfliers = False, ax = axes[1,2])
p6.set(xlabel=None)
p7 = sns.boxplot(y = Taoyuan1["WindDirec"].dropna(), showfliers = False, ax = axes[2,0])
p8 = sns.boxplot(y = Taoyuan1["Temp"].dropna(), showfliers = False, ax = axes[2,1])
sns.boxplot(y = Taoyuan1["Humidity"].dropna(), showfliers = False, ax = axes[2,2]);


