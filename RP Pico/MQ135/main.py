from machine import Pin, ADC
from time import sleep, ticks_ms
from umqtt.simple import MQTTClient
import network
import json

# Objects
Analog = ADC(26)
LED = Pin("LED", Pin.OUT)
GREEN_Led = Pin(16, Pin.OUT)

# WiFi
SSID = "PARSA"
SSID_PASSWORD = "44527481"

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
    sleep(2)

# Check Connection
print("Connecting to your wifi...")
do_connect()
GREEN_Led.value(0)


# Global variables and constants:
username="Parsa"
broker=  "iot.scu.ac.ir"
topic = "v1/devices/me/telemetry"
Mqtt_CLIENT_ID = "PicoAir"
PASSWORD="scu99ce"
# MQTT
client = MQTTClient(client_id=Mqtt_CLIENT_ID, server=broker, port=1883,
                    user=username, password=PASSWORD, keepalive=10000) #Confiuracion del Cliente MQTT
client.connect()
UPDATE_TIME_INTERVAL = 5000 # in ms unit
last_update = ticks_ms()
# **************************************#
data = dict()
#***************************************#

while True:
    if ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        LED.off()
        sensor = Analog.read_u16()
        print("Sensor :", sensor)
        data["AirQuality"] = sensor
        data2 = json.dumps(data)
        
        print('connection finished')
        LED.on()
        client.publish(topic, data2)
        print("Data_Published")
        
        last_update = ticks_ms()
        