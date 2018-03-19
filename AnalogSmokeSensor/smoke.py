# http://github.com/timestocome

# Raspberry Pi Analog to Digital Converter
# https://cdn-learn.adafruit.com/downloads/pdf/raspberry-pi-analog-to-digital-converters.pdf

# Smoke Sensor
# https://wiki.eprolabs.com/index.php?title=Smoke_Sensor_MQ2

# Raspberry Pi Gas Sensor
# https://tutorials-raspberrypi.com/configure-and-read-out-the-raspberry-pi-gas-sensor-mq-x/


# Learn to read analog information into the Raspberry Pi
# This Smoke Sensor also has a digital output

# Wiring

# MCP3008
# Vdd -> 3.3V pin 1 red wire
# Vref -> 3.3V pin 17 red
# Agrd -> Ground black
# Clk -> Sclk #23 purple
# Dout -> Miso #21 Orange 
# Din -> Mosi #19 Yellow
# Cs/SHDN -> CE0 #24 Green
# Dgrd -> Ground black
#
# Cho input signal from Smoke sensor


# Smoke Sensor
# Vcc -> 5V pin 2 red
# Grd -> grn black
# Analog out -> Blue -> resistors to 330/440 split 5V down to 3.5V







##########################
# AdaFruit test code from above tutorial



import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008



SPI_PORT = 0
SPI_DEVICE = 0

mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))



print('Reading mcp values...')

print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)


while True:

    # read all channels
    values = [0]*8
    
    for i in range(8):
        # read each channel
        values[i] = mcp.read_adc(i)
        
    # print values
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))

    # Pause for half a second.
    time.sleep(0.5)
