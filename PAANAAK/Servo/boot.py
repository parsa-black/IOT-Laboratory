from machine import Pin, PWM
from LCD.lcdInit import tft,wr
from LCD.ShowBmp import showBmp
from LCD.ST7735 import TFT
from LCD.iransans12 import font12
from time import sleep
import utime
MID = 1500000
MIN = 1000000
MAX = 2000000
pwm = PWM(Pin(18))
pwm.freq(50)
pwm.duty_ns(MID)
# Main Loop
showBmp(tft,'./LCD/scu.bmp',(37,20))
sleep(5)
tft.fill(TFT.GREEN)
wr.text((60,20),"SCU",TFT.WHITE,font12)
wr.text((45,32),"IOT Lab",TFT.WHITE,font12)
while True:
    wr.text((25,64),"Servo Motor",TFT.CYAN,font12)  # Show Desplay
    pwm.duty_ns(MIN)
    utime.sleep(1)
    pwm.duty_ns(MID)
    utime.sleep(1)
    pwm.duty_ns(MAX)
    utime.sleep(1)