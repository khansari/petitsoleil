import constants
import pigpio
import mirror
import servo
import target


pi_client = pigpio.pi()
mirror_client = mirror.MirrorClient(constants.OBSERVER_COORDINATE)
servo_client = servo.ServoClient(pi_client, constants.SERVO_PARAMETERS)
target_client = target.TargetClient(pi_client, constants.TARGET_PARAMETERS)

try:
  while True:
    raw_input('Press enter:')
    target_coordinate = target_client.GetCurrentTargetLocation()
    sun_coordinate = mirror_client.GetSunCoordinate()
    mirror_coordinate = mirror_client.GetMirrorCoordinate(target_coordinate)

    sun_coordinate.Print()
    mirror_coordinate.Print()

    # angle = int(raw_input('write and angle: '))
    servo_client.MoveTo(sun_coordinate)
    # time.sleep(0.1)
except KeyboardInterrupt:
  pass
