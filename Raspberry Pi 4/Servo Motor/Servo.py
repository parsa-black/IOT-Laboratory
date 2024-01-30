import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(11, GPIO.OUT)
servo = GPIO.PWM(11, 50) # Note 11 is Pin, 50 = 50Hz pulse

# start PWM, vlaue of 0 (pulse off)
servo.start(0)
print("Waiting for 2 Second")
time.sleep(2)

# Move Servo
print("Roatating 180 degrees in 10 steps")

# Define variable duty
duty = 2

# Loop for duty values from 2 to 12 (0 to 180)
while duty <= 12:
    servo.ChangeDutyCycle(duty)
    time.sleep(0.7)
    servo.ChangeDutyCycle(0)
    time.sleep(0.3)
    duty += 1
    
# Wait
time.sleep(2)

# Trun Back to 90 degrees
print("90 degrees")
servo.ChangeDutyCycle(7)
time.sleep(2)

# Trun Back to 0 degrees
print("0 degrees")
servo.ChangeDutyCycle(2)
time.sleep(0.5)
servo.ChangeDutyCycle(0)

# Clean things up at the end
servo.stop()
GPIO.cleanup()
print("The End")
