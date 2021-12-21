import requests
import json
import ast


# =============================================================================
# ## 創建 Rich Menus
# > 發送一個 request 請求到 https://api.line.me/v2/bot/richmenu 創建 Rich menus
# > * 請求需要在 headers 中的 Authorization 屬性內帶上 Line Bot 的 Token 值
# > * body 內則是關於選單的設置
# =============================================================================

body = {
        "size": {
            "width": 2205,
            "height": 744
        },
        "selected": "true", # 控制 Rich menus 是否預設開啟， true 及 false 請使用字串格式
        "name": "圖文選單", # Rich menus 的名稱
        "chatBarText": "點我收合選單", # 圖文選單下方的文字內容，點擊可開關選單，可以設置為「點我收合選單」
        "areas": [
            {
                "bounds": {
                    "x": 55,
                    "y": 130,
                    "width": 580,
                    "height": 580
                },
                "action":{
                    "type": "message",
                    "text":"@請回傳您的位置"
                }
            },
            {
                "bounds": {
                    "x": 650,
                    "y": 130,
                    "width": 580,
                    "height": 580
                },
                "action": {
                    "type": "message",
                    "text":"@請回傳您的位置" 
                }
            },
            {
                "bounds": {
                    "x": 1260,
                    "y": 110,
                    "width": 580,
                    "height": 580
                },
                "action": {
                    "type": "message",
                    "text":"@請點選您要看的疾病"
                }
            },
            {
                "bounds": {
                    "x": 1860,
                    "y": 110,
                    "width": 580,
                    "height": 580
                },
                "action": {
                    "type": "message",
                    "text":"@請點選您要看的小百科"
                }
            }
        ]
}



headers = {"Authorization":"Bearer UBpmysfAVIzw2uqQgj5NvMW314kcbhqxYKbVm430ZiTJnZEj4cdeZUapCUlAn9f49B2Qi+LMzd+hw4xVE9Nz2CKqo24Py4HwQb8jj5K4ob/SNx7seCr3NkpOGm/ILQYzzk2pf+ccv12JeUAr9s+gKAdB04t89/1O/w1cDnyilFU=",
           "Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)


# =============================================================================
# 將 bytes 轉為 dict
# =============================================================================
richMenuId = req.content
richMenuId_str = richMenuId.decode("UTF-8")
richMenuId = ast.literal_eval(richMenuId_str)
richMenuId = "".join(richMenuId.values()) # to string
richMenuId


# =============================================================================
# ## 設定 Rich Menus 的圖片
# > * 需要透過 line-bot-sdk-python 來將圖片掛上圖文選單，執行成功後什麼都不會回傳  
# > * !!! 需要注意，圖片的大小需和 Rich menus 的 size 一模一樣
# =============================================================================
from linebot import LineBotApi

line_bot_api = LineBotApi('UBpmysfAVIzw2uqQgj5NvMW314kcbhqxYKbVm430ZiTJnZEj4cdeZUapCUlAn9f49B2Qi+LMzd+hw4xVE9Nz2CKqo24Py4HwQb8jj5K4ob/SNx7seCr3NkpOGm/ILQYzzk2pf+ccv12JeUAr9s+gKAdB04t89/1O/w1cDnyilFU=')

with open("D:/air.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(richMenuId, "image/jpeg", f)


# =============================================================================
# ## 啟用 Rich Menus
# > * 啟用 Rich menus 只要透過發送 request 就能完成，request 的 url 為 https://api.line.me/v2/bot/user/all/richmenu/ 再加上 Rich menus 的 ID   
# > * 請求成功會回傳一個空物件
# =============================================================================
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/{}'.format(richMenuId), 
                       headers=headers)

print(req.text)


# =============================================================================
# 查看所有 Rich menus
# =============================================================================
rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)

# =============================================================================
# 刪除 Rich menus
# =============================================================================
line_bot_api.delete_rich_menu(richMenuId)

