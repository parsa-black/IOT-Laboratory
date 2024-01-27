# Load necessary libraries
from machine import Pin
from umqtt.simple import MQTTClient
import time
import json
import dht
# Objects:
sensor = dht.DHT11(Pin(14))

# Stratup
led = Pin(02, Pin.OUT)

# Global variables and constants:
username="Parsa"
broker=  "iot.scu.ac.ir"
topic = "v1/devices/me/telemetry"
Mqtt_CLIENT_ID = "ESP-WROOM-32"
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
led1=True
# Main Loop
while True:
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        try:
            sensor.measure()
            t = sensor.temperature()
            h = sensor.humidity()
            print(t, h)
            data["temperature"] = t
            data["humidity"] = h
            data["led"] = led1
            data2 = json.dumps(data)  # convert it to json

            print('connection finished')
            client.publish(topic, data2)
            print("Data_Published")
        
            led.value(not led.value())
            led1 = not led1
            last_update = time.ticks_ms()
        except OSError as e:
            print('Failed to read DHT11 sensor.')
            