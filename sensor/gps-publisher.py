import lcm
import time
import os
from gps import *
from time import *
import time
import threading

from exlcm import gps_t

gpsd = None #seting the global variable
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

def send_gps_signal (lc, lat, lon):

    msg = gps_t()
    msg.timestamp = int(time.time() * 1000000)
    msg.lat = lat
    msg.lon = lon
    msg.enabled = True
    print ('gps-sim: published message at %d. Lat = %.5f, Lon = %.5f' % (msg.timestamp, msg.lat, msg.lon))
    lc.publish("GPS", msg.encode())


if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  lc = lcm.LCM()
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      send_gps_signal(lc, gpsd.fix.latitude, gpsd.fix.longitude)
 
      time.sleep(5) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."

