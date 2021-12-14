import paho.mqtt.client as mqtt
import json
import pymysql

def sqlsave(jsonData):
  # 打开数据库连接
    db = pymysql.connect(host="104.155.221.250",user="sikei",password="zxcv1234",database="ESP32",charset='utf8') 
  # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
  # SQL 插入语句
    sql = "INSERT INTO sensor_data (location, datetime, Temperature, Humidity, MQ135, MQ7, PM25) VALUES ('%s','%s','%s','%s','%s','%s','%s');" \
    %(jsonData['location'], jsonData['datetime'], jsonData['temperature'], jsonData['humidity'], jsonData['MQ135'], jsonData['MQ7'], jsonData['PM25']) 
    cursor.execute(sql)
    db.commit()
    print("数据库保存成功！")
    # 关闭数据库连接
    db.close()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("cfi101/#")
def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))
    get_data=msg.payload #bytes  b'[s]
    print(get_data)
    string=get_data.decode()  #string
    data = '{'+string+'}'
    msgjson=json.loads(data)
    print(msgjson)
    sqlsave(msgjson)

YOUR_BROKER = 'mqtt2.tibame.cloud'
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(YOUR_BROKER, 1883, 60)
client.loop_forever()

while True:
    on_subscribe()