from sklearn import datasets, metrics
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from math import sqrt
import numpy as np
import pandas as pd
import pymysql
from datetime import datetime

# =============================================================================
# 取得資料
# =============================================================================
def get_data(table):
    config = {"host" : "airiot.tibame.cloud", "port" : 3306, "user" : "hsuan",
          "passwd" : "hsuan", "db" : "model", "charset" : "utf8mb4"}

    conn = pymysql.connect(**config) ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    
    SQL = "select * from {}".format(table)
    print('資料筆數 :',cursor.execute(SQL))
    
    results = cursor.fetchall()
    
    data = pd.DataFrame(results, columns = ["Date", "Station", "PM2.5", "SO2", "CO", "O3", "NO2", "NOx",
                                            "NO", "windSpeed", "windDirec", "Humidity", "Temp",
                                            "Direc", "E", "N", "NE", "NW", "S", "SE", "SW", "W"])
    data = data.drop(["Direc", 'NOx', 'NO', "windDirec", "windSpeed", "Station"], axis=1)
    # 關閉連線
    cursor.close()
    conn.close()
    
    return data

df = get_data("knn")

df = df[df.Date >= datetime.strptime("2021-01-01", "%Y-%m-%d")].sort_values(by = "Date")

df = df.set_index("Date")

# =============================================================================
# 訓練集、測試集
# =============================================================================
X = df.iloc[:,2:df.shape[1]]
y = df.iloc[:,1:2].values # PM2.5

X_train = X[:int(0.9*(len(X)))] ; X_test = X[int(0.9*(len(X))):]
y_train = y[:int(0.9*(len(y)))] ; y_test = y[int(0.9*(len(y))):]

# =============================================================================
# 標準化
# =============================================================================
sc_x = StandardScaler()
sc_y = StandardScaler()
x_train = sc_x.fit_transform(X_train)
y_train = sc_y.fit_transform(y_train)

# =============================================================================
# RMSLE
# =============================================================================
def rmsle(real, predicted):
    sum=0.0
    for x in range(len(predicted)):
        if predicted[x]<0 or real[x]<0:
            continue
        p = np.log(predicted[x]+1)
        r = np.log(real[x]+1)
        sum = sum + (p - r)**2
    return ((sum/len(predicted))**0.5)[0]

# =============================================================================
# 建模
# =============================================================================
regressor = GradientBoostingRegressor(max_depth=5, n_estimators=30)
regressor.fit(x_train,y_train)
gbrt_y_predict = sc_y.inverse_transform(regressor.predict(sc_x.transform(X_test)))

# =============================================================================
# 評估迴歸模型
# =============================================================================
rmse_gbrt = sqrt(metrics.mean_squared_error(y_test, gbrt_y_predict))
mae_gbrt = metrics.mean_absolute_error(y_test, gbrt_y_predict)
r2_gbrt = metrics.r2_score(y_test,gbrt_y_predict)
rmsle_gbrt = rmsle(y_test,gbrt_y_predict)

test_data_evalue = {"linear": [rmse_gbrt, mae_gbrt, r2_gbrt, rmsle_gbrt]}
test_evalue = pd.DataFrame(test_data_evalue).round(3)
test_evalue.index = ["RMSE", "MAE", "R2", "RMSLE"]
test_evalue