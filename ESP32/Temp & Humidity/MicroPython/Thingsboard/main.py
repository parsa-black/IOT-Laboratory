# Load necessary libraries
from machine import Pin
from umqtt.simple import MQTTClient
import time
import network
import json
import dht

# Objects:
sensor = dht.DHT11(Pin(14))

# WiFi
SSID = "SSID_NAME"
SSID_PASSWORD = "WIFI_PASSWORD"

def do_connect():
    time.sleep(1)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            time.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())
    time.sleep(2)

# Main
print("Connecting to your wifi...")
do_connect()

# Global variables and constants:
# MQTT Basic
username="DEVICE_USERNAME"
broker=  "HOST_NAME"
topic = "v1/devices/me/telemetry"
Mqtt_CLIENT_ID = "CLIENT_ID"
PASSWORD="PASSWORD"
# MQTT
client = MQTTClient(client_id=Mqtt_CLIENT_ID, server=broker, port=1883,
                    user=username, password=PASSWORD, keepalive=10000) #Confiuracion del Cliente MQTT
client.connect()
UPDATE_TIME_INTERVAL = 5000 # in ms unit
last_update = time.ticks_ms()
data = dict()

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
            data2 = json.dumps(data)  # convert it to json

            print('connection finished')
            client.publish(topic, data2)
            print("Data_Published")
        
            last_update = time.ticks_ms()
        except OSError as e:
            print('Failed to read DHT11 sensor.')
            