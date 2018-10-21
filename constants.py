import numpy as np
import servo

OBSERVER_COORDINATE = ['37.48996', '-122.25905']  # [lat, long]

SERVO_PARAMETERS = {
  'pitch': 
      servo.ServoParameters(pin=19, pulse_range=(2447, 1577), angle_range=(0, np.deg2rad(90))),
  'yaw': 
      servo.ServoParameters(pin=13, pulse_range=(2366, 500), angle_range=(np.deg2rad(143), np.deg2rad(323))),
}

