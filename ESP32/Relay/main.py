from machine import Pin
import time

# Define the pin
relay_pin = Pin(5, Pin.OUT)

# relay ON
def relay_on():
    relay_pin.on()
    print("Relay turned ON")

# relay OFF
def relay_off():
    relay_pin.off()
    print("Relay turned OFF")


while True:

    relay_on()
    time.sleep(5)  # Wait for 5 seconds

    relay_off()
    time.sleep(5)  # Wait for 5 seconds