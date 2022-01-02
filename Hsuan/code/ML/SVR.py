from sklearn import datasets, metrics
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
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
    data = data.drop(["Direc", 'NOx', 'NO'], axis=1)
    # 關閉連線
    cursor.close()
    conn.close()
    
    return data

df = get_data("knn")

# df = df[df.Date >= datetime.strptime("2021-06-01", "%Y-%m-%d")].sort_values(by = "Date")

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
x_train_svr = sc_x.fit_transform(X_train)
y_train_svr = sc_y.fit_transform(y_train)

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
# C: 決定給誤差/被分錯的資料「多少」懲罰值
#    > C 越大，代表容錯越小，卻容易 overfitting  
#    > C 越小，代表容錯越大，可以追求更大的 margin
# degree: 增加模型複雜度，3 代表轉換到三次空間進行分類。
#    > gamma: 數值越大越能做複雜的分類邊界。
#    > gamma 大，資料點的影響力範圍比較近，對超平面來說，近點的影響力權重較大，容易勾勒出擬合近點的超平面，也容易造成 overfitting  
#    > gamma 小，資料點的影響力範圍比較遠，對超平面來說，較遠的資料點也有影響力，因此能勾勒出平滑、近似直線的超平面  
# epsilon = margin of tolerance
#    > 越大，代表容忍區塊越大，越多資料會被忽視，造成模型的準確度越低  
#    > 越小越接近 0，所有的資料殘差(error)都會被考慮，卻也容易造成 overfitting
# =============================================================================

# =============================================================================
# linear
# =============================================================================
### 建模
svr_linear = SVR(kernel = "linear", C = 1)
# 利用訓練集讓模型進行學習
svr_linear.fit(x_train_svr, y_train_svr)
'''
fit_transform：是 fit 和 transform 的组合，既包括了模型訓練又包含了轉換(資料標準化)
scaler.inverse_transform：是將標準化後的資料轉換為原始數據
'''
svr_linear_y_predict = sc_y.inverse_transform(svr_linear.predict(sc_x.transform(X_test)))

### 評估迴歸模型
# test data
RMSE_svr_linear = sqrt(metrics.mean_squared_error(y_test, svr_linear_y_predict))
MAE_svr_linear = metrics.mean_absolute_error(y_test, svr_linear_y_predict)
R2_svr_linear = metrics.r2_score(y_test,svr_linear_y_predict)
RMSLE_svr_linear = rmsle(y_test,svr_linear_y_predict)

# training data
svr_train_y_RMSE_linear = sqrt(metrics.mean_squared_error(y_train,sc_y.inverse_transform(svr_linear.predict(sc_x.transform(X_train)))))
svr_train_y_MAE_linear = metrics.mean_absolute_error(y_train,sc_y.inverse_transform(svr_linear.predict(sc_x.transform(X_train))))
svr_train_y_R2_linear = metrics.r2_score(y_train,sc_y.inverse_transform(svr_linear.predict(sc_x.transform(X_train))))
svr_train_y_RMSLE_linear = rmsle(y_train,sc_y.inverse_transform(svr_linear.predict(sc_x.transform(X_train))))

# =============================================================================
# poly
# =============================================================================
### 建模
svr_poly = SVR(kernel='poly', gamma='auto', C=1)
# 利用訓練集讓模型進行學習
svr_poly.fit(x_train_svr, y_train_svr)
svr_poly_y_predict = sc_y.inverse_transform(svr_poly.predict(sc_x.transform(X_test)))

### 評估迴歸模型
# test data
RMSE_svr_poly = sqrt(metrics.mean_squared_error(y_test, svr_poly_y_predict))
MAE_svr_poly = metrics.mean_absolute_error(y_test, svr_poly_y_predict)
R2_svr_poly = metrics.r2_score(y_test,svr_poly_y_predict)
RMSLE_svr_poly = rmsle(y_test,svr_poly_y_predict)

# training data
svr_train_y_RMSE_poly = sqrt(metrics.mean_squared_error(y_train,sc_y.inverse_transform(svr_poly.predict(sc_x.transform(X_train)))))
svr_train_y_MAE_poly = metrics.mean_absolute_error(y_train,sc_y.inverse_transform(svr_poly.predict(sc_x.transform(X_train))))
svr_train_y_R2_poly = metrics.r2_score(y_train,sc_y.inverse_transform(svr_poly.predict(sc_x.transform(X_train))))
svr_train_y_RMSLE_poly = rmsle(y_train,sc_y.inverse_transform(svr_poly.predict(sc_x.transform(X_train))))

# =============================================================================
# rbf
# =============================================================================
### 建模
svr_rbf = SVR(kernel='rbf', gamma=0.1, C=15)
# 利用訓練集讓模型進行學習
svr_rbf.fit(x_train_svr, y_train_svr)
svr_rbf_y_predict = sc_y.inverse_transform(svr_rbf.predict(sc_x.transform(X_test)))

### 評估迴歸模型
# test data
RMSE_svr_rbf = sqrt(metrics.mean_squared_error(y_test, svr_rbf_y_predict))
MAE_svr_rbf = metrics.mean_absolute_error(y_test, svr_rbf_y_predict)
R2_svr_rbf = metrics.r2_score(y_test,svr_rbf_y_predict)
RMSLE_svr_rbf = rmsle(y_test,svr_rbf_y_predict)

# training data
svr_train_y_RMSE_rbf = sqrt(metrics.mean_squared_error(y_train,sc_y.inverse_transform(svr_rbf.predict(sc_x.transform(X_train)))))
svr_train_y_MAE_rbf = metrics.mean_absolute_error(y_train,sc_y.inverse_transform(svr_rbf.predict(sc_x.transform(X_train))))
svr_train_y_R2_rbf = metrics.r2_score(y_train,sc_y.inverse_transform(svr_rbf.predict(sc_x.transform(X_train))))
svr_train_y_RMSLE_rbf = rmsle(y_train,sc_y.inverse_transform(svr_rbf.predict(sc_x.transform(X_train))))

# =============================================================================
# Random Forest
# =============================================================================
### 建模
rf_reg = RandomForestRegressor(n_estimators = 500, random_state = 123)
rf_reg.fit(X_train,y_train)

rf_y_predict = rf_reg.predict(X_test)

### 評估迴歸模型
# test data
RMSE_rf = sqrt(metrics.mean_squared_error(y_test, rf_y_predict))
MAE_rf = metrics.mean_absolute_error(y_test, rf_y_predict)
R2_rf = metrics.r2_score(y_test,rf_y_predict)
RMSLE_rf = rmsle(y_test,rf_y_predict)

# training data
rf_ytp_RMSE = sqrt(metrics.mean_squared_error(y_train, rf_reg.predict(X_train)))
rf_ytp_MAE = metrics.mean_absolute_error(y_train, rf_reg.predict(X_train))
rf_ytp_R2 = metrics.r2_score(y_train, rf_reg.predict(X_train))
rf_ytp_RMSLE = rmsle(y_train, rf_reg.predict(X_train))

# =============================================================================
# 比較表
# =============================================================================
test_data_evalue = {"linear": [RMSE_svr_linear, MAE_svr_linear, R2_svr_linear , RMSLE_svr_linear],
                    "poly": [RMSE_svr_poly, MAE_svr_poly, R2_svr_poly , RMSLE_svr_poly],
                    "rbf": [RMSE_svr_rbf, MAE_svr_rbf, R2_svr_rbf , RMSLE_svr_rbf],
                    "Random Forest":[RMSE_rf, MAE_rf, R2_rf, RMSLE_rf]}
test_evalue = pd.DataFrame(test_data_evalue).round(3)
test_evalue.index = ["RMSE", "MAE", "R2", "RMSLE"]
test_evalue

train_data_evalue = {"linear": [svr_train_y_RMSE_linear, svr_train_y_MAE_linear, svr_train_y_R2_linear , svr_train_y_RMSLE_linear],
                    "poly": [svr_train_y_RMSE_poly, svr_train_y_MAE_poly, svr_train_y_R2_poly , svr_train_y_RMSLE_poly],
                    "rbf": [svr_train_y_RMSE_rbf, svr_train_y_MAE_rbf, svr_train_y_R2_rbf , svr_train_y_RMSLE_rbf],
                    "Random Forest":[rf_ytp_RMSE, rf_ytp_MAE, rf_ytp_R2, rf_ytp_RMSLE]}
train_evalue = pd.DataFrame(train_data_evalue).round(3)
train_evalue.index = ["RMSE", "MAE", "R2", "RMSLE"]
train_evalue