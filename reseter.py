# reseter
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
    state = resetState.INIT
    trigger = False
    reset_period = 10 # seconds
    reset_dwell  = 100 # milliseconds

    sm = None #state machine state variable

    def __init__(self):
        """ Constructor goes here """
        state = resetState.INIT
        trigger = False
        sm = {  resetState.INIT: FTReseter.init,
                resetState.RESET: FTReseter.reset,
                resetState.SET:   FTReseter.set
         }
        logging.basicConfig(format=format, filename= 'log.log', level=logging.INFO, datefmt="%H:%M:%S")

    def set_period (self, p):
        reset_period = p

    def set_dwell(self, d):
        reset_dwell = d


    def init(self):
        # init initialise the output pins 
        log.info("init.")
        try:
            state = SET
            d = ftd.open(0)    # Open first FTDI device
            di = d.getDeviceInfo() 

            OP = 0x01            # Bit mask for output D0
            d.setBitMode(OP, 1)  # Set pin as output, and async bitbang mode
            d.write(str(OP))     # Set output high
            d.write(str(0))      # Set output low
        except:
            logging.info("Exception")
            state = INIT
            d.close()
        else:
            state = SET    

        time.sleep(2)
        return    

    def reset(self):
        logging.info("reset.")
        #reset

        state = Set   
        time.sleep(2)
        return

    def set(self):        
        logging.info("set.")
        if trigger:  
            state = RESET
        
    def reseter_state_machine_run(self):
        loggin.info("reseter_state_machine_run")



if __name__ == "__main__":
    init_reseter()