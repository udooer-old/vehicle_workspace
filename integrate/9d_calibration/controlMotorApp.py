#!/usr/bin/python3
import sys
sys.path.append('/usr/local/lib/python3/dist-packages')
from pymoos import pymoos
import time
import pigpio

class controlMotorMOOS(pymoos.comms):
    """pongMOOS is an example python MOOS app.
    It registers for 'PING' and responds with 'PONG' and the number of received
    'PING's

    Attributes:
        moos_community: a string representing the address of the Community
        moos_port:      an interger defining the port
    """
    def __init__(self, moos_community, moos_port):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(controlMotorMOOS, self).__init__()
        self.server = moos_community
        self.port = moos_port
        self.name = 'controlMotor'
        self.state = ""

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)
        self.run(self.server, self.port, self.name)

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return self.register('CALIBRATION', 0)

    def __on_new_mail(self):
        """OnNewMail callback"""
        for msg in self.fetch():
            if msg.key() == 'CALIBRATION':
                self.state = msg.string()
        return True



def main():
    M = controlMotorMOOS('localhost', 9000)
    
    PWM_PIN_left = 18
    left_1 = 23
    left_2 = 24
    PWM_PIN_right = 13
    right_1 = 22
    right_2 = 27
    PWM_FREQ = 800
    vol = int(1.2/3.3*1000000)
    pi = pigpio.pi()
    while True:
        if (M.state == "start"):
            pi.hardware_PWM(PWM_PIN_left, PWM_FREQ, vol)
            pi.hardware_PWM(PWM_PIN_right, PWM_FREQ, vol)
            pi.write(left_1,0)
            pi.write(left_2,1)
            pi.write(right_1,0)
            pi.write(right_2,1)
            time.sleep(0.1)
        elif (M.state == "finish"):
            pi.set_mode(PWM_PIN_left, pigpio.INPUT)
            pi.set_mode(PWM_PIN_right, pigpio.INPUT)
            pi.set_mode(left_1, pigpio.INPUT)
            pi.set_mode(left_2, pigpio.INPUT)
            pi.set_mode(right_1, pigpio.INPUT)
            pi.set_mode(right_2, pigpio.INPUT)
if __name__ == "__main__":
    main()
