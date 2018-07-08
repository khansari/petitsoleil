import constants
import pigpio
import mirror
import servo
import target
import time


pi_client = pigpio.pi()
mirror_client = mirror.MirrorClient(constants.OBSERVER_COORDINATE)
servo_client = servo.ServoClient(pi_client, constants.SERVO_PARAMETERS)
target_client = target.TargetClient(pi_client, constants.TARGET_PARAMETERS)

try:
  while True:
    #raw_input('Press enter:')
    target_coordinate = target_client.GetCurrentTargetLocation()
    target_coordinate.Print()
    sun_coordinate = mirror_client.GetSunCoordinate()
    mirror_coordinate = mirror_client.GetMirrorCoordinate(target_coordinate)

    sun_coordinate.Print()
    mirror_coordinate.Print()
    target_coordinate.Print()

    servo_client.MoveTo(mirror_coordinate)
    time.sleep(60)
except KeyboardInterrupt:
  pass
