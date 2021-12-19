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
                TextSendMessage(
                text='請選擇最您想了解的資訊',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="認識指標", text="@認識空氣品質指標")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="好物推薦", text="@今日好物推薦")
                        ),
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
            message = TextSendMessage(
                text='請選擇最您關心的疾病',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="COVID-19", text="COVID-19")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="流感", text="流感")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="腸病毒", text="腸病毒")
                        ),
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
                    text = "下圖為 COVID-19 趨勢圖"
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = "https://img.onl/lIcW63",
                    preview_image_url = "https://img.onl/lIcW63"
                ),
                TextSendMessage(
                text='請選擇最您想了解的資訊',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="認識疾病", text="@認識 COVID-19")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="好物推薦", text="@防疫商品推薦")
                        ),
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '流感': 
        try:
            message = [  #串列
                TextSendMessage(  #傳送文字
                    text = "下圖為流感之趨勢圖"
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = "https://img.onl/lIcW63",
                    preview_image_url = "https://img.onl/lIcW63"
                ),
                TextSendMessage(
                text='請選擇最您想了解的資訊',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="認識疾病", text="@什麼是流感")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="好物推薦", text="@流感商品推薦")
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
                    text = "下圖為腸病毒之趨勢圖"
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = "https://img.onl/lIcW63",
                    preview_image_url = "https://img.onl/lIcW63"
                ),
                TextSendMessage(
                text='請選擇最您想了解的資訊',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="認識疾病", text="@什麼是腸病毒")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="好物推薦", text="@腸病毒商品推薦")
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


if __name__ == "__main__":
    app.debug = True
    app.run()