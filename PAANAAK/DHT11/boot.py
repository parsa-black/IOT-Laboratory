from machine import Pin
from time import sleep
from LCD.lcdInit import tft,wr
from LCD.ShowBmp import showBmp
from LCD.ST7735 import TFT
from LCD.iransans12 import font12
import dht

# Objects:
sensor = dht.DHT11(Pin(18)) # Pin18 is INPUT

# Main Loop
showBmp(tft,'./LCD/scu.bmp',(37,20))
sleep(5)
tft.fill(TFT.GREEN)
wr.text((60,20),"SCU",TFT.WHITE,font12)
wr.text((45,32),"IOT Lab",TFT.WHITE,font12)
while True:
    try:
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        print(t, h)
        wr.text((35,64),"Temp: ",TFT.CYAN,font12)  # Show Desplay
        wr.text((100,64),str(t),TFT.CYAN,font12)  # Show Desplay
        wr.text((30,74),"Humd: ",TFT.CYAN,font12)  # Show Desplay
        wr.text((100,74),str(h),TFT.CYAN,font12)  # Show Desplay
        wr.text((40,108),"__OK__",TFT.BLUE,font12)
        sleep(2)
    except OSError as e:
        print('Failed to read DHT11 sensor.')
        wr.text((40,108),"ERROR!",TFT.BLUE,font12) 
