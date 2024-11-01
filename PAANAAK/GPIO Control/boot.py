from LCD.lcdInit import tft,wr
from LCD.ST7735 import TFT
from LCD.iransans12 import font12
from umqtt.simple import MQTTClient
from machine import Pin, PWM
import time, utime
import network
import json

# Wi-Fi and ThingsBoard configuration
WIFI_SSID = 'BLVCK'
WIFI_PASSWORD = 'IOT'
THINGSBOARD_HOST = 'iot.scu.ac.ir'
ACCESS_TOKEN = 'IOT'

# Servo Setup
MID = 1500000
MIN = 1000000
MAX = 2000000
# GPIO setup
pwm = PWM(Pin(32))
pwm.freq(50)
pwm.duty_ns(MID)


# GPIO setup
gpio_state = {2: False}  # Track GPIO state for pin 2
gpio_pin = 2
gpio_control = Pin(gpio_pin, Pin.OUT)
gpio_control.value(0)  # Set GPIO to LOW initially

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("Connected to WiFi:", wlan.ifconfig())

# Get GPIO status
def get_gpio_status():
    return json.dumps(gpio_state)  # Return GPIO state as JSON

# Set GPIO status
def set_gpio_status(pin, status):
    gpio_control.value(1 if status else 0)  # Set GPIO HIGH or LOW
    gpio_state[pin] = status  # Update the state
    print(f"GPIO {pin} set to {'ON' if status else 'OFF'}")

# Handle incoming messages
def message_callback(topic, msg):
    print("Received message on topic:", topic)
    print("Message payload:", msg)
    data = json.loads(msg)
    
    if data['method'] == 'getGpioStatus':
        # Reply with GPIO status
        client.publish(topic.replace(b'request', b'response'), get_gpio_status(), 1)
        print("Sent GPIO status response to ThingsBoard")
    elif data['method'] == 'setGpioStatus':
        # Update GPIO status based on 'enabled' param
        params = data['params']
        pin = params['pin']
        enabled = params['enabled']
        
        set_gpio_status(pin, enabled)
        
        # Reply with the updated GPIO status
        client.publish(topic.replace(b'request', b'response'), get_gpio_status(), 1)
        # Immediately update ThingsBoard with the new GPIO status
        client.publish('v1/devices/me/attributes', get_gpio_status(), 1)
        print("Updated GPIO status on ThingsBoard")

# Connect to ThingsBoard
client = MQTTClient("ESP32", THINGSBOARD_HOST, user=ACCESS_TOKEN, password="")
client.set_callback(message_callback)

def connect_mqtt():
    client.connect()
    client.subscribe(b'v1/devices/me/rpc/request/+')
    print("Connected to ThingsBoard MQTT and subscribed to RPC requests")

# Main loop
showBmp(tft,'./LCD/scu.bmp',(37,20))
time.sleep(5)
tft.fill(TFT.GREEN)
wr.text((60,20),"SCU",TFT.WHITE,font12)
wr.text((45,32),"IOT Lab",TFT.WHITE,font12)
def main():
    connect_wifi()
    connect_mqtt()
    try:
        while True:
            pwm.duty_ns(MIN)
            utime.sleep(1)
            pwm.duty_ns(MID)
            utime.sleep(1)
            pwm.duty_ns(MAX)
            utime.sleep(1)
            client.check_msg()  # Check for incoming messages
            time.sleep(1)
    finally:
        client.disconnect()

# Run the main loop
main()
