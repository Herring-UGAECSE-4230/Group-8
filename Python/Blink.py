import RPi.GPIO as GPIO #sets up the py file to use RPi. 
import time             #and the time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

while True: #Get settings for squarewave from console
    Frq = int(input("frequency: ")) 
    duty = int(input("duty percent: "))
    print (Frq, " Hz")
    Ht = T0*(duty/100) #take inputted dutycycle and determine time spent high vs low
    Lt = T0*(1-duty/100)

    while True:# squarewave loop
        GPIO.output(26, GPIO.LOW)
        time.sleep(Lt)
        GPIO.output(26, GPIO.HIGH)
        time.sleep(Ht)


##import wiringpi

