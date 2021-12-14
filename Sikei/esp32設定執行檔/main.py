from time import sleep, localtime, time
from machine import Pin,ADC
from dht import DHT11
from umqtt.simple import MQTTClient
import esp
esp.osdebug(None)
mqtt_broker = 'mqtt2.tibame.cloud'
mqtt_client = MQTTClient(client_id='ESP32', server=mqtt_broker)
p = DHT11(Pin(25))

p1 = ADC(Pin(33))
p1.atten(ADC.ATTN_11DB)

p2 = ADC(Pin(32))
p2.atten(ADC.ATTN_11DB)

p3 = ADC(Pin(35))
p3.atten(ADC.ATTN_11DB)

while True:
    mqtt_client.connect()
    p.measure()
    temp = p.temperature()
    hum = p.humidity()
    mq135 = p1.read()
    mq7 = p2.read()
    pm25 = p3.read()
    dt = localtime(time() + 28800)
    dt = f'{dt[0]:04}/{dt[1]:02}/{dt[2]:02}-{dt[3]:02}:{dt[4]:02}:{dt[5]:02}'
    topic = 'cfi101/sikei'
    content = f'"location":"sikei","datetime":{dt},"temperature":{temp},"humidity":{hum},"MQ135":{mq135},"MQ7":{mq7},"PM2.5":{pm25}'
    print(content)
    mqtt_client.publish(topic, content)
    mqtt_client.disconnect()
    sleep(3)
