import argparse
import constants
import datetime
import pigpio
import mirror
import numpy as np
import servo
import target
import threading
import time

def MirrorCommandCallback(
    mirror_client, servo_client, target_coordinate):
  print('************************************************************')
  # Printing time in pacific time zone.
  print(datetime.datetime.now() + datetime.timedelta(hours=7))
  target_coordinate.Print()
  sun_coordinate = mirror_client.GetSunCoordinate()
  sun_coordinate.Print()

  if target_coordinate.name == 'sun':
    servo_client.MoveTo(sun_coordinate)
    return 60

  if ((sun_coordinate.pitch < np.deg2rad(20) and sun_coordinate.yaw > np.deg2rad(180)) or
      (sun_coordinate.pitch < np.deg2rad(40) and sun_coordinate.yaw < np.deg2rad(180))):
    print '%s: hybernate mode.' % datetime.datetime.now()
    return 300

  mirror_coordinate = mirror_client.GetMirrorCoordinate(target_coordinate)
  mirror_coordinate.Print()
  servo_client.MoveTo(mirror_coordinate)
  return 60


def ButtonStatusThread(target_client, mirror_command_callback):
  prev_target = target_client.GetTarget()
  while True:
    current_target = target_client.GetTarget()
    if current_target.name != prev_target.name:
      prev_target = current_target
      mirror_command_callback(target_coordinate=current_target.coordinate)
    time.sleep(1)


parser = argparse.ArgumentParser()
parser.add_argument(
    '--target', default=None,
    help='Overrides the button definition and manually defines a target.')
args = parser.parse_args()

pi_client = pigpio.pi()
mirror_client = mirror.MirrorClient(constants.OBSERVER_COORDINATE)
servo_client = servo.ServoClient(pi_client, constants.SERVO_PARAMETERS)
target_client = target.TargetClient(pi_client, constants.TARGET_PARAMETERS)
target = target_client.GetTarget()

mirror_command_callback = functools.partial(
    MirrorCommandCallback, 
    mirror_client=mirror_client, 
    servo_client=servo_client)

button_status_thread = threading.Thread(
    target=ButtonStatusThread, arg=(target_client, mirror_command_callback))
button_status_thread.start()
time.sleep(5)  # Letting thread to start.

while True:
  sleeptime = mirror_command_callback(target_coordinate=target.coordinate)
  time.sleep(sleeptime)
