from machine import Pin, ADC
from time import sleep
import network

# Objects:
Flame_Pin = 34
Buzzer_Pin = 33
LED_Pin = 2
Red_Led = 32
# Value:
OFF = 0
ON = 1

# Stratup
Red = Pin(Red_Led, Pin.OUT)
Buzzer = Pin(Buzzer_Pin, Pin.OUT)
Flame = ADC(Pin(Flame_Pin))
Flame.atten(ADC.ATTN_11DB)

# WiFi
SSID = "SSID_NAME"
SSID_PASSWORD = "WIFI_PASSWORD"

# Connection Stratup
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
while True:
    fv = Flame.read()  # flame_value
    print(fv)
    sleep(2)
    if (fv < 2800):
        print("Fire")
        Red.value(ON)
        Buzzer.value(ON)
    else:
        print("No-Fire")
        Red.value(OFF)
        Buzzer.value(OFF)
    