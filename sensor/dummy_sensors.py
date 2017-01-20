import respire_data_pb2
import time
import random

class Sensor:
    """ the Sensor class 
    """
    def __init__ (self, lat, lon, uid):
        self.uid = uid
        self.lat = lat
        self.lon = lon
        self.measure = None


    def __str__ (self):
        return '[sensor %d] lat,lon = %.6f,%.6f\n%s' % (self.uid, self.lat, self.lon, str(self.measure))


    def generate_random_sample (self):
        """ generate a random sample measurement 
        """
        timestamp = int(time.time())
        res = respire_data_pb2.Measure()
        res.timestamp = timestamp
        res.pm2_5 = int(random.random()*120)
        res.pm10 = int(random.random()*120)
        res.gps_lat = self.lat
        res.gps_lon = self.lon
        self.measure = res


def generate_sensors ():
    """ generate dummy sensors from file
    """
    sensors = []
    with open ('dummy_sensors.txt','r') as fp:
        lines = fp.readlines()
        for line in lines:
            uid = int(line.split(',')[0])
            lat = float(line.split(',')[1])
            lon = float(line.split(',')[2])
            s = Sensor(lat,lon, uid)
            sensors.append (s)
    return sensors

def main ():
    # generate set of sensors
    sensors = generate_sensors()

    while True:
        # wait for some time
        time.sleep (1)
        for sensor in sensors:
            # generate a random sample
            sensor.generate_random_sample ()
            print (sensor)
            # todo : send sample to the cloud

if __name__ == "__main__":
    main()

