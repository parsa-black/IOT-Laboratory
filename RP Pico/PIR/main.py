from machine import Pin
<<<<<<< HEAD
import utime
# Objects
led = Pin(28, Pin.OUT)
pir = Pin(16, Pin.IN, Pin.PULL_UP)
=======
from umqtt.simple import MQTTClient
import utime
import network
import json

# Objects
led = Pin(28, Pin.OUT)
pir = Pin(16, Pin.IN, Pin.PULL_UP)

# WiFi
SSID = "SSID_NAME"
SSID_PASSWORD = "WIFI_PASSWORD"

# Connect To WiFi
def do_connect():
    sleep(1)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())
    GREEN_Led.value(1)
     buzzer.duty_u16(1000)
    sleep(1)
    buzzer.duty_u16(0)

# Check Connection
print("Connecting to your wifi...")
do_connect()
GREEN_Led.value(0)

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
last_update = ticks_ms()
# **************************************#
data = dict()
#***************************************#

>>>>>>> bd5fd4d822c25a81b9822e6bd28a23bc4f0e140d
# Code
led.low()
utime.sleep(3)
while True:
<<<<<<< HEAD
   print(pir.value())
   if pir.value() == 1:
       print("Movement")
       led.high()
=======
    sensor = pir.value()
   print(pir.value())
    data["Motion"] = sensor
    if sensor == 1:
        print("Motion Sensor")
       led.high()
       JsonData = json.dump(data)
>>>>>>> bd5fd4d822c25a81b9822e6bd28a23bc4f0e140d
       utime.sleep(5)
   else:
       print("Waiting for movement")
       led.low()
<<<<<<< HEAD
=======
       JsonData = json.dump(data)
>>>>>>> bd5fd4d822c25a81b9822e6bd28a23bc4f0e140d
       utime.sleep(1)
utime.sleep(0.2)