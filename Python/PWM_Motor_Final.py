import RPi.GPIO as GPIO
import time
#Setting up library and GPIOs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
clk = 21
dt = 20
sw = 26
ir = 15
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ir, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#setting up needed vars
anchor = time.time() #Checks every 5ms for clk and dt values
anchorT = time.time()
anchorW = time.time() #Checks every 500ms for the button
counter = 0 #changes with rotation
freq = 0
switch = True
lastCounter = 0 #stores previous value. used to find direction and speed
lastClkState = GPIO.input(clk)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 0.1)
pwm.start(50)
numHigh = 0
latch = False
IRinput = GPIO.input(ir)
while(True):
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if(time.time() - anchor >= 0.005): #Updates counter. Checks every 5ms for debouncing.
        if(switch):
            anchor = time.time()
            if (clkState != lastClkState):
                if (dtState != clkState):
                    counter += 0.5
                else:
                    counter -= 0.5
            lastClkState = clkState
            if(round(counter) > 25):
                counter = 25
            if(round(counter) < 0):
                counter = 0
            if(round(counter) * 20 != freq):
                freq = round(counter) * 20
                if(freq > 0):
                    pwm.ChangeFrequency(freq)
                    print(freq)
                    print(round(counter))
                    #print to ir
    if(time.time() - anchorT >= 0.5):
        numHigh = (numHigh*120)/3
        print("Actual freq: " + str(numHigh))
        numHigh = 0
    if(time.time() - anchorW >= 0.5): #Checks for button presses. Checks every 500ms for readability.
        if(GPIO.input(sw) == False):
            if(switch):
                pwm.ChangeFrequency(0)
            else:
                pwm.ChangeFrequency(freq)
            switch = not (switch)
            anchorW = time.time()
            print("button press")
    IRinput = GPIO.input(ir)
    if(IRinput == True and latch):
        numHigh += 1
        latch = False
    else:
        latch = True