#importing any needed libraries
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
#setting up neded GPIOs 
GPIO.setmode(GPIO.BCM) #Our algorithm is able to be within 1% error range for a length down to about 10 ms.
SPEAKER_PIN = 2
LED_PIN = 3
GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)

global length
length = 100 #length of MC unit in milliseconds

#opens the required input file
with open ('encoderDemo.txt') as file:
    lines=[line.rstrip() for line in file.readlines()]
#opens the output file and intializes the outut array to attention    
outputFile = open('encoder output.txt', 'w')
output = ['-.-.- | attention']
morseArr = ['- . - . -']
for i in lines: #iterates thru each line
    
    words = i.split() #divides line by spaces into words
    
    it = 0
    for j in words: #iterates thru each word
        currentWord = "\n"#adds the new line before each word after attention
        if it != 0:
            currentWord += "       "#adds a tab space if the word is the first on the line
        for letter in j:
            currentWord += morseChars[letter]#each letter has its morse code value saved to a temp varaible
            currentWord += "   "#a blank is added between letter
        morseArr.append(currentWord.strip())#adds the morse code for each word to the morse arr so it can be iterated through for the led and speaker
        currentWord = currentWord[0:len(currentWord)-2]#cuts of the added space on the final letter ???
        currentWord += " | " + j #adds the word and | to teh end of the morse code section for that word
        output.append(currentWord) #end of word
        it += 1
    morseArr.append("- . -")#adds the morse code for over to the array used for led and speaker after each sentence
    output.append('\n-.- | over')#adds the morse code for over to the output file after each sentence   
morseArr.append(". - . - .")#adds the morse code for out to the array used for led and speaker at the end
output.append('\n.-.-. | out') #adds the morse code for out to the output file at the end
outputFile.writelines(output)
outputFile.close()

#asks and waits for a user to input a freq
def readFreq():
    global length
    print("Enter duration of a MC unit in ms:")
    length = float(input())
#called on the start of the program
readFreq()


if(length > 50):#sets the limit for freq that are considered too small based on instructions
    times = time.perf_counter()#used to calculate the average of the output intervals
    it = 0#uses an iterator to save how many times there is an output interval
    for i in morseArr:#iterates through the saved MorseArr to enabl the led and speaker on each dash and dot
        for j in i:
            test = 1#defaut value of one interval for a period
            rate = 1
            if(j == " "):
                test = 0#changes time to none if it is a blank being output
            if(j == "-"):
                rate = 3#changes value to 3 times as long if it is a dash being output
            for i in range(0, rate):#outputs the values to the speaker and led based on the current char 
                it += 1
                GPIO.output(2, test)
                GPIO.output(3, test)
                time.sleep(length/1000)
        for i in range(0, 7):#used to output the long blank after each word
                it += 1
                GPIO.output(2, 0)
                GPIO.output(3, 0)
                time.sleep(length/1000)
    timee = time.perf_counter()#sets final time so how long execution took on average can be calculated
    print((timee - times)/it)#prints the average time