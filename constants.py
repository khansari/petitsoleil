
class MotorParameters(object):
  def __init__(self, pin, pulse_range, angle_range):
    self.pin = pin
    self.pulse_range = pulse_range
    self.angle_range = angle_range

class TargetParameters(object):
  def __init__(self, name, pitch, yaw):
    self.name = name
    self.pitch = pitch
    self.yaw = yaw


MOTOR_PARAMETERS = {
  'pitch': MotorParameters(pin=19, pulse_range=(2500, 1500), angle_range=(0, 90)),
  'yaw': MotorParameters(pin=13, pulse_range=(500, 1500), angle_range=(0, 90)),
}

TARGET_PARAMETERS = {
  18: TargetParameters(name='tree', pitch=10, yaw=150),
  23: TargetParameters(name='house', pitch=10, yaw=150),
}
