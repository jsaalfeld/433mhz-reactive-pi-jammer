import RPi.GPIO as GPIO

class Receiver:
    data_pin = 0
    gnd_pin = 0
    vcc_pin = 0

    def __init__(self, data_pin, gnd_pin, vcc_pin):
        self.data_pin = data_pin
        self.gnd_pin = gnd_pin
        self.vcc_pin = vcc_pin
        # For receiving, set the data_pin as input
        GPIO.setup(self.data_pin, GPIO.IN)

    def readToInfinity(self):
        while True:
            print(GPIO.input(self.data_pin))
    
