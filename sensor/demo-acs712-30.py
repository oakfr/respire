#!/usr/bin/python
import sys
print (sys.path)
from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import time
import os

"""
================================================
ABElectronics ADC Pi ACS712 30 Amp current sensor demo
Version 1.0 Created 15/07/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

Requires python smbus to be installed
run with: python demo-acs712-30.py
================================================

Initialise the ADC device using the default addresses and sample rate,
change this value if you have changed the address selection jumpers

Sample rate can be 12,14, 16 or 18
"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x6A, 0x6B, 12)

# change the 2.5 value to be half of the supply voltage.


def calcCurrent(inval):
    return ((inval) - 2.5) / 0.066

while (True):

    os.system('clear')

    # read from adc channels and print to screen
    for k in range(1,5):
        #print ("Current on channel %d: %02f" % (k,calcCurrent(adc.read_voltage(k))))
        print ("Current on channel %d: %02f" % (k,adc.read_voltage(k)))

    # wait 0.5 seconds before reading the pins again
    time.sleep(0.5)
