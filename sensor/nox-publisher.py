import sys
from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import os
from time import sleep
import lcm
import time
import serial

from exlcm import gaz_t

def init_nox ():
    i2c_helper = ABEHelpers()
    bus = i2c_helper.get_smbus()
    adc = ADCPi(bus, 0x6A, 0x6B, 12)
    return adc

def is_valid (mes):
    return True


def get_n_factors ():
    # at 20 deg.
    return (1.35, 1.28)

def get_measurement (nox_reader):
    sn1_we = nox_reader.read_voltage (3)
    sn1_ae = nox_reader.read_voltage (4)
    sn2_we = nox_reader.read_voltage (1)
    sn2_ae = nox_reader.read_voltage (2)
    (n_sn1, n_sn2) = get_n_factors ()
    sn1_ae *= n_sn1
    sn2_ae *= n_sn2
    calibration_file = "nox-calibration.txt"
    (sn1_we_off, sn1_ae_off, sn1_sens, sn1_nox_sens,\
     sn2_we_off, sn2_ae_off, sn2_sens, sn2_nox_sens) = \
    [float (a) for a in open(calibration_file,"r").readlines()]
    no2 = 0
    o3 = 0
    sn1 = (sn1_we - sn1_we_off) - (sn1_ae - sn1_ae_off)
    sn2 = (sn2_we - sn2_we_off) - (sn2_ae - sn2_ae_off)
    no2 = sn1 / sn1_sens
    o3 = sn2 / sn2_sens
    print (no2, o3)
    return (no2, o3, True)


def send_gaz_signal (lc, no2, o3):

    msg = gaz_t()
    msg.timestamp = int(time.time())
    msg.no2 = no2
    msg.o3 = o3
    msg.enabled = True
    print ('[gaz] published message NO2=%d, O3=%d' % (msg.no2, msg.o3))
    lc.publish("GAZ", msg.encode())


def main ():
    lc = lcm.LCM()
    nox_reader = init_nox ()

    try:
        while True:
            if nox_reader is None:
                nox_reader = init_nox ()
            (no2, o3, is_valid) = get_measurement (nox_reader)
            if is_valid:
                send_gaz_signal(lc, no2, o3)
            time.sleep(2)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()


