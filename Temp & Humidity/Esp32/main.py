from umqtt import MQTTClient
from machine import Pin, reset, Timer
from time import sleep
import network
import dht



# wifi conenction credentials
SSID = "PARSA"
PASSWORD = "44527481"

# MQTT Server Parameters
# ThingsBoard MQTT settings
THINGSBOARD_SERVER = "iot.scu.ac.ir"
ACCESS_TOKEN = "YrdzdUzEkaHhORX0P0UU"
TOPIC = "v1/devices/me/telemetry"



wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_sta.connect(SSID, PASSWORD)

print("trying to connect to wifi")
while not wlan_sta.isconnected():
    pass

# Pin Setup
sensor = dht.DHT11(Pin(14))
sleep(1)

# setup the timer
timer = Timer(0)

def sub_callback(topic, msg):
  print((topic, msg))
  
# Connect to ThingsBoard MQTT  
def connect_and_subscribe():
  client = MQTTClient("esp32", THINGSBOARD_SERVER, user=ACCESS_TOKEN, password="")
  client.set_callback(sub_callback)
  client.connect()
  client.subscribe(TOPIC)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (THINGSBOARD_SERVER, TOPIC))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  reset()
  
try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

def get_states(timer):
  dht11.measure()
  temp = sensor.temperature()
  humidity = sensor.humidity()
  client.publish(MQTT_TOPIC,ujson.dumps({"temperature":temp,"humidity":humidity}))
  

timer.init(period=3000, callback=get_states)

while True:
  try:
    client.check_msg()
  except OSError as e:
    restart_and_reconnect()