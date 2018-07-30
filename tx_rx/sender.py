import RPi.GPIO as GPIO
import logging

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
    LOG = logging.getLogger('433_jammer.Sender')
    
    def __init__(self, data_pin, gnd_pin, vcc_pin):
        self.data_pin = data_pin
        self.gnd_pin = gnd_pin
        self.vcc_pin = vcc_pin
        GPIO.setup(self.data_pin, GPIO.OUT)

