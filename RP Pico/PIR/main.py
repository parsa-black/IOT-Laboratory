from machine import Pin
import utime
# Objects
led = Pin(28, Pin.OUT)
pir = Pin(16, Pin.IN, Pin.PULL_UP)
# Code
led.low()
utime.sleep(3)
while True:
   print(pir.value())
   if pir.value() == 1:
       print("Movement")
       led.high()
       utime.sleep(5)
   else:
       print("Waiting for movement")
       led.low()
       utime.sleep(1)
utime.sleep(0.2)