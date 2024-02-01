import RPi.GPIO as GPIO
import time
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
Ypins = [27, 22, 10, 9]
Dpins = [5, 6, 12, 13, 21, 20, 19, 16]
clockPin = 18
oldValue = 'NaN'
off = False;
GPIO.setup(clockPin, GPIO.OUT, initial=GPIO.LOW)
curValue = "NaN";
for i in Ypins:
    GPIO.setup(i, GPIO.IN)
for l in Xpins:
    GPIO.setup(l, GPIO.OUT, initial=GPIO.LOW)
for k in Dpins:
    GPIO.setup(k, GPIO.OUT, initial=GPIO.LOW)
def displayChar(val):
    act = binaryChar[val]
    for i in range(0, 8):
        if(act[i] == '1'):
            GPIO.output(Dpins[i], GPIO.HIGH)
        else:
            GPIO.output(Dpins[i], GPIO.LOW)
def readKeypad(row, chars):
    global curValue
    global off
    GPIO.output(row, GPIO.HIGH)
    for j in range(0, 4):
        if(GPIO.input(Ypins[j]) == 1):
            time.sleep(0.5)
            if(chars[j] == '#'):
                if(off):
                    off = False
                else:
                    off = True
            else:
                if(not off):
                    curValue = chars[j]
    GPIO.output(row, GPIO.LOW)
while True:
    
    readKeypad(Xpins[0], char[0:4])
    readKeypad(Xpins[1], char[4:8])
    readKeypad(Xpins[2], char[8:12])
    readKeypad(Xpins[3], char[12:16])
    print(curValue)
    if(not off):
        displayChar(curValue)
    else:
        displayChar('NaN')
    GPIO.output(clockPin, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(clockPin, GPIO.LOW)