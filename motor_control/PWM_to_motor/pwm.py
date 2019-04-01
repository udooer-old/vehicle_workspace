import pigpio
import time

PWM_PIN = 18
PWM_FREQ = 800
pi = pigpio.pi()

try:
    print('Ctrl-C to end the program')
    while True:
        for i in range(0,50):
            pi.hardware_PWM(PWM_PIN, PWM_FREQ, i*20000)
            time.sleep(0.1)
        for i in range(49,-1,-1):
            pi.hardware_PWM(PWM_PIN, PWM_FREQ, i*20000)
            time.sleep(0.1)
except KeyboardInterrupt:
    print('\nclose the program by keyboard')
finally:
    pi.set_mode(PWM_PIN, pigpio.INPUT)
