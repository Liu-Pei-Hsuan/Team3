from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import json
import configparser
import os
from urllib import parse
import time
import sys
from math import *
import numpy as np
from locData import *
from datetime import datetime
import numpy as np

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
ngrokUrl = 'https://0352-111-249-3-147.ngrok.io/'


config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
my_line_id = config.get('line-bot', 'my_line_id')
end_point = config.get('line-bot', 'end_point')
client_id = config.get('line-bot', 'client_id')
client_secret = config.get('line-bot', 'client_secret')
HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {config.get("line-bot","channel_access_token")}'# your code here
}


@app.route("/", methods=['POST'])
def index():
    body = request.json
    events = body["events"]
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
#         if events[0]["type"] == "message":
#             if events[0]["message"]["type"] == "text":
#                 text = events[0]["message"]["text"]
#                 payload["messages"] = [
#                         {
#                             "type": "text",
#                             "text": text
#                         }
#                     ]
#                 replyMessage(payload)
        if events[0]["type"] == "message":
            if (events[0]["message"]["type"] == "text"):
                text = events[0]["message"]["text"]
                if (text == "照片"):
                    originalContentUrl = ngrokUrl + "/static/taipei_101.jpeg"
                    print(originalContentUrl)
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": text
                            },
                            {
                                "type": "sticker", # line 貼圖
                                "packageId": "789",
                                "stickerId": "10856"
                            },getImageMessage(originalContentUrl),getTaipei101ImageMessage(),
                            {
                                "type": "image",
                                "originalContentUrl": "https://i.imgur.com/9WVhDtx.jpg",
                                "previewImageUrl": "https://i.imgur.com/9WVhDtx.jpg"
                            }
                        ]
                    replyMessage(payload)

                elif (text == "自我介紹"):
                    payload["messages"] = [
                    {
                        "type": "text",
                        "text":"我今年9歲"
                    },
                    {
                        "type": "sticker",  # line 貼圖
                        "packageId": "789",
                        "stickerId": "10856"
                    },
                    {
                        "type": "text",
                        "text":"幹嘛看我搖屁股？？"
                    },
                    {
                        "type": "text",
                        "text":"臭三八"
                    },
                    {
                        "type": "sticker",  # line 貼圖
                        "packageId": "6632",
                        "stickerId": "11825393"
                    }
                    ]
                    replyMessage(payload),

                elif (text == "我的名字"):
                    payload["messages"] = [getNameEmojiMessage("YI")]
                    replyMessage(payload)

                elif text == "今日確診人數":
                    payload["messages"] = [
                        {
                            "type": "text",
                            "text": covid19Message()
                        }
                    ]
                    replyMessage(payload)

                elif (text == "出去玩"):
                    payload["messages"] = [
                        {
                            "type": "sticker",  # line 貼圖
                            "packageId": "6632",
                            "stickerId": "11825393"
                        }
                    ]
                    replyMessage(payload)

                elif (text == "地標1"):
                    payload["messages"] = [
                        {
                            "type": "location",  # line 貼圖
                            "title": "my location",
                            "address": "大竹國小",
                            "latitude":25.02499314293323,
                            "longitude": 121.258470161944
                        }
                    ]
                    replyMessage(payload)

                elif text == "地標":
                    payload["messages"] = getLocationConfirmMessage_MR()
                    replyMessage(payload)

                elif text == "地地標":
                    payload["messages"] = [getLocationConfirmMessage_ME()]
                    replyMessage(payload)

                elif text == "地標影片":
                    payload["messages"] = [getMRTVideoMessage()]
                    replyMessage(payload)

                elif text == "quota":
                    payload["messages"] = [
                        {
                            "type": "text",
                            "text": getalertmessage()
                        }
                    ]
                    replyMessage(payload)

                else: # 通用格式
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": text
                            }
                        ],
                    replyMessage(payload)

            if (events[0]["message"]["type"] == "location"):
                # 下為使用者回饋經緯度
                Find_loc = np.matrix([[events[0]["message"]["latitude"], events[0]["message"]["longitude"]]])
                # 距測站距離(全部)
                disALL = np_getDistance(loltALL_center,Find_loc)
                # 距離測站最短距離(全部)
                disMinName = nameALL[int(disALL.argmin(axis=0))]
                disMinDistance = floor(disALL[int(disALL.argmin(axis=0))])
                textplus = ("離%s最近，距離 %1.1f 公里" %(disMinName,disMinDistance))

                payload["messages"] = [
                    {
                        "type": "text",
                        "text": textplus
                    },
                    # {   ##下方是回傳經緯度給用戶，不需要先關
                    #     "type": "text",
                    #     "text": events[0]["message"]["latitude"]
                    # },
                    # {
                    #     "type": "text",
                    #     "text": events[0]["message"]["longitude"]
                    # }
                ]
                replyMessage(payload)
    return 'OK'

##            if events[0]["message"]["type"] == "location":
##                addr = events[0]["message"]["address"]
##                lat = events[0]["message"]["latitude"]
##                lon = events[0]["message"]["longitude"]
##                payload["messages"] = [getLocationConfirmMessage(addr, lat, lon)]
##
##                replyMessage(payload)
##
##            elif events[0]["type"] == "postback":
##                if "params" in events[0]["postback"]:
##                    reservedTime = events[0]["postback"]["params"]["datetime"].replace("T", " ")
##                    payload["messages"] = [
##                        {
##                            "type": "text",
##                            "text": F"已完成預約於{reservedTime}的叫車服務"
##                        }
##                    ]
##                    replyMessage(payload)
##
##                else:
##                    data = json.loads(events[0]["postback"]["data"])
##                    action = data["action"]
##                    if action == "get_near":
##                        data["action"] = "get_detail"
##                        payload["messages"] = [getCarouselMessage(data)]
##                    elif action == "get_detail":
##                        del data["action"]
##                        payload["messages"] = [getTaipei101ImageMessage(),
##                                               getTaipei101LocationMessage(),
##                                               getMRTVideoMessage(),
##                                               getCallCarMessage()]
##
##                    replyMessage(payload)

# @app.route("/callback", methods=['POST'])
# def callback():
#     signature = request.headers['X-Line-Signature']
#
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#
#     return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    if event.message.type == "text":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = event.message.text)
            )
    if event.message.type=="location":
        addr_get = event.message.address
        latitude_get = event.message.latitude
        longitude_get = event.message.longitude
        text_replay= "title: your Location\n" + "address: " + addr_get

        # # print("use %s usec"%(endtime-starttime).microseconds)
                    # message = LocationSendMessage(
            #     addr_get = event.message.address
            #     latitude_get = event.message.latitude
            #     longitude_get = event.message.longitude
            #     message = LocationSendMessage(
            #         title="Your location",
            #         address=addr_get,
            #         latitude=latitude_get,  # 緯度
            #         longitude=longitude_get  # 經度
            #     )
            #     line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = textplus))
    return 'OK'


@app.route("/sendTextMessageToMe", methods=['POST'])
def sendTextMessageToMe():
    # your code here
    return 'OK'


def getNameEmojiMessage(name):
    lookUpStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    productId = "5ac21a8c040ab15980c9b43f"
    message = dict()
    message["type"] = "text"
    message["text"] = "".join("$" for r in range(len(name)))
    emojis_list = list()
    for i, nChar in enumerate(name):
        emojis_list.append(
            {
              "index": i,
              "productId": productId,
              "emojiId": f"{lookUpStr.index(nChar) + 1 :03}"
            }
        )
    message["emojis"] = emojis_list
    return message



def getCarouselMessage(data):
    message = dict()
    # your code here
    return message


def getLocationConfirmMessage():
    message = dict()
    return message


def getCallCarMessage(data):
    message = dict()
    # your code here
    return message


def getPlayStickerMessage():
    message = dict()
    # your code here
    return message


def getMRTVideoMessage():
    message = dict()
    message["type"] = "video"
    message["originalContentUrl"] = "https://14cf-111-249-58-35.ngrok.io/static/taipei_101_video.mp4"
    return message

def getLocationConfirmMessage_MR():
    messageout = []
    message = dict()
    message["type"] = "location"
    message["title"] = "tibame"
    message["address"] = "320桃園市中壢區復興路46號9樓"
    message["latitude"] = "24.9576403"
    message["longitude"] = "121.222834"
    messageout.append(message)
    message = dict()
    message["type"] = "video"
    message["originalContentUrl"] = "https://a74d-2001-b400-e358-40eb-90b5-2df7-af3e-d20f.ngrok.io/static/taipei_101_video.mp4"
    message["previewImageUrl"] = "https://a74d-2001-b400-e358-40eb-90b5-2df7-af3e-d20f.ngrok.io/static/taipei_101.jpeg"
    message["trackingId"] = "track-id"
    messageout.append(message)
    return messageout

def getCarouselMessage(data):
    message = dict()
    message["type"] = "template"
    message["altText"] = "this is a image carousel template"
    message["template"] = {
          "type": "image_carousel",
          "columns": [
              {
                "imageUrl": F"{ngrokUrl}/static/taipei_101.jpeg",
                "action": {
                  "type": "postback",
                  "label": "台北101",
                  "data": json.dumps(data)
                }
              },
              {
                "imageUrl": F"{ngrokUrl}/static/taipei_1.jpeg",
                "action": {
                  "type": "postback",
                  "label": "台北101",
                  "data": json.dumps(data)
                }
              }
          ]
    }
    return message

def getLocationConfirmMessage(title, latitude, longitude):
    message = dict()
    message["type"] = "template"
    message["altText"] = "this is a confirm template"
    data = {"title": title, "latitude": latitude, "longitude": longitude, "action": "get_near"}
    message["template"] = {
          "type": "confirm",
          "text": F"您是否確定搜尋{title}附近景點？",
          "actions": [
                    {
                       "type": "postback",
                       "label": "是",
                       "data": json.dumps(data),
                       "text": "是"
                      },
                    {
                        "type": "message",
                        "label": "否",
                        "text": "否"
                      }
          ]
    }
    return message


def getMRTSoundMessage():
    message = dict()
    # your code here
    return message


def getTaipei101ImageMessage(originalContentUrl=F"https://45fd-111-249-58-131.ngrok.io/static/taipei_101.jpeg"):

    return getImageMessage(originalContentUrl)


def getImageMessage(originalContentUrl):
    message = dict()
    message["type"]="image"
    message["originalContentUrl"]=originalContentUrl
    message["previewImageUrl"]=originalContentUrl
    return message


def getTaipei101LocationMessage():
    message = dict()
    # your code here
    return message

def getalertmessage():
    url_quota='https://api.line.me/v2/bot/message/quota'
    url_Totle='https://api.line.me/v2/bot/message/quota/consumption'
    user_agent='Bearer {6fr0EKeOLsJ5Dr4+D8e3wrC3IRhGXKU9F5p8crI6Ek24zVVqidS864BqFj5+60x6CRNDZhtJuWSoFAxJRkevJ2D/ZID93sqIz8UI94DrECJQNFigCVNoZJPiqNfa0ajZuedNbxxFfO1tpbY7Zm56dwdB04t89/1O/w1cDnyilFU=}'
    data={
        'Authorization':user_agent
    }
    quota=(requests.get(url=url_quota,headers=data)).json()
    quota=quota['value']
    Totle=(requests.get(url=url_Totle,headers=data)).json()
    Totle=Totle['totalUsage']
    return F"已經POST則數：{Totle} , 剩餘POST則數 : {quota}"



def replyMessage(payload):
    response = requests.post('https://api.line.me/v2/bot/message/reply',headers=HEADER,data=json.dumps(payload))
    print(response.text)
    return 'OK'
def pushMessage(payload):
    response = requests.post('https://api.line.me/v2/bot/message/push',headers=HEADER,data=json.dumps(payload))
    print(response.text)
    return 'OK'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def covid19Message():
    res = requests.get("https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4001&limited=TWN")
    date = res.json()[0]["a04"]
    total_count = res.json()[0]["a05"]
    today_count = res.json()[0]["a06"]
    return f"日期：{date}, 今日確診人數：{today_count}, 總共確診人數：{total_count}"

def getLocationConfirmMessage_ME():
    message = dict()
    message["type"] = "location"
    message["title"] = "tibame"
    message["address"] = "320桃園市中壢區復興路46號9樓"
    message["latitude"] = "24.9576403"
    message["longitude"] = "121.222834"
    return message

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(img_path)
            # your code here
    return 'OK'


@app.route('/line_login', methods=['GET'])
def line_login():
    if request.method == 'GET':
        code = request.args.get("code", None)
        state = request.args.get("state", None)

        if code and state:
            # your code here
            content = None
            name = content["displayName"]
            userID = content["userId"]
            pictureURL = content["pictureUrl"]
            statusMessage = content["statusMessage"]
            return render_template('profile.html', name=name, pictureURL=
                                   pictureURL, userID=userID, statusMessage=
                                   statusMessage)
        else:
            return render_template('login.html', client_id=client_id,
                                   end_point=end_point)


if __name__ == "__main__":
    app.debug = True
    app.run()
