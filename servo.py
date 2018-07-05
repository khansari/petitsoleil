import RPi.GPIO as GPIO
import time

def AngleToDutyCycle(angle):
  return angle * (11.5 - 2.5)/(180. - 0.) + 2.5

JOINTS_PIN = [19, 26]
BUTTONS_PIN = [18, 23]

GPIO.setmode(GPIO.BCM)
for button_pin in BUTTONS_PIN:
  GPIO.setup(BUTTONS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

joints = []
for joint_pin in JOINTS_PIN:
  GPIO.setup(joint_pin, GPIO.OUT)
  joints.append(GPIO.PWM(joint_pin, 50))
  joints[-1].start(2.5) # Initialization

try:
  while True:
    for button_pin in BUTTONS_PIN:
      input_state = GPIO.input(button_pin)
      if not input_state:
        print 'Button %d pressed' % button_pin
    time.sleep(0.2)
    angle = 0 # int(raw_input('write and angle: '))
    for joint in joints:
      joint.ChangeDutyCycle(AngleToDutyCycle(angle))
    continue
except KeyboardInterrupt:
  GPIO.output(BUTTON_PIN_POWER, False)
  for joint in joints:
    joint.stop()
  GPIO.cleanup()
