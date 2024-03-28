import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 1000)
pwm.start(50)
'''anchor = time.time()
counter = 1
while(True):
    if(time.time() - anchor > 2):
        pwm.ChangeFrequency(counter * 50)
        print("frequency = " + str(counter * 50))
        anchor = time.time()
        counter = counter + 1
    if(counter == 11):
        break
pwm.stop()'''