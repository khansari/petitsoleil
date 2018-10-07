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
  'idle': target.TargetParameters(
      pin=None, coordinate=coordinate.Coordinate(pitch=40, yaw=250, degree=True, name='idle')),
  'sun': target.TargetParameters(
      pin=None, coordinate=coordinate.Coordinate(pitch=None, yaw=None, name='sun')),
  'tree': target.TargetParameters(
      pin=18, coordinate=coordinate.Coordinate(pitch=30, yaw=145, degree=True, name='tree')),
  'house': target.TargetParameters(
      pin=23, coordinate=coordinate.Coordinate(pitch=-15, yaw=237, degree=True, name='house')),
  'dining': target.TargetParameters(
      pin=23, coordinate=coordinate.Coordinate(pitch=-15, yaw=270, degree=True, name='dining')),
  'ceiling': target.TargetParameters(
      pin=None, coordinate=coordinate.Coordinate(pitch=15, yaw=265, degree=True, name='ceiling')),
  'living': target.TargetParameters(
      pin=None, coordinate=coordinate.Coordinate(pitch=10, yaw=265, degree=True, name='living')),
}
