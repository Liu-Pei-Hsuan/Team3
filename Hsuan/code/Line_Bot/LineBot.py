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

ngrok = "https://4453-60-251-232-252.ngrok.io"


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

productId = ["5ac1bfd5040ab15980c9b435", "5ac21e6c040ab15980c9b444"]
emoji_ID = ["026", "130", "187", "181"]

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
                text = "https://www.google.com.tw/"
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
                    text = "下圖為距離您最近測站之空氣品質數值結果"
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
        try:
            message = TextSendMessage(  
                text = "指標介紹......"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@今日好物推薦':
        Products_Featured(event)   

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
                  "productId": productId[0],
                  "emojiId": emoji_ID[1]
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
                  "productId": productId[0],
                  "emojiId": emoji_ID[0]
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
                  "productId": productId[0],
                  "emojiId": emoji_ID[2]
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
                  "productId": productId[1],
                  "emojiId": emoji_ID[3]
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
                    original_content_url = "https://img.onl/lIcW63",
                    preview_image_url = "https://img.onl/lIcW63"
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
                    original_content_url = "https://img.onl/lIcW63",
                    preview_image_url = "https://img.onl/lIcW63"
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
                text = "COVID-19 介紹......"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@防疫商品推薦':
        COVID_19_Products(event)
        
    elif mtext == '@什麼是流感':
        try:
            message = TextSendMessage(  
                text = "流感介紹......"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@流感商品推薦':
        influenza_Products(event)
        
    elif mtext == '@什麼是腸病毒':
        try:
            message = TextSendMessage(  
                text = "腸病毒介紹......"
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
                        thumbnail_image_url='https://img.onl/kDyaWW',
                        title='PM2.5 推薦商品',
                        text='請選擇',
                        actions=[
                            URITemplateAction(
                                label='推薦 1',
                                uri='http://www.e-happy.com.tw'
                            ),
                            URITemplateAction(
                                label='推薦 2',
                                uri='http://www.e-happy.com.tw'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://img.onl/kDyaWW',
                        title='CO 推薦商品',
                        text='請選擇',
                        actions=[
                            URITemplateAction(
                                label='推薦 1',
                                uri='http://www.e-happy.com.tw'
                            ),
                            URITemplateAction(
                                label='推薦 2',
                                uri='http://www.e-happy.com.tw'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://img.onl/kDyaWW',
                        title='SO2 推薦商品',
                        text='請選擇',
                        actions=[
                            URITemplateAction(
                                label='推薦 1',
                                uri='http://www.e-happy.com.tw'
                            ),
                            URITemplateAction(
                                label='推薦 2',
                                uri='http://www.e-happy.com.tw'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://img.onl/kDyaWW',
                        title='O3 推薦商品',
                        text='請選擇',
                        actions=[
                            URITemplateAction(
                                label='推薦 1',
                                uri='http://www.e-happy.com.tw'
                            ),
                            URITemplateAction(
                                label='推薦 2',
                                uri='http://www.e-happy.com.tw'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://img.onl/kDyaWW',
                        title='NO2 推薦商品',
                        text='請選擇',
                        actions=[
                            URITemplateAction(
                                label='推薦 1',
                                uri='http://www.e-happy.com.tw'
                            ),
                            URITemplateAction(
                                label='推薦 2',
                                uri='http://www.e-happy.com.tw'
                            ),
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
   
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
                        uri='http://www.e-happy.com.tw'
                    ),
                    URITemplateAction(  #開啟網頁
                        label='流行疾病',
                        uri='http://www.e-happy.com.tw'
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