import RPi.GPIO as GPIO
import logging
import time

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
    LOG = logging.getLogger('433_jammer.Receiver')

    def __init__(self, data_pin, gnd_pin, vcc_pin):
        self.data_pin = data_pin
        self.gnd_pin = gnd_pin
        self.vcc_pin = vcc_pin
        # For receiving, set the data_pin as input
        GPIO.setup(self.data_pin, GPIO.IN)

    def listen(self, freq, clock, sample, duty):
        sample_length = float(1/(sample*1000))
        self.LOG.debug('The length of one sample is: ' + str(sample_length) + 's')
        k = 10000
        i = 0
        test = []
        while True:
            time.sleep(sample_length)
            test.append(GPIO.input(self.data_pin))
            i += 1
            if i >= k:
                break
        for entry in test:
            if entry != 0:
                print(entry)
