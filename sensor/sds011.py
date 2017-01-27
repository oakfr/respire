import subprocess
import re
import sys
import time
import datetime
import lcm

from exlcm import part_t

def send_particles_signal (lc):

    msg = part_t()
    msg.timestamp = int(time.time() * 1000000)
    output = subprocess.check_output(["od", "--endian=big" ,"-x", "-N10", "/dev/ttyUSB0"])
    data = output.split()[2:4]
    rawpm25 = (data[0][:2], data[0][2:4])
    rawpm10 = (data[1][:2], data[1][2:4])
    pm25 = ((int(rawpm25[1],16) * 256 + int(rawpm25[0], 16)) / 10)
    pm10 = ((int(rawpm10[1],16) * 256 + int(rawpm10[0], 16)) / 10)
    msg.pm_10 = pm10
    msg.pm_2_5 = pm25
    msg.enabled = True
    print ('sds: published message at %d' % msg.timestamp)
    print ('PM2.5 = %d, PM10 = %d' % (msg.pm_2_5, msg.pm_10))
    lc.publish("PM", msg.encode())


lc = lcm.LCM()
try:
    while True:
        send_particles_signal(lc)
        time.sleep(2)
except KeyboardInterrupt:
    pass

