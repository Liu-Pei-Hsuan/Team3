import pandas as pd
import pymysql

# =============================================================================
# 取得資料
# =============================================================================
def get_data(table):
    config = {"host" : "mqtt2.tibame.cloud", "port" : 3306, "user" : "hsuan",
          "passwd" : "hsuan", "db" : "prd", "charset" : "utf8mb4"}

    conn = pymysql.connect(**config) ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    
    SQL = "select * from {}".format(table)
    print('資料筆數 :',cursor.execute(SQL))
    
    results = cursor.fetchall()
    data = pd.DataFrame(results, columns = ["class", "name", "price", "image", "url"])
    
    # 關閉連線
    cursor.close()
    conn.close()
    
    return data

df = get_data("prdinfo")
df =df[df["name"].str.startswith("【")].reset_index(drop = True)

# =============================================================================
# 處理網址裡的空值問題
# =============================================================================
new_url = []
for i in df["url"]:
    url = i.replace(" ", "%20")
    new_url.append(url)
    
df["new_url"] = new_url

# =============================================================================
# # Line Bot 要呈現的商品名稱
# =============================================================================
product_name = []
for j, i in enumerate(df["name"]):
    string = i.split("】")[0]
    split_strings = string.split()
    split_strings.insert(len(split_strings), "】")
    split_strings.insert(len(split_strings) + 1, " 價格：")
    split_strings.insert(len(split_strings) + 2, "{}".format(df.price[j]))
    split_strings.insert(len(split_strings) + 3, "元")
    final_string = ''.join(split_strings)
    if "│" in final_string:
        change = list(final_string)
        change[5:10] = ""
        final_string = "".join(change)
    product_name.append(final_string)
    
df["product_name"] = product_name

# =============================================================================
# # 將所有 class 切開
# =============================================================================
### 1. 安全護目鏡
glass = df[df["class"] == "安全護目鏡"].reset_index(drop = True)

### 2. 活性碳口罩
mask = df[df["class"] == "活性碳口罩"].reset_index(drop = True)

### 3. 活性碳空氣清淨機
Air_clear = df[df["class"] == "活性碳空氣清淨機"].reset_index(drop = True)

### 4. 防毒面具 (只有一個商品)
Gas_mask = df[df["class"] == "3M 6200防毒面具"].reset_index(drop = True)

### 5. 一氧化碳偵測儀
CO_Detector = df[df["class"] == "一氧化碳偵測儀"].reset_index(drop = True)

### 6. 瓦斯警報器
Gas_alarm = df[df["class"] == "瓦斯警報器"].reset_index(drop = True)

### 7. PM2.5 空氣清淨機
PM25_clean = df[df["class"] == "PM2.5 空氣清淨機"].reset_index(drop = True)

### 8. 酒精
alcohol = df[df["class"] == "酒精"].reset_index(drop = True)

### 9. 酒精濕紙巾
alcohol_wipes = df[df["class"] == "酒精濕紙巾"].reset_index(drop = True)

### 10. 乾洗手
Dry_hands = df[df["class"] == "乾洗手"].reset_index(drop = True)

### 11. 不織布口罩
mask_il = df[df["class"] == "不織布口罩"].reset_index(drop = True)

### 12. 漂白水
bleach = df[df["class"] == "漂白水"].reset_index(drop = True)

### 13. 肥皂
soap = df[df["class"] == "肥皂"].reset_index(drop = True)
