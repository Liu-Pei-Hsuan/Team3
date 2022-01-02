import matplotlib.pyplot as plt
import pandas as pd
import pymysql
from sklearn.preprocessing import LabelEncoder
import datetime
from datetime import timedelta
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
    data = pd.DataFrame(results, columns = ["ID", "type", "year", "age", "county", "week", "case"])
    data = data.drop("ID", axis=1)
    
    # 關閉連線
    cursor.close()
    conn.close()
    
    return data

df = get_data("enterovirus")

# =============================================================================
# LabelEncoder
'''
1. 0 ~ 2 歲：0
2. 10 ~ 14 歲：1
3. 15 歲以上：2
4. 3 ~ 4 歲：3
5. 5 ~ 9 歲：4
'''
# =============================================================================
Label_Encoder = LabelEncoder()
df["new_age"] = Label_Encoder.fit_transform(df['age'])

### 不區 type (住院、門診)
df1 = df.groupby(["year","week", "new_age"], as_index=False).sum()
df1.week = df1.week.astype(int)
df1["new_age"] = df1["new_age"].astype(str)
df1 = df1.sort_values(by = ["year","week"])
df_2021 = df1[df1.year >= 2021].reset_index(drop = True)

### 加入每週第一天日期
def get_start_date_from_calendar_week(year, calendar_week):       
    monday = datetime.datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
    return monday
    
total_week = int(len(df_2021)/5)
week_first_day = []
for i in range(1, total_week+1):
    date = get_start_date_from_calendar_week(2021, i)
    date5 = np.repeat(date, 5)
    week_first_day.extend(date5)

df_2021["date"] = week_first_day
df_2021 = df_2021.set_index("date")


# =============================================================================
# 將不同年齡層分開
# =============================================================================
age_0_2 = df_2021[df_2021["new_age"] == "0"]
age_10_14 = df_2021[df_2021["new_age"] == "1"]
age_15 = df_2021[df_2021["new_age"] == "2"]
age_3_4 = df_2021[df_2021["new_age"] == "3"]
age_5_9 = df_2021[df_2021["new_age"] == "4"]


# =============================================================================
# 趨勢圖
# =============================================================================
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定字體
plt.rcParams['axes.unicode_minus'] = False                # 用來正常顯示負號
plt.rcParams["figure.figsize"] = (10,6)
fig = plt.figure(dpi=150)
plt.plot(age_0_2["case"], label = "0-2 歲", color = "darkorange")
plt.plot(age_3_4["case"], label = "3-4 歲", color = "forestgreen")
plt.plot(age_5_9["case"], label = "5-9 歲", color = "royalblue")
plt.plot(age_10_14["case"], label = "10-14 歲", color = "mediumpurple")
plt.plot(age_15["case"], label = "15 歲以上", color = "firebrick") #linestyle='-', marker = "o"
plt.axhline(y=df_2021["case"].mean(), color = 'red', linestyle='-.', label = "平均值",linewidth=3.0)
plt.xlabel("時間", fontsize=12)                # 設定 x 軸標題及粗體
plt.ylabel("病例數", fontsize=12)  # 設定 y 軸標題及粗體
plt.title("腸病毒趨勢圖", fontsize = 20, fontweight = "bold")   # 設定標題、文字大小、粗體及位置
plt.legend(loc='best', fontsize=13)
plt.grid()
plt.show()

fig.savefig('app/static/enterovirus.png', bbox_inches="tight", pad_inches=0.1)
