# reseter
import sys
import ftd2xx as ftd
import logging
import threading
import time
from enum import Enum

class resetState( Enum ):
    INIT  = 0
    RESET = 1
    SET   = 2

    rs = None


def init_reseter():
    rs = FTReseter()
    rs.init()

class FTReseter:
    """ FTReseter class...."""
    device = None
    state = resetState.INIT
    trigger = False
    reset_period = 10 # seconds
    reset_dwell  = 100 # milliseconds

    sm = None #state machine state variable

    def __init__(self):
        """ Constructor goes here """
        self.state = resetState.INIT
        self.trigger = False
        self.sm = {  resetState.INIT: FTReseter.init,
                resetState.RESET: FTReseter.reset,
                resetState.SET:   FTReseter.set
         }
        #logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        print("__init__")

    def set_period (self, p):
        self.reset_period = p

    def set_dwell(self, d):
        self.reset_dwell = d


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
            self.state = resetState.INIT
            if self.device is not None:
                self.device.close()
        else:
            self.state = resetState.SET    
            self.device.close()
        time.sleep(2)
        return    

    def reset(self):
        self.device.write(str(0))      # Set output low
        time.sleep(0.05) # pull reset low for 50 ms
        logging.info("reset.")
        #reset

        self.state = resetState.Set   
        time.sleep(2)
        return

    def set(self):        
        self.device.write(str(OP))     # Set output high
        logging.info("set.")
        if self.trigger:  
            self.state = resetState.RESET
        
    def reseter_state_machine_run(self):
        logging.info("reseter_state_machine_run")



if __name__ == "__main__":
    init_reseter()
    logging.info('Exiting reserer.py main')