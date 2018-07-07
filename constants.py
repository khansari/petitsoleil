import coordinate
import servo
import target


OBSERVER_COORDINATE = ['37.49000', '-122.25910']  # [lat, long]

MOTOR_PARAMETERS = {
  'pitch': 
      servo.ServoParameters(pin=19, pulse_range=(2500, 1500), angle_range=(0, np.rad2deg(90))),
  'yaw': 
      servo.ServoParameters(pin=13, pulse_range=(500, 1500), angle_range=(0, np.rad2deg(90))),
}

TARGET_PARAMETERS = {
  -1: target.TargetParameters(
      name='idle', coordinate=coordinate.Coordinate(pitch=90, yaw=90, degree=True, name='idle')),
  18: target.TargetParameters(
      name='tree', coordinate=coordinate.Coordinate(pitch=0, yaw=0, degree=True, name='tree')),
  23: target.TargetParameters(
      name='house', coordinate=coordinate.Coordinate(pitch=0, yaw=90, degree=True, name='house'))
}
