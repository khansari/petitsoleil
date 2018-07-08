import argparse
import constants
import datetime
import pigpio
import mirror
import numpy as np
import servo
import target
import time


parser = argparse.ArgumentParser()
parser.add_argument(
    '--target', default=None,
    help='Overrides the button definition and manually defines a target.')
args = parser.parse_args()

pi_client = pigpio.pi()
mirror_client = mirror.MirrorClient(constants.OBSERVER_COORDINATE)
servo_client = servo.ServoClient(pi_client, constants.SERVO_PARAMETERS)
target_client = target.TargetClient(pi_client, constants.TARGET_PARAMETERS)

while True:
  if args.target is None:
    target_coordinate = target_client.GetTargetCoordinateFromButtons()
  else:
    target_coordinate = target_client.GetTargetCoordinateFromName(target_name=args.target)
  target_coordinate.Print()
  sun_coordinate = mirror_client.GetSunCoordinate()
  sun_coordinate.Print()

  if ((sun_coordinate.pitch < np.deg2rad(20) and sun_coordinate.yaw > np.deg2rad(180)) or
      (sun_coordinate.pitch < np.deg2rad(40) and sun_coordinate.yaw < np.deg2rad(180))):
    time.sleep(300)
    print '%s: hybernate mode.' % datetime.datetime.now()
    continue

  try: 
    mirror_coordinate = mirror_client.GetMirrorCoordinate(target_coordinate)
  except pigpio.error:
    mirror_coordinate = mirror_client.GetMirrorCoordinate(
        target_coordinate, sleeptime=0)
  mirror_coordinate.Print()
  target_coordinate.Print()

  servo_client.MoveTo(mirror_coordinate)
  time.sleep(60)
