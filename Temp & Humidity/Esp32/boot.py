from machine import Pin
from time import sleep
import network

led_pins = [23, 22, 21]

RED_Pin = 23
YELLOW_Pin = 22
GREEN_Pin = 21

OFF = 0
ON = 1

# Replace the following with your WIFI Credentials
SSID = "<PLACE_YOUR_SSID_HERE>"
SSID_PASSWORD = "<PLACE_YOUR_WIFI_PASWORD_HERE>"

# Stratup
RED_Led = Pin(RED_Pin, Pin.OUT)
YELLOW_Led = Pin(YELLOW_Pin, Pin.OUT)
GREEN_Led = Pin(GREEN_Pin, Pin.OUT)

def do_connect():
    YELLOW_Led.value(ON)
    sleep(1)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            YELLOW_Led.value(OFF)
            RED_Led.value(ON)
            sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())
    YELLOW_Led.value(OFF)
    GREEN_Led.value(ON)
    sleep(2)

# Main
print("Connecting to your wifi...")
do_connect()
YELLOW_Led.value(OFF)
GREEN_Led.value(OFF)
RED_Led.value(OFF)


