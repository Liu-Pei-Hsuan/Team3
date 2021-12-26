from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, LocationAction, FlexSendMessage
from linebot.models import PostbackEvent, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn

import requests
import json
import configparser
import os
from urllib import parse
from urllib.parse import parse_qsl
import numpy as np
import math
from locData import *
import pandas as pd
import pymysql

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

ngrok = "https://7f53-2001-b400-e388-93f5-79fd-a9b4-341b-6193.ngrok.io/"


config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
my_line_id = config.get('line-bot', 'my_line_id')
end_point = config.get('line-bot', 'end_point')
client_id = config.get('line-bot', 'client_id')
client_secret = config.get('line-bot', 'client_secret')
HEADER = {
    'Content-type': 'application/json',    ### 告知我們的資料是以 json 形式
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'  ### 驗證機制
}

productId_region = ["5ac1bfd5040ab15980c9b435", "5ac21e6c040ab15980c9b444"]
emoji_ID_region = ["026", "130", "187", "181"]
dis = []
# =============================================================================
@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body:" + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent)
def handle_message(event):
    if event.message.type != "text":
        mtext=""
    else:
        mtext = event.message.text
    if mtext == '@請回傳您的位置':
        try:
            message = TextSendMessage(
                text='請選擇您要查看的位置',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=LocationAction(label="傳送位置"))
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)


        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
### 1. 氣象
            
    elif mtext == '@各區天氣預報':
        try:
            # message = json.load(open('C:/Users/user/OneDrive/桌面/Air/code/Line_Bot/weather.txt','r',encoding='utf-8'))
            message = weather_json
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('@各區天氣預報',message))

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
       
        
# =============================================================================
#     mtext 的部分要放位置回傳的資料         
# =============================================================================
### 2. 空氣品質

    elif  event.message.type == "location":
        try:
            Find_loc = np.matrix([[event.message.latitude, event.message.longitude]])
            # 距測站距離(全部)
            disALL = np_getDistance(loltALL_center, Find_loc)
            # 距離測站最短距離(全部)
            disMinName = nameALL[int(disALL.argmin(axis=0))]
            disMinDistance = math.floor(disALL[int(disALL.argmin(axis=0))])
            
            if disMinName == "中原大學站":
                message = [
                    TextSendMessage(text = "距離%s最近，距離 %1.1f 公里" % (disMinName, disMinDistance)),
                    TextSendMessage(text="中原大學站氣象網址")
                ]            
            
            elif disMinName == "TibaMe站":
                message = [
                    FlexSendMessage('@各區天氣預報', station(disMinName, disMinDistance)),
                    FlexSendMessage('@各區天氣預報', Air_json)
                ]
            elif disMinName == "陽明高中站":
                message = [
                    FlexSendMessage('@各區天氣預報', station(disMinName, disMinDistance)),
                    FlexSendMessage('@各區天氣預報', Air_json)
                ]
            elif disMinName == "武陵高中站":
                message = [
                    FlexSendMessage('@各區天氣預報', station(disMinName, disMinDistance)),
                    FlexSendMessage('@各區天氣預報', Air_json)
                ]
            elif disMinName == "大竹站":
                message = [
                    FlexSendMessage('@各區天氣預報', station(disMinName, disMinDistance)),
                    FlexSendMessage('@各區天氣預報', Air_json)
                ]
            elif disMinName == "桃園站":
                message = [
                    FlexSendMessage('@各區天氣預報', station(disMinName, disMinDistance)),
                    FlexSendMessage('@各區天氣預報', Air_json)
                ]
            elif disMinName == "大園站":
                message = [
                    FlexSendMessage('@各區天氣預報', station(disMinName, disMinDistance)),
                    FlexSendMessage('@各區天氣預報', Air_json)
                ]
            elif disMinName == "觀音站":
                message = [
                    FlexSendMessage('@各區天氣預報', station(disMinName, disMinDistance)),
                    FlexSendMessage('@各區天氣預報', Air_json)
                ]
            elif disMinName == "平鎮站":
                message = [
                    FlexSendMessage('@各區天氣預報', station(disMinName, disMinDistance)),
                    FlexSendMessage('@各區天氣預報', Air_json)
                ]
            elif disMinName == "龍潭站":
                message = [
                    FlexSendMessage('@各區天氣預報', station(disMinName, disMinDistance)),
                    FlexSendMessage('@各區天氣預報', Air_json)
                ]
            elif disMinName == "中壢站":
                message = [
                    FlexSendMessage('@各區天氣預報', station(disMinName, disMinDistance)),
                    FlexSendMessage('@各區天氣預報', Air_json)
                ]
            else:
                message = [
                    TextSendMessage(text = "發生錯誤")
                ]
            line_bot_api.reply_message(event.reply_token, message)
            dis.append(disMinName) #把函式內的disName存在列表裡，方便外面呼叫
        except:
            pass
        
    elif mtext == '@空氣': 
        try:
            message = [  #串列
                TextSendMessage(  #傳送文字
                    text = "距離您最近測站之空氣品質數值結果"
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = "https://img.onl/xkKwb9",
                    preview_image_url = "https://img.onl/xkKwb9"
                ),
                TemplateSendMessage(
                    alt_text='按鈕樣板',
                    template=ButtonsTemplate(
                        title='請選擇您最想了解的資訊',
                        text='請選擇：',
                        actions=[
                            MessageTemplateAction(
                                label='認識指標',
                                text='@認識空氣品質指標'
                                ),
                             MessageTemplateAction(
                                label='好物推薦',
                                text='@今日好物推薦'
                                )
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    # elif mtext == '@認識空氣品質指標':
    #     emojis_pm25 = [
    #     {"index": 0, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "016"},
    #     {"index": 1, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "013"},
    #     {"index": 2, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "054"},
    #     {"index": 3, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "094"},
    #     {"index": 4, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "057"}
    #     ]

    #     emojis_CO = [
    #     {"index": 0, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "003"},
    #     {"index": 1, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "015"},
    #     ] 
        
    #     emojis_SO2 = [
    #     {"index": 0, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "019"},
    #     {"index": 1, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "015"},
    #     {"index": 2, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "054"}
    #     ]
        
    #     emojis_O3 = [
    #     {"index": 0, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "015"},
    #     {"index": 1, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "055"}
    #     ]
        
    #     emojis_NO2 = [
    #     {"index": 0, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "014"},
    #     {"index": 1, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "015"},
    #     {"index": 2, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "054"}
    #     ]
         
    #     try:
    #         message = [
    #             TextSendMessage(
    #                 text = "$$$$$\n\n國家 PM2.5 室內標準值為 35μm (微米)，在此狀況下空氣都是乾淨無害，但高於 35μm 時，敏感族群可能會感覺到不適，超過 50μm 時，則會對所有人群健康造成不良的影響。此外，煮菜的油煙、焚香跟抽菸都會產生懸浮微粒，導致 pm2.5 升高唷！", emojis = emojis_pm25
    #         ),
    #             TextSendMessage(
    #                 text = "$$\n\n一氧化碳雖然是無色、無臭、無味氣體，但吸入對人體有十分大的傷害，與血液結合會生成碳氧血紅蛋白，導致不能提供氧氣給身體各部位。如果出現頭痛、頭暈、噁心想吐、四肢無力等症狀，應立即採取開啟對外窗戶，使室內外空氣流通，並盡速就醫。", emojis = emojis_CO
    #         ),
    #              TextSendMessage(
    #                 text = "$$$\n\n二氧化硫數值高於 5ppm 時，我們會明顯感覺到一股刺鼻的味道，當數值達到 20ppm 時會對我們的眼睛、呼吸道造成刺激性的影響，此時要盡可能避免外出，如果必須出門則需針對眼、口、鼻進行必要的防範措施，千萬不能輕忽，否則造成更嚴重的身體傷害。", emojis = emojis_SO2
    #         ),
    #               TextSendMessage(
    #                 text = "$$\n\n臭氧值大部分都會低於 120ppb，當數值接近或超過 300ppb 時，對人體就會有不良的影響，例如眼睛刺痛、肺功能降低等等。日常生活中，午後時光要特別留心臭氧的危害，通常臭氧濃度最高的時候會出現在下午 2 ～ 4 點左右，即一天之中陽光最強、溫度最高的時段，此時應避免出門，特別是秋天。", emojis = emojis_O3
    #         ),
    #                TextSendMessage(
    #                 text = "$$$\n\n二氧化氮值在 100 以下都屬於正常，但高於 100 時則容易對過敏族群造成影響，而高於 150 時會對所有人群的健康造成傷害；另外，二氧化氮會造成使支氣管疾病更加嚴重，出門時觀察一下這個指標吧！", emojis = emojis_NO2
    #         )
    #         ]
    #         line_bot_api.reply_message(event.reply_token,message)
    #     except:
    #         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    
    elif mtext == '@認識空氣品質指標':
        try:
            message = Air_var_json
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('@各區天氣預報',message))


        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    # elif mtext == '@認識空氣品質指標':
    #     try:
    #         message = [
    #             TextSendMessage(
    #                 text = "國家 PM2.5 室內標準值為 35μm (微米)，在此狀況下空氣都是乾淨無害，但高於 35μm 時，敏感族群可能會感覺到不適，超過 50μm 時，則會對所有人群健康造成不良的影響。此外，煮菜的油煙、焚香跟抽菸都會產生懸浮微粒，導致 PM2.5 升高唷！"
    #         )
    #         ]
    #         line_bot_api.reply_message(event.reply_token,message)
    #     except:
    #         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    elif mtext == '@今日好物推薦':
        try:
            message = Air_recommend
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('@今日好物推薦',message))

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))              
        
    elif mtext == "@口罩":
        try:
            message = TextSendMessage(
                text='請選擇',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="一般情況：活性碳口罩", text="@活性碳口罩")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="嚴重情況：3M 6200 防毒面具", text="@3M 6200 防毒面具")
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    
    elif mtext == '@活性碳口罩': 
        mask = get_data("mask")
        try:
            message = [
                TemplateSendMessage(
                alt_text='活性碳口罩推薦商品',
                template=ButtonsTemplate(
                    title='活性碳口罩推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(
                                  label = mask["product_name"][0],
                                  uri = mask.url[0]
                               ),
                               URITemplateAction(
                                  label = mask["product_name"][1],
                                  uri = mask.url[1]
                               ),
                               URITemplateAction(
                                  label = mask["product_name"][2],
                                  uri = mask.url[2]
                               ),
                               URITemplateAction(
                                  label = mask["product_name"][3],
                                  uri = mask.url[3]
                               )
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@活性碳空氣清淨機':
        Air_clear = get_data("Air_clean")
        try:
            message = [
                TemplateSendMessage(
                alt_text='活性碳空氣清淨機推薦商品',
                template=ButtonsTemplate(
                    title='活性碳空氣清淨機推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(
                                  label = Air_clear["product_name"][0],
                                  uri = Air_clear.url[0]
                               ),
                               URITemplateAction(
                                  label = Air_clear["product_name"][1],
                                  uri = Air_clear.url[1]
                               ),
                               URITemplateAction(
                                  label = Air_clear["product_name"][2],
                                  uri = Air_clear.url[2]
                               ),
                               URITemplateAction(
                                  label = Air_clear["product_name"][3],
                                  uri = Air_clear.url[4]
                               )
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@3M 6200 防毒面具':
        Gas_mask = get_data("Gas_mask")
        try:
            message = [
                TemplateSendMessage(
                alt_text='3M 6200 防毒面具推薦商品',
                template=ButtonsTemplate(
                    title='3M 6200 防毒面具推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(
                                  label = Gas_mask["product_name"][0],
                                  uri = Gas_mask["new_url"][0]
                               )#,
                               # URITemplateAction(
                               #    label = Gas_mask["product_name"][1],
                               #    uri = Gas_mask["new_url"][1]
                               # )
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@瓦斯警報器':
        Gas_alarm = get_data("Gas_alarm")
        try:
            message = [
                TemplateSendMessage(
                alt_text='瓦斯警報器',
                template=ButtonsTemplate(
                    title='瓦斯警報器',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(
                                  label = Gas_alarm["product_name"][0],
                                  uri = Gas_alarm.url[0]
                               ),
                               URITemplateAction(
                                  label = Gas_alarm["product_name"][1],
                                  uri = Gas_alarm.url[1]
                               ),
                               URITemplateAction(
                                  label = Gas_alarm["product_name"][2],
                                  uri = Gas_alarm.url[2]
                               ),
                               URITemplateAction(
                                  label = Gas_alarm["product_name"][3],
                                  uri = Gas_alarm.url[3]
                               )
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    # elif mtext == '@PM2.5 空氣清淨機':
    #     try:
    #         message = products("PM2.5 空氣清淨機", get_data("PM25_clean"))
    #         line_bot_api.reply_message(event.reply_token, FlexSendMessage('@PM2.5 空氣清淨機',message))

    #     except:
    #         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@PM2.5 空氣清淨機': 
        PM25_clean = get_data("PM25_clean")
        try:
            message = [
                TemplateSendMessage(
                alt_text='PM2.5 空氣清淨機',
                template=ButtonsTemplate(
                    title='PM2.5 空氣清淨機',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(
                                  label = PM25_clean["product_name"][0],
                                  uri = PM25_clean["new_url"][0]
                                ),
                                URITemplateAction(
                                    label = PM25_clean["product_name"][1],
                                    uri = PM25_clean["new_url"][1]
                                ),
                                  URITemplateAction(
                                    label = PM25_clean["product_name"][2],
                                    uri = PM25_clean["new_url"][2]
                                ),
                                  URITemplateAction(
                                    label = PM25_clean["product_name"][3],
                                    uri = PM25_clean["new_url"][3]
                                  )
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

            
    elif mtext == '@一氧化碳偵測儀': 
        CO_Detector = get_data("CO_Detector")
        try:
            message = [
                TemplateSendMessage(
                alt_text='一氧化碳偵測儀推薦商品',
                template=ButtonsTemplate(
                    title='一氧化碳偵測儀推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(
                                  label = CO_Detector["product_name"][0],
                                  uri = CO_Detector.url[0]
                               ),
                               URITemplateAction(
                                  label = CO_Detector["product_name"][1],
                                  uri = CO_Detector.url[1]
                               ),
                               URITemplateAction(
                                  label = CO_Detector["product_name"][2],
                                  uri = CO_Detector.url[2]
                               ),
                               URITemplateAction(
                                  label = CO_Detector["product_name"][3],
                                  uri = CO_Detector.url[3]
                               )
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@安全護目鏡': 
        glass = get_data("glass1")
        try:
            message = [
                TemplateSendMessage(
                alt_text='安全護目鏡推薦商品',
                template=ButtonsTemplate(
                    title='安全護目鏡推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(
                                  label = glass["product_name"][0],
                                  uri = glass.url[0]
                               ),
                               URITemplateAction(
                                  label = glass["product_name"][1],
                                  uri = glass.url[1]
                               ),
                               URITemplateAction(
                                  label = glass["product_name"][2],
                                  uri = glass.url[2]
                               ),
                               URITemplateAction(
                                  label = glass["product_name"][3],
                                  uri = glass.url[3]
                               )
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
       
# =============================================================================
### 3. 流行疾病

    elif mtext == '@請點選您要看的疾病':
        try:
            message = disease_json
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('@請點選您要看的疾病',message))

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
            
    elif mtext == 'COVID-19':
        try:
            message = FlexSendMessage('@各區天氣預報', covid19_json)
            line_bot_api.reply_message(event.reply_token, message)

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@各縣市疫情':
        try:
            message = covid19_place
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('@各縣市疫情',message))

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    
    elif mtext == '@國內疫情':
        try:
            message = [
                FlexSendMessage('@國內疫情',covid19_today)
                ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
    elif mtext == '@桃園疫情':
        try:
            message = TextSendMessage(  
                text = "今日桃園市共 __ 例，其中桃園區共 __ 例，中壢區 __ 例 ....."
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@其他縣市':
        try:
            message = covid19_county
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('@其他縣市',message))

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))               
        
    elif mtext == '@北部地區':
        lst = [0, 14, 28, 42, 56, 70, 84]
        emojis_list = list()
        for i in lst:
            emojis_list.append(
                {
                  "index": i,
                  "productId": productId_region[0],
                  "emojiId": emoji_ID_region[1]
                }
            )
        try:
            message = [  #串列
                TextSendMessage(
                    text = "$ 台北市共新增 {} 例 \n$ 新北市共新增 {} 例 \n$ 基隆市共新增 {} 例 \n$ 桃園市共新增 {} 例 \n$ 新竹市共新增 {} 例 \n$ 新竹縣共新增 {} 例 \n$ 宜蘭縣共新增 {} 例".format(0, 0, 0, 0, 0, 0, 0), emojis = emojis_list
                )
                # TextSendMessage(
                #     text = "台北市共新增 {} 例 \n新北市共新增 {} 例".format(0, 0)
                # ),
                # TextSendMessage(
                #     text = "基隆市共新增 {} 例".format(0)
                # ),
                # TextSendMessage(
                #     text = "桃園市共新增 {} 例".format(0)
                # ),
                # TextSendMessage(
                #     text = "新竹市共新增 {} 例 \n新竹縣共新增 {} 例".format(0, 0)
                # ),
                # TextSendMessage(
                #     text = "宜蘭縣共新增 {} 例".format(0)
                # )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@中部地區':
        lst = [0, 14, 28, 42, 56]
        emojis_list = list()
        for i in lst:
            emojis_list.append(
                {
                  "index": i,
                  "productId": productId_region[0],
                  "emojiId": emoji_ID_region[0]
                }
            )
        try:
            message = [  #串列
                TextSendMessage(
                    text = "$ 苗栗縣共新增 {} 例 \n$ 台中市共新增 {} 例 \n$ 彰化縣共新增 {} 例 \n$ 南投縣共新增 {} 例 \n$ 雲林縣共新增 {} 例".format(0, 0, 0, 0, 0), emojis = emojis_list
                )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

            
    elif mtext == '@南部地區':
        lst = [0, 14, 28, 42, 56, 70]
        emojis_list = list()
        for i in lst:
            emojis_list.append(
                {
                  "index": i,
                  "productId": productId_region[0],
                  "emojiId": emoji_ID_region[2]
                }
            )
        try:
            message = [  #串列
                TextSendMessage(
                    text = "$ 嘉義縣共新增 {} 例 \n$ 嘉義市共新增 {} 例 \n$ 台南市共新增 {} 例 \n$ 高雄市共新增 {} 例 \n$ 屏東縣共新增 {} 例 \n$ 澎湖縣共新增 {} 例".format(0, 0, 0, 0, 0, 0), emojis = emojis_list
                )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@東部地區':
        lst = [0, 14]
        emojis_list = list()
        for i in lst:
            emojis_list.append(
                {
                  "index": i,
                  "productId": productId_region[1],
                  "emojiId": emoji_ID_region[3]
                }
            )
        try:
            message = [  #串列
                TextSendMessage(
                    text = "$ 花蓮縣共新增 {} 例 \n$ 台東縣共新增 {} 例".format(0, 0), emojis = emojis_list
                )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '流行性感冒':
        try:
            message = influenza_json
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('流行性感冒',message))

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '腸病毒':
        try:
            message = Enterovirus_json
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('@各區天氣預報',message))

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))  
                       
    elif mtext == '@認識 COVID-19':
        try:
            message = TextSendMessage(  
                text = "COVID-19 雖然致死率不高，但傳染力極強，稍有不慎就容易感染，進而造成社會恐慌與醫療系統崩潰。在疫情尚未完全清零的情況下，在外仍須配戴好口罩、落實個人衛生保健，並配合政府防疫要求。"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@防疫商品推薦':
        try:
            message = covid19_recommend
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('@防疫商品推薦',message))

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
                 
        
    elif mtext == "@酒精類":
        try:
            message = TextSendMessage(
                text='請選擇您要查看的商品類別',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="酒精", text="@酒精")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="酒精濕紙巾", text="@酒精濕紙巾")
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@酒精': 
        alcohol = get_data("alcohol")
        try:
            message = [
                TemplateSendMessage(
                alt_text='酒精推薦商品',
                template=ButtonsTemplate(
                    title='酒精推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(label = alcohol["product_name"][0], uri = alcohol.url[0]),
                              URITemplateAction(label = alcohol["product_name"][1], uri = alcohol.url[1]),
                              URITemplateAction(label = alcohol["product_name"][2], uri = alcohol.url[2]),
                              URITemplateAction(label = alcohol["product_name"][3], uri = alcohol.url[3])
                             ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@酒精濕紙巾': 
        alcohol_wipes = get_data("alcohol_wipes")
        try:
            message = [
                TemplateSendMessage(
                alt_text='酒精濕紙巾推薦商品',
                template=ButtonsTemplate(
                    title='酒精濕紙巾推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(label = alcohol_wipes["product_name"][0], uri = alcohol_wipes.url[0]),
                              URITemplateAction(label = alcohol_wipes["product_name"][1], uri = alcohol_wipes.url[1]),
                              URITemplateAction(label = alcohol_wipes["product_name"][2], uri = alcohol_wipes.url[2]),
                              URITemplateAction(label = alcohol_wipes["product_name"][3], uri = alcohol_wipes.url[3])
                             ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@乾洗手': 
        Dry_hands = get_data("Dry_hands")
        try:
            message = [
                TemplateSendMessage(
                alt_text='乾洗手推薦商品',
                template=ButtonsTemplate(
                    title='乾洗手推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(label = Dry_hands["product_name"][1], uri = Dry_hands.url[0]),
                              URITemplateAction(label = Dry_hands["product_name"][1], uri = Dry_hands.url[1]),
                              URITemplateAction(label = Dry_hands["product_name"][2], uri = Dry_hands.url[2]),
                              URITemplateAction(label = Dry_hands["product_name"][3], uri = Dry_hands.url[3])
                             ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
            
    elif mtext == '@不織布口罩': 
        mask_il = get_data("mask_il")
        try:
            message = [
                TemplateSendMessage(
                alt_text='不織布口罩推薦商品',
                template=ButtonsTemplate(
                    title='不織布口罩推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(label = mask_il["product_name"][0], uri = mask_il.url[0]),
                              URITemplateAction(label = mask_il["product_name"][1], uri = mask_il.url[1]),
                              URITemplateAction(label = mask_il["product_name"][2], uri = mask_il.url[2]),
                              URITemplateAction(label = mask_il["product_name"][3], uri = mask_il.url[3])
                             ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@漂白水': 
        bleach = get_data("bleach")
        try:
            message = [
                TemplateSendMessage(
                alt_text='漂白水推薦商品',
                template=ButtonsTemplate(
                    title='漂白水推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(label = bleach["product_name"][0], uri = bleach.url[0]),
                              URITemplateAction(label = bleach["product_name"][1], uri = bleach.url[1]),
                              URITemplateAction(label = bleach["product_name"][2], uri = bleach.url[2]),
                              URITemplateAction(label = bleach["product_name"][3], uri = bleach.url[3])
                             ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
            
    elif mtext == '@肥皂': 
        soap = get_data("soap")
        try:
            message = [
                TemplateSendMessage(
                alt_text='肥皂推薦商品',
                template=ButtonsTemplate(
                    title='肥皂推薦商品',
                    text='請選擇：',
                    actions=[
                              URITemplateAction(label = "排名 1", uri = soap.url[0]), ### 待改
                               URITemplateAction(label = "排名 2", uri = soap.url[1]), ### 待改
                               URITemplateAction(label = "排名 3", uri = soap.url[2]), ### 待改
                               URITemplateAction(label = "排名 4", uri = soap.url[3]) ### 待改
                             ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        

# =============================================================================
### 4. 小百科

    # elif mtext == '@請點選您要看的小百科':
    #     Encyclopedia(event)
    
    elif mtext == '@請點選您要看的小百科':
        try:
            # message = json.load(open('C:/Users/user/OneDrive/桌面/Air/code/Line_Bot/weather.txt','r',encoding='utf-8'))
            message = Encyclopedia_json
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('@請點選您要看的小百科',message))


        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        

# =============================================================================
### 5. 吃飯

    elif mtext == "吃飯吃飯吃飯":
        try:
            message = TextSendMessage(  
                text = food()
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    
    elif mtext == '奕璋自我介紹':
        try:
            message = angel
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('奕璋自我介紹',message))

        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    
# =============================================================================
# function        
# =============================================================================       
        
# def covid19title():
#     url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4001&limited=TWN'
#     res = requests.get(url)
#     date = res.json()[0]['a04']
#     total = res.json()[0]['a05']
#     today = res.json()[0]['a06']
#     return f'$公告日期：{date}\n       確診人數：{today}人\n       累計確診人數：{total}人'

def covid19title():
    url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4001&limited=TWN'
    res = requests.get(url)
    date = res.json()[0]['a04']
    today = res.json()[0]['a06']
    die = res.json()[0]["a09"]
    return date, today, die
        
              
### 流感商品推薦
def influenza_Products(event):
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://img.onl/jfFt7a',
                title='流感商品推薦',
                text='請選擇：',
                actions=[
                    MessageTemplateAction(  #顯示文字計息
                        label='漂白水',
                        text='@漂白水'
                    ),
                    MessageTemplateAction(  #顯示文字計息
                        label='乾洗手',
                        text='@乾洗手'
                    ),
                    MessageTemplateAction(  #顯示文字計息
                        label='不織布口罩',
                        text='@不織布口罩'
                    ),
                    MessageTemplateAction(  #顯示文字計息
                        label='肥皂',
                        text='@肥皂'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))  
        

### 腸病毒商品推薦
def Enterovirus_Products(event):
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://img.onl/jfFt7a',
                title='腸病毒商品推薦',
                text='請選擇：',
                actions=[
                    MessageTemplateAction(  #顯示文字計息
                        label='漂白水',
                        text='@漂白水'
                    ),
                    MessageTemplateAction(  #顯示文字計息
                        label='酒精',
                        text='@酒精'
                    ),
                    MessageTemplateAction(  #顯示文字計息
                        label='不織布口罩',
                        text='@不織布口罩'
                    ),
                    MessageTemplateAction(  #顯示文字計息
                        label='肥皂',
                        text='@肥皂'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))  
        

        
def get_data(table):
    config = {"host" : "mqtt2.tibame.cloud", "port" : 3306, "user" : "hsuan",
          "passwd" : "hsuan", "db" : "prd", "charset" : "utf8mb4"}

    conn = pymysql.connect(**config) ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    
    SQL = "select * from {}".format(table)
    print('資料筆數 :',cursor.execute(SQL))
    
    results = cursor.fetchall()
    data = pd.DataFrame(results, columns = ["class", "name", "price", "image", "url", "new_url", "product_name"])
    
    # 關閉連線
    cursor.close()
    conn.close()
    
    return data
    

### 小百科 ButtonsTemplate
def Encyclopedia(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate( ## 最多 4 個按鈕
                thumbnail_image_url='https://img.onl/2Aba0o',  #顯示的圖片
                title='小百科',  #主標題
                text='請選擇您感興趣的主題：',  #副標題
                actions=[
                    URITemplateAction(  #開啟網頁
                        label='空氣品質',
                        uri='https://github.com/Liu-Pei-Hsuan/Team3/blob/main/Yi/%E5%B0%88%E9%A1%8C%E6%96%87%E7%8D%BB/%E7%A9%BA%E6%B0%A3%E5%93%81%E8%B3%AA.pdf'
                    ),
                    URITemplateAction(  #開啟網頁
                        label='流行疾病',
                        uri='https://github.com/Liu-Pei-Hsuan/Team3/blob/main/Yi/%E5%B0%88%E9%A1%8C%E6%96%87%E7%8D%BB/%E6%B5%81%E8%A1%8C%E7%96%BE%E7%97%85.pdf'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
def handle_emjoi(event):
    emoji = [
        {
            "index": 0,
            "productId": "5ac222bf031a6752fb806d64",
            "emojiId": "050"
        },
        {
            "index": 1,
            "productId": "5ac21a8c040ab15980c9b43f",
            "emojiId": "001"
        },
        {
            "index": 2,
            "productId": "5ac21a8c040ab15980c9b43f",
            "emojiId": "025"
        },
    ]         
    message=TextSendMessage(text='$$$ 09 回覆emoji訊息', emojis=emoji)

    print(event)
    line_bot_api.reply_message(event.reply_token, message)

def replyMessage(payload):
    response = requests.post('https://api.line.me/v2/bot/message/reply',headers=HEADER,data=json.dumps(payload))
    print(response.text)
    return 'OK'

def food():
    import random
    food = ["早到晚到", "孫東寶"] #"麥當勞","大四喜","素食","麻豆子","711關東煮","雙贏涼麵","早到晚到","排骨酥麵","八方雲集", "孫東寶"
    good = random.choice(food)
        
    return f'今天吃什麼：{good}'

# =============================================================================
# Flex Message JSON
# =============================================================================

weather_json = {
  "type": "bubble",
  "size": "mega",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "各區天氣預報",
            "size": "xl",
            "weight": "bold",
            "flex": 0
          },
          {
            "type": "text",
            "text": " ",
            "flex": 0
          },
          {
            "type": "icon",
            "url": "https://cdn4.iconfinder.com/data/icons/thanksgiving-2020-filled-2/64/thanksgiving-78-128.png",
            "size": "xxl",
            "offsetStart": "xs",
            "offsetTop": "sm"
          }
        ]
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "請選擇您想查看的區域",
            "margin": "md",
            "size": "sm",
            "color": "#828282"
          }
        ]
      }
    ],
    "spacing": "none",
    "borderWidth": "none",
    "paddingAll": "md",
    "paddingTop": "lg",
    "paddingStart": "lg",
    "paddingEnd": "md"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "contents": [],
        "margin": "md"
      },
      {
        "type": "text",
        "text": " ",
        "size": "5px"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "桃園區",
              "uri": "https://google.com"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4b73a5",
            "position": "relative",
            "gravity": "center",
            "flex": 8,
            "offsetBottom": "none"
          },
          {
            "type": "text",
            "text": " ",
            "flex": 1
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "中壢區",
              "uri": "https://google.com"
            },
            "style": "primary",
            "margin": "none",
            "color": "#539cd8",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          }
        ],
        "cornerRadius": "none",
        "borderWidth": "bold",
        "offsetTop": "sm",
        "paddingAll": "none",
        "spacing": "none"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "大園區",
              "uri": "https://google.com"
            },
            "style": "primary",
            "margin": "none",
            "color": "#539cd8",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          },
          {
            "type": "text",
            "text": " ",
            "flex": 1
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "觀音區",
              "uri": "https://google.com"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4b73a5",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          }
        ],
        "cornerRadius": "none",
        "borderWidth": "bold",
        "offsetTop": "md",
        "paddingAll": "none"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "龍潭區",
              "uri": "https://google.com"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4b73a5",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          },
          {
            "type": "text",
            "text": " ",
            "flex": 1
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "平鎮區",
              "uri": "https://google.com"
            },
            "style": "primary",
            "margin": "none",
            "color": "#539cd8",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          }
        ],
        "cornerRadius": "none",
        "borderWidth": "bold",
        "offsetTop": "lg",
        "paddingAll": "none",
        "spacing": "none"
      }
    ],
    "offsetBottom": "md",
    "spacing": "none"
  },
  "styles": {
    "header": {
      "backgroundColor": "#FFE4B5"
    },
    "hero": {
      "backgroundColor": "#FFE4C4"
    },
    "body": {
      "backgroundColor": "#FFF8DC"
    },
    "footer": {
      "backgroundColor": "#FFE4B5"
    }
  }
}

Air_json = {
  "type": "bubble",
  "size": "kilo",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "空氣品質相關資訊",
            "size": "xl",
            "flex": 0,
            "weight": "bold",
            "offsetStart": "md"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/world-pollution-2/512/dust-pollution-city-smoke-air-pm2.5-smog-512.png",
            "size": "3xl",
            "margin": "sm",
            "offsetTop": "xs",
            "offsetStart": "md"
          }
        ]
      }
    ]
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "空氣品質即時通",
          "uri": "https://google.com"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "認識空氣品質指標",
          "text": "@認識空氣品質指標"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "好物推薦",
          "text": "@今日好物推薦"
        }
      }
    ]
  },
  "styles": {
    "header": {
      "backgroundColor": "#66CDAA"
    },
    "hero": {
      "backgroundColor": "#FFE4B5"
    },
    "body": {
      "backgroundColor": "#E9F5DB"
    },
    "footer": {
      "backgroundColor": "#FFF8DC"
    }
  }
}

Air_var_json = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/016.png?v=1"
              },
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/013.png?v=1"
              },
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/054.png?v=1"
              },
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/094.png?v=1"
              },
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/057.png?v=1"
              }
            ]
          },
          {
            "type": "text",
            "text": " "
          },
          {
            "type": "text",
            "text": "國家 PM2.5 室內標準值為 35μm (微米)，在此狀況下空氣都是乾淨無害，但高於 35μm 時，敏感族群可能會感覺到不適，超過 50μm 時，則會對所有人群健康造成不良的影響。此外，煮菜的油煙、焚香跟抽菸都會產生懸浮微粒，導致 pm2.5 升高唷！",
            "offsetTop": "none",
            "wrap": True,
            "style": "normal",
            "size": "md",
            "align": "start"
          }
        ]
      },
      "styles": {
        "body": {
          "backgroundColor": "#B4EBCA"
        }
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/003.png?v=1"
              },
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/015.png?v=1"
              }
            ]
          },
          {
            "type": "text",
            "text": " "
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "一氧化碳雖然是無色、無臭、無味氣體，但吸入對人體有十分大的傷害，與血液結合會生成碳氧血紅蛋白，導致不能提供氧氣給身體各部位。如果出現頭痛、頭暈、噁心想吐、四肢無力等症狀，應立即採取開啟對外窗戶，使室內外空氣流通，並盡速就醫。",
                "margin": "none",
                "size": "md",
                "wrap": True
              }
            ]
          }
        ]
      },
      "styles": {
        "body": {
          "backgroundColor": "#E9F5DB"
        }
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/019.png?v=1"
              },
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/015.png?v=1"
              },
              {
                "type": "icon",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/054.png?v=1",
                "size": "3xl"
              }
            ]
          },
          {
            "type": "text",
            "text": " "
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "二氧化硫數值高於 5ppm 時，我們會明顯感覺到一股刺鼻的味道，當數值達到 20ppm 時會對我們的眼睛、呼吸道造成刺激性的影響，此時要盡可能避免外出，如果必須出門則需針對眼、口、鼻進行必要的防範措施，千萬不能輕忽，否則造成更嚴重的身體傷害",
                "margin": "none",
                "size": "md",
                "wrap": True
              }
            ]
          }
        ]
      },
      "styles": {
        "body": {
          "backgroundColor": "#B4EBCA"
        }
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/015.png?v=1"
              },
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/055.png?v=1"
              }
            ]
          },
          {
            "type": "text",
            "text": " "
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "臭氧值大部分都會低於 120ppb，當數值接近或超過 300ppb 時，對人體就會有不良的影響，例如眼睛刺痛、肺功能降低等等。日常生活中，午後時光要特別留心臭氧的危害，通常臭氧濃度最高的時候會出現在下午 2 ～ 4 點左右，即一天之中陽光最強、溫度最高的時段，此時應避免出門，特別是秋天。",
                "margin": "none",
                "size": "md",
                "wrap": True
              }
            ]
          }
        ]
      },
      "styles": {
        "body": {
          "backgroundColor": "#E9F5DB"
        }
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/014.png?v=1"
              },
              {
                "type": "icon",
                "size": "3xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/015.png?v=1"
              },
              {
                "type": "icon",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/054.png?v=1",
                "size": "3xl"
              }
            ]
          },
          {
            "type": "text",
            "text": " "
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "二氧化氮值在 100 以下都屬於正常，但高於 100 時則容易對過敏族群造成影響，而高於 150 時會對所有人群的健康造成傷害；另外，二氧化氮會造成使支氣管疾病更加嚴重，出門時觀察一下這個指標吧！",
                "margin": "none",
                "size": "md",
                "wrap": True
              }
            ]
          }
        ]
      },
      "styles": {
        "body": {
          "backgroundColor": "#B4EBCA"
        }
      }
    }
  ]
}

Air_recommend = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "kilo",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/016.png?v=1",
                "margin": "none",
                "offsetTop": "sm"
              },
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/013.png?v=1",
                "offsetTop": "sm"
              },
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/054.png?v=1",
                "offsetTop": "sm"
              },
              {
                "type": "icon",
                "size": "xl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/094.png?v=1",
                "offsetTop": "sm"
              },
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/057.png?v=1",
                "offsetTop": "sm"
              },
              {
                "type": "text",
                "text": "推薦商品",
                "size": "xl",
                "flex": 0,
                "weight": "bold"
              }
            ]
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "PM2.5 空氣清淨機",
              "text": "@PM2.5 空氣清淨機"
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "活性碳口罩",
              "text": "@活性碳口罩"
            }
          }
        ]
      },
      "styles": {
        "header": {
          "backgroundColor": "#66CDAA"
        },
        "hero": {
          "backgroundColor": "#FFE4B5"
        },
        "body": {
          "backgroundColor": "#E9F5DB"
        },
        "footer": {
          "backgroundColor": "#FFF8DC"
        }
      }
    },
    {
      "type": "bubble",
      "size": "kilo",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/003.png?v=1",
                "offsetTop": "sm",
                "margin": "none"
              },
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/015.png?v=1",
                "offsetTop": "sm",
                "margin": "none"
              },
              {
                "type": "text",
                "text": "推薦商品",
                "size": "xl",
                "flex": 0,
                "weight": "bold",
                "offsetStart": "md"
              }
            ]
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "一氧化碳偵測儀",
              "text": "@一氧化碳偵測儀"
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "瓦斯警報器",
              "text": "@瓦斯警報器"
            }
          }
        ]
      },
      "styles": {
        "header": {
          "backgroundColor": "#66CDAA"
        },
        "hero": {
          "backgroundColor": "#FFE4B5"
        },
        "body": {
          "backgroundColor": "#E9F5DB"
        },
        "footer": {
          "backgroundColor": "#FFF8DC"
        }
      }
    },
    {
      "type": "bubble",
      "size": "kilo",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/019.png?v=1",
                "offsetTop": "sm"
              },
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/015.png?v=1",
                "offsetTop": "sm"
              },
              {
                "type": "icon",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/054.png?v=1",
                "size": "xxl",
                "offsetTop": "sm"
              },
              {
                "type": "text",
                "text": "推薦商品",
                "size": "xl",
                "flex": 0,
                "weight": "bold",
                "offsetStart": "md"
              }
            ]
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "安全護目鏡",
              "text": "@安全護目鏡"
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "口罩",
              "text": "@口罩"
            }
          }
        ]
      },
      "styles": {
        "header": {
          "backgroundColor": "#66CDAA"
        },
        "hero": {
          "backgroundColor": "#FFE4B5"
        },
        "body": {
          "backgroundColor": "#E9F5DB"
        },
        "footer": {
          "backgroundColor": "#FFF8DC"
        }
      }
    },
    {
      "type": "bubble",
      "size": "kilo",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/015.png?v=1",
                "margin": "none",
                "offsetTop": "sm"
              },
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/055.png?v=1",
                "offsetTop": "sm"
              },
              {
                "type": "text",
                "text": "推薦商品",
                "size": "xl",
                "flex": 0,
                "weight": "bold"
              }
            ]
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "PM2.5 空氣清淨機",
              "text": "@PM2.5 空氣清淨機"
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "活性碳口罩",
              "text": "@活性碳口罩"
            }
          }
        ]
      },
      "styles": {
        "header": {
          "backgroundColor": "#66CDAA"
        },
        "hero": {
          "backgroundColor": "#FFE4B5"
        },
        "body": {
          "backgroundColor": "#E9F5DB"
        },
        "footer": {
          "backgroundColor": "#FFF8DC"
        }
      }
    },
    {
      "type": "bubble",
      "size": "kilo",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/014.png?v=1",
                "margin": "none",
                "offsetTop": "sm"
              },
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/015.png?v=1",
                "margin": "none",
                "offsetTop": "sm"
              },
              {
                "type": "icon",
                "size": "xxl",
                "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21a8c040ab15980c9b43f/android/054.png?v=1",
                "margin": "none",
                "offsetTop": "sm"
              },
              {
                "type": "text",
                "text": "推薦商品",
                "size": "xl",
                "flex": 0,
                "weight": "bold",
                "offsetStart": "md"
              }
            ]
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "安全護目鏡",
              "text": "@安全護目鏡"
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "口罩",
              "text": "@口罩"
            }
          }
        ]
      },
      "styles": {
        "header": {
          "backgroundColor": "#66CDAA"
        },
        "hero": {
          "backgroundColor": "#FFE4B5"
        },
        "body": {
          "backgroundColor": "#E9F5DB"
        },
        "footer": {
          "backgroundColor": "#FFF8DC"
        }
      }
    }
  ]
}

def products(prdClass, df):
    product = {
      "type": "bubble",
      "size": "kilo",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "text": prdClass,
                "size": "xl",
                "flex": 0,
                "weight": "bold",
                "offsetStart": "md"
              }
            ]
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": df["product_name"][0],
              "uri": df["new_url"][0]
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": df["product_name"][1],
              "uri": df["new_url"][1]
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": df["product_name"][2],
              "uri": df["new_url"][2]
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": df["product_name"][3],
              "uri": df["new_url"][3]
            }
          }
        ]
      },
      "styles": {
        "header": {
          "backgroundColor": "#66CDAA"
        },
        "hero": {
          "backgroundColor": "#FFE4B5"
        },
        "body": {
          "backgroundColor": "#E9F5DB"
        },
        "footer": {
          "backgroundColor": "#FFF8DC"
        }
      }
    }
    
    return product

def station(disMinName, disMinDistance):
    station = {
          "type": "bubble",
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "contents": [
                  {
                    "type": "span",
                    "text": "距離"
                  },
                  {
                    "type": "span",
                    "text": "{}".format(disMinName),
                    "color": "#4F94CD",
                    "weight": "bold",
                    "size": "lg"
                  },
                  {
                    "type": "span",
                    "text": "最近，距離 "
                  },
                  {
                    "type": "span",
                    "text": "{}".format(disMinDistance),
                    "weight": "bold"
                  },
                  {
                    "type": "span",
                    "text": " 公里，接著將為您提供最近測站相關資訊"
                  }
                ],
                "wrap": True
              }
            ]
          },
          "styles": {
            "body": {
              "backgroundColor": "#FFF8DC"
            }
          }
        }
    return station

def product_json():
    product_json = {
          "type": "bubble",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "PM2.5 空氣清淨機",
                "size": "xl",
                "offsetTop": "none",
                "offsetStart": "none",
                "offsetEnd": "none",
                "margin": "none",
                "weight": "bold",
                "offsetBottom": "none"
              }
            ],
            "borderWidth": "none",
            "paddingEnd": "none",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#A2CD5A",
              "endColor": "#ffffff"
            },
            "height": "60px",
            "margin": "none",
            "spacing": "none"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "product[new_url][0]",
                  "uri": "https:/google.com"
                },
                "margin": "none",
                "style": "link"
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "uri": "https:/google.com",
                  "label": "product[\"new_url\"][1]"
                }
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "uri": "https:/google.com",
                  "label": "product[\"new_url\"][2]"
                }
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "uri": "https:/google.com",
                  "label": "product[\"new_url\"][3]"
                }
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "uri": "https:/google.com",
                  "label": "product[\"new_url\"][4]"
                }
              }
            ],
            "spacing": "none",
            "margin": "none"
          }
        }
    return product_json

covid19_json = {
  "type": "bubble",
  "size": "giga",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "COVID-19 趨勢圖",
        "size": "xl",
        "weight": "bold"
      }
    ],
    "spacing": "none",
    "borderWidth": "none",
    "paddingAll": "md",
    "paddingTop": "lg",
    "paddingStart": "lg",
    "paddingEnd": "md"
  },
  "hero": {
    "type": "image",
    "url": "https://img.onl/lIcW63",
    "size": "full",
    "aspectMode": "fit",
    "aspectRatio": "18:11"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "COVID-19 簡介：",
        "weight": "bold",
        "style": "italic",
        "decoration": "underline",
        "color": "#104E8B",
        "size": "lg"
      },
      {
        "type": "text",
        "text": " ",
        "size": "5px"
      },
      {
        "type": "text",
        "text": "COVID-19 雖然致死率不高，但傳染力極強，稍有不慎就容易感染，進而造成社會恐慌與醫療系統崩潰。在疫情尚未完全清零的情況下，在外仍須配戴好口罩、落實個人衛生保健，並配合政府防疫要求。",
        "wrap": True
      },
      {
        "type": "text",
        "text": " ",
        "size": "12px"
      },
      {
        "type": "text",
        "text": "更多資訊：",
        "color": "#104E8B",
        "size": "lg",
        "weight": "bold",
        "style": "italic",
        "decoration": "underline"
      },
      {
        "type": "text",
        "text": " ",
        "size": "10px"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "防疫商品推薦",
          "text": "@防疫商品推薦"
        },
        "style": "primary",
        "color": "#4F94CD"
      },
      {
        "type": "separator",
        "margin": "md",
        "color": "#E2EBFD"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "各縣市疫情狀況",
          "text": "@各縣市疫情"
        },
        "color": "#4F94CD",
        "style": "primary"
      }
    ]
  },
  "styles": {
    "header": {
      "backgroundColor": "#A4D3EE"
    },
    "hero": {
      "backgroundColor": "#A4D3EE"
    },
    "body": {
      "backgroundColor": "#A4D3EE"
    },
    "footer": {
      "backgroundColor": "#FFE4B5"
    }
  }
}

covid19_recommend = {
  "type": "bubble",
  "size": "kilo",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "防疫商品推薦",
            "size": "xl",
            "margin": "30px",
            "flex": 0,
            "weight": "bold"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/social-media-1-filled-outline-77-background/468/Layer4-512.png",
            "size": "3xl",
            "margin": "md",
            "offsetTop": "sm"
          }
        ]
      }
    ],
    "margin": "none"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "1px",
    "contents": [
      {
        "type": "button",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "酒精類",
          "text": "@酒精類"
        },
        "color": "#27408B",
        "margin": "none",
        "gravity": "center"
      },
      {
        "type": "button",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "乾洗手",
          "text": "@乾洗手"
        },
        "color": "#27408B"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "不織布口罩",
          "text": "@不織布口罩"
        },
        "color": "#27408B"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "安全護目鏡",
          "text": "@安全護目鏡"
        },
        "color": "#27408B"
      }
    ],
    "flex": 0,
    "margin": "none",
    "borderWidth": "none",
    "cornerRadius": "none",
    "alignItems": "center",
    "justifyContent": "space-around"
  },
  "styles": {
    "body": {
      "backgroundColor": "#7FA5F8"
    },
    "footer": {
      "backgroundColor": "#E2EBFD"
    }
  }
}

covid19_place = {
  "type": "bubble",
  "size": "kilo",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "選擇您想查看的地點",
            "size": "19px",
            "flex": 0,
            "weight": "bold"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/search-engine-optimisation-seo/44/seo_icons-26-512.png",
            "size": "3xl",
            "margin": "sm",
            "offsetTop": "sm"
          }
        ]
      }
    ],
    "margin": "none"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "1px",
    "contents": [
      {
        "type": "button",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "全台",
          "text": "@國內疫情"
        },
        "color": "#27408B",
        "margin": "none",
        "gravity": "center"
      },
      {
        "type": "button",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "桃園",
          "text": "@桃園疫情"
        },
        "color": "#27408B"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "其他縣市",
          "text": "@其他縣市"
        },
        "color": "#27408B"
      }
    ],
    "flex": 0,
    "margin": "none",
    "borderWidth": "none",
    "cornerRadius": "none",
    "alignItems": "center",
    "justifyContent": "space-around"
  },
  "styles": {
    "body": {
      "backgroundColor": "#7FA5F8"
    },
    "footer": {
      "backgroundColor": "#E2EBFD"
    }
  }
}

covid19_county = {
  "type": "bubble",
  "size": "kilo",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "各地區疫情現況",
            "size": "19px",
            "flex": 0,
            "weight": "bold"
          },
          {
            "type": "icon",
            "url": "https://cdn2.iconfinder.com/data/icons/coronavirus-77/512/coronavirus-covid-12-512.png",
            "size": "3xl",
            "margin": "sm",
            "offsetTop": "sm"
          }
        ]
      }
    ],
    "margin": "none"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "1px",
    "contents": [
      {
        "type": "button",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "北部地區",
          "text": "@北部地區"
        },
        "color": "#27408B",
        "margin": "none",
        "gravity": "center"
      },
      {
        "type": "button",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "中部地區",
          "text": "@中部地區"
        },
        "color": "#27408B"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "南部地區",
          "text": "@南部地區"
        },
        "color": "#27408B"
      },
      {
        "type": "button",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "東部地區",
          "text": "@東部地區"
        },
        "color": "#27408B",
        "margin": "none",
        "gravity": "center"
      }
    ],
    "flex": 0,
    "margin": "none",
    "borderWidth": "none",
    "cornerRadius": "none",
    "alignItems": "center",
    "justifyContent": "space-around"
  },
  "styles": {
    "body": {
      "backgroundColor": "#7FA5F8"
    },
    "footer": {
      "backgroundColor": "#E2EBFD"
    }
  }
}

announcement = {
  "type": "bubble",
  "size": "mega",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "3xl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "3xl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "3xl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "3xl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "3xl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "3xl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "3xl"
          }
        ]
      }
    ]
  },
  "styles": {
    "body": {
      "backgroundColor": "#A4D3EE"
    }
  }
}

covid19_today = {
  "type": "bubble",
  "size": "mega",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "xxl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "xxl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "xxl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "xxl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "xxl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "xxl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "xxl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "xxl"
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/borrow-book-filled-outline/340/announcement_message_megaphone_speech_advertisement_communication_announce-512.png",
            "size": "xxl"
          }
        ]
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21ae3040ab15980c9b440/android/136.png?v=1",
            "offsetTop": "sm",
            "size": "xl"
          },
          {
            "type": "text",
            "text": "日期：{}".format(covid19title()[0])
          }
        ]
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21ae3040ab15980c9b440/android/136.png?v=1",
            "offsetTop": "sm",
            "size": "xl"
          },
          {
            "type": "text",
            "text": "確診人數：{}".format(covid19title()[1])
          }
        ]
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://stickershop.line-scdn.net/sticonshop/v1/sticon/5ac21ae3040ab15980c9b440/android/136.png?v=1",
            "offsetTop": "sm",
            "size": "xl"
          },
          {
            "type": "text",
            "text": "新增死亡人數：{}".format(covid19title()[2])
          }
        ]
      }
    ],
    "height": "130px",
    "offsetBottom": "md"
  },
  "styles": {
    "body": {
      "backgroundColor": "#A4D3EE"
    }
  }
}

influenza_json = {
  "type": "bubble",
  "size": "giga",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "流行性感冒趨勢圖",
        "size": "xl",
        "weight": "bold"
      }
    ],
    "spacing": "none",
    "borderWidth": "none",
    "paddingAll": "md",
    "paddingTop": "lg",
    "paddingStart": "lg",
    "paddingEnd": "md"
  },
  "hero": {
    "type": "image",
    "url": "https://img.onl/jQt3oE",
    "size": "full",
    "aspectMode": "fit",
    "aspectRatio": "18:11"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "什麼是流行性感冒：",
        "weight": "bold",
        "style": "italic",
        "decoration": "underline",
        "color": "#104E8B",
        "size": "lg"
      },
      {
        "type": "text",
        "text": " ",
        "size": "5px"
      },
      {
        "type": "text",
        "text": "國人常常混肴流行性感冒與一般感冒，雖然症狀雷同，但是傳染力更病情的嚴重程度並不是同一個等級。如果你有喉嚨痛、肌肉酸痛、身體乏力的症狀，千萬不要諱疾忌醫，給醫生專業診斷，保護自己也能守護周遭的親朋好友。",
        "wrap": True
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "流行性感冒推薦商品：",
            "color": "#104E8B",
            "size": "lg",
            "weight": "bold",
            "style": "italic",
            "decoration": "underline",
            "margin": "none",
            "position": "relative",
            "offsetEnd": "none",
            "flex": 0
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/social-media-1-filled-outline-77-background/468/Layer4-512.png",
            "margin": "md",
            "size": "3xl",
            "offsetTop": "2px"
          }
        ],
        "margin": "md"
      },
      {
        "type": "text",
        "text": " ",
        "size": "5px"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "漂白水",
              "text": "@漂白水"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4F94CD",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          },
          {
            "type": "text",
            "text": " ",
            "flex": 1
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "乾洗手",
              "text": "@乾洗手"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4F94CD",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          }
        ],
        "cornerRadius": "none",
        "borderWidth": "bold",
        "offsetTop": "sm",
        "paddingAll": "none",
        "spacing": "none"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "肥皂",
              "text": "@肥皂"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4F94CD",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          },
          {
            "type": "text",
            "text": " ",
            "flex": 1
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "不織布口罩",
              "text": "@不織布口罩"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4F94CD",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          }
        ],
        "cornerRadius": "none",
        "borderWidth": "bold",
        "offsetTop": "sm",
        "paddingAll": "none"
      }
    ]
  },
  "styles": {
    "header": {
      "backgroundColor": "#A4D3EE"
    },
    "hero": {
      "backgroundColor": "#A4D3EE"
    },
    "body": {
      "backgroundColor": "#A4D3EE"
    },
    "footer": {
      "backgroundColor": "#FFE4B5"
    }
  }
}

### 腸病毒
Enterovirus_json = {
  "type": "bubble",
  "size": "giga",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "腸病毒趨勢圖",
        "size": "xl",
        "weight": "bold"
      }
    ],
    "spacing": "none",
    "borderWidth": "none",
    "paddingAll": "md",
    "paddingTop": "lg",
    "paddingStart": "lg",
    "paddingEnd": "md"
  },
  "hero": {
    "type": "image",
    "url": "https://img.onl/bUt2N",
    "size": "full",
    "aspectMode": "fit",
    "aspectRatio": "18:11"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "什麼是腸病毒：",
        "weight": "bold",
        "style": "italic",
        "decoration": "underline",
        "color": "#104E8B",
        "size": "lg"
      },
      {
        "type": "text",
        "text": " ",
        "size": "5px"
      },
      {
        "type": "text",
        "text": "腸病毒雖好發在小朋友身上，但是大人也不得輕忽，病毒種類繁多，對身體造成的健康影響不容小覷。最好的防範就是落實個人衛生保健，勤洗手、不要隨處觸碰眼、口、鼻，這樣才能有效遏止唷！",
        "wrap": True
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "腸病毒推薦商品：",
            "color": "#104E8B",
            "size": "lg",
            "weight": "bold",
            "style": "italic",
            "decoration": "underline",
            "margin": "none",
            "position": "relative",
            "offsetEnd": "none",
            "flex": 0
          },
          {
            "type": "icon",
            "url": "https://cdn1.iconfinder.com/data/icons/social-media-1-filled-outline-77-background/468/Layer4-512.png",
            "margin": "md",
            "size": "3xl",
            "offsetTop": "2px"
          }
        ],
        "margin": "md"
      },
      {
        "type": "text",
        "text": " ",
        "size": "5px"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "肥皂",
              "text": "@肥皂"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4F94CD",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          },
          {
            "type": "text",
            "text": " ",
            "flex": 1
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "酒精",
              "text": "@酒精"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4F94CD",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          }
        ],
        "cornerRadius": "none",
        "borderWidth": "bold",
        "offsetTop": "sm",
        "paddingAll": "none",
        "spacing": "none"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "漂白水",
              "text": "@漂白水"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4F94CD",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          },
          {
            "type": "text",
            "text": " ",
            "flex": 1
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "不織布口罩",
              "text": "@不織布口罩"
            },
            "style": "primary",
            "margin": "none",
            "color": "#4F94CD",
            "position": "relative",
            "gravity": "center",
            "flex": 8
          }
        ],
        "cornerRadius": "none",
        "borderWidth": "bold",
        "offsetTop": "sm",
        "paddingAll": "none"
      }
    ]
  },
  "styles": {
    "header": {
      "backgroundColor": "#A4D3EE"
    },
    "hero": {
      "backgroundColor": "#A4D3EE"
    },
    "body": {
      "backgroundColor": "#A4D3EE"
    },
    "footer": {
      "backgroundColor": "#FFE4B5"
    }
  }
}

### 小百科
Encyclopedia_json = {
  "type": "bubble",
  "size": "kilo",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "小百科",
            "weight": "bold",
            "size": "xl",
            "flex": 0,
            "offsetStart": "none",
            "margin": "70px",
            "offsetBottom": "none",
            "gravity": "center"
          },
          {
            "type": "icon",
            "url": "https://cdn2.iconfinder.com/data/icons/education-and-knowledge-4-1/128/173-128.png",
            "size": "3xl",
            "offsetStart": "md",
            "offsetTop": "sm"
          }
        ]
      }
    ],
    "margin": "none",
    "spacing": "none",
    "paddingTop": "md",
    "paddingBottom": "sm"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "空氣品質",
          "uri": "https://github.com/Liu-Pei-Hsuan/Team3/blob/main/Yi/%E5%B0%88%E9%A1%8C%E6%96%87%E7%8D%BB/%E7%A9%BA%E6%B0%A3%E5%93%81%E8%B3%AA.pdf"
        },
        "flex": 0,
        "style": "secondary",
        "color": "#66CDAA"
      },
      {
        "type": "separator",
        "margin": "md"
      },
      {
        "type": "button",
        "style": "secondary",
        "action": {
          "type": "uri",
          "label": "流行疾病",
          "uri": "https://github.com/Liu-Pei-Hsuan/Team3/blob/main/Yi/%E5%B0%88%E9%A1%8C%E6%96%87%E7%8D%BB/%E6%B5%81%E8%A1%8C%E7%96%BE%E7%97%85.pdf"
        },
        "color": "#7AC5CD"
      }
    ],
    "flex": 0
  },
  "styles": {
    "header": {
      "backgroundColor": "#FFE4B5"
    },
    "body": {
      "backgroundColor": "#FFF8DC"
    }
  }
}

disease_json = {
  "type": "bubble",
  "size": "kilo",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "請選擇您最關心的疾病",
            "size": "lg",
            "flex": 0,
            "weight": "bold"
          },
          {
            "type": "icon",
            "url": "https://cdn0.iconfinder.com/data/icons/coronavirus-33/512/cough-virus-flu-sick-coronavirus-512.png",
            "size": "3xl",
            "margin": "none",
            "offsetTop": "xs",
            "offsetStart": "md"
          }
        ]
      }
    ]
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "COVID-19",
          "text": "COVID-19"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "流行性感冒",
          "text": "流行性感冒"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "腸病毒",
          "text": "腸病毒"
        }
      }
    ]
  },
  "styles": {
    "header": {
      "backgroundColor": "#7FA5F8"
    },
    "hero": {
      "backgroundColor": "#FFE4B5"
    },
    "body": {
      "backgroundColor": "#E2EBFD"
    },
    "footer": {
      "backgroundColor": "#FFF8DC"
    }
  }
}

angel = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "哈囉大家好！",
        "weight": "bold",
        "size": "md",
        "wrap": True
      },
      {
        "type": "text",
        "text": "我是奕璋，綽號是火星仙子",
        "weight": "bold",
        "size": "md",
        "wrap": True
      },
      {
        "type": "image",
        "url": "https://upload.wikimedia.org/wikipedia/zh/thumb/2/2f/SailorMoon_mars.jpg/220px-SailorMoon_mars.jpg",
        "margin": "md",
        "size": "full"
      }
    ]
  }
}



if __name__ == "__main__":
    app.debug = True
    app.run()
