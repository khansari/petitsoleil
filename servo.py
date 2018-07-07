import numpy as np
import pigpio
import RPi.GPIO as GPIO
import time

class MotorParameters(object):
  def __init__(self, pin, pulse_range, angle_range):
    self.pin = pin
    self.pulse_range = pulse_range
    self.angle_range = angle_range


MOTOR_PARAMETERS = {
  'pitch': MotorParameters(pin=19, pulse_range=(2500, 1500), angle_range=(0, 90)),
  'yaw': MotorParameters(pin=13, pulse_range=(500, 1500), angle_range=(0, 90)),
}


def AngleToPulseWidth(angle, motor_parameter):
  return int(np.interp(angle, motor_parameter.angle_range, motor_parameter.pulse_range))

JOINTS_PIN = [19, 26]
BUTTONS_PIN = [18, 23]

GPIO.setmode(GPIO.BCM)
for button_pin in BUTTONS_PIN:
  GPIO.setup(BUTTONS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

motor_control = pigpio.pi()

try:
  while True:
    for button_pin in BUTTONS_PIN:
      input_state = GPIO.input(button_pin)
      if not input_state:
        print 'Button %d pressed' % button_pin
    time.sleep(0.2)
    angle = int(raw_input('write and angle: '))
    for angle_name in ['pitch', 'yaw']:
      pulse_width = AngleToPulseWidth(angle, MOTOR_PARAMETERS[angle_name])
      motor_control.set_servo_pulsewidth(
          MOTOR_PARAMETERS[angle_name].pin, pulse_width)   
except KeyboardInterrupt:
  GPIO.output(BUTTON_PIN_POWER, False)
  for joint in joints:
    joint.stop()
  GPIO.cleanup()
