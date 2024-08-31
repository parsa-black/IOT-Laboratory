# import required modules
from machine import ADC, Pin
import utime
 
# Init 
soil = ADC(Pin(26)) # Soil moisture PIN reference
 
#Calibraton values
min_moisture=19200
max_moisture=49300
 
while True:
    moisture = (max_moisture-soil.read_u16())*100/(max_moisture-min_moisture) 
    # print values
    print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
    utime.sleep(0.5) # set a delay between readings
    