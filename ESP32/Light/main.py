from machine import Pin, ADC
from umqtt.simple import MQTTClient
import time
import json

# Objects
LDR = ADC(Pin(33))
LDR.atten(ADC.ATTN_0DB)
LDR.width(ADC.WIDTH_12BIT)
LED = Pin(02, Pin.OUT)
LED1 = Pin(19, Pin.OUT)
val = 0

# Global variables and constants:
username="Parsa"
broker=  "iot.scu.ac.ir"
topic = "v1/devices/me/telemetry"
Mqtt_CLIENT_ID = "EspLdr"
PASSWORD="scu99ce"
# MQTT
client = MQTTClient(client_id=Mqtt_CLIENT_ID, server=broker, port=1883,
                    user=username, password=PASSWORD, keepalive=10000) #Confiuracion del Cliente MQTT
client.connect()
UPDATE_TIME_INTERVAL = 2000 # in ms unit
last_update = time.ticks_ms()
# **************************************#
data = dict()
#***************************************#
LED1.value(0)

while True:
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        val = LDR.read() * 0.008
        if val > 20 :
            LED1.value(1)
            light = 1
        else:
           LED1.value(0)
           light = 0
           
        data["Value"] = val
        data["Light"] = light
        dataJson = json.dumps(data)
           
        print('connection finished')
        print(val, light)
        client.publish(topic, dataJson)
        print("Data_Published")
        
        last_update = time.ticks_ms()
        