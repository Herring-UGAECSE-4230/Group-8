import RPi.GPIO as GPIO
import time
import numpy
morseChars = {  #character list
    'a':'. -',
    'b':'- . . .',
    'c':'- . - .',
    'd':'- . .',
    'e':'.',
    'f':'. . - .',
    'g':'- - .',
    'h':'. . . .',
    'i':'. .',
    'j':'. - - -',
    'k':'- . -',
    'l':'. - . .',
    'm':'- -',
    'n':'- .',
    'o':'- - -',
    'p':'. - - .',
    'q':'- - . -',
    'r':'. - .',
    's':'. . .',
    't':'-',
    'u':'. . -',
    'v':'. . . -',
    'w':'. - -',
    'x':'- . . -',
    'y':'- . - -',
    'z':'- - . .',
    '1':'. - - - -',
    '2':'. . - - -',
    '3':'. . . - -',
    '4':'. . . . -',
    '5':'. . . . .',
    '6':'- . . . .',
    '7':'- - . . .',
    '8':'- - - . .',
    '9':'- - - - .',
    '0':'- - - - -',
    ' ':' '
    }
GPIO.setmode(GPIO.BCM) #Our algorithm is able to be within 1% error range for a length down to about 10 ms.
SPEAKER_PIN = 2
LED_PIN = 3
GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)

global length
length = 100 #length of MC unit in milliseconds

with open ('encoderDemo.txt') as file:
    lines=[line.rstrip() for line in file.readlines()]
    
outputFile = open('encoder output.txt', 'w')
output = ['-.-.- | attention']
morseArr = ['- . - . -']
for i in lines: #iterates thru each line
    
    words = i.split() #divides line by spaces into words
    
    it = 0
    for j in words: #iterates thru each word
        currentWord = "\n"
        if it != 0:
            currentWord += "       "
        for letter in j:
            currentWord += morseChars[letter]
            currentWord += "   "
        morseArr.append(currentWord.strip())
        currentWord = currentWord[0:len(currentWord)-2]
        currentWord += " | " + j
        output.append(currentWord) #end of word
        it += 1
    morseArr.append("- . -")
    output.append('\n-.- | over')   
morseArr.append(". - . - .")
output.append('\n.-.-. | out') #end of file
outputFile.writelines(output)
outputFile.close()


def readFreq():
    global length
    print("Enter duration of a MC unit in ms:")
    length = float(input())

readFreq()


if(length > 50):
    times = time.perf_counter()
    it = 0
    for i in morseArr:
        for j in i:
            test = 1
            rate = 1
            if(j == " "):
                test = 0
            if(j == "-"):
                rate = 3
            for i in range(0, rate):
                it += 1
                GPIO.output(2, test)
                GPIO.output(3, test)
                time.sleep(length/1000)
        for i in range(0, 7):
                it += 1
                GPIO.output(2, 0)
                GPIO.output(3, 0)
                time.sleep(length/1000)
    timee = time.perf_counter()
    print((timee - times)/it)