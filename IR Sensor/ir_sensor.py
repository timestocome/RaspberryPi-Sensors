
# http://github.com/timestocome
# Set up and test IR sensor input on RaspberryPi


import RPi.GPIO as gpio
import time


gpio.setmode(gpio.BOARD)



# board 13 - gpio 27
signal_pin = 13

gpio.setup(signal_pin, gpio.IN)

signal = -1
s_time = time.time()

while True:
    
    if gpio.input(signal_pin) != signal:
        dt = s_time - time.time()
        s_time = time.time()
        signal = gpio.input(signal_pin)

        # convert seconds to ms by dividing by 1000
        print(signal, dt)
