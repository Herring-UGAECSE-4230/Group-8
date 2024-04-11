#importing of needed libraries
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
    '. - . - .':'out'
    }
GPIO.setmode(GPIO.BCM) #Our algorithm is able to be within 1% error range for a length down to about 10 ms.
Input = 17

#setting up of pins used
SPEAKER_PIN = 2
LED_PIN = 3
GPIO.setup(SPEAKER_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Input, GPIO.IN)
#GPIO.setup(Output, GPIO.OUT, initial=GPIO.LOW)
sum = 0#sum use to add all of the time it takes to complete attention

counter = 0
output = '- . - . -   '
print("Press down to start")
ending = False
while(GPIO.input(Input) == 0):#once key state is switched to pressed the while loop will break and the attention input section will begin
    pass
anchor = time.time()#setting the anchor for the current time
print("Starting")
prev = GPIO.input(Input)#saves pervious input to see when it changes
while(counter < 9):
    time.sleep(0.02)#small software debounce
    if(prev != GPIO.input(Input)):#checks if the state has changed from pressed to unpressed or vice versa
        sum += time.time() - anchor#adds time elapsed to total time
        counter += 1
        prev = GPIO.input(Input)
        anchor = time.time()#sets a new anchor to be used next state change
    print(counter)
intr = sum/15#calculates the users average interval time based on the attention input
print(intr)
#sets up variables to be used in main polling loop
curr = ""
anchor = time.time() 
prev = GPIO.input(Input)
currentWord = ""
tabs = ""#string that dynamically changes based on if a tab is needed
tabsBool = False
ledOn = False
outputFile = open('decoder output.txt', 'w')
anchor2 = time.time()#sets a second anchor to be used to print the current word and morse string
reading = True
morseWord = ""#used to save the morse code of the current word
outputFile.write(output + "| " + 'attention\n')#writes attention to the output file
while(reading):
    time.sleep(0.02)#used as a small software debounce
    if(prev != GPIO.input(Input)):#checks if the state has changed
        times = time.time() - anchor#calcuates the time that the last high or low took based on the anchor   
        prev = GPIO.input(Input)
        if(GPIO.input(Input) == 1):#if the current state is pressed times has tracked the time of the last space
            GPIO.output(2, 1)#output high to speaker
            GPIO.output(3, 1)#output high to led
            ledOn = True
            if(times >= intr*2): #next letter because time is two times greater than current set interval
                try:#used in case value is not found in the dictionary
                    currentWord += morseChars[curr]#add tanslated letter to the current word
                    morseWord += curr + "   "#adds the current morsecode string to the Morseword for the output
                except:
                    currentWord += "?"#current word gets a question mark meaning the whole word is set to question mark if the morse code is not recognized
                curr = ""
                anchor = time.time()
            else:#case where the time was less than two times the interval space added
                curr += " "
                anchor = time.time()
            if(times >= intr*7): #next word because time is seven times greater than current set interval
                print(morseWord)
                print(currentWord)
                if(len(morseWord.strip()) != 0):#checks if the input is an empty string or only spaces
                    if(tabsBool):#checks if tab is needed
                        tabs = "    "
                    if(ending):
                        if(currentWord == 'k'):#checks if the word is over and ends if lsat word was out
                            currentWord = 'over'
                            outputFile.write(morseWord + "| " + currentWord)
                            reading = False
                            break#ends the loop
                    ending = False
                    if(currentWord == 'out'):
                     ending = True#sets a flag to check if the program will end
                     tabs = ""
                    if('?' in currentWord):#if one ? is found sets the whole word to ? as intended
                        currentWord = '?'
                    outputFile.write(tabs + morseWord + " | " + currentWord)#writes the morse code and the word to the output file
                    curr = ""#clears all the vars
                    currentWord = ""
                    morseWord = ""
                    outputFile.write("\n")
                    tabsBool = True
                anchor = time.time()
        else:
            GPIO.output(2, 0)#turns of the led because the key is now up
            GPIO.output(3, 0)
            ledOn= False
            if(times >= intr*2):
                curr += "-"#adds a dash if time is two times bigger than the interval
            else:
                curr += "."#adds a period if the interval is less than two times the interval
            anchor = time.time()
    if(ledOn):
        GPIO.output(2, 1)
        GPIO.output(3, 1)
    if(time.time() - anchor2 > 0.25):
        anchor2 = time.time()
        print(curr)
        print(currentWord)
outputFile.close()#closes the output file to finish writing
