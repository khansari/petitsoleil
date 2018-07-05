#!/usr/bin/env python
# to use with Pi Traffic Light

import RPi.GPIO as GPIO

LED = 14

# Pin Setup:
GPIO.setmode(GPIO.BCM)   # Broadcom pin-numbering scheme.
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)

print 'LED is on on pin %d' % LED
try:
  while (1):
    GPIO.output(LED, True)  
except KeyboardInterrupt:
  print "Good bye"
  GPIO.output(LED, False)