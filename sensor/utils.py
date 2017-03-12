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


def find_device (vendor):
    for i in range(10):
        device="USB%d"%i
        if vendor == device_to_vendor (device):
            return device
    raise LookupError("ERROR: failed to find device for vendor %s" % vendor)
    return ""


def find_devices ():
    gps_vendor = "Cygnal Integrated Products, Inc."
    nox_vendor = "Prolific Technology, Inc."
    gps_device = find_device (gps_vendor)
    nox_device = find_device (nox_vendor)
    print ("gps device = " + gps_device)
    print ("nox device = " + nox_device)


if __name__ == "__main__":
    find_devices ()

