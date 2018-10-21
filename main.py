import argparse
import constants
import datetime
import functools
import pigpio
import mirror
import numpy as np
import servo
import target
import threading
import time

class ButtonStatusThread(threading.Thread):
  """Thread class with a stop() method. The thread itself has to check
  regularly for the stopped() condition."""

  def __init__(self, target_client, mirror_command_callback):
    super(ButtonStatusThread, self).__init__()
    self._stop_event = threading.Event()
    self._target_client = target_client
    self._mirror_command_callback = mirror_command_callback

  def stop(self):
    self._stop_event.set()

  def stopped(self):
    return self._stop_event.is_set()

  def run(self):
    while not self.stopped():
      new_target = self._target_client.MayUpdateTarget()
      if new_target is not None:
        self._mirror_command_callback()
      time.sleep(0.1)


def MirrorCommandCallback(
    mirror_client, servo_client, target_client, no_hybernate=False):
  print('************************************************************')
  # Printing time in pacific time zone.
  print(datetime.datetime.now() + datetime.timedelta(hours=-7))
  target_coordinate = target_client.GetTarget()
  if target_coordinate is None:
    print 'Petit Soleil is off.'
    return 300

  if target_coordinate.name != 'sun':
    target_coordinate.Print()
  sun_coordinate = mirror_client.GetSunCoordinate()
  sun_coordinate.Print()

  if target_coordinate.name == 'sun':
    servo_client.MoveTo(sun_coordinate)
    return 60
  elif target_coordinate.name == 'idle':
    servo_client.MoveTo(target_coordinate)
    return 60  

  if not no_hybernate and (
      (sun_coordinate.pitch < np.deg2rad(20) and sun_coordinate.yaw > np.deg2rad(180)) or
      (sun_coordinate.yaw < np.deg2rad(140))):
    print('Hybernate mode is active.')
    servo_client.MoveTo(constants.TARGET_PARAMETERS['idle'])
    return 300

  mirror_coordinate = mirror_client.GetMirrorCoordinate(target_coordinate)
  mirror_coordinate.Print()
  servo_client.MoveTo(mirror_coordinate)
  return 60


parser = argparse.ArgumentParser()
parser.add_argument(
    '--target', default=None,
    help='Overrides the button definition and manually defines a target.')
parser.add_argument(
    '--no_hybernate', action='store_true', default=False,
    help='When set, then the device does not go to hybernate mode.')
flags = parser.parse_args()

pi_client = pigpio.pi()
mirror_client = mirror.MirrorClient(constants.OBSERVER_COORDINATE)
servo_client = servo.ServoClient(pi_client, constants.SERVO_PARAMETERS)
target_client = target.TargetClient(user_target_name=flags.target)
mirror_command_callback = functools.partial(
    MirrorCommandCallback, 
    mirror_client=mirror_client, 
    servo_client=servo_client,
    target_client=target_client,
    no_hybernate=flags.no_hybernate)

button_status_thread = ButtonStatusThread(target_client, mirror_command_callback)
try:
  button_status_thread.start()
  print('Started button status thread.')
  time.sleep(1)  # Letting thread to start.

  while True:
    sleeptime = mirror_command_callback()
    time.sleep(sleeptime)
except KeyboardInterrupt:
  button_status_thread.stop()
  button_status_thread.join()
