import matplotlib.pyplot as plt
import pandas as pd
import pymysql
from sklearn.preprocessing import LabelEncoder
import datetime
from datetime import datetime
import numpy as np

# =============================================================================
# 取得資料
# =============================================================================
def get_data(table):
    config = {"host" : "mqtt2.tibame.cloud", "port" : 3306, "user" : "hsuan",
          "passwd" : "hsuan", "db" : "Disease", "charset" : "utf8mb4"}

    conn = pymysql.connect(**config) ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    
    SQL = "select * from {}".format(table)
    print('資料筆數 :',cursor.execute(SQL))
    
    results = cursor.fetchall()
    
    if table == "COVID19":
        data = pd.DataFrame(results, columns = ["ID", "date", "city", "境內"])
        data = data.drop("ID", axis=1)
        
    elif table == "COVID19_foreign":
        data = pd.DataFrame(results, columns = ["ID", "date", "境外"])
        data = data.drop("ID", axis=1)
    
    # 關閉連線
    cursor.close()
    conn.close()
    
    return data

Taiwan = get_data("COVID19").groupby("date", as_index=False).sum()
#Taiwan = Taiwan.set_index("date")
foreign = get_data("COVID19_foreign").sort_values("date").reset_index(drop = True)
#foreign = foreign.set_index("date")

covid19 = pd.merge(Taiwan, foreign, how = "outer").sort_values(by = "date")
covid19 = covid19[covid19.date > datetime.strptime("2021-10-01", "%Y-%m-%d").date()]
covid19.fillna(0, inplace=True)
covid19 = covid19.set_index("date")
# =============================================================================
# 趨勢圖
# =============================================================================
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定字體
plt.rcParams['axes.unicode_minus'] = False                # 用來正常顯示負號
plt.rcParams["figure.figsize"] = (10,6)
fig = plt.figure(dpi=150)
# plt.fill_between(foreign.index, 0, foreign.number, facecolor=(0.3, 0.3, 0.45 ,.4), edgecolor=(0, 0, 0, 1))
plt.plot(covid19["境內"], label = "台灣確診人數", color = "darkorange")
# plt.bar(covid19.index, covid19["境外"], label = "台灣確診人數", color = "forestgreen")
plt.plot(covid19["境外"], label = "境外確診人數", color = "forestgreen")
plt.xlabel("時間", fontsize=12)                # 設定 x 軸標題及粗體
plt.ylabel("確診人數", fontsize=12)  # 設定 y 軸標題及粗體
plt.title("COVID-19 趨勢圖", fontsize = 20, fontweight = "bold")   # 設定標題、文字大小、粗體及位置
plt.legend(loc='best', fontsize=14)
plt.xlim()
plt.grid()
plt.show()


fig.savefig('app/static/covid19.png', bbox_inches="tight", pad_inches=0.1)
