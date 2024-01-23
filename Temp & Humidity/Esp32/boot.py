from machine import Pin
from time import sleep

led_pin_number = [23, 22, 21]
led_pins = []

OFF = 0
ON = 1

def setup_pins():
    for pin in led_pin_number:
        led_pins.append(Pin(pin, Pin.OUT))

def turn_off():
    for pin in led_pins:
        pin.value(OFF)

def turn_on():
    for pin in led_pins:
        pin.value(ON)

setup_pins()
turn_on()
sleep(2)
turn_off()
sleep(2)
