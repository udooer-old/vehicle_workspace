import threading
import queue
import time
import pigpio

def read_kbd_input(Q):
    print('Ready for keyboard input:')
    while (True):
        input_str = input()
        Q.put(input_str)

def main():
    EXIT_COMMAND = "exit"
    print('press "exit" to close the program')
    Q = queue.Queue()
    thread = threading.Thread(target=read_kbd_input, args=(Q,), daemon=True)
    thread.start()

    #motor pin config 
    PWM_PIN_left = 18
    left_1 = 23
    left_2 = 24
    PWM_PIN_right = 13
    right_1 = 22
    right_2 = 27
    PWM_FREQ = 800
    pi = pigpio.pi()
    vol = int(3.2/3.3*1000000)

    while (True):
        if (Q.qsize() > 0):
            input_str = Q.get()
            print("input_str = {}".format(input_str))
            if (input_str == EXIT_COMMAND):
                print("Exiting program")
                pi.set_mode(PWM_PIN_left, pigpio.INPUT)
                pi.set_mode(left_1, pigpio.INPUT)
                pi.set_mode(left_2, pigpio.INPUT)
                pi.set_mode(PWM_PIN_right, pigpio.INPUT)
                pi.set_mode(right_1, pigpio.INPUT)
                pi.set_mode(right_2, pigpio.INPUT)
                break
            elif (input_str == "f"):
                vol1 = int(0.8/3.3*1000000)
                vol2 = int(0.8/3.3*1000000)
                pi.hardware_PWM(PWM_PIN_left, PWM_FREQ, vol1)
                pi.write(left_1,0)
                pi.write(left_2,1)
                pi.hardware_PWM(PWM_PIN_right, PWM_FREQ, vol2)
                pi.write(right_1,1)
                pi.write(right_2,0)
            elif (input_str == "b"):
                pi.hardware_PWM(PWM_PIN_left, PWM_FREQ, vol)
                pi.write(left_1,1)
                pi.write(left_2,0)
                pi.hardware_PWM(PWM_PIN_right, PWM_FREQ, vol)
                pi.write(right_1,0)
                pi.write(right_2,1)
            elif (input_str == "r"): 
                pi.hardware_PWM(PWM_PIN_left, PWM_FREQ, vol)
                pi.write(left_1,0)
                pi.write(left_2,1)
                pi.hardware_PWM(PWM_PIN_right, PWM_FREQ, vol)
                pi.write(right_1,0)
                pi.write(right_2,1)
            elif (input_str == "l"):
                pi.hardware_PWM(PWM_PIN_left, PWM_FREQ, vol)
                pi.write(left_1,1)
                pi.write(left_2,0)
                pi.hardware_PWM(PWM_PIN_right, PWM_FREQ, vol)
                pi.write(right_1,1)
                pi.write(right_2,0)
            else :
                pi.set_mode(PWM_PIN_left, pigpio.INPUT)
                pi.set_mode(left_1, pigpio.INPUT)
                pi.set_mode(left_2, pigpio.INPUT)
                pi.set_mode(PWM_PIN_right, pigpio.INPUT)
                pi.set_mode(right_1, pigpio.INPUT)
                pi.set_mode(right_2, pigpio.INPUT)
        time.sleep(0.01)
    print("End.")

if __name__ == '__main__':
    main()
