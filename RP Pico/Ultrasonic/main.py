from machine import Pin
import utime

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

def ultrasonic():
    timepassed = 0
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signalloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signalloff
    distance_cm = (timepassed * 0.0343) / 2
    distance_cm = round(distance_cm,2)
    print(f"Distance: {distance_cm}")

while True:
    ultrasonic()
    utime.sleep(1)
    