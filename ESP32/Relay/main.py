from machine import Pin
import time

# Define the pin
relay_pin = Pin(02, Pin.OUT)

# relay ON
def relay_on():
    relay_pin.value(1)
    print("Relay turned ON")

# relay OFF
def relay_off():
    relay_pin.value(0)
    print("Relay turned OFF")


while True:

    relay_on()
    time.sleep(2)  # Wait for 2 seconds

    relay_off()
    time.sleep(2)  # Wait for 2 seconds
        