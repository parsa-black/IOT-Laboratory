from machine import Pin, ADC
from LCD.lcdInit import tft,wr
from LCD.ShowBmp import showBmp
from LCD.ST7735 import TFT
from LCD.iransans12 import font12
from time import sleep

# Soil Moisture
soil = ADC(Pin(36)) # ADC1_CH0
m = 100

min_moisture=0
max_moisture=4095

soil.atten(ADC.ATTN_11DB)       #Full range: 3.3v
soil.width(ADC.WIDTH_12BIT)     #range 0 to 4095

# Main Loop
showBmp(tft,'./LCD/scu.bmp',(37,20))
sleep(5)
tft.fill(TFT.GREEN)
wr.text((60,20),"SCU",TFT.WHITE,font12)
wr.text((45,32),"IOT Lab",TFT.WHITE,font12)
while True:
    try:
        t = soil.read()
        m = (max_moisture - t)*100/(max_moisture - min_moisture)
        moisture = '{:.1f} %'.format(m)
        print(str(moisture))
        wr.text((35,64),"Soil: ",TFT.CYAN,font12)  # Show Desplay
        wr.text((80,64),str(moisture),TFT.CYAN,font12)  # Show Desplay
        wr.text((40,108),"__OK__",TFT.BLUE,font12)
        sleep(3)
    except OSError as e:
        print("Failed to read Sensor")
        wr.text((40,108),"ERROR!",TFT.BLUE,font12) 