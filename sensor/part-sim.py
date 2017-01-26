import lcm
import time

from exlcm import part_t

def send_particles_signal (lc):

    msg = part_t()
    msg.timestamp = int(time.time() * 1000000)
    msg.pm_10 = 20
    msg.pm_2_5 = 15
    msg.enabled = True
    print ('part-sim: published message at %d' % msg.timestamp)
    lc.publish("PM", msg.encode())


lc = lcm.LCM()
try:
    while True:
        send_particles_signal(lc)
        time.sleep(2)
except KeyboardInterrupt:
    pass

