from machine import Pin
from LCD.lcdInit import tft,wr
from LCD.ShowBmp import showBmp
from LCD.ST7735 import TFT
from LCD.iransans12 import font12
from umqtt.simple import MQTTClient
import ds18x20,onewire,machine
import time, network
import json

# WiFi
SSID = "BLVCK"
SSID_PASSWORD = "44527481"
 
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            wr.text((47,108),"Wifi..",TFT.RED,font12)  # Show Desplay
    print('Connected! Network config:', sta_if.ifconfig())
    time.sleep(2)


def read_sensor():
    temps=[]        
    time.sleep(1)
    ds_pin = machine.Pin(18,Pin.IN, Pin.PULL_UP)
    disconnected_temp=0
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    sum=0
    #Add & Edit by Prbarkati :checking if sensor is disconnected
    attempt=0
    while(len(temps)<5):
        attempt+=1
        if(len(temps)==0):
            if attempt>=2:
                disconnected_temp+=1
                print('Sensor Disconnection Error Try:',disconnected_temp)
                time.sleep(1)
                if disconnected_temp>=10:
                    print('Sensor Disconnection Error')
                    wr.text((40,108),"ERROR!",TFT.RED,font12)  # Show Desplay
                    disconnected_temp=0
                    return -100
        if roms==[]:
            roms = ds_sensor.scan()

        for rom in roms:
            try:
                wr.text((44,108),"__OK__",TFT.GREEN,font12)  # Show Desplay
                ds_sensor.convert_temp()
                time.sleep_ms(750)
                t=ds_sensor.read_temp(rom)
                temps.append(t)
                sum+=t
                time.sleep(1)
            except:
                
                disconnected_temp+=1
                print('tempreture sensor error  Try: ',disconnected_temp)
                if disconnected_temp>=10:
                    print('Sensor Disconnection Error')
                    wr.text((40,108),"ERROR!",TFT.RED,font12)  # Show Desplay
                    disconnected_temp=0
                    return -100
                time.sleep(1)
                continue            
    print(sum/len(temps))
    lastvalue = (int((sum/len(temps)*10))/10)
    return lastvalue
    time.sleep(2)

# Main
showBmp(tft,'./LCD/scu.bmp',(37,20))
time.sleep(7)
showBmp(tft,'./LCD/logo.bmp',(37,20))
time.sleep(3)
tft.fill(TFT.GREEN)
wr.text((60,20),"SCU",TFT.WHITE,font12)
wr.text((45,32),"IOT Lab",TFT.WHITE,font12)
wr.text((40,86),"Loading...",TFT.CYAN,font12)  # Show Desplay
print("Connecting to WiFi...")
# Connect to Internet Before Send MQTT Basic Parameters
do_connect()

# After Connection to WiFi
# Global variables and constants:
# MQTT Basic
username="ParsaBlack"
broker=  "iot.scu.ac.ir"
topic = "v1/devices/me/telemetry"
Mqtt_CLIENT_ID = "TestDevNo1"
PASSWORD="scu99ce"

# MQTT
client = MQTTClient(client_id=Mqtt_CLIENT_ID, server=broker, port=1883,
                    user=username, password=PASSWORD, keepalive=10000) #Confiuracion del Cliente MQTT
client.connect()
UPDATE_TIME_INTERVAL = 3000 # in ms unit
last_update = time.ticks_ms()
data = dict()


# Main Loop
while True:
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        try:
            temp = read_sensor()
            data["temperature"] = temp
            DataJSON = json.dumps(data)  # convert it to json
            print('connection finished')
            client.publish(topic, DataJSON)
            wr.text((60,64),str(temp),TFT.WHITE,font12)  # Show Desplay
            wr.text((30,86),"Thingsboard",TFT.CYAN,font12)  # Show Desplay
            print("Data_Published")
            last_update = time.ticks_ms()
        except OSError as e:
            print('Failed to read Sensor.')
            wr.text((40,108),"ERROR!",TFT.BLUE,font12)  # Show Desplay