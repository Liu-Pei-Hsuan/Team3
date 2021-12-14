from time import sleep, localtime, time
from machine import Pin,ADC
from dht import DHT11
from umqtt.simple import MQTTClient
import esp
esp.osdebug(None)
mqtt_broker = 'mqtt2.tibame.cloud'
mqtt_client = MQTTClient(client_id='ESP32', server=mqtt_broker)

setA_CO_MQ7 = 99.042
setB_CO_MQ7 = -1.518
setA_O3_MQ131 = 42.84561841
setB_O3_MQ131 =  -1.043297135
setA_NOx_MQ131 = -462.43
setB_NOx_MQ131 = -2.204
setA_SO2_MQ136 = 40.44109566
setB_SO2_MQ136 = -1.085728557

RL = 10
MQ131_R0 = 0.005
MQ7_R0 = 1.1
MQ136_R0 = 0.005

# dht11 pin number
p = DHT11(Pin(13))

# mq131 pin number
p1 = ADC(Pin(32))
p1.atten(ADC.ATTN_11DB)

# mq7 pin number
p2 = ADC(Pin(35))
p2.atten(ADC.ATTN_11DB)

# pm2.5 pin number
p3 = ADC(Pin(34))
p3.atten(ADC.ATTN_11DB)


# mq136 pin number
p4 = ADC(Pin(33))
p4.atten(ADC.ATTN_11DB)

# pm135 pin number
# p5 = ADC(Pin(number))
# p5.atten(ADC.ATTN_11DB)


while True:
    mqtt_client.connect()
    p.measure()
    temp = p.temperature()
    hum = p.humidity()
    #mq7
    mq7 = p2.read()
    V1 = 5*mq7/1024
    Rs1 = (5*RL/V1)-MQ7_R0
    # Ratio = Rs/R0
    Ratio1 = Rs1/MQ7_R0
    CO = round(Ratio1**setB_CO_MQ7*setA_CO_MQ7,4)
    
    #mq131
    mq131 = p1.read()
    V2 = 5*mq131/1024
    Rs2 = (5*RL/V2)-MQ131_R0
    # Ratio = Rs/R0
    Ratio2 = Rs2/MQ131_R0
    O3 = round(Ratio2**setB_O3_MQ131*setA_O3_MQ131*1000,4)
    
    #mq136
    mq136 = p4.read()
    V3 = 5*mq136/1024
    Rs3 = (5*RL/V3)-MQ136_R0
    # Ratio = Rs/R0
    Ratio3 = Rs3/MQ136_R0
    SO2 = round(Ratio3**setB_SO2_MQ136*setA_SO2_MQ136*1000,4)
    
    #mq131
    NO2 = 0
#     pm25 = p3.read()
# #     pm25_r = 0
#     calcVoltage = pm25 * (5.0 / 1024)
#     dustDensity = (0.17 * calcVoltage - 0.1)*1000
#     if dustDensity<0:
#         pm25_r = 0
#     else:
#         pm25_r = dustDensity
#     mq135 = p4.read()
    dt = localtime(time() + 28800)
    dt = f'{dt[0]:04}/{dt[1]:02}/{dt[2]:02} {dt[3]:02}:{dt[4]:02}:{dt[5]:02}'
    topic = 'cfi101/sikei' 
    # 注意要修改loction位置(自己定義自己的位置名稱)
    content = f'"location":"武陵高中","datetime":"{dt}","temperature":{temp},"humidity":{hum},"NO2":{mq131},"CO":{CO},"O3":{O3},"SO2":{SO2},"PM25":0'
    print(content)
    mqtt_client.publish(topic, content)
    mqtt_client.disconnect()
    sleep(3)

