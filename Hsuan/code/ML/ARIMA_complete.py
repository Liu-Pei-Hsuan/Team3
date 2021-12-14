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

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定字體
plt.rcParams['axes.unicode_minus'] = False                # 用來正常顯示負號

# =============================================================================
# 資料前處理
# =============================================================================
def get_data(file):
    # 1. 讀入資料
    global data
    data = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/{}.csv".format(file))
    data = data.loc[:, ["DataCreationDate", "PM2.5", 'SO2', 'CO', 'O3', 'NO2',
                        'NOx', 'NO', 'Temp', 'Humidity']]
    
    # 2. KNN 補值
    imputer = KNNImputer(n_neighbors=1)
    for i in data.columns[1:]:
        data[[i]] = imputer.fit_transform(data[[i]])
    
    # 3. 時間轉換
    # data["date"] = pd.to_datetime(data['DataCreationDate']).dt.date
    data['DataCreationDate'] = pd.to_datetime(data['DataCreationDate'])
    df = data.set_index('DataCreationDate')
    df.head()
    
    return df

Taoyuan = "Taoyuan"
df = get_data(Taoyuan)

# # =============================================================================
# # 時間序列圖
# # =============================================================================
# def timeseries_plot(feature):
#     plt.figure(figsize=(20, 10))
#     df_plot = df[feature]
#     df_plot.plot()
    
# timeseries_plot("PM2.5")

# # =============================================================================
# # ACF、PACF 圖
# # =============================================================================
# def ACF_PACF(feature): # feature = 所要選取的變數
#     series = df[[feature]]
#     pyplot.figure(figsize=(20,10))
#     pyplot.subplot(211)
#     plot_acf(series, ax=pyplot.gca())
#     pyplot.subplot(212)
#     plot_pacf(series, ax=pyplot.gca())
#     pyplot.show()

# ACF_PACF(("PM2.5"))

# =============================================================================
# 分成訓練集和驗證集
# =============================================================================
def Train_Test_Data(feature, size = 0.8): 
    '''
    feature = 所要選取的變數  ;  size = 切割資料比例
    '''
    
    df1 = df[feature]
    
    train = df1[:int(0.8*(len(df1)))]
    valid = df1[int(0.8*(len(df1))):]
    
    return train, valid

train, valid =Train_Test_Data("PM2.5", size = 0.8)

# =============================================================================
# 各種 plot
# =============================================================================
def timeseries_plot(feature, train, valid):
    # 原始時間序列圖
    plt.figure(figsize=(20, 10))
    df_plot = df[feature]
    df_plot.plot()
    
    # ACF、PACF
    pyplot.figure(figsize=(20,10))
    pyplot.subplot(211)
    plot_acf(df_plot, ax=pyplot.gca())
    pyplot.subplot(212)
    plot_pacf(df_plot, ax=pyplot.gca())
    pyplot.show()
    
    # 訓練、驗證資料時間序列圖
    plt.figure(figsize=(20,10))
    plt.plot(train)
    plt.plot(valid)

    '''
    使用 seasonal_decompose 查看時間序列狀況
      1. 第一個小圖 observed 就是我們觀測到的實際值
      2. 第二個圖 Trend 可以看到它整體的變化趨勢
      3. 第三個 seasonal 是整個序列表現出來的季節性部分
      4. 第四個 residual 是殘差
    '''
    result = seasonal_decompose(df_plot, model='additive')
    result.plot()
    pyplot.show()

timeseries_plot("PM2.5", train, valid)

# =============================================================================
# Auto Arima
# =============================================================================
from pmdarima.arima import auto_arima

## model 1
# Best : ARIMA(3,1,0)(2,1,0)[12]
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

# # =============================================================================
# # ARIMA - MA
# # =============================================================================
# moving_avg = data["PM2.5"].rolling(12).mean()

# plt.figure(figsize=(20,10))
# plt.plot(data["PM2.5"])
# plt.plot(moving_avg, color='red')
# plt.xlim(4000, 4393)

# data_3 = data["PM2.5"] - moving_avg
# data_3.head(12)

# data_3.dropna(inplace=True)

# #Determing rolling statistics
# rolmean = data_3.rolling(12).mean()
# rolstd = data_3.rolling(12).std()

# #Plot rolling statistics:
# plt.figure(figsize=(20,10))
# orig = plt.plot(data_3, color='blue',label='Original')
# mean = plt.plot(rolmean, color='red', label='Rolling Mean')
# std = plt.plot(rolstd, color='black', label = 'Rolling Std')
# plt.legend(loc='best')
# plt.title('Rolling Mean & Standard Deviation')
# plt.show(block=False)


# =============================================================================
# 利用 ARIMA 模型決定是否差分
# =============================================================================
def ARIMA_plot(feature):
    plt.rcParams.update({'figure.figsize':(15,18)})
    
    ###  Original Series
    # sharex, sharey控制 x, y 軸之間的屬性共享，當 = True 或 all 表示 x 或 y 軸屬性將在所有子圖中共享
    fig, axes = plt.subplots(3, 2, sharex=False)  
    p1 = data[[feature]].plot(grid=True, ax = axes[0,0])
    p1.set_title('Original Series')
    p2 = plot_acf(data[[feature]], ax = axes[0,1])
    
    # 1st Differencing
    p3 = data[[feature]].diff().plot(grid=True, ax = axes[1,0])
    p3.set_title('1st Order Differencing')
    p4 = plot_acf(data[[feature]].diff().dropna(), ax = axes[1,1])
    
    # 2nd Differencing
    p5 = data[[feature]].diff().diff().plot(grid=True, ax = axes[2,0])
    p5.set_title('2nd Order Differencing')
    p6 = plot_acf(data[[feature]].diff().diff().dropna(), ax = axes[2,1])
    
    plt.suptitle('利用 ARIMA 模型決定是否差分',  y = 0.92, fontweight = "bold", fontsize = 14)
    plt.show()
    
ARIMA_plot("PM2.5")


# =============================================================================
# 配適模型
# =============================================================================
def ARIMA_model(feature, p, d, q):
    model = ARIMA(data[[feature]], order=(p, d, q))
    global model_fit
    model_fit = model.fit()
    print(model_fit.summary())
    return model_fit
    
model_fit = ARIMA_model("PM2.5", 3, 2, 0)
    
# =============================================================================
# 檢查殘差
# =============================================================================
def Residual():
    plt.rcParams.update({'figure.figsize':(10, 5)})
    # Plot residual errors
    residuals = pd.DataFrame(model_fit.resid)
    fig, ax = plt.subplots(1,2)
    residuals.plot(title="Residuals", ax=ax[0])
    residuals.plot(kind='kde', title='Density', ax=ax[1])
    plt.show()

Residual()


# =============================================================================
# 模型預測
# =============================================================================

# Create Training and Test
def split_data(length, feature):
    train = data.loc[:int(length), feature]
    test = data.loc[int(length):, feature]
    return train, test
    

def ARIMA_model(data, p, d, q):
    model = ARIMA(data, order=(p, d, q))
    fitted = model.fit()  
    print(model_fit.summary())
    return fitted
  

# training, testing data   
train, test = split_data(4368, "PM2.5")

# ARIMA model
train_model = ARIMA_model(train, 1, 1, 2)
# test_model = ARIMA_model(test, 1, 1, 2)

pred = pd.Series(train_model.forecast(24, alpha=0.05), index=test.index)


def pred_plot():
    plt.rcParams.update({'figure.figsize':(10, 5)})
    plt.plot(train, label='training')
    plt.plot(test, label='actual')
    plt.plot(pred, label='forecast')
    plt.title('Forecast v.s. Actuals')
    plt.legend(loc='upper left', fontsize=8)
    plt.xlim(4350, 4393)
    plt.show()
    
pred_plot()

