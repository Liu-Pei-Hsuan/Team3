import requests
import time
from bs4 import BeautifulSoup
import pymysql
import pandas as pd

searchPrd_list = ['漂白水', '瓦斯警報器', '一氧化碳偵測儀', '3M 6200防毒面具', '酒精濕紙巾', '乾洗手', '活性碳口罩', '不織布口罩', '活性碳空氣清淨機', 'PM2.5 空氣清淨機',
                  '酒精', '肥皂', '安全護目鏡']
prdData = []
for searchPrd in searchPrd_list:
    url = f" https://m.momoshop.com.tw/search.momo?searchKeyword={searchPrd}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    print(f'=====  Search satr {searchPrd}  =====')
    for prd in soup.select('.goodsItemLi'):
        prdClass = str(searchPrd)
        prdName = prd.select_one('.prdName').text.strip()
        prdPrice = prd.select_one('.price').text
        prdImg = prd.select_one('.goodsImg')['src']
        prdUrl = 'https://m.momoshop.com.tw/' + prd.select_one('a')['href']
        prd2tuple = [prdClass, prdName, prdPrice, prdImg, prdUrl]
        prdData.append(prd2tuple)
        print(f'類別:{searchPrd}')
        print(prdName)
        print(prdPrice)
        print(prdImg)
        print(prdUrl)
        print('-' * 100)
    time.sleep(2)
prdData.pop(0)

df = pd.DataFrame(prdData, columns = ["class", "name", "price", "image", "url"])
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
    # split_strings.insert(len(split_strings) + 1, " 價格：")
    split_strings.insert(len(split_strings) + 1, "{}".format(df.price[j]))
    split_strings.insert(len(split_strings) + 2, "元")
    final_string = ''.join(split_strings)
    
    # if "│" in final_string:
    #     change = list(final_string)
    #     change[5:10] = ""
    #     final_string = "".join(change)
        
    # elif "’" in final_string:
    #     final_string = final_string.replace("Dr.Bronner’s", "")

    product_name.append(final_string)
  
df["product_name"] = product_name



from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format('hsuan', 'hsuan', 'mqtt2.tibame.cloud:3306', 'prd','utf8mb4'))
con = engine.connect()#建立連線
df.to_sql(name='product', con=con, if_exists='replace', index=False)
con.close()
