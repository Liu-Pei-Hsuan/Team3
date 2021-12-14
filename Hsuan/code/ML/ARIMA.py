import ARIMA_function as arima_fn

import numpy as np
import pandas as pd
from pandas import Series
import pandas_profiling as pp
from matplotlib import pyplot
# 這樣才能 show 出來
%matplotlib inline
import matplotlib.pyplot as plt
from sklearn.datasets import load_files
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf
from pmdarima.arima import auto_arima

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定字體
plt.rcParams['axes.unicode_minus'] = False                # 用來正常顯示負號

# =============================================================================
# 資料前處理
# =============================================================================
Dayuan = "Dayuan" ; Taoyuan = "Taoyuan" ; Guanyin = "Guanyin"
Longtan = "Longtan" ; Zhongli = "Zhongli" ; Pingzhen = "Pingzhen"

data, df = arima_fn.get_data(Taoyuan) # 選擇所要預測之測站

# =============================================================================
# 分成訓練集和驗證集
# =============================================================================
train, valid = arima_fn.Train_Test_Data(df, "PM2.5", size = 0.8) # 選擇所要預測之變數


# =============================================================================
# 各種 plot
# =============================================================================
arima_fn.timeseries_plot(df, "PM2.5", train, valid) # 選擇所要預測之變數

# =============================================================================
# Auto Arima
# =============================================================================
## model 1
# Best : ARIMA(3,1,0)(2,1,0)[12]
# stepwise_model.order (取出最佳模型)
stepwise_model = auto_arima(data["PM2.5"], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                            start_P=0, seasonal=True, d=1, D=1, trace=True, error_action='ignore',  
                            suppress_warnings=True, stepwise=True)
print(stepwise_model.aic())

## model 2
# Best : ARIMA(3,1,0)(0,0,0)[0]
stepwise_model = auto_arima(data["PM2.5"], start_p=1, start_q=1, max_p=3, max_q=3, start_P=0,
                            seasonal=False, d=2, D=1, trace=True, error_action='ignore',
                            suppress_warnings=True, stepwise=True)
print(stepwise_model.aic())


# =============================================================================
# 利用 ARIMA 模型決定是否差分
# =============================================================================
arima_fn.ARIMA_plot("PM2.5") # 選擇所要預測之變數


# =============================================================================
# 配適模型
# =============================================================================
model_fit = arima_fn.arima_model("PM2.5", stepwise_model.order) # 選擇所要預測之變數，以及最佳模型
# =============================================================================
# 檢查殘差
# =============================================================================
arima_fn.Residual()

# =============================================================================
# 模型預測
# =============================================================================

# training, testing data   
train, test = arima_fn.split_data(4368, "PM2.5") # 選擇所要預測之變數、training data 資料數

# ARIMA model
train_model = arima_fn.ARIMA_model(train, 3, 2, 0)
# test_model = ARIMA_model(test, 1, 1, 2)

# 預測
future_24_hour = train_model.forecast(24, alpha=0.05)
pred = pd.Series(train_model.forecast(24, alpha=0.05), index=test.index)
arima_fn.pred_plot(train, test, pred, 4350, 4393) # 要查看資料的範圍

