import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

while True:
    Frq = int(input("frequency: ")) 
    T0 = 1/Frq
    duty = int(input("duty percent: "))
    print (Frq, " Hz")
    Ht = T0*(duty/100)
    Lt = T0*(1-duty/100)

    while True:
        GPIO.output(26, GPIO.LOW)
        time.sleep(Lt)
        GPIO.output(26, GPIO.HIGH)
        time.sleep(Ht)


##import wiringpi

