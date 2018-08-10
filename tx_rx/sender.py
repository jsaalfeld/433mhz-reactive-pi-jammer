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

    def send_jam(self, curr_time, sleep_time, duty_cycle, clock):
        """jamming-Signal für die Wetterstation"""
        first = True
        curr_time = time()
        LOG.debug("sending jam signal")
        cnt = 7
        self.last_state = GPIO.LOW
        
        freq = round(clock)
        LOG.debug('freq: ' + str(freq))
        LOG.debug('duty: ' + str(duty_cycle * 100))
        p = GPIO.PWM(self.data_pin, freq)
        p.start(duty_cycle * 100)
        precise_sleep(sleep_time, curr_time)
        p.stop()
        
        def steckdosen_jam(self, curr_time, sleep_time):
            """jamming-Signal für die Steckdosen"""
            
            
##            
        return True
