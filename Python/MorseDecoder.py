import RPi.GPIO as GPIO
import time
import numpy
morseChars = {  #character list
    '':'',
    '. -':'a',
    '- . . .':'b',
    '- . - .':'c',
    '- . .':'d',
    '.':'e',
    '. . - .':'f',
    '- - .':'g',
    '. . . .':'h',
    '. .':'i',
    '. - - -':'j',
    '- . -':'k',
    '. - . .':'l',
    '- -':'m',
    '- .':'n',
    '- - -':'o',
    '. - - .':'p',
    '- - . -':'q',
    '. - .':'r',
    '. . .':'s',
    '-':'t',
    '. . -':'u',
    '. . . -':'v',
    '. - -':'w',
    '- . . -':'x',
    '- . - -':'y',
    '- - . .':'z',
    '. - - - -':'1',
    '. . - - -':'2',
    '. . . - -':'3',
    '. . . . -':'4',
    '. . . . .':'5',
    '- . . . .':'6',
    '- - . . .':'7',
    '- - - . .':'8',
    '- - - - .':'9',
    '- - - - -':'0',
    '- . -':'over',
    '. - . - .':'out'
    }
GPIO.setmode(GPIO.BCM) #Our algorithm is able to be within 1% error range for a length down to about 10 ms.
Input = 17
#Output = 4 #unused
SPEAKER_PIN = 2
LED_PIN = 3
GPIO.setup(SPEAKER_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Input, GPIO.IN)
#GPIO.setup(Output, GPIO.OUT, initial=GPIO.LOW)
sum = 0
#while(True):
#    GPIO.output(Output, 1)
#    print(GPIO.input(Input))
counter = 0
output = '- . - . -   '
print("Press down to start")
ending = False
while(GPIO.input(Input) == 0):
    pass
anchor = time.time()
print("Starting")
prev = GPIO.input(Input)
while(counter < 9):
    time.sleep(0.02)
    if(prev != GPIO.input(Input)):
        sum += time.time() - anchor
        counter += 1
        prev = GPIO.input(Input)
        anchor = time.time()
    print(counter)
intr = sum/15
print(intr)
curr = ""
anchor = time.time()
prev = GPIO.input(Input)
currentWord = "" 
co = 0
ct = 0
tabs = ""
tabsBool = False
ledOn = False
outputFile = open('decoder output.txt', 'w')
anchor2 = time.time()
reading = True
morseWord = ""
outputFile.write(output + "| " + 'attention\n')
while(reading):
    time.sleep(0.02)
    if(prev != GPIO.input(Input)):
        times = time.time() - anchor
        #print(times)       
        prev = GPIO.input(Input)
        if(GPIO.input(Input) == 1):
            GPIO.output(2, 1)
            GPIO.output(3, 1)
            ledOn = True
            if(times >= intr*2): #next letter
                #print('3 space')
                co = co + 1
                try:
                    currentWord += morseChars[curr]
                    morseWord += curr + "   "
                except:
                    currentWord += "?"
                curr = ""
                anchor = time.time()
#            elif(time <= 0.05):
#                pass
            else:
                #print('space')
                curr += " "
                anchor = time.time()
            if(times >= intr*7): #next word
                print(morseWord)
                print(currentWord)
                if(len(morseWord.strip()) != 0):
                    if(tabsBool):
                        tabs = "    "
                    if(ending):
                        if(currentWord == 'out'):
                            outputFile.write(morseWord + "| " + currentWord)
                            reading = False
                            break
                    ending = False
                    if(currentWord == 'over'):
                     ending = True
                     tabs = ""
                    if('?' in currentWord):
                        currentWord = '?'
                    outputFile.write(tabs + morseWord + " | " + currentWord)
                    curr = ""
                    currentWord = ""
                    morseWord = ""
                    co = 0
                    ct = ct + 1
                    outputFile.write("\n")
                    tabsBool = True
                anchor = time.time()
        else:
            GPIO.output(2, 0)
            GPIO.output(3, 0)
            ledOn= False
            if(times >= intr*2):
                #print('3 pressed')
                curr += "-"
#            elif(time <= 0.05):
#                pass
            else:
                #print("pressed")
                curr += "."
            anchor = time.time()
    if(ledOn):
        GPIO.output(2, 1)
        GPIO.output(3, 1)
    if(time.time() - anchor2 > 0.25):
        anchor2 = time.time()
        print(curr)
        print(currentWord)
outputFile.close()
