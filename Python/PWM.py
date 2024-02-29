import RPi.GPIO as GPIO
import time


#Setting up library and GPIOs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
clk = 21
dt = 20
sw = 26
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
anchor = time.time()
anchorT = time.time()
counter = 0
lastCounter = 0
lastRot = 0
prevRot = 9
speed = 0
lastClkState = GPIO.input(clk)
while(True):
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if(time.time() - anchor >= 0.005):
        anchor = time.time()
        if (clkState != lastClkState):
            if (dtState != clkState):
                counter += 0.5
            else:
                counter -= 0.5
        lastClkState = clkState
        #print(counter)
    if(time.time() - anchorT >= 0.3):
        counter = round(counter)
        anchorT = time.time()
        if(counter > lastCounter):
            print("clockWise")
            lastRot = 0
        elif(counter < lastCounter):
            print("counterClockWise")
            lastRot = 1
        else:
            print("None")
            lastRot = 2
        if(lastRot == prevRot and lastRot != 2):
            speed = counter - lastCounter
            print(str(speed/0.3) + " turns per second")
        prevRot = lastRot
        lastCounter = counter
    