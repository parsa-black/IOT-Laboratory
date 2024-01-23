from machine import Pin
from time import sleep

led_pin_number = [23, 22, 21]
led_pins = []

OFF = 0
ON = 1

# Stratup
def setup_pins():
    for pin in led_pin_number:
        led_pins.append(Pin(pin, Pin.OUT))

def turn_off():
    for pin in led_pins:
        pin.value(OFF)

def turn_on():
    for pin in led_pins:
        pin.value(ON)

# Main
sleep(2.5)
setup_pins()
turn_on()
sleep(0.5)
turn_off()
sleep(0.5)
turn_on()
sleep(0.5)
turn_off()
print('boot done')
