import lcm
import glib
import gobject
from exlcm import gps_t
from exlcm import part_t
from sendsigfox import Sigfox

class Sheriff ():
    def __init__(self, sgfx):
        self.pm_1 = 0
        self.pm_10 = 0
        self.pm_25 = 0
        self.lat = 0
        self.lon = 0
        self.gps_enabled=False
        self.pm_enabled=False
        self.sgfx = sgfx

    def send_sigfox (self):
        print ('writing to sigfox...')
        print ("lat =      %s" % (str(self.lat)))
        print ("lon =      %s" % (str(self.lat)))
        print ("pm_1 =    %s" % (str(self.pm_1)))
        print ("pm_10 =    %s" % (str(self.pm_10)))
        print ("pm_25 =    %s" % (str(self.pm_25)))
        message = "1234CAFE"
        self.sgfx.sendMessage(message)
        return True

    def gps_handler(self, channel, data):
	print ('\treceived gps message...')
        msg = gps_t.decode(data)
        self.lat = msg.lat
        self.lon = msg.lon
        self.gps_enabled = msg.enabled

    def pm_handler(self, channel, data):
	print ('\treceived pm message...')
        msg = part_t.decode(data)
        self.pm_10 = msg.pm_10
        self.pm_25 = msg.pm_25
        self.pm_1 = msg.pm_1
        self.pm_enabled = msg.enabled

def main():
    sgfx = Sigfox('/dev/ttyAMA0')
    sheriff = Sheriff(sgfx)
    lc = lcm.LCM()

    def handle(*a):
        try:
            lc.handle()
        except Exception:
            pass
        return True
    gobject.io_add_watch(lc, gobject.IO_IN, handle)

    subscription = lc.subscribe("GPS", sheriff.gps_handler)
    subscription = lc.subscribe("PM", sheriff.pm_handler)

    mainloop = glib.MainLoop()
    gobject.timeout_add (15000, sheriff.send_sigfox)
    try:
        mainloop.run()
    except KeyboardInterrupt:
        pass

    lc.unsubscribe(subscription)

if __name__ == "__main__":
    main()
