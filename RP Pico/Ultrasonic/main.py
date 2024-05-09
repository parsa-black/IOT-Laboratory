from machine import Pin
from umqtt.simple import MQTTClient
import utime
import time
import network
import json

# Objects
TRIGGER = Pin(2, Pin.OUT)
ECHO = Pin(3, Pin.IN)
LED = Pin("LED", Pin.OUT)
GREEN_Led = Pin(18, Pin.OUT)

# WiFi
SSID = "PARSA"
SSID_PASSWORD = "44527481"

# Connect To WiFi
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
    GREEN_Led.value(1)
    time.sleep(2)

# Check Connection
print("Connecting to your wifi...")
do_connect()
GREEN_Led.value(0)

# Global variables and constants:
# MQTT Basic
username="Parsa"
broker=  "iot.scu.ac.ir"
topic = "v1/devices/me/telemetry"
Mqtt_CLIENT_ID = "PicoSonic"
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

def ultrasonic():
    timepassed = 0
    TRIGGER.low()
    utime.sleep_us(2)
    TRIGGER.high()
    utime.sleep_us(5)
    TRIGGER.low()
    while ECHO.value() == 0:
        signalloff = utime.ticks_us()
    while ECHO.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signalloff
    distance_cm = (timepassed * 0.0343) / 2
    distance_cm = round(distance_cm,2)
    return distance_cm


while True:
    if  time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
         try:
            Distance = ultrasonic()
            data["Distance"] = Distance
            dataJson = json.dumps(data)
        
            print('connection finished')
            LED.on()
            client.publish(topic, dataJson)
            print(f'Distance: {Distance}')
            print("Data_Published")
        
            last_update = time.ticks_ms()
            
         except OSError as e:
            print('Failed to read SRF05 sensor.')   
    
