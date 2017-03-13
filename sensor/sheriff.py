import lcm
import glib
import gobject
import json
import requests
from exlcm import gps_t
from exlcm import part_t
from exlcm import gaz_t
from sendsigfox import Sigfox
import time
import math


def post_message (data):
    print ("posting data %s" % data)
    url = 'http://olivierkoch.org/sigfox/index.php'
    device = '0'
    data = {'device':device,'data':data, 'time':'%d'%time.time()}
    data_json = json.dumps(data)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=data_json, headers=headers)


class Sheriff ():
    def __init__(self, sgfx):
        self.pm_1 = 12
        self.pm_10 = 23
        self.pm_25 = 32
        self.lat = 48.85231
        self.lon = 2.35112
        self.no2 = 22
        self.o3 = 14
        self.gps_enabled=False
        self.pm_enabled=False
        self.sgfx = sgfx

    def send_sigfox (self):
        print ('writing to sigfox...')
        print ("lat =      %s" % (str(self.lat)))
        print ("lon =      %s" % (str(self.lon)))
        print ("pm_1 =    %s" % (str(self.pm_1)))
        print ("pm_10 =    %s" % (str(self.pm_10)))
        print ("pm_25 =    %s" % (str(self.pm_25)))
        print ("no2 =      %s" % (str(self.no2)))
        print ("o3 =       %s" % (str(self.o3)))
        message = self.to_hex()
        if self.sgfx:
            self.sgfx.sendMessage(message)
        else:
            print ("Sigfox board not initialized.")
            post_message (message)
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

    def gaz_handler(self, channel, data):
        print ('\treceived gaz message...')
        msg = gaz_t.decode(data)
        self.no2 = msg.no2
        self.o3 = msg.o3

    def to_hex (self):
        """ convert data to 12-byte hexa format """
        out = ""
        # lat, lon on 7 chars
        out += "{0:#0{1}x}".format(int(round(100000*(self.lat+90))),9)[2:]
        out += "{0:#0{1}x}".format(int(round(100000*(self.lon+180))),9)[2:]
        # measurements on 3 chars
        out += "{0:#0{1}x}".format(max([0,min([255,int(round(self.pm_1))])]),4)[2:]
        out += "{0:#0{1}x}".format(max([0,min([255,int(round(self.pm_25))])]),4)[2:]
        out += "{0:#0{1}x}".format(max([0,min([255,int(round(self.pm_10))])]),4)[2:]
        out += "{0:#0{1}x}".format(max([0,min([255,int(round(self.no2))])]),4)[2:]
        out += "{0:#0{1}x}".format(max([0,min([255,int(round(self.o3))])]),4)[2:]
        return out 



def main():
    sgfx = None
    try:
        sgfx = Sigfox('/dev/ttyAMA0')
    except:
        print ("Failed to init Sigfox board.")

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
    subscription = lc.subscribe("GAZ", sheriff.gaz_handler)

    mainloop = glib.MainLoop()
    gobject.timeout_add (2000, sheriff.send_sigfox)
    try:
        mainloop.run()
    except KeyboardInterrupt:
        pass

    lc.unsubscribe(subscription)

if __name__ == "__main__":
    main()
