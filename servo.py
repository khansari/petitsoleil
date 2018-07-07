
import numpy as np
import time


class ServoParameters(object):
  def __init__(self, pin, pulse_range, angle_range):
    self.pin = pin
    self.pulse_range = pulse_range
    self.angle_range = angle_range


class ServoClient(object):
  def __init__(self, pi_client, servo_parameters):
    self._pi_client = pi_client
    self._pitch_motor = servo_parameters['pitch']
    self._yaw_motor = servo_parameters['yaw']

  def AngleToPulseWidth(self, angle, motor_parameter):
    return int(np.interp(angle, 
                         motor_parameter.angle_range, 
                         motor_parameter.pulse_range))

  def MoveTo(self, coordinate, sleeptime=0.002):
    pitch_pw_current = self._pi_client.get_servo_pulsewidth(self._pitch_motor.pin)
    yaw_pw_current = self._pi_client.get_servo_pulsewidth(self._yaw_motor.pin)
    pitch_pw_target = self.AngleToPulseWidth(coordinate.pitch, self._pitch_motor)
    yaw_pw_target = self.AngleToPulseWidth(coordinate.yaw, self._yaw_motor)
    num_points = max(abs(pitch_pw_target - pitch_pw_current),
                     abs(yaw_pw_target - yaw_pw_current))

    for pitch_pw_command, yaw_pw_command in zip(
        np.linspace(pitch_pw_current, pitch_pw_target, num_points), 
        np.linspace(yaw_pw_current, yaw_pw_target, num_points)):
      self._pi_client.set_servo_pulsewidth(self._pitch_motor.pin, pitch_pw_command)
      self._pi_client.set_servo_pulsewidth(self._yaw_motor.pin, yaw_pw_command)
      time.sleep(sleeptime)
