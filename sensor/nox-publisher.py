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


def read_calibration_file ():
    filename = 'calib-nox.json'
    data = json.loads (open (filename,'r').read())
    sn1_data = data['sensor 1 (no2)']
    sn1_we_elec_offset = float(sn1_data['WE electronic offset'])
    sn1_ae_elec_offset = float(sn1_data['AE electronic offset'])
    sn1_we_total_zero_offset = float(sn1_data['WE total zero offset'])
    sn1_ae_total_zero_offset = float(sn1_data['AE total zero offset'])
    sn1_we_sensitivity = float(sn1_data['WE sensitivity'])
    sn2_data = data['sensor 2 (ox)']
    sn2_we_elec_offset = float(sn2_data['WE electronic offset'])
    sn2_ae_elec_offset = float(sn2_data['AE electronic offset'])
    sn2_we_total_zero_offset = float(sn2_data['WE total zero offset'])
    sn2_ae_total_zero_offset = float(sn2_data['AE total zero offset'])
    sn2_we_sensitivity = float(sn2_data['WE sensitivity'])
    return (sn1_we_elec_offset, sn1_ae_elec_offset, sn1_we_total_zero_offset, sn1_ae_total_zero_offset, sn1_we_sensitivity, \
            sn2_we_elec_offset, sn2_ae_elec_offset, sn2_we_total_zero_offset, sn2_ae_total_zero_offset, sn2_we_sensitivity)


def get_correction_factor_no2_nt (temperature):
    # round to nearest 10 degrees
    temp10 = int(round (1.0 * temperature / 10))*10
    lut = {-30: .8, -20: .8, -10: 1, 0: 1.2, 10:1.6, 20:1.8, 30:1.9, 40:2.5, 50:3.6}
    return lut[temp10]


def get_correction_factor_ox_kpt (temperature):
    # round to nearest 10 degrees
    temp10 = int(round (1.0 * temperature / 10))*10
    lut = {-30: .1, -20: .1, -10: .2, 0: .3, 10: .7, 20:1, 30:1.7, 40:3, 50:4}
    return lut[temp10]


def calibrate (we_sn1, ae_sn1, we_sn2, ae_sn2, calib_data, temperature=22):
    """ return calibrated measurement in ppb.
        sensor 1 is NO2, sensor 2 is O3 """
    (sn1_wee, sn1_aee, sn1_wet, sn1_aet, sn1_we_sens, sn2_wee, sn2_aee, sn2_wet, sn2_aet, sn2_we_sens) = calib_data
    # suggested algorithm for type A NO2: 1
    we_sn1 -= sn1_wee
    ae_sn1 -= sn1_aee
    nt = get_correction_factor_no2_nt (temperature)
    we_sn1 -= nt * ae_sn1
    no2_ppb = we_sn1 / sn1_we_sens
    # suggested algorithm for type A OX: 3
    sn2_we0 = sn2_wet - sn2_wee
    sn2_ae0 = sn2_aet - sn2_aee
    kpt = get_correction_factor_ox_kpt (temperature)
    we_sn2 -= sn2_wee
    ae_sn2 -= sn2_aee
    we_sn2 -= (sn2_we0 - sn2_ae0) + kpt * ae_sn2
    o3_ppb = we_sn2 / sn2_we_sens
    return (no2_ppb, o3_ppb)


def get_measurement (nox_reader, calib_data):
    we_sn1 = nox_reader.read_voltage (3)
    ae_sn1 = nox_reader.read_voltage (4)
    we_sn2 = nox_reader.read_voltage (1)
    ae_sn2 = nox_reader.read_voltage (2)
    # todo add temperature here
    (no2_ppb, o3_ppb) = calibrate (we_sn1, ae_sn1, we_sn2, ae_sn2, calib_data)
    return (no2_ppb, o3_ppb, True)


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
    calib_data = read_calibration_file()

    try:
        while True:
            if nox_reader is None:
                nox_reader = init_nox ()
            (no2, o3, is_valid) = get_measurement (nox_reader, calib_data)
            if is_valid:
                send_gaz_signal(lc, no2, o3)
            time.sleep(2)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()


