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
    
    def __init__(self, data_pin, gnd_pin, vcc_pin):
        self.data_pin = data_pin
        self.gnd_pin = gnd_pin
        self.vcc_pin = vcc_pin
        GPIO.setup(self.data_pin, GPIO.OUT)

    def send_checksum(self, curr_time):
        """sends a checksum of 0xFF to destroy the data packet"""
        LOG.debug("sending checksum")
        cnt = 8
        first = True
        last_state = GPIO.input(self.data_pin)
        
   
        if first:
            GPIO.output(self.data_pin, GPIO.HIGH)
            precise_sleep((500 / 1000000), curr_time)
            first = False
        else:
            curr_time = time()
            GPIO.output(self.data_pin, GPIO.HIGH)
            precise_sleep((500 / 1000000), curr_time)
            
        GPIO.output(self.data_pin, GPIO.LOW)
        
        cnt -= 1
        
        while cnt >= 0:
            curr_time = time()
            
            state = GPIO.input(self.data_pin)
            LOG.debug(last_state)
            LOG.debug(state)
            
            if state == GPIO.HIGH and last_state == GPIO.LOW:
                LOG.debug('count: ' + str(cnt))
                cnt -= 1
                GPIO.output(self.data_pin, GPIO.HIGH)
                precise_sleep((500 / 1000000), curr_time)
                GPIO.output(self.data_pin, GPIO.LOW) 
            
            last_state = state
            
        return True
