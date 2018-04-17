# http://github.com/timestocome
# set up, read, AM2320 temp and humidity sensor on Raspberry Pi


# sensor spec sheet: https://akizukidenshi.com/download/ds/aosong/AM2320.pdf


# code to read sensor 
# http://github.com/Gozem/am2320/blob/master/am2320.py 


# turn on i2c in Raspberry Pi preferences
# AM2320 pins if looking at grid side [VCC, SDA, GRD, SCL]
# Connect to Pi 3V, SDA (pin 3), SCL (pin 5), GRD (pin 9)
# SCL clock signal
# SDA data signal

# more info: http://learn.sparkfun.com/tutorials/i2c


import posix              # portable operating system interface
from fcntl import ioctl   # i/o control. file control
import time


class AM2320:
    
    I2C_ADDR = 0x5c        # 92
    I2C_SLAVE = 0x0703     # 1795
    
    # init I2C bus
    def __init__(self, i2cbus=1):
        self._i2cbus = i2cbus
        
    # convert data    
    @staticmethod
    def _calc_crc16(data):
            
            crc = 0xFFF
            
            for x in data:
                
                crc = crc ^ x
                
                for bit in range(0, 8):
                    if (crc & 0x0001) == 0x0001:
                        crc >>= 1
                        crc ^= 0XA001
                    else:
                        crc >>= 1
                        
            return crc
    
    # combine least and most significant bytes
    # bit shift then or
    @staticmethod
    def _combine_bytes(msb, lsb):
            return msb << 8 | lsb    
        
    # open I2C bus, fetch data   
    def readSensor(self):
            
            fd = posix.open("/dev/i2c-%d" % self._i2cbus, posix.O_RDWR)
            ioctl(fd, self.I2C_SLAVE, self.I2C_ADDR)
            
            # wake up AM2320 sensor, it sleeps when not being
            # called to keep from heating up and effecting temp, humidity
            try:
                posix.write(fd, b'\0x00')
            except:
                pass
            time.sleep(0.001)  # sleep at least 0.8ms
            
            # write at addr 0x03, start register 0x00, n_registers = 0x04
            posix.write(fd, b'\x03\x00\x04')
            time.sleep(0.0016)  # wait for sensor result min 1.5ms
            
            
            # 8 bytes of data
            # 0: modbus function code 0x03
            # 1: n registers to read 0x04
            # 2: humidity msb ( most significate byte )
            # 3: humidity lsb ( least significate byte )
            # 4: temp msb
            # 5: temp lsb
            # 6: CRC lsb
            # 7: CRC msb
            data = bytearray(posix.read(fd, 8))
            
            # check data[0], data[1]
            if data[0] != 0x03 or data[1] != 0x04:
                print("First two bytes mismatch")
                
            #CRC check
            if self._calc_crc16(data[0:6]) != self._combine_bytes(data[7], data[6]):
                pass
                              
            # temp resolution 16bits
            # temp bit 15 == 1 means negative temperature, 0 positive
            # temp in addition to most significant bit Bit14 ~ Bit0
            # indicates string value
            # sensor value is string of 10x actual temp
                              
            temp = self._combine_bytes(data[4], data[5])
            if temp & 0x8000:
                temp = -(temp & 0x7FFF)    # wrap back to positive, and with 32767
            temp /= 10.0
            
            humidity = self._combine_bytes(data[2], data[3]) / 10.0
            
            return (temp, humidity)
                              

##############################################################
# run code
##############################################################

am2320 = AM2320(1)
(t, h) = am2320.readSensor()
t = 32 + t * 9/5      # convert from C to F
print("temp %.1f, humidity %.1f" %(t, h))
                              
                              

                              
            
            
                
