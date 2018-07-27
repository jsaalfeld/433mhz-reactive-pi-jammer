#!/usr/bin/python3
#!/usr/bin/env python3

import argparse
import sys
import os
import logging
import configparser
import RPi.GPIO as GPIO
from receiver.receiver import Receiver

LOG = logging.getLogger('433_jammer')
parser = argparse.ArgumentParser(description='Waits for a signal with a specific structure and tries to jam that')
parser.add_argument('--verbosity', help='set verbosity level: 10 - Debug, 20 - Info, 30 - Warning, 40 - Error, 50 - Critical', type=int, default=30)
parser.add_argument('--config', help='path to config file',  default=['gpio.config'])

def main(argv):
    args = parser.parse_args()
    verbosity = args.verbosity
    config_file = os.path.abspath(args.config[0])
    logging.basicConfig()
    logging.getLogger().setLevel(args.verbosity)
    LOG.debug('Verbosity is at level: ' + str(verbosity))
    LOG.debug('Using config file: ' + str(config_file))
    receiver_gnd, receiver_vcc, receiver_data, sender_gnd, sender_vcc, sender_data, signal_freq, signal_clock, signal_sample, signal_duty = getConfigValues(config_file)
    LOG.debug('Config - Receiver - GND: ' + str(receiver_gnd))
    LOG.debug('Config - Receiver - VCC: ' + str(receiver_vcc))
    LOG.debug('Config - Receiver - Data: ' + str(receiver_data))
    LOG.debug('Config - Sender - GND: ' + str(sender_gnd))
    LOG.debug('Config - Sender - VCC: ' + str(sender_vcc))
    LOG.debug('Config - Sender - Data: ' + str(sender_data))
    LOG.debug('Config - Signal - Frequency in MHz: ' + str(signal_freq))
    LOG.debug('Config - Signal - Clock in Hz: ' + str(signal_clock))
    LOG.debug('Config - Signal - Sample in MHz: ' + str(signal_sample))
    LOG.debug('Config - Signal - Duty in %: ' + str(signal_duty*100))
    GPIO.setmode(GPIO.BCM)
    receiver = Receiver(receiver_data, receiver_gnd, receiver_vcc)
    receiver.readToInfinity()

def getConfigValues(configFile):
    receiver_gnd = 0
    receiver_vcc = 0
    receiver_data = 0
    sender_gnd = 0
    sender_vcc = 0
    sender_data = 0
    signal_freq = 0
    signal_clock = 0
    signal_sample = 0

    config = configparser.ConfigParser()
    config.readfp(open(configFile))
    receiver_gnd = config.getint('receiver', 'gnd')
    receiver_vcc = config.getint('receiver', 'vcc')
    receiver_data = config.getint('receiver', 'data')
    sender_gnd = config.getint('sender', 'gnd')
    sender_vcc = config.getint('sender', 'vcc')
    sender_data = config.getint('sender', 'data')
    freq_str = config.get('signal', 'freq')
    signal_freq = freq_str[0:len(freq_str)-3]
    clock_str = config.get('signal', 'clock')
    signal_clock = clock_str[0:len(clock_str)-3]
    sample_str = config.get('signal', 'sample')
    signal_sample = sample_str[0:len(sample_str)-3]
    signal_duty = config.getfloat('signal', 'duty')

    return receiver_gnd, receiver_vcc, receiver_data, sender_gnd, sender_vcc, sender_data, signal_freq, signal_clock, signal_sample, signal_duty

if __name__ == '__main__':
    main(sys.argv[1:])
