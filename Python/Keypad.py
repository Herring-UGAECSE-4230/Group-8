import RPi.GPIO as GPIO
import time
from datetime import datetime

#Setting up library and GPIOs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
binaryChar = {  #SSD character list
    'NaN':'00000000',
    1:'00001100',
    2:'11011010',
    3:'11110010',
    4:'01100110',
    5:'10110110',
    6:'10111110',
    7:'11100000',
    8:'11111110',
    9:'11110110',
    0:'11111100',
    'A':'11101110',
    'B':'00111110',
    'C':'10011100',
    'D':'01111010',
    '*':'00000001'
    }
Xpins = [2, 3, 4, 17] #X pins on keypad
char = [1, 2, 3, 'A', 4, 5, 6, 'B', 7, 8, 9, 'C', '*', 0, '#', 'D'] #Chars on keypad
Ypins = [27, 22, 23, 24] #Y pins on keypad
Dpins = [5, 6, 12, 13, 21, 20, 19, 16] #Inputs to flip flops
clockPins = [9, 10, 25, 26] #Clock pins for each flip flop
invalidPin = 8 #Error LED pin
GPIO.setup(invalidPin, GPIO.OUT, initial=GPIO.LOW)
for i in Ypins:
    GPIO.setup(i, GPIO.IN)
for l in Xpins:
    GPIO.setup(l, GPIO.OUT, initial=GPIO.LOW)
for k in Dpins:
    GPIO.setup(k, GPIO.OUT, initial=GPIO.LOW)
for h in clockPins:
    GPIO.setup(h, GPIO.OUT, initial=GPIO.HIGH)

it = 0 #Counts through each SSD for editing
inputKey = False #Checks if a key was recently pressed
inTimer = False #If the timer is currently incrementing
bCounter = 0 #How many consecutive B presses were input
am = True
state = [0, 0, 0, 0] #Saved states for each SSD
off = False
curValue = "NaN" #Value of most recent input

def incState(): #Runs every minute when the clock turns
    global am
    if(state[3] == 9): 
        state[2] = state[2] + 1 #Incrementing left M digit based on right M digit
        state[3] = 0
    else:
        state[3] = state[3] + 1 #Incrementing right M digit
    if(state[2] == 6): 
        state[1] = state[1] + 1
        state[2] = 0
    if(state[1] == 10): 
        state[0] = state[0] + 1
        state[1] = 0
    if(state[0] == 1 and state[1] == 2): #Changes AM to PM and vice versa at 12:00
        am = not am
        state[0] = 1
        state[1] = 2
    if(state[0] == 1 and state[1] == 3): #Goes from 12:00 to 1:00 like a 12 hour clock
        state[0] = 0
        state[1] = 1
        
def runTimer(): #Main loop of the clock. Updates every 60 seconds.
    print("Run Timer")
    global bCounter, inTimer, am
    
    inTimer = True
    anchor = time.time() #Creating timer that will be referenced in a minute
    while(True):
        readKeypad(Xpins[3], char[12:16])
        readKeypad(Xpins[1], char[4:8])
        if(time.time() - anchor >= 60): #Updates whenever a minute has passed
            anchor = time.time() #Resetting timer for the next minute
            incState()
            updateClock()
        if(off): #Turns off display
            for i in range(0, 4):
                displayChar('NaN')
                clock(clockPins[i])
        if(bCounter >= 3): #Returns to start menu
            state = [0, 0, 0, 0]
            am = True
            updateClock()
            bCounter = 0
            inTimer = False
            return
        
def updateClock(): #Sends rising edge to flip flops, updating their value based on state[]
    for i in range(0, 4):
        displayChar(state[i])
        if(i == 1):
            if(not am):
                GPIO.output(Dpins[7], GPIO.HIGH) #Altering the dot pin for the right H digit.
        clock(clockPins[i])
        if(i == 1):
            GPIO.output(Dpins[i], GPIO.LOW)
            
def displayChar(val): #Sets the output pins to a certain value based on the binaryChar dictionary.
    act = binaryChar[val]
    for i in range(0, 8):
        if(act[i] == '1'):
            GPIO.output(Dpins[i], GPIO.HIGH)
        else:
            GPIO.output(Dpins[i], GPIO.LOW)
            
def compareValue(val): #Checks for valid input for manual clock mode and returns False if invalid
    global am, it
    
    if(val == 'A' or val == 'B' or val == 'C' or val == 'D'): #Letters are always invalid
        return False
    else:
        if(it == 0): #Left H digit
            if(not(val == 0 or val == 1 or val == 2)): #Can only be in range 0-2.
                return False
            else:
                state[it] = val
        elif(it == 2): #Left M digit
            if(val > 5): #Can only be in range 0-5.
                return False
            else:
                state[it] = val
        else:
            if(it == 1 and state[0] == 0 and val == 0): #Turns 00 on the hour digits to 12 since 12:00 AM is midnight.
               state[0] = 1
               state[1] = 2
            elif(it == 1 and state[0] == 1 and val == 2): #Sets PM light if set to 12 PM.
               am = False
               state[1] = 2
            elif(it == 1 and ((state[0] == 1 and val >= 3) or (state[0] == 2))):
                if(state[0] == 2):
                    if(not(val == 0 or val == 1 or val == 2 or val == 3)):
                        return False
                am = False
                
                state[0] = state[0] - 1
                state[it] = val
                if(val == 0):
                    state[0] = 0
                    state[1] = 10
                elif(val == 1):
                    state[0] = 0
                    state[1] = 11
                state[1] = state[1] - 2   
            else:
                state[it] = val
        return True
def addValues():
    global inTimer, state, inputKey, off, it
    
    anchor = time.time()
    updateClock()
    switch = True
    ledon = False
    while(it <= 3):
        readKeypad(Xpins[0], char[0:4])
        readKeypad(Xpins[1], char[4:8])
        readKeypad(Xpins[2], char[8:12])
        readKeypad(Xpins[3], char[12:16])
        if(off):
            displayChar('NaN')
            for i in range(0, 4):
                clock(clockPins[i])
        else:
            updateClock()
            if(time.time() - anchor >= 0.5):
                print(switch)
                anchor = time.time()
                if(switch):
                    state[it] = 8
                    updateClock()
                    switch = False
                else:
                    state[it] = 'NaN'
                    updateClock()
                    switch = True
            if(inputKey):
                if(compareValue(curValue)):
                    if(ledon):
                        GPIO.output(invalidPin, GPIO.LOW)
                        ledon = False
                    inputKey = False
                    print(state)
                    updateClock()
                    it = it + 1
                else:
                    inputKey = False
                    GPIO.output(invalidPin, GPIO.HIGH)
                    ledon = True
    it = 0
    return
def readKeypad(row, chars):
    global bCounter, curValue, off, inputKey

    GPIO.output(row, GPIO.HIGH)
    for j in range(0, 4):
        if(GPIO.input(Ypins[j]) == 1):
            time.sleep(0.5)
            if(chars[j] == 'B'):
                print(inTimer)
                print(bCounter)
                if(inTimer):
                    curValue = 0
                    bCounter = bCounter + 1
                else:
                    print('B')
                    inputKey = True
                    curValue = 'B'
            elif(chars[j] == 'A'):
                if(inTimer):
                    curValue = 0
                    bCounter = 0
                else:
                    print('A')
                    inputKey = True
                    curValue = 'A'
            elif(chars[j] == '#'):
                if(off):
                    updateClock()
                    off = False
                else:
                    off = True
                print(off)
            elif(chars[j] == '*'):
                pass
            else:
                if(not off):
                    inputKey = True
                    print(chars[j])
                    curValue = chars[j]
    GPIO.output(row, GPIO.LOW)
def clock(Pin):
    GPIO.output(Pin, GPIO.HIGH)
    #time.sleep(0.25)
    GPIO.output(Pin, GPIO.LOW)
def startT(): #Runs the beginning menu 
    global am, curValue, inputKey, state, inTimer
    
    am = True
    state = [0, 0, 0, 0]
    updateClock()
    while(True):
        readKeypad(Xpins[0], char[0:4])
        readKeypad(Xpins[1], char[4:8])
        if(inputKey):
            inputKey = False
            if(curValue == 'A'):
                now = datetime.now()
                print(now)
                hour = '{0:02d}'.format(now.hour)
                hour = int(hour)
                if(hour == 12):
                    am = False
                if(hour == 0):
                    hour = 12
                if(hour > 12):
                    hour = hour - 12
                    am = False
                state[0] = hour//10
                state[1] = hour%10
                minute = '{0:02d}'.format(now.minute)
                state[2] = int(minute[0])
                state[3] = int(minute[1])
                print(state)
                updateClock()
                runTimer()
            if(curValue == 'B'):
                addValues()
                runTimer()
updateClock()
startT()

