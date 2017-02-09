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
    """ class for GPS poller """
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


def read_gps_data_from_file (filename):
    """ read GPS data from file """
    try:
        with open (filename,'r') as fp:
            d = [float(a) for a in fp.readline().split(' ')]
            return (d[0],d[1],int(d[2]), True)
    except:
        return (.0, .0, 0, False)


def write_gps_data_to_file (filename, lat, lon, gps_timestamp):
    """ write GPS data to file """
    with open (filename, 'w') as fp:
        fp.write ('%.5f %.5f %d' % (lat, lon, gps_timestamp))


def is_valid_data (lat, lon):
    """ test for GPS data validity """
    if isnan(lat) or isnan(lon):
        return False
    if lat < 1E-6 or lon < 1E-6:
        return False
    return True


def publish_msg (lat, lon, gps_timestamp, enabled):
    """ publish GPS message """
    msg = gps_t()
    msg.timestamp = int(time.time())
    msg.lat = lat
    msg.lon = lon
    msg.enabled = enabled
    msg.gps_timestamp = gps_timestamp
    lc.publish("GPS", msg.encode())


def send_gps_signal (lc, lat, lon):
    """ send LCM signal with GPS data """
    gps_data_filename = '/home/pi/gps_data.txt'
    time_now = int(time.time())
    if is_valid_data (lat, lon):
        # gps data is valid, publish it and save it to file
        gps_timestamp = time_now
        publish_msg (lat, lon, gps_timestamp, True)
        write_gps_data_to_file (gps_data_filename, lat, lon, gps_timestamp)
        print ("[gps] GPS OK.  lat = %.5f, lon = %.5f" % (lat, lon))
    else:
        # try to read from file
        (lat, lon, gps_timestamp, is_valid) = read_gps_data_from_file (gps_data_filename)
        if is_valid:
            # gps data is invalid, read it from file
            publish_msg (lat, lon, gps_timestamp, False)
            delta_hours = (time_now - gps_timestamp)*1.0 / 3600
            print ("[gps] GPS DOWN.  Fallback values lat = %.5f, lon = %.5f (%.2f hours late)" % (lat, lon, delta_hours))
        else:
            print ("[gps] ERROR No GPS data available.  Failed to read backup file %s.  Skipping..." % gps_data_filename)
            


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

