import pigpio
import time

PWM_PIN_left= 18
left_1 = 23
left_2 = 24
PWM_PIN_right= 12
right_1 = 22
right_2 = 27
PWM_FREQ = 800
pi = pigpio.pi()
voltage= float(input('enter the voltage value(-3.3v ~ 3.3v):'))
con3 = int(abs(voltage)/3.3*1000000)
try:
    print('Ctrl-C to end the program')
    while True:
        if voltage > 0:
            pi.hardware_PWM(PWM_PIN_left, PWM_FREQ, con3)
            pi.write(left_1,1)
            pi.write(left_2,0)
            pi.hardware_PWM(PWM_PIN_right, PWM_FREQ, con3)
            pi.write(right_1,1)
            pi.write(right_2,0)
            time.sleep(0.1)
        if voltage < 0:
            pi.hardware_PWM(PWM_PIN_left, PWM_FREQ, con3)
            pi.write(left_1, 0)
            pi.write(left_2, 1)
            pi.hardware_PWM(PWM_PIN_right, PWM_FREQ, con3)
            pi.write(right_1,1)
            pi.write(right_2,0)
            time.sleep(0.1)

except KeyboardInterrupt:
    print('\nclose the program by keyboard')
finally:
    pi.set_mode(PWM_PIN_left, pigpio.INPUT)
    pi.set_mode(left_1, pigpio.INPUT)
    pi.set_mode(left_2, pigpio.INPUT)
    pi.set_mode(PWM_PIN_right, pigpio.INPUT)
    pi.set_mode(right_1, pigpio.INPUT)
    pi.set_mode(right_2, pigpio.INPUT)
