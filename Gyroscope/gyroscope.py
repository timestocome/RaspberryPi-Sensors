# http://github.com/timestocome

# source code from
# https://github.com/bashardawood/L3G4200D-Python/blob/master/gyro.py

# data sheet
# https://www.parallax.com/sites/default/files/downloads/27911-Gyroscope-3-Axis-L3G4200D-Guide-v1.1.pdf

# i2c must be set up on Raspberry Pi first
# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c


# wiring
# ground to ground (pin 6)
# vcc to 5V (pin 4)
# SDA to SDA (pin 3)
# SCL to SCL (pin 5)



#!/usr/bin/python

from time import sleep
import smbus
import string




#converts 16 bit two's compliment reading to signed int
def getSignedNumber(number):
    if number & (1 << 15):
        return number | ~65535
    else:
        return number & 65535



#open /dev/i2c-1
i2c_bus = smbus.SMBus(1)

#i2c slave address of the L3G4200D
# type sudo i2cdetect -y 1 to see which memory location has signal
i2c_address = 0x69




#initialise the L3G4200D

#normal mode and all axes on to control reg1
# hz = 250
#i2c_bus.write_byte_data(i2c_address,0x20,0x0F)

#full 2000dps to control reg4
hz = 2000
i2c_bus.write_byte_data(i2c_address,0x23,0x20)

# give the chip time to wake up
sleep(0.5)  

px = py = pz = 0
#read data, combine and display
while True:

                # read low and high bytes for x 
                i2c_bus.write_byte(i2c_address,0x28)
                X_L = i2c_bus.read_byte(i2c_address)
                i2c_bus.write_byte(i2c_address,0x29)
                X_H = i2c_bus.read_byte(i2c_address)
                # combine h and low bits ( shift H 8 bytes and or with L )
                X = X_H << 8 | X_L

                # y
                i2c_bus.write_byte(i2c_address,0x2A)
                Y_L = i2c_bus.read_byte(i2c_address)
                i2c_bus.write_byte(i2c_address,0x2B)
                Y_H = i2c_bus.read_byte(i2c_address)
                Y = Y_H << 8 | Y_L

                # z
                i2c_bus.write_byte(i2c_address,0x2C)
                Z_L = i2c_bus.read_byte(i2c_address)
                i2c_bus.write_byte(i2c_address,0x2D)
                Z_H = i2c_bus.read_byte(i2c_address)
                Z = Z_H << 8 | Z_L

                X = getSignedNumber(X)
                Y = getSignedNumber(Y)
                Z = getSignedNumber(Z)
                
                
                # http://forum.arduino.cc/index.php?topic=183417.0
                # 0.00875 degrees-per-second-per-LSB is 114.285714285714 LSB's-per-degree-per-second.  :(

                # To get DPS from the raw number you subtract the Zero Rate Offset
                # (the value you get when not rotating),
                # multiply the answer by 8.75 to get milli-DPS
                # and divide by 1000 to get DPS (or multiply by 8750 
                # to get micro-DPS and divide by 1,000,000 to get DPS).
                
        

                print('x %.1f y %.1f z %.1f location' %(X, Y, Z))
                
                 # see documentation and sample code
                 # https://www.parallax.com/product/27911
                dx = (px - X) / 114
                dy = (py - Y) / 114
                dz = (pz - Z) / 114
                print(dx, dy, dz)
                
                
                px = X
                py = Y
                pz = Z
                
                
                
                
               
                sleep(1.0)
