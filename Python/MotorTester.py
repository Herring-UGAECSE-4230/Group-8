import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pwm = GPIO.PWM(18, 0)
pwm.start(50)
anchor = time.time()
counter = 1
while(True):
    if(time.time() - anchor > 10):
        pwm.changeFrequency(counter * 50)
        counter = counter + 1
    if(counter == 11):
        break
pwm.stop()