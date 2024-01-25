import pigpio #set up pigpio library
pi=pigpio.pi()
pi.set_PWM_frequency(26, int(input("frequency: ")))# get input for freq
pi.set_PWM_dutycycle(26, int(input("duty(0 to 255): ")))# and duty
