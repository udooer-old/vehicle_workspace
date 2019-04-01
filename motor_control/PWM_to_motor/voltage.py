import pigpio
import time

PWM_PIN_positive = 18
PWM_PIN_negative = 12
PWM_FREQ = 800
pi = pigpio.pi()
voltage= float(input('enter the voltage value(-3.3v ~ 3.3v):'))
con3 = int(abs(voltage)/3.3*1000000)
try:
    print('Ctrl-C to end the program')
    while True:
        if voltage > 0:
            pi.hardware_PWM(PWM_PIN_positive, PWM_FREQ, con3)
            pi.write(PWM_PIN_negative,0)
            time.sleep(0.1)
        if voltage < 0:
            pi.hardware_PWM(PWM_PIN_negative, PWM_FREQ, con3)
            pi.write(PWM_PIN_positive, 0)
            time.sleep(0.1)

except KeyboardInterrupt:
    print('\nclose the program by keyboard')
finally:
    pi.set_mode(PWM_PIN_positive, pigpio.INPUT)
    pi.set_mode(PWM_PIN_negative, pigpio.INPUT)
