from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, LocationAction
from linebot.models import PostbackEvent, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn

import requests
import json
import configparser
import os
from urllib import parse
from urllib.parse import parse_qsl

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

ngrok = "https://4a65-36-228-193-220.ngrok.io/"


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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
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

# =============================================================================
#     mtext 的部分要放位置回傳的資料         
# =============================================================================
### 1. 氣象
    elif mtext == '@氣象':
        try:
            message = TextSendMessage(  
                text = "https://5zrbk.csb.app/"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    
# =============================================================================
#     mtext 的部分要放位置回傳的資料         
# =============================================================================
### 2. 空氣品質
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
            
    elif mtext == '@認識空氣品質指標':
        emojis_pm25 = [
        {"index": 0, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "016"},
        {"index": 1, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "013"},
        {"index": 2, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "054"},
        {"index": 3, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "094"},
        {"index": 4, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "057"}
        ]

        emojis_CO = [
        {"index": 0, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "003"},
        {"index": 1, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "015"},
        ] 
        
        emojis_SO2 = [
        {"index": 0, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "019"},
        {"index": 1, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "015"},
        {"index": 2, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "054"}
        ]
        
        emojis_O3 = [
        {"index": 0, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "015"},
        {"index": 1, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "055"}
        ]
        
        emojis_NO2 = [
        {"index": 0, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "014"},
        {"index": 1, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "015"},
        {"index": 2, "productId": "5ac21a8c040ab15980c9b43f", "emojiId": "054"}
        ]
         
        try:
            message = [
                TextSendMessage(
                    text = "$$$$$\n\n國家 PM2.5 室內標準值為 35μm (微米)，在此狀況下空氣都是乾淨無害，但高於 35μm 時，敏感族群可能會感覺到不適，超過 50μm 時，則會對所有人群健康造成不良的影響。此外，煮菜的油煙、焚香跟抽菸都會產生懸浮微粒，導致 pm2.5 升高唷！", emojis = emojis_pm25
            ),
                TextSendMessage(
                    text = "$$\n\n一氧化碳雖然是無色、無臭、無味氣體，但吸入對人體有十分大的傷害，與血液結合會生成碳氧血紅蛋白，導致不能提供氧氣給身體各部位。如果出現頭痛、頭暈、噁心想吐、四肢無力等症狀，應立即採取開啟對外窗戶，使室內外空氣流通，並盡速就醫。", emojis = emojis_CO
            ),
                 TextSendMessage(
                    text = "$$$\n\n二氧化硫數值高於 5ppm 時，我們會明顯感覺到一股刺鼻的味道，當數值達到 20ppm 時會對我們的眼睛、呼吸道造成刺激性的影響，此時要盡可能避免外出，如果必須出門則需針對眼、口、鼻進行必要的防範措施，千萬不能輕忽，否則造成更嚴重的身體傷害。", emojis = emojis_SO2
            ),
                  TextSendMessage(
                    text = "$$\n\n臭氧值大部分都會低於 120ppb，當數值接近或超過 300ppb 時，對人體就會有不良的影響，例如眼睛刺痛、肺功能降低等等。日常生活中，午後時光要特別留心臭氧的危害，通常臭氧濃度最高的時候會出現在下午 2 ～ 4 點左右，即一天之中陽光最強、溫度最高的時段，此時應避免出門，特別是秋天。", emojis = emojis_O3
            ),
                   TextSendMessage(
                    text = "$$$\n\n二氧化氮值在 100 以下都屬於正常，但高於 100 時則容易對過敏族群造成影響，而高於 150 時會對所有人群的健康造成傷害；另外，二氧化氮會造成使支氣管疾病更加嚴重，出門時觀察一下這個指標吧！", emojis = emojis_NO2
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
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
        Products_Featured(event)   
        
    elif mtext == "@口罩":
        try:
            message = TextSendMessage(
                text='請選擇您要查看的位置',
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
        mask = product()[1]
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
        Air_clear = product()[2]
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
                                  label = Air_clear["product_name"][4],
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
        Gas_mask = product()[3]
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
                               ),
                               URITemplateAction(
                                  label = Gas_mask["product_name"][1],
                                  uri = Gas_mask["new_url"][1]
                               )
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@瓦斯警報器':
        Gas_alarm = product()[5]
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
            
    elif mtext == '@PM2.5 空氣清淨機': 
        PM25_clean = product()[6]
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
        CO_Detector = product()[4]
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
        glass = product()[0]
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
            message =  TemplateSendMessage(
                alt_text='請選擇您最關心的疾病',
                template=ButtonsTemplate(
                    title='請選擇您最關心的疾病',
                    text='請選擇：',
                    actions=[
                        MessageTemplateAction(label="COVID-19", text="COVID-19"),
                        MessageTemplateAction(label="流感", text="流感"),
                        MessageTemplateAction(label="腸病毒", text="腸病毒")
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
            
    elif mtext == 'COVID-19': 
        try:
            message = [  #串列
                TextSendMessage(  #傳送文字
                    text = "COVID-19 趨勢圖"
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = "https://img.onl/lIcW63",
                    preview_image_url = "https://img.onl/lIcW63"
                ),
                TextSendMessage(
                text='請選擇您最想了解的資訊',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="認識 COVID-19", text="@認識 COVID-19")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="防疫商品推薦", text="@防疫商品推薦")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="各縣市疫情狀況", text="@各縣市疫情")
                        ),
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@各縣市疫情': 
        try:
            message = [
                TemplateSendMessage(
                alt_text='請選擇您最想查詢的地點',
                template=ButtonsTemplate(
                    title='請選擇您最想查詢的地點',
                    text='請選擇：',
                    actions=[
                        MessageTemplateAction(label="全台", text="@國內疫情"),
                        MessageTemplateAction(label="桃園", text="@桃園疫情"),
                        MessageTemplateAction(label="其他縣市", text="@其他縣市")
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    
    elif mtext == '@國內疫情':
        try:
            message = TextSendMessage(  
                text = "今日共新增 {} 例，其中本土共 {} 例，境外共 {} 例".format(0, 0, 0)
            )
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
            
            
    elif mtext == "@其他縣市":
        COVID_19_num(event)       
        
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
            
   
            
    elif mtext == '流感': 
        try:
            message = [  #串列
                TextSendMessage(  #傳送文字
                    text = "流行性感冒趨勢圖"
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = "https://img.onl/7ro5BO",
                    preview_image_url = "https://img.onl/7ro5BO"
                ),
                TextSendMessage(
                text='請選擇您最想了解的資訊',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="什麼是流感", text="@什麼是流感")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="流感商品推薦", text="@流感商品推薦")
                        ),
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
            
    elif mtext == '腸病毒': 
        try:
            message = [  #串列
                TextSendMessage(  #傳送文字
                    text = "腸病毒趨勢圖"
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = "https://img.onl/ZcJDSA",
                    preview_image_url = "https://img.onl/ZcJDSA"
                ),
                TextSendMessage(
                text='請選擇您最想了解的資訊',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="什麼是腸病毒", text="@什麼是腸病毒")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="腸病毒商品推薦", text="@腸病毒商品推薦")
                        ),
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
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
        COVID_19_Products(event)
        
    elif mtext == '@什麼是流感':
        try:
            message = TextSendMessage(  
                text = "國人常常混肴流行性感冒與一般感冒，雖然症狀雷同，但是傳染力更病情的嚴重程度並不是同一個等級。如果你有喉嚨痛、肌肉酸痛、身體乏力的症狀，千萬不要諱疾忌醫，給醫生專業診斷，保護自己也能守護周遭的親朋好友。"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@流感商品推薦':
        influenza_Products(event)
        
    elif mtext == '@什麼是腸病毒':
        try:
            message = TextSendMessage(  
                text = "腸病毒雖好發在小朋友身上，但是大人也不得輕忽，病毒種類繁多，對身體造成的健康影響不容小覷。最好的防範就是落實個人衛生保健，勤洗手、不要隨處觸碰眼、口、鼻，這樣才能有效遏止唷！"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
      
        
    elif mtext == "@腸病毒商品推薦":
        Enterovirus_Products(event)
        

# =============================================================================
### 4. 小百科

    elif mtext == '@請點選您要看的小百科':
        Encyclopedia(event)

    
            
### COVID-19 商品推薦
def COVID_19_Products(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            ## 最多 4 個按鈕
            template=ButtonsTemplate(
                thumbnail_image_url='https://img.onl/jfFt7a',  #顯示的圖片
                title='防疫商品推薦',  #主標題
                text='請選擇：',  #副標題
                actions=[
                    URITemplateAction(  #開啟網頁
                        label='【快潔適★買1送1】 99 元', #字數上限 20 字
                        uri='http://www.e-happy.com.tw'
                    ),
                    URITemplateAction(
                        label='推薦 2',
                        uri='http://www.e-happy.com.tw'
                    ),
                    URITemplateAction(
                        label='推薦 3',
                        uri='http://www.e-happy.com.tw'
                    ),
                    URITemplateAction(
                        label='推薦 4',
                        uri='http://www.e-happy.com.tw'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
### 各縣市 COVID-19 確診人數
def COVID_19_num(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='各縣市疫情現況',
            ## 最多 4 個按鈕
            template=ButtonsTemplate(
                thumbnail_image_url='https://img.onl/jfFt7a',  #顯示的圖片
                title='各縣市疫情現況',  #主標題
                text='請選擇：',  #副標題
                actions=[
                    MessageTemplateAction(  #顯示文字計息
                        label='北部地區',
                        text='@北部地區'
                    ),
                    MessageTemplateAction(  #顯示文字計息
                        label='中部地區',
                        text='@中部地區'
                    ),
                    MessageTemplateAction(  #顯示文字計息
                        label='南部地區',
                        text='@南部地區'
                    ),
                    MessageTemplateAction(  #顯示文字計息
                        label='東部地區',
                        text='@東部地區'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
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
                    URITemplateAction(
                        label='推薦 1',
                        uri='http://www.e-happy.com.tw'
                    ),
                    URITemplateAction(
                        label='推薦 2',
                        uri='http://www.e-happy.com.tw'
                    ),
                    URITemplateAction(
                        label='推薦 3',
                        uri='http://www.e-happy.com.tw'
                    ),
                    URITemplateAction(
                        label='推薦 4',
                        uri='http://www.e-happy.com.tw'
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
                    URITemplateAction(
                        label='推薦 1',
                        uri='http://www.e-happy.com.tw'
                    ),
                    URITemplateAction(
                        label='推薦 2',
                        uri='http://www.e-happy.com.tw'
                    ),
                    URITemplateAction(
                        label='推薦 3',
                        uri='http://www.e-happy.com.tw'
                    ),
                    URITemplateAction(
                        label='推薦 4',
                        uri='http://www.e-happy.com.tw'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))  
        
  
### 空氣品質好物推薦        
def Products_Featured(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='PM2.5 推薦商品',
                        text='請選擇品項',
                        actions=[
                            MessageTemplateAction(
                                label='PM2.5 空氣清淨機',
                                text='@PM2.5 空氣清淨機'
                            ),
                            MessageTemplateAction(
                                label='活性碳口罩',
                                text='@活性碳口罩'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='CO 推薦商品',
                        text='請選擇品項',
                        actions=[
                            MessageTemplateAction(
                                label='一氧化碳偵測儀',
                                text='@一氧化碳偵測儀'
                            ),
                            MessageTemplateAction(
                                label='瓦斯警報器',
                                text='@瓦斯警報器'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='SO2 推薦商品',
                        text='請選擇品項',
                        actions=[
                             MessageTemplateAction(
                                label='安全護目鏡',
                                text='@安全護目鏡'
                            ),
                            MessageTemplateAction(
                                label='口罩',
                                text='@口罩'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='O3 推薦商品',
                        text='請選擇品項',
                        actions=[
                            MessageTemplateAction(
                                label='活性碳口罩',
                                text='@活性碳口罩'
                            ),
                            MessageTemplateAction(
                                label='活性碳空氣清淨機',
                                text='@活性碳空氣清淨機'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='NO2 推薦商品',
                        text='請選擇品項',
                        actions=[
                            MessageTemplateAction(
                                label='安全護目鏡',
                                text='@安全護目鏡'
                            ),
                            MessageTemplateAction(
                                label='口罩',
                                text='@口罩'
                            )
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

# =============================================================================
def product():
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

    return glass, mask, Air_clear, Gas_mask, CO_Detector, Gas_alarm, PM25_clean
        
   
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

    


if __name__ == "__main__":
    app.debug = True
    app.run()