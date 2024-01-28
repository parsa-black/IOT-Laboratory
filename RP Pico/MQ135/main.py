from machine import Pin, ADC
from time import sleep

analog_pin = ADC(28)
led = Pin("LED", Pin.OUT)

while True:
    led.off()
    sensor = analog_pin.read_u16()
    print("Sensor :", sensor)
    sleep(1.5)
    led.on()
    sleep(0.5)
    