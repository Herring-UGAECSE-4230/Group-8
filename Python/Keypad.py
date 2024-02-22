import RPi.GPIO as GPIO
import time
from datetime import datetime
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
binaryChar = {
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
Xpins = [2, 3, 4, 17]
char = [1, 2, 3, 'A', 4, 5, 6, 'B', 7, 8, 9, 'C', '*', 0, '#', 'D']
Ypins = [27, 22, 23, 24]
Dpins = [5, 6, 12, 13, 21, 20, 19, 16]
clockPins = [9, 10, 25, 26]
invalidPin = 8
it = 0
inputKey = False
oldValue = 'NaN'
inTimer = False
bCounter = 0
am = True
state = [0, 0, 0, 0]
off = False;
GPIO.setup(invalidPin, GPIO.OUT, initial=GPIO.LOW)
curValue = "NaN";
for i in Ypins:
    GPIO.setup(i, GPIO.IN)
for l in Xpins:
    GPIO.setup(l, GPIO.OUT, initial=GPIO.LOW)
for k in Dpins:
    GPIO.setup(k, GPIO.OUT, initial=GPIO.LOW)
for h in clockPins:
    GPIO.setup(h, GPIO.OUT, initial=GPIO.HIGH)
def incState():
    if(state[3] == 9):
        state[2] = state[2] + 1
        state[3] = 0
    else:
        state[3] = state[3] + 1
    if(state[2] == 6):
        state[1] = state[1] + 1
        state[2] = 0
    if(state[1] == 9):
        state[0] = state[0] + 1
        state[1] = 0
    if(state[0] == 1 and state[1] == 3):
        am = not am
        state[0] = 0
        state[1] = 1
def runTimer():
    global bCounter
    anchor = time.time()
    while(True):
        if(time.time() - anchor >= 60):
            anchor = time.time()
            incState()
            if(off):
                for i in range(0, 4):
                    displayChar('NAN')
                    clock(clockPins[i])
            else:
                updateClock()
        readKeypad(Xpins[1], char[4:8])
        if(bCounter >= 3):
            bCounter = 0
            inTimer = False
            return
def updateClock():
    for i in range(0, 4):
        displayChar(state[i])
        if(i == 1):
            if(not am):
                GPIO.output(Dpins[7], GPIO.HIGH)
        clock(clockPins[i])
        if(i == 1):
            GPIO.output(Dpins[i], GPIO.LOW)
def displayChar(val):
    act = binaryChar[val]
    for i in range(0, 8):
        if(act[i] == '1'):
            GPIO.output(Dpins[i], GPIO.HIGH)
        else:
            GPIO.output(Dpins[i], GPIO.LOW)
def compareValue(val):
    global it
    if(val == 'A' or val == 'B' or val == 'C' or val == 'D'):
        return False
    else:
        if(it == 0):
            if(not(val == 0 or val == 1 or val == 2)):
                return False
            else:
                state[it] = val
        else:
            if(it == 1 and ((state[0] == 1 and val >= 3) or (state[0] == 2))):
                if(state[0] == 2):
                    if(not(val == 0 or val == 1 or val == 2 or val == 3)):
                        return False
                am = False
                state[0] = state[0] - 1
                state[it] = val
                state[1] = state[1] - 2   
            else:
                state[it] = val
        return True
def addValues():
    anchor = time.time()
    global inTimer
    updateClock()
    global state
    global inputKey
    global off
    global it
    switch = True
    ledon = False
    while(it <= 4):
        readKeypad(Xpins[0], char[0:4])
        readKeypad(Xpins[1], char[4:8])
        readKeypad(Xpins[2], char[8:12])
        readKeypad(Xpins[3], char[12:16])
        if(off):
            displayChar('NaN')
            for i in range(0, 4):
                clock(clockPins[i])
        else:
            if(time.time() - anchor >= 0.5):
                anchor = time.time()
                if(switch):
                    for i in range(it, 4):
                        displayChar(8)
                    switch = False
                else:
                    for i in range(it, 4):
                        displayChar('NaN')          
                    switch = True
            if(inputKey):
                if(compareValue(curValue)):
                    if(ledon):
                        GPIO.output(invalidPin, GPIO.LOW)
                        ledon = False
                    inputKey = False
                    updateClock()
                    it = it + 1
                else:
                    inputKey = False
                    GPIO.output(invalidPin, GPIO.HIGH)
                    ledon = True
    inTimer = True
def readKeypad(row, chars):
    global bCounter
    global curValue
    global off
    global inputKey
    GPIO.output(row, GPIO.HIGH)
    for j in range(0, 4):
        if(GPIO.input(Ypins[j]) == 1):
            time.sleep(0.5)
            if(inTimer and chars[j] == 'B'):
                bCounter = bCounter + 1
            if(inTimer and chars[j] == 'A'):
                bCounter = 0
            if(chars[j] == '#'):
                if(off):
                    off = False
                else:
                    for i in range(0, 4):
                        displayChar('NAN')
                        clock(clockPins[i])
                    off = True
            if(chars[j] == '*'):
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
def startT():
    global am
    global curValue
    global inputKey
    am = True
    global state
    global inTimer
    state = [0, 0, 0, 0]
    while(True):
        readKeypad(Xpins[0], char[0:4])
        readKeypad(Xpins[1], char[4:8])
        if(inputKey):
            inputKey = False
            if(curValue == 'A'):
                inTimer = True
                now = datetime.now()
                hour = '{0:02d}'.format(now.hour)
                hour = int(hour)
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

