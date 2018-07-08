import coordinate
import numpy as np
import servo
import target


OBSERVER_COORDINATE = ['37.48996', '-122.25905']  # [lat, long]

SERVO_PARAMETERS = {
  'pitch': 
      servo.ServoParameters(pin=19, pulse_range=(2447, 1577), angle_range=(0, np.deg2rad(90))),
  'yaw': 
      servo.ServoParameters(pin=13, pulse_range=(2366, 500), angle_range=(np.deg2rad(143), np.deg2rad(323))),
}

TARGET_PARAMETERS = {
  -1: target.TargetParameters(
      name='idle', coordinate=coordinate.Coordinate(pitch=90, yaw=90, degree=True, name='idle')),
  18: target.TargetParameters(
      name='tree', coordinate=coordinate.Coordinate(pitch=20, yaw=145, degree=True, name='tree')),
  23: target.TargetParameters(
      name='house', coordinate=coordinate.Coordinate(pitch=-12, yaw=328, degree=True, name='house'))
}
