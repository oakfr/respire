import sys
from time import sleep
import lcm
import time
import serial

from exlcm import gaz_t

def init_nox ():
    print ("initializing NOx reader...")
    try:
        s = serial.Serial("/dev/nox", 9600)
        print ("success.")
        return s
    except:
        print ("Failed to init NOx")
        return None


def is_valid (mes):
    if (not 'PM1' in mes) or (not 'PM2.5' in mes) or (not 'PM10' in mes):
        return False
    if mes['PM1'] < 1E-6 or mes['PM2.5'] < 1E-6 or mes['PM10'] < 1E-6:
        return False
    return True


def get_measurement (nox_reader):
    line = nox_reader.readline()
    try:
        elements = [float(el.strip()) for el in line.split(',')]
    except:
        return (0,0,False)
    no2 = elements[-2]
    o3 = elements[-1]
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


