import pandas as pd

### Taoyuan
Tao_weather = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/weather/history_Taoyuan_weather.csv")
Tao_AQI = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/history_AQI/history_Taoyuan_AQI.csv")
Tao_data = pd.merge(Tao_AQI, Tao_weather, how = "right")


### Dayuan
Da_weather = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/weather/history_Dayuan_weather.csv")
Da_AQI = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/history_AQI/history_Dayuan_AQI.csv")
Da_data = pd.merge(Da_AQI, Da_weather, how = "right")


### Guanyin
Guan_weather = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/weather/history_Guanyin_weather.csv")
Guan_AQI = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/history_AQI/history_Guanyin_AQI.csv")
Guan_data = pd.merge(Guan_AQI, Guan_weather, how = "right")


### Longtan
Long_weather = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/weather/history_Longtan_weather.csv")
Long_AQI = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/history_AQI/history_Longtan_AQI.csv")
Long_data = pd.merge(Long_AQI, Long_weather, how = "right")


### Pingzhen
Ping_weather = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/weather/history_Pingzhen_weather.csv")
Ping_AQI = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/history_AQI/history_Pingzhen_AQI.csv")
Ping_data = pd.merge(Ping_AQI, Ping_weather, how = "right")


### Zhongli
Zhong_weather = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/weather/history_Zhongli_weather.csv")
Zhong_AQI = pd.read_csv("C:/Users/user/OneDrive/桌面/Air/data/history_AQI/history_Zhongli_AQI.csv")
Zhong_data = pd.merge(Zhong_AQI, Zhong_weather, how = "right")
    
    
### Output csv file
Tao_data.to_csv("C:/Users/user/OneDrive/桌面/Air/data/Taoyuan.csv", encoding = "utf-8-sig", index = False)
Da_data.to_csv("C:/Users/user/OneDrive/桌面/Air/data/Dayuan.csv", encoding = "utf-8-sig", index = False)
Guan_data.to_csv("C:/Users/user/OneDrive/桌面/Air/data/Guanyin.csv", encoding = "utf-8-sig", index = False)
Long_data.to_csv("C:/Users/user/OneDrive/桌面/Air/data/Longtan.csv", encoding = "utf-8-sig", index = False)
Ping_data.to_csv("C:/Users/user/OneDrive/桌面/Air/data/Pingzhen.csv", encoding = "utf-8-sig", index = False)
Zhong_data.to_csv("C:/Users/user/OneDrive/桌面/Air/data/Zhongli.csv", encoding = "utf-8-sig", index = False)
