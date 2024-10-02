from time import sleep
from machine import Pin
import dht

# Objects:
sensor = dht.DHT11(Pin(28)) # Pin14 is INPUT

# Main Loop
while True:
    try:
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        print(t, h)
        sleep(1)
        
    except OSError as e:
        print('Failed to read DHT11 sensor.')
