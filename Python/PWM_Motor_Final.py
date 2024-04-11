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
GPIO.setup(18, GPIO.OUT)


#setting up timers
anchor = time.time() #Checks every 5ms for clk and dt values
anchorT = time.time() #Checks every 3s to calculate RPM
anchorW = time.time() #Checks every 500ms for the button


counter = 80 #Tracks the position of the encoder
switch = True #True if the motor should move (switch has not been pressed yet)
IRlatch = True #True if the IRinput value can be changed.
numHigh = 0 #Counts the number of rising edges from the IR sensor in the last 3s
lastCounter = 0 #Stores previous value. used to find direction and speed
lastClkState = GPIO.input(clk) #Previous value at the clk pin on the encoder. Used to determine if the encoder is turning.

pwm = GPIO.PWM(18, 1000) #pwm will have a frequency of 1k Hz
duty = 25 #duty cycle changes to alter the RPM
expRPM = 2000 #the expected RPM according to our transfer function

pwm.start(25) 
IRinput = GPIO.input(ir) #Initializing IRinput value
while(True):
    clkState = GPIO.input(clk) #Current values of clk and dt
    dtState = GPIO.input(dt)
    
    if(time.time() - anchor >= 0.005): #Updates counter. Checks every 5ms for debouncing.
        if(switch): #Can't change duty cycle when pwm is disabled
            anchor = time.time()
            if (clkState != lastClkState): #If clkState has changed, the values of dt and clk indicate
                if (dtState != clkState):  #the direction the encoder is rotating
                    counter += 0.5
                else:
                    counter -= 0.5
            lastClkState = clkState
            
            if(round(counter) > 172): #Max and min counter values
                counter = 172
            if(round(counter) < 0):
                counter = 0
            if((round(counter) * 25) != expRPM): #If counter has changed, adjust duty cycle
                expRPM = (round(counter) * 25) #Each tick of the counter will ideally change the RPM by 25
                duty = 2.48+(0.0122*expRPM)-(0.00000238*(expRPM**2))+(0.000000000929*(expRPM**3))
                #duty = -21.7 + 0.101*expRPM - (1.27*(10**-4)*(expRPM**2)) + (8.53*(10**-8)*(expRPM**3)) - (2.96*(10**-11)*(expRPM**4)) + (5.14*(10**-15)*(expRPM**5)) - (3.48*(10**-19)*(expRPM**6))
                pwm.ChangeDutyCycle(duty) #Duty is set according to our transfer function 
                print("Expected RPM: " + str(expRPM))
                    
    if(time.time() - anchorT >= 3): #Calculating the actual RPM based on the last three seconds
        numHigh = (numHigh*20)/3 
        print("RPM " + str(numHigh))
        numHigh = 0
        anchorT = time.time()
        
    if(time.time() - anchorW >= 0.5): #Checks for button presses. Checks every 500ms for readability.
        if(GPIO.input(sw) == False):
            if(switch):
                pwm.ChangeDutyCycle(0)
            else:
                pwm.ChangeDutyCycle(duty)
            switch = not (switch)
            anchorW = time.time()
            
    IRinput = not GPIO.input(ir) #Flips the sensor reading because it's more intuitive
    if(IRinput and IRlatch): #If the input was low and became high, increment counter
        numHigh += 1
        IRlatch = False #Clears the latch while the input is high
    if(not IRinput): #Indicating the input is low again, sets the latch
        IRlatch = True
        
