import lcm
import time

from exlcm import gps_t

def send_gps_signal (lc):

    msg = gps_t()
    msg.timestamp = int(time.time() * 1000000)
    msg.lat = 48.86667
    msg.lon = 2.333333
    msg.enabled = True
    print ('gps-sim: published message at %d' % msg.timestamp)
    lc.publish("GPS", msg.encode())


lc = lcm.LCM()
try:
    while True:
        send_gps_signal(lc)
        time.sleep(2)
except KeyboardInterrupt:
    pass

