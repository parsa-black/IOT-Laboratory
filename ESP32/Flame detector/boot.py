from machine import Pin
from time import sleep
import network

# Objects:
LED_Pin = 2

OFF = 0
ON = 1

# WiFi
SSID = "SSID_NAME"
SSID_PASSWORD = "WIFI_PASSWORD"

# Stratup
Led = Pin(LED_Pin, Pin.OUT)

def do_connect():
    Led.value(OFF)
    sleep(0.5)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, SSID_PASSWORD)
        while not wlan.isconnected():
            print("Attempting to connect....")
            sleep(0.5)
    print('Connected! Network config:', sta_if.ifconfig())
    Led.value(ON)
    sleep(0.5)
     
 # Main
print("Connecting to your wifi...")
do_connect()
Led.value(OFF)   