from machine import Pin, ADC
import time

adc_pin = 13  # ADC pin number
adc = ADC(Pin(adc_pin))
adc.atten(ADC.ATTN_11DB)

while True:
    analog_value = adc.read()
    
    print("Analog Value:", analog_value)
    
    time.sleep(1)