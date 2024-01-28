from machine import Pin
import network
from utime import sleep

# Objects
RED_Pin = 6
GREEN_Pin = 7

OFF = 0
ON = 1

# Replace the following with your WIFI Credentials
SSID = "PARSA"
SSID_PASSWORD = "44527481"

# Stratup
RED_Led = Pin(RED_Pin, Pin.OUT)
GREEN_Led = Pin(GREEN_Pin, Pin.OUT)


#------------------------------------------------
def do_connect():
    RED_Led.value(ON)
    sleep(1)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            sleep(1)
    print('Connected! \nIP Address:', sta_if.ifconfig())
    RED_Led.value(OFF)
    GREEN_Led.value(ON)
    sleep(2)

# Check WiFi Connection
RED_Led.value(OFF)
GREEN_Led.value(OFF)
print("Connecting to your wifi...")
do_connect()
GREEN_Led.value(OFF)
