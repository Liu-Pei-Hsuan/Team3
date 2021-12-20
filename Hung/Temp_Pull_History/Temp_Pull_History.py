#write_to_mysql
import os
import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
import csv,time

# 測站編號，桃園 6 個測站編報
# Path_route='csv/data.csv'
strr="""
C0C480_%25E6%25A1%2583%25E5%259C%2592
C0C540_%25E5%25A4%25A7%25E5%259C%2592
C0C590_%25E8%25A7%2580%25E9%259F%25B3
C0C650_%25E5%25B9%25B3%25E9%258E%25AE
C0C670_%25E9%25BE%258D%25E6%25BD%25AD
C0C700_%25E4%25B8%25AD%25E5%25A3%25A2
"""

strr2="""
C0C480_桃園
C0C540_大園
C0C590_觀音
C0C650_平鎮
C0C670_龍潭
C0C700_中壢
"""

#站點 dict =>> 站碼:站名
station={}
station2={}
#站點 list =>> 站碼
twStationList = []
for strrex in strr.split('\n'):
    if strrex == "":
#         print (strrex)
        pass
    else :
        strrex.split('_')[0]
        twStationList.append(strrex.split('_')[0])
        station[strrex.split('_')[0]]=strrex.split('_')[1]
for strrex in strr2.split('\n'):
    if strrex == "":
#         print (strrex)
        pass
    else :
        strrex.split('_')[0]
        station2[strrex.split('_')[0]]=strrex.split('_')[1]


        
#從網站取的資料funtioin

def get_connect_data(url,path,daaaa,get_station_name2) : 
    res  = ss.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')    
    #value處理
    form = []
    tmp_table = soup.tbody
    tmp_table2 = tmp_table.find_all("tr")
    tmp_table3 = tmp_table2[2:]
    for value_table in tmp_table3:
        value_table = value_table.find_all("td")
        value_to_form =[]
        if value_table == []:
            pass
        else:
            value_to_form.append(get_station_name2)
            value_to_form.append(daaaa)
            for i in range(1,17):
#                 print(value_table[i])
                value_value = value_table[i]
                value_value=value_value.string.replace("\xa0","")
                if (value_value == "...") | (value_value == "&") :
                    value_value="0"
                    pass
                if value_value == "" or value_value == " ":
                    break
                else:
                    value_to_form.append(value_value)
            write_csv(value_to_form,path)        
            form.append(value_to_form)
#     print(form)    

import csv
#創建CSV
def create_csv(input_CSV,Path_route):
    path = Path_route
    with open(path, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(input_CSV)
#寫入CSV
def write_csv(input_CSV,Path_route):
    path = Path_route
    with open(path, 'a+', encoding='utf-8-sig', newline='') as csvfile:
        csv_write = csv.writer(csvfile)
        csv_write.writerow(input_CSV)        
        
# 處理年份
yearList=[]
yearList.append('2018')
yearList.append('2019')
yearList.append('2020')
yearList.append('2021')
# 處理月份
monthList = []
for i in range(1,13): 
    monthList.append(i)
    
#第一次跑
# url
urlGetCookie='https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0C630&stname=%25E5%25A4%25A7%25E6%25BA%25AA&datepicker=2021-11-27'
#偽造瀏覽器字串
user_agent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'

#字典(偽造身分文件)
# headers={
#     'User-Agent': user_agent
# }


headersstr = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cache-Control: max-age=0
Connection: keep-alive
Cookie: TS0102b38c=0107dddfeff781f8a2836307a9aa3a35964a404c6b181bcdaf9a2cceed9e7fe5290efdc18af202effca47b7d3be06f0756e7e2be0b; TS29327008027=08dc4bbcbbab200017ff46a26e99b5e9919a84771b0f4243d7c879bbe9f35a8fdaf512bfca3de6ab08c262c7e1113000c694dad8d0642e4f6f4e5ae7dceaefc67681d4d70c25cf80a0935ad6ed125bfb742466c1f8fdaf2ede188af1d2fa450c
Host: e-service.cwb.gov.tw
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"""

headers = {r.split(': ')[0]: r.split(': ')[-1] for r in headersstr.split('\n')}
#連線並取得title
ss = requests.session()
for get_station in twStationList:
    Path_route='Temp_Data/'+get_station+'_data.csv'
    res  = ss.get(urlGetCookie, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles =soup.find_all("th")[11:28]
    csvtitle=[]
    csvtitle.append("站別")
    for title in titles:
        title = title.contents  ## 利用 contents 來定位標籤內的文字
        title=title[0] #+title[2]+title[4]
        csvtitle.append(title)
#         print(title)

    create_csv(csvtitle,Path_route)
print (csvtitle)
    
#產生網址 2018-01-01 ~ 2021-12-07
for get_station in twStationList:
    #get_station => 站碼 station.get => 取的站名
    get_station_name=station.get(get_station)
    get_station_name2=station2.get(get_station)
    Path_route='Temp_Data/'+get_station+'_data.csv'
    for get_year in yearList:
        get_max_number=7*31+5*30
        get_count=0
        for get_month in monthList:
            time.sleep(5)
#             print(get_month)
            if get_month in {1,3,5,7,8,10,12,0}:
#                 print(get_month)
                for get_day in range(1,32):
                    url_Loadin='https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station={}&stname={}&datepicker={}-{}-{}'.format(get_station,get_station_name,get_year,str(get_month).zfill(2),str(get_day).zfill(2))
#                     print (url_Loadin)
                    get_count+=1
                    date_input=get_year+str(get_month).zfill(2)+str(get_day).zfill(2)
#                     print("datepicker={}-{}-{}".format(get_year,str(get_month).zfill(2),str(get_day).zfill(2)))
                    print("{}-{} =>>> {}-{}-{}".format(get_station,str((get_count/get_max_number)*100)[0:7],get_year,str(get_month).zfill(2),str(get_day).zfill(2)))
                    get_connect_data(url_Loadin,Path_route,date_input,get_station_name2)
            elif get_month in {2,4,6,9,11}:
#                 print(get_month)
                for get_day in range(1,31):
                    url_Loadin='https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station={}&stname={}&datepicker={}-{}-{}'.format(get_station,get_station_name,get_year,str(get_month).zfill(2),str(get_day).zfill(2))
#                     print (url_Loadin) 
                    get_count+=1
                    date_input=get_year+str(get_month).zfill(2)+str(get_day).zfill(2)
                    print("{}-{} =>>> {}-{}-{}".format(get_station,str((get_count/get_max_number)*100)[0:7],get_year,str(get_month).zfill(2),str(get_day).zfill(2)))
                    get_connect_data(url_Loadin,Path_route,date_input,get_station_name2)