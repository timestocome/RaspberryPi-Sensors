

# http://github.com/timestocome
# setup for  ball tilt sensor
# S signal to pi
# - ground
# center pin is +5V

import time
import RPi.GPIO as gpio


# setup
channel = 18               #  gpio number for incoming signal
gpio.setmode(gpio.BCM)     #  use gpio number as pin reference, not board number 
gpio.setup(channel, gpio.IN, pull_up_down=gpio.PUD_UP)  # sets a default input


# do something if sensor is tilted
def alert(event=None):
    print('tilt detected')
    
    
# loop forever
# bounce time is minimum time between callbacks
# alert is function to call if event occurs
# edge can be FALLING, RISING or BOTH
def loop():
    gpio.add_event_detect(channel, gpio.FALLING, callback=alert, bouncetime=100)
    

###################################################################################
# run code

loop()


