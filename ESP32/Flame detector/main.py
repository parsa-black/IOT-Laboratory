# Load necessary libraries
from machine import Pin, ADC
from umqtt.simple import MQTTClient	# umqtt.simple 1.3.4
from time import sleep
import time
import json

# Objects:
Flame_Pin = 34
Buzzer_Pin = 33
LED_Pin = 2
Red_Led = 32

# Value:
Value = 2600   # Can Change This Value
OFF = 0
ON = 1

# Stratup
Led = Pin(LED_Pin, Pin.OUT)
Red = Pin(Red_Led, Pin.OUT)
Buzzer = Pin(Buzzer_Pin, Pin.OUT)
Flame = ADC(Pin(Flame_Pin))
Flame.atten(ADC.ATTN_11DB)

# MQTT Basic
username="Parsa"
broker=  "iot.scu.ac.ir"
topic = "v1/devices/me/telemetry"
Mqtt_CLIENT_ID = "ESP32-KY-026"
PASSWORD="scu99ce"
# MQTT
client = MQTTClient(client_id=Mqtt_CLIENT_ID, server=broker, port=1883,
                    user=username, password=PASSWORD, keepalive=10000) #Confiuracion del Cliente MQTT
client.connect()
UPDATE_TIME_INTERVAL = 5000 # in ms unit
last_update = time.ticks_ms()
# **************************************#
data = dict()
#***************************************#

# Main
print("Connecting to your wifi...")
do_connect()
Led.value(OFF) 
while True:
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        try:
            fv = Flame.read()  # flame_value
            print(fv)
            data["Analog"] = fv
            dataJson = json.dumps(data)
            print('connection finished')
            client.publish(topic, dataJson)
            print("Data_Published")
            sleep(0.5)
            if (fv < Value): 
                print("Fire")
                Fire = 1
                Red.value(ON)
                Buzzer.value(ON)
                sleep(2.5)
            else:
                print("No-Fire")
                Red.value(OFF)
                Buzzer.value(OFF)
                sleep(2.5)
        except OSError as e:
            print("Failed")
    
