from machine import Pin
from time import sleep
import network

# Objects:
LED_Pin = 2

OFF = 0
ON = 1

# WiFi
SSID = "PARSA"
SSID_PASSWORD = "44527481"

# Stratup
Led = Pin(LED_Pin, Pin.OUT)

def do_connect():
    Led.value(OFF)
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
    Led.value(ON)
    sleep(2)

# Main
print("Connecting to your wifi...")
do_connect()
Led.value(OFF)
