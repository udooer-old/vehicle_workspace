#!/usr/bin/python3
import sys
sys.path.append('/usr/local/lib/python3/dist-packages')
from pymoos import pymoos
import time
import pigpio

class getOutputMOOS(pymoos.comms):
    """pongMOOS is an example python MOOS app.
    It registers for 'PING' and responds with 'PONG' and the number of received
    'PING's

    Attributes:
        moos_community: a string representing the address of the Community
        moos_port:      an interger defining the port
    """
    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(getOutputMOOS, self).__init__()
        self.server = moos_community
        self.port = moos_port
        self.name = 'getOutputPyMOOS'
        self.iter = 0
        self.output = 0

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)
        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return self.register('OUTPUT_VOLTAGE', 0)

    def __on_new_mail(self):
        """OnNewMail callback"""
        for msg in self.fetch():
            if msg.key() == 'OUTPUT_VOLTAGE':
                self.output = msg.double()
        return True



def main():
    T = getOutputMOOS('localhost', 9000)
    
    PWM_PIN_left = 18
    left_1 = 23
    left_2 = 24
    PWM_PIN_right = 13
    right_1 = 27
    right_2 = 22
    PWM_FREQ = 800
    pi = pigpio.pi()
    try:
        print('Ctrl-C to end the program')
        while True:
            O = int(abs(T.output)/3.3*1000000)
            if vol1 > 0:
                pi.hardware_PWM(PWM_PIN_left, PWM_FREQ, O+1)
                pi.hardware_PWM(PWM_PIN_right, PWM_FREQ, O+1)
                pi.write(left_1,0)
                pi.write(left_2,1)
                pi.write(right_1,1)
                pi.write(right_2,0)
             if T.output > 0:
                pi.hardware_PWM(PWM_PIN_left, PWM_FREQ, O+1)
                pi.hardware_PWM(PWM_PIN_right, PWM_FREQ, O+1)
                pi.write(left_1,0)
                pi.write(left_2,1)
                pi.write(right_1,1)
                pi.write(right_2,0)
                time.sleep(0.1)
    
    except KeyboardInterrupt:
        print('\nclose the program by keyboard')
    finally:
        pi.set_mode(PWM_PIN_left, pigpio.INPUT)
        pi.set_mode(PWM_PIN_right, pigpio.INPUT)
        pi.set_mode(left_1, pigpio.INPUT)
        pi.set_mode(left_2, pigpio.INPUT)
        pi.set_mode(right_1, pigpio.INPUT)
        pi.set_mode(right_2, pigpio.INPUT)
if __name__ == "__main__":
    main()
