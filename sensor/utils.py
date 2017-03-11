import os
import re
import subprocess

def device_to_vendor (device):
    p = subprocess.Popen (["udevadm", "info", "--query=all", "--name=tty%s" % device], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate ()
    d = re.findall ("ID_VENDOR_FROM_DATABASE=(.*)", out)
    if len(d) == 0:
        return ""
    else:
        return d[0]


def find_devices ():
    gps_vendor = "Cygnal Integrated Products, Inc."
    nox_vendor = "Prolific Technology, Inc."
    gps_device = ""
    nox_device = ""
    for i in range(10):
        device="USB%d"%i
        vendor=device_to_vendor(device)
        if vendor == gps_vendor:
            gps_device = device
        if vendor == nox_vendor:
            nox_device = device

    print ("gps device = " + gps_device)
    print ("nox device = " + nox_device)


if __name__ == "__main__":
    find_devices ()

