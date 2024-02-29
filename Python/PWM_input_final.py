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
#setting up needed vars
anchor = time.time() #Checks every 5ms for clk and dt values
anchorT = time.time() #Checks every 300ms to display direction and speed
anchorW = time.time() #Checks every 500ms for the button
counter = 0 #changes with rotation
lastCounter = 0 #stores previous value. used to find direction and speed
thisRot = 0 #Direction of most recent rotation
prevRot = 9 #Direction of past rotation
speed = 0
lastClkState = GPIO.input(clk)

while(True):
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if(time.time() - anchor >= 0.005): #Updates counter. Checks every 5ms for debouncing.
        anchor = time.time()
        if (clkState != lastClkState):
            if (dtState != clkState):
                counter += 0.5
            else:
                counter -= 0.5
        lastClkState = clkState
        #print(counter)
    if(time.time() - anchorT >= 0.3): #Shows direction and speed. Checks every 300 ms for readability.
        counter = round(counter)
        anchorT = time.time()
        if(counter > lastCounter):
            print("clockWise")
            thisRot = 0
        elif(counter < lastCounter):
            print("counterClockWise")
            thisRot = 1
        else:
            print("None")
            thisRot = 2
        if(thisRot == prevRot and thisRot != 2): #Speed is not shown if the direction was just changed.
            speed = counter - lastCounter
            print(str(speed/0.3) + " turns per second")
        prevRot = thisRot
        lastCounter = counter
    if(time.time() - anchorW >= 0.5): #Checks for button presses. Checks every 500ms for readability.
        if(GPIO.input(sw) == False):
            anchorW = time.time()
            print("button press")