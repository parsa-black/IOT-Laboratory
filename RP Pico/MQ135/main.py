from machine import Pin, ADC, PWM
from time import sleep, ticks_ms
from umqtt.simple import MQTTClient
import network
import json

# Objects
Analog = ADC(26)
buzzer = PWM(Pin(15))
buzzer.freq(500)
LED = Pin("LED", Pin.OUT)
GREEN_Led = Pin(16, Pin.OUT)
RED_Led = Pin(14, Pin.OUT)

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

while True:
    if ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        LED.off()
        # Value
        sensor = Analog.read_u16() / 100
        
        #  Data         
        print("Sensor :", sensor)
        data["AirQuality"] = sensor
         # Buzzer
        if sensor > 460 :
            RED_Led.value(1)
            buzzer.duty_u16(1000)
            sleep(1.5)
            buzzer.duty_u16(0)
        else:
             RED_Led.value(0)
         # JsonS    
        data2 = json.dumps(data)
        
        print('connection finished')
        LED.on()
        client.publish(topic, data2)
        print("Data_Published")
        
        last_update = ticks_ms()
        