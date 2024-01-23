import pigpio
pi=pigpio.pi()
pi.set_PWM_frequency(26, int(input("frequency: ")))
pi.set_PWM_dutycycle(26, int(input("duty(0 to 255): ")))
while True:
    pass
pi.set_PWM_dutycycle(26, 0)