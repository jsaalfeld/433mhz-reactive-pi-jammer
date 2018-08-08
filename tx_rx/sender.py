import RPi.GPIO as GPIO
import logging
from utils.helpers import precise_sleep
from time import time, sleep

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
        GPIO.setup(self.recv_data_pin, GPIO.IN)

    def send_jam(self, curr_time):
        """sends a jam signal"""
        first = True
        curr_time = time()
        LOG.debug("sending checksum")
        cnt = 7
        self.last_state = GPIO.LOW
        
        
##        GPIO.output(self.data_pin, GPIO.HIGH)
##        precise_sleep((509 / 1000), curr_time)
##        GPIO.output(self.data_pin, GPIO.LOW)
##        
        freq = 15000
        p = GPIO.PWM(self.data_pin, freq)
        p.start(25.0)
##        precise_sleep((506 / 1000), curr_time)
        sleep(1)
        p.stop()
   
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
        
##        while cnt >= 1:
##            state = GPIO.input(self.recv_data_pin)
##            if not first:
##                curr_time = time()
##            first = False
                
##            LOG.debug(last_state)
##            LOG.debug(state)
##            LOG.debug(cnt)
            
##            if state == GPIO.HIGH and self.last_state == GPIO.LOW:
##                LOG.debug('count: ' + str(cnt))
####                if cnt % 2 == 0:
####                    GPIO.output(self.data_pin, GPIO.HIGH)
####                    precise_sleep((410 / 1000000), curr_time)
####                    GPIO.output(self.data_pin, GPIO.LOW) 
####                else:
####                    GPIO.output(self.data_pin, GPIO.HIGH)
####                    precise_sleep((190 / 1000000), curr_time)
####                    GPIO.output(self.data_pin, GPIO.LOW)
##                GPIO.output(self.data_pin, GPIO.HIGH)
##                precise_sleep((425 / 1000000), curr_time)
##                GPIO.output(self.data_pin, GPIO.LOW)
##                cnt -= 1
##            self.last_state = state
##            
        return True
