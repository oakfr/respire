import spidev
import usbiss
import opc
import sys
from time import sleep

#spi = spidev.SpiDev()
#spi.open(0, 0)
#spi.mode = 1
#spi.max_speed_hz = 500000

spi = usbiss.USBISS("/dev/opc", 'spi', spi_mode = 2, freq = 500000)

sleep(2.0)


try:
    alphasense = opc.OPCN2(spi)
except:
    print ("Failed to init OPC N2")
    sys.exit(1)

# Turn the opc ON
alphasense.on()

sleep(2.0)
# Read the information string
print (alphasense.read_info_string())

for k in range(5):
    # Read the histogram
    sleep(2.0)
#print (alphasense.histogram())
    print (alphasense.pm())

# Turn the opc OFF
sleep(2.0)
alphasense.off()
