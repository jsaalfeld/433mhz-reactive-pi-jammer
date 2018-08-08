import RPi.GPIO as GPIO
import logging
from utils.helpers import precise_sleep
from time import time

class Singleton(type):
    _instances = {}
    LOG = logging.getLogger('433_jammer.Sender.Signleton')
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Sender(metaclass=Singleton):
    pass
    data_pin = 0
    gnd_pin = 0
    vcc_pin = 0
    receiver = None
    global LOG
    LOG = logging.getLogger('433_jammer.Sender')
    
    def __init__(self, data_pin, recv_data_pin, gnd_pin, vcc_pin):
        self.data_pin = data_pin
        self.recv_data_pin = recv_data_pin
        self.gnd_pin = gnd_pin
        self.vcc_pin = vcc_pin
        self.last_state = None
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(27, GPIO.IN)

    def send_checksum(self, curr_time):
        """sends a checksum of 0xFF to destroy the data packet"""
        first = True
        curr_time = time()
        LOG.debug("sending checksum")
        cnt = 6
        self.last_state = GPIO.LOW
        
   
##        if first:
##            GPIO.output(self.data_pin, GPIO.HIGH)
##            precise_sleep((500 / 1000000), curr_time)
##            first = False
##        else:
##            curr_time = time()
##            GPIO.output(self.data_pin, GPIO.HIGH)
##            precise_sleep((500 / 1000000), curr_time)
##            
##        GPIO.output(self.data_pin, GPIO.LOW)
##        
##        cnt -= 1
        
        while cnt >= 1:
            if not first:
                curr_time = time()
            first = False
                
            state = GPIO.input(self.recv_data_pin)
##            LOG.debug(last_state)
##            LOG.debug(state)
##            LOG.debug(cnt)
            
            if state == GPIO.HIGH and self.last_state == GPIO.LOW:
                LOG.debug('count: ' + str(cnt))
                cnt -= 1
                GPIO.output(self.data_pin, GPIO.HIGH)
                precise_sleep((430 / 1000000), curr_time)
                GPIO.output(self.data_pin, GPIO.LOW) 
            
            self.last_state = state
            
        return True
