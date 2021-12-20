# to_mysql
import os
import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
import json
from sqlalchemy import create_engine
import sqlalchemy

resource_id=0
# resource_id to get totol_______start
def get_totol(resource_id):
    limit=10
    url_get_totol = 'https://data.epa.gov.tw/api/3/action/datastore_search?api_key=9be7b239-557b-4c10-9775-78cadfc555e9&resource_id=' + resource_id + '&q={%22County%22:%22%E6%A1%83%E5%9C%92%E5%B8%82%22}&limit=' + str(limit)
    resp = requests.get(url_get_totol)
    soup = BeautifulSoup(resp.text, features="html.parser")
    data = json.loads(resp.text)
    totol=data['result']['total']
    return str(totol)
# resource_id to get totol_______end

def get_data_save_to_sql(date,resource_id,totle):
    engine = create_engine('mysql+pymysql://{}:{}@mqtt2.tibame.cloud/AQI_History'.format('yi','yi'))
    print(date+"..Start!")
    url_get_data = 'https://data.epa.gov.tw/api/3/action/datastore_search?api_key=9be7b239-557b-4c10-9775-78cadfc555e9&resource_id=' + resource_id + '&q={%22County%22:%22%E6%A1%83%E5%9C%92%E5%B8%82%22}&limit=' + str(totle)
    res = requests.get(url_get_data)
#     soup = BeautifulSoup(res.text, features="html.parser")
    data = json.loads(res.text)
    #轉 pandas 用 list
    json_to_pandas=[]
    for json_in in (data['result']['records']):
        #轉換格式為pandas接受格式
        json_to_pandas.append(json_in)
    # with open("test.json","w",encoding="utf-8") as f:
    #     f.write(json.dumps(json_to_pandas))
    #json轉df
    df = pd.read_json(json.dumps(json_to_pandas),encoding="utf-8-sig", orient='records')
    #排版df
    df_done=df[['DataCreationDate','County','SiteName','AQI','SO2','CO','O3','PM10','PM2.5','NO2','NOx','NO','WindSpeed','WindDirec']]
    #存到CSV
    date_change=date[0:4]+"_"+date[5:7]
    df_done.to_sql(name='AQI_hour', con=engine, if_exists = 'append', index=False)
    print(date+"..Done!")

#取得所有aqx_p_488 日期與 resource_id _____start
url = 'https://data.epa.gov.tw/dataset/aqx_p_488'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, features="html.parser")
list_date=[]
dict_resource_id={}
count_time=0
for i in soup.find_all("tr"):
    if count_time < 2 :
        count_time+=1
        pass 
    else:
        if count_time == 2 :
            day=str('2021/12')
            resource=i.find("a", href=True)['href'].split('/')[4]   
            list_date.append(day)
            dict_resource_id[day]=resource
#             print(day + '|' + resource)
            count_time+=1    
        else:
            try:
                day=i.text.replace('\n','').replace(' ','').replace('空氣品質指標(AQI)(歷史資料)(','').replace(')下載','')
                resource=i.find("a", href=True)['href'].split('/')[4]
                list_date.append(day)
                dict_resource_id[day]=resource
#                 print(day + '|' + resource)
                count_time+=1
            except:
                count_time+=1
#取得所有aqx_p_488 日期與 resource_id _____end

#設定要get到的範圍_____start
input_list=[]
start_year=2021
start_month=12
end_year=2018
end_month=1
for yearlist in range(end_year,start_year+1,1):
#     print (yearlist)
    if end_year != yearlist:
        for month in range(1,13):
            input_list.append(str(yearlist) + "/" + str(month).zfill(2))
    else:
        for month in range(end_month,13):
            input_list.append(str(yearlist) + "/" + str(month).zfill(2))
input_list[0]
#設定要get到的範圍_____end

#data_in get date
for data_in in input_list:
    #get resource_id 
    resource_id=dict_resource_id.get(data_in)
#     print(resource_id)
    totle=get_totol(resource_id)
#     print(get_totol(resource_id))
    get_data_save_to_sql(data_in,resource_id,totle)