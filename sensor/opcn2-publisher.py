import spidev
import usbiss
import opc
import sys
from time import sleep
import lcm
import time

from exlcm import part_t

def init_opc ():
    print ("initializing OPC reader...")
    try:
        spi = usbiss.USBISS("/dev/opc", 'spi', spi_mode = 2, freq = 500000)
        sleep(2)
        opc_reader = opc.OPCN2(spi)
        sleep (2)
        opc_reader.on ()
        sleep (2)
        print ("success.")
        return opc_reader
    except:
        print ("Failed to init OPC")
        return None


def is_valid (mes):
    if (not 'PM1' in mes) or (not 'PM2.5' in mes) or (not 'PM10' in mes):
        return False
    if mes['PM1'] < 1E-6 or mes['PM2.5'] < 1E-6 or mes['PM10'] < 1E-6:
        return False
    return True


def get_measurement (opc_reader):
    avg_pm10=0
    avg_pm25=0
    avg_pm1=0
    # average over several values
    n_valid=0
    n_trial=0
    min_mes=5
    for k in range(2*min_mes):
        sleep(2.0)
        mes = opc_reader.pm()
        n_trial+=1
        if is_valid (mes):
            print (mes)
            avg_pm10 += mes['PM10']
            avg_pm25 += mes['PM2.5']
            avg_pm1 += mes['PM1']
            n_valid+=1
        if n_valid==min_mes:
            break
    avg_pm10 /= n_valid
    avg_pm25 /= n_valid
    avg_pm1 /= n_valid
    return (avg_pm1, avg_pm25, avg_pm10)


def send_particles_signal (lc, pm1, pm25, pm10):

    msg = part_t()
    msg.timestamp = int(time.time())
    msg.pm_1 = int(pm1)
    msg.pm_25 = int(pm25)
    msg.pm_10 = int(pm10)
    msg.enabled = True
    print ('part-sim: published message PM1=%d, PM2.5=%d, PM10=%d' % (msg.pm_1, msg.pm_25, msg.pm_10))
    lc.publish("PM", msg.encode())


def main ():
    lc = lcm.LCM()
    opc_reader = init_opc ()

    try:
        while True:
            if opc_reader is None:
                opc_reader = init_opc ()
            if opc_reader is not None:
                (pm1, pm25, pm10) = get_measurement (opc_reader)
                send_particles_signal(lc, pm1, pm25, pm10)
            time.sleep(2)
    except KeyboardInterrupt:
        if opc_reader is not None:
            # Turn the opc OFF
            opc_reader.off()
        pass

if __name__ == "__main__":
    main()


