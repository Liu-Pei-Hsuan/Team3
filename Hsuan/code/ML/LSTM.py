from keras.models import Sequential
from keras.layers import Dense, LSTM, Bidirectional
from tensorflow import random
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from numpy import array
import pymysql
from datetime import datetime

random.set_seed(123)

# Make our plot a bit formal
font = {'family' : 'Arial', 'weight' : 'normal', 'size' : 10}
plt.rc('font', **font)

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
    data = data.drop(["windDirec", "NOx", "NO", "Direc", "Station"], axis=1)
    # 關閉連線
    cursor.close()
    conn.close()
    
    return data

df = get_data("locf")
df = df[df.Date >= datetime.strptime("2021-01-01", "%Y-%m-%d")].sort_values(by = "Date")
df = df.set_index("Date")


# Set input number of timestamps and training days
n_timestamp = 12
train_days = round(len(df)*0.9)  # number of days to train from
testing_days = round(len(df)*0.1) # number of days to be predicted
n_epochs = 80
filter_on = 1

## 訓練和測試資料集
train_set = df[0:train_days].reset_index(drop=True)
test_set = df[train_days: train_days+testing_days].reset_index(drop=True)
training_set = train_set.iloc[:, 1:2].values
testing_set = test_set.iloc[:, 1:2].values

## 將資料標準化，範圍是0到1
sc = StandardScaler()
training_set_scaled = sc.fit_transform(training_set)
testing_set_scaled = sc.fit_transform(testing_set)

# =============================================================================
# Split data into n_timestamp
# =============================================================================
def data_split(sequence, n_timestamp):
    X = []
    y = []
    for i in range(len(sequence)):
        end_ix = i + n_timestamp
        if end_ix > len(sequence)-1:
            break
        # i to end_ix as input
        # end_ix as target output
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


X_train, y_train = data_split(training_set_scaled, n_timestamp)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test, y_test = data_split(testing_set_scaled, n_timestamp)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

## 我們要在這裡選擇模型類型，我們要使用兩個LSTM細胞堆疊在一起的堆疊模型
model_type = 2
if model_type == 1:
    # Single cell LSTM
    model = Sequential()
    model.add(LSTM(units = 50, activation='relu',input_shape = (X_train.shape[1], 1)))
    model.add(Dense(units = 1))
if model_type == 2:
    # Stacked LSTM
    model = Sequential()
    model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
if model_type == 3:
    # Bidirectional LSTM
    model = Sequential()
    model.add(Bidirectional(LSTM(50, activation='relu'), input_shape=(X_train.shape[1], 1)))
    model.add(Dense(1))

# =============================================================================
# 模型訓練 
# =============================================================================
### 1. Adam
model.compile(optimizer = 'adam', loss = 'mean_squared_error')
Adam_history = model.fit(X_train, y_train, epochs = n_epochs, batch_size = 32)
Adam_loss = Adam_history.history['loss']
Adam_epochs = range(len(Adam_loss))
Adam_y_predicted = model.predict(X_test)

### 2. SGD
model.compile(optimizer = 'sgd', loss = 'mean_squared_error')
SGD_history = model.fit(X_train, y_train, epochs = n_epochs, batch_size = 32)
SGD_loss = SGD_history.history['loss']
SGD_epochs = range(len(SGD_loss))
SGD_y_predicted = model.predict(X_test)

### 3. RMSProp
model.compile(optimizer = 'rmsprop', loss = 'mean_squared_error')
RMSProp_history = model.fit(X_train, y_train, epochs = n_epochs, batch_size = 32)
RMSProp_loss = RMSProp_history.history['loss']
RMSProp_epochs = range(len(RMSProp_loss))
RMSProp_y_predicted = model.predict(X_test)

# =============================================================================
# 將標準化後的資料復原
# =============================================================================
def De_normalize(y_predicted):
    
    y_predicted_descaled = sc.inverse_transform(y_predicted)
    y_train_descaled = sc.inverse_transform(y_train)
    y_test_descaled = sc.inverse_transform(y_test)
    y_pred = y_predicted.ravel()
    y_pred = [round(yx, 2) for yx in y_pred]
    y_tested = y_test.ravel()
    
    mse = mean_squared_error(y_test_descaled, y_predicted_descaled)
    mae = mean_absolute_error(y_test_descaled, y_predicted_descaled)
    r2 = r2_score(y_test_descaled, y_predicted_descaled)
    print("MSE=" + str(round(mse,2)))
    print("MAE=" + str(round(mae,2)))
    print("R2=" + str(round(r2,2)))
    return round(mse,2), round(mae,2), round(r2,2), y_test_descaled, y_predicted_descaled

Adam_pred = De_normalize(Adam_y_predicted)
SGD_pred = De_normalize(SGD_y_predicted)
RMSProp_pred = De_normalize(RMSProp_y_predicted)

result = {"MSE": [Adam_pred[0], SGD_pred[0], RMSProp_pred[0]],
          "MAE": [Adam_pred[1], SGD_pred[1], RMSProp_pred[1]],
          "R2": [Adam_pred[2], SGD_pred[2], RMSProp_pred[2]]}
result_df = pd.DataFrame(result)
result_df.index = ["Adam", "SGD", "RMSprop"]
result_df


plt.figure(figsize=(8,7))

plt.subplot(3, 1, 1)
plt.plot(df['PM2.5'], color = 'black', linewidth=1, label = 'True value')
plt.ylabel("PM2.5")
plt.xlabel("time")
plt.title("All data")


plt.subplot(3, 2, 3)
plt.plot(Adam_pred[3], color = 'black', linewidth=1, label = 'True value')
plt.plot(Adam_pred[4], color = 'red',  linewidth=1, label = 'Predicted')
plt.legend(frameon=False)
plt.ylabel("PM2.5")
plt.xlabel("time")
plt.title("Predicted data (n days)")

plt.subplot(3, 2, 4)
plt.plot(Adam_pred[3][0:12], color = 'black', linewidth=1, label = 'True value')
plt.plot(Adam_pred[4][0:12], color = 'red', label = 'Predicted')
plt.legend(frameon=False)
plt.ylabel("PM2.5")
plt.xlabel("time")
plt.title("Predicted data (first 75 days)")

plt.subplot(3, 3, 7)
plt.plot(Adam_epochs, Adam_loss, color='black')
plt.ylabel("Loss (MSE)")
plt.xlabel("Epoch")
plt.title("Training curve")

plt.subplot(3, 3, 8)
plt.plot(Adam_pred[3]-Adam_pred[4], color='black')
plt.ylabel("Residual")
plt.xlabel("time")
plt.title("Residual plot")

plt.subplot(3, 3, 9)
plt.scatter(Adam_pred[3], Adam_pred[4], s=2, color='black')
plt.ylabel("Y true")
plt.xlabel("Y predicted")
plt.title("Scatter plot")

plt.subplots_adjust(hspace = 0.5, wspace=0.3)
plt.show()