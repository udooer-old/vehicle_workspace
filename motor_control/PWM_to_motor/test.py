#!/usr/bin/python3
import sys
sys.path.append('/usr/local/lib/python3/dist-packages')
from pymoos import pymoos
import time


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
        self.name = 'getOutputMOOS'
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
                self.notify('GET', self.output, -1)
        return True



def main():
    T = getOutputMOOS('localhost', 9000)
    
    try:
        print('Ctrl-C to end the program')
        while True:
            o = int(abs(T.output)/3.3*1000000)
            T.notify('MAIN', o, -1)
            time.sleep(1)
    
    except KeyboardInterrupt:
        print('\nclose the program by keyboard')
    finally:
        print('finally done!!')
if __name__ == "__main__":
    main()
