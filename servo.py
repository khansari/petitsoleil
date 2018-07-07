import constants
import numpy as np
import pigpio
import RPi.GPIO as GPIO
import time

class MirrorClient(object):
  def __init__(self, pi_client, pitch_motor, yaw_motor):
    self._pi_client = pi_client
    self._pitch_motor = pitch_motor
    self._yaw_motor = yaw_motor

  def AngleToPulseWidth(self, angle, motor_parameter):
    return int(np.interp(angle, 
                         motor_parameter.angle_range, 
                         motor_parameter.pulse_range))

  def MoveTo(self, pitch, yaw, sleeptime=0.002):
    pitch_pw_current = self._pi_client.get_servo_pulsewidth(self._pitch_motor.pin)
    yaw_pw_current = self._pi_client.get_servo_pulsewidth(self._yaw_motor.pin)
    pitch_pw_target = self.AngleToPulseWidth(pitch, self._pitch_motor)
    yaw_pw_target = self.AngleToPulseWidth(yaw, self._yaw_motor)

    num_points = max(abs(pitch_pw_target - pitch_pw_current),
                     abs(yaw_pw_target - yaw_pw_current))

    for pitch_pw_command, yaw_pw_command in zip(
        np.linspace(pitch_pw_current, pitch_pw_target, num_points), 
        np.linspace(yaw_pw_current, yaw_pw_target, num_points)):
      self._pi_client.set_servo_pulsewidth(self._pitch_motor.pin, pitch_pw_command)
      self._pi_client.set_servo_pulsewidth(self._yaw_motor.pin, yaw_pw_command)
      time.sleep(sleeptime)


# GPIO.setmode(GPIO.BCM)
# for button_pin in BUTTONS_PIN:
#   GPIO.setup(BUTTONS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pi_client = pigpio.pi()
mirror_client = MirrorClient(pi_client, 
                             constants.MOTOR_PARAMETERS['pitch'],
                             constants.MOTOR_PARAMETERS['yaw'])

try:
  while True:
    # for button_pin in BUTTONS_PIN:
    #   input_state = GPIO.input(button_pin)
    #   if not input_state:
    #     print 'Button %d pressed' % button_pin
    # time.sleep(0.2)
    angle = int(raw_input('write and angle: '))
    mirror_client.MoveTo(angle, angle)
except KeyboardInterrupt:
  # GPIO.output(BUTTON_PIN_POWER, False)
  GPIO.cleanup()
