import wiringpi
wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(26)
wiringpi.softToneWrite(26, int(input("frequency: ")))
while True:
    pass
wiringpi.softToneWrite(26, 0)