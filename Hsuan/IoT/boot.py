# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('junghome', '06220223') # 輸入wifi_name,password
# wifi.connect('TibaMe_Guest', '425110803') # 教室用
while not wifi.isconnected():
    pass
print(wifi.ifconfig())

import ntptime
ntptime.settime() #UTC

