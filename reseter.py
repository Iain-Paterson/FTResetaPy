# reseter
import sys
import ftd2xx as ftd
import logging
import threading
from threading import Lock
import time
from enum import Enum
rs ={}
class resetState( Enum ):
    INIT  = 0
    RESET = 1
    SET   = 2

def init_reseter():
    rs = FTReseter()
    rs.init()
    rs.reseterTHD.join()

class FTReseter:
    """ FTReseter class...."""
    device = None
    state = resetState.INIT
    trigger = False
    reset_period = 10 # seconds
    reset_dwell  = 0.100 # milliseconds
    reseterTHD = None
    lock =Lock()

    OP = 0x01            # Bit mask for output D0

    #global.sm = None #state machine state variable

    def __init__(self):
        """ Constructor goes here """
        #self.lock = Lock()
        logging.basicConfig(filename = 'ex.log', level=logging.DEBUG, format= '%(asctime)s %(message)s',  datefmt='%m/%d/%Y %I:%M:%S %p')
        print("__init__")

    def set_period (self, p):
        self.lock.acquire()
        try:
            self.reset_period = p
        finally:
            self.lock.release()

    def set_dwell(self, d):
        self.lock.acquire()
        try:
            self.reset_dwell = d
        finally:
            self.lock.release()

    def get_period(self):
        self.lock.acquire()
        try:
            p =self.reset_period 
        finally:
            self.lock.release()
        return p

    def get_dwell(self):
        self.lock.acquire()
        try:
            d =self.reset_dwell
        finally:
            self.lock.release()        
        return d

    def init(self):
        # init initialise the output pins 
        logging.info("init.")
        
        try:
            self.state = resetState.SET
            try:
                self.device = ftd.open(0)    # Open first FTDI device
            except:
                self.device = None
                return

            di = self.device.getDeviceInfo() 

            OP = 0x01            # Bit mask for output D0
            self.device.setBitMode(OP, 1)  # Set pin as output, and async bitbang mode
            self.device.write(str(OP))     # Set output high
            self.device.write(str(0))      # Set output low
        except:
            logging.info("Exception")
            state = resetState.INIT
            if self.device is not None:
                self.device.close()
        else:
            state = resetState.SET    
            self.reseterTHD = threading.Thread(target = reseter_state_machine_run ,args = (self,) )
            self.reseterTHD.start()
        
        return state    

    def reset(self):
        self.device.write(str(0))      # Set output low
        time.sleep(self.get_dwell())   # pull reset low for say 50 ms
        self.device.write( str(self.OP))    # set reset pin high 
        logging.info("reset.")
        #reset

        self.state = resetState.SET
        return resetState.SET

    def set(self):        
        self.device.write(str(self.OP))     # Set output high
        logging.info("set.")
        time.sleep(self.get_period() - self.get_dwell()) 
        return resetState.RESET


state = resetState.INIT
        #self.trigger = False

def reseter_state_machine_run(self):
    logging.info("reseter_state_machine_run")
    rs = self
    sm = {  resetState.INIT: rs.init,
            resetState.RESET: rs.reset,
            resetState.SET:   rs.set
        }
    state = resetState.RESET
    while True:
       
        state = sm[state]()
        time.sleep(1)
        print ( "Sleeping!")



if __name__ == "__main__":
    init_reseter()
    logging.info('Exiting reserer.py main')