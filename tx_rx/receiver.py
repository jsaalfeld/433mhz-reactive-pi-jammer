import RPi.GPIO as GPIO
import logging
from time import time
from utils.helpers import precise_sleep

class Singleton(type):
    _instances = {}
    LOG = logging.getLogger('433_jammer.Receiver.Singleton')
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Receiver(metaclass=Singleton):
    pass
    data_pin = 0
    gnd_pin = 0
    vcc_pin = 0
    sender = None
    global LOG
    LOG = logging.getLogger('433_jammer.Receiver')

    def __init__(self, data_pin, gnd_pin, vcc_pin, sync_length, tolerance, MAX_SYNC):
        self.data_pin = data_pin
        self.gnd_pin = gnd_pin
        self.vcc_pin = vcc_pin
        self.last_rise = time()
        self.old_state = GPIO.LOW
        self.MAX_SYNC = MAX_SYNC
        self.sync = [0] * MAX_SYNC
        self.sync_count = 0
        self.tolerance = tolerance / 1000000
        self.last_sync = None
        self.sync_length = sync_length / 1000000
        # For receiving, set the data_pin as input
        GPIO.setup(self.data_pin, GPIO.IN)
        LOG.debug('done')
     
    def skip(self, quantity):
        """skips rising edges with a given quantity of edges"""
        LOG.debug('skipping edges')
        
        
        while True:
            curr_time = time()
            state = GPIO.input(self.data_pin)
            
            if state == GPIO.HIGH and self.old_state == GPIO.LOW:
                quantity -= 1
            
            self.old_state = state
            
            if quantity < 0:
                return curr_time
            
    def listen(self):
        """identifies sync signals for a given sync pulse length"""
        
        LOG.debug('listening for sync signals')
        
        while True:
            check = False
            state = GPIO.input(self.data_pin)
            curr_time = time()

            if self.sync_count >= self.MAX_SYNC:
                self.sync_count = 0
                
            sync_delay = self.last_rise + (self.sync_length)
                        
            if state == GPIO.HIGH and self.old_state == GPIO.LOW:
                # rising edge detected
                if (sync_delay - self.tolerance < curr_time < sync_delay + self.tolerance):
                    # possible sync detected
                    if self.last_sync:
                        if (curr_time - self.last_sync) > (4000 / 1000000):
                            # if last possible sync signal is too long ago, it is just random noise
                            self.sync = [0] * self.MAX_SYNC
                            LOG.debug('reset')
                    
                    self.sync[self.sync_count] = 1
                    self.last_sync = curr_time
                    self.sync_count += 1
                    
                    check = self.check_sync()
                    
                self.last_rise = curr_time
            self.old_state = state
            
            # if sync signal detected return time stamp for precise timing
            if check:
                self.sync = [0] * self.MAX_SYNC
                LOG.debug("sync detected")
                return curr_time
            
##    def listen(self, freq, clock, sample, duty):
##        sample_length = float(1/(sample*1000))
##        self.LOG.debug('The length of one sample is: ' + str(sample_length) + 's')
##        k = 10000
##        i = 0
##        test = []
##        while True:
##            time.sleep(sample_length)
##            test.append(GPIO.input(self.data_pin))
##            i += 1
##            if i >= k:
##                break
##        for entry in test:
##            if entry != 0:
##                print(entry)        

    def check_sync(self):
        """checks for sync signal and returns true if sync signal is detected"""
        LOG.debug('checking')
        check = False
        for cnt in range(0, self.MAX_SYNC):
            if self.sync[cnt] == 1:
                check = True
            else:
                return False
        return check


    

    