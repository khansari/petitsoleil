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
    super(StoppableThread, self).__init__()
    self._stop_event = threading.Event()
    self._target_client = target_client
    self._mirror_command_callback = mirror_command_callback

  def stop(self):
    self._stop_event.set()

  def stopped(self):
    return self._stop_event.is_set()

  def run(self):
    prev_target = self._target_client.GetTarget()
    while not stopped():
      current_target = self._target_client.GetTarget()
      if current_target.coordinate.name != prev_target.coordinate.name:
        prev_target = current_target
        self._mirror_command_callback(
            target_coordinate=current_target.coordinate)
      time.sleep(1)


def MirrorCommandCallback(
    mirror_client, servo_client, target_coordinate):
  print('************************************************************')
  # Printing time in pacific time zone.
  print(datetime.datetime.now() + datetime.timedelta(hours=-7))
  target_coordinate.Print()
  sun_coordinate = mirror_client.GetSunCoordinate()
  sun_coordinate.Print()

  if target_coordinate.name == 'sun':
    servo_client.MoveTo(sun_coordinate)
    return 60
  elif target_coordinate.name == 'idle':
    servo_client.MoveTo(target_coordinate)
    return 60
   

  if ((sun_coordinate.pitch < np.deg2rad(20) and sun_coordinate.yaw > np.deg2rad(180)) or
      (sun_coordinate.pitch < np.deg2rad(40) and sun_coordinate.yaw < np.deg2rad(180))):
    print('Hybernate mode is active.')
    servo_client.MoveTo(constants.TARGET_PARAMETERS['idle'].coordinate)
    return 300

  mirror_coordinate = mirror_client.GetMirrorCoordinate(target_coordinate)
  mirror_coordinate.Print()
  servo_client.MoveTo(mirror_coordinate)
  return 60


parser = argparse.ArgumentParser()
parser.add_argument(
    '--target', default=None,
    help='Overrides the button definition and manually defines a target.')
args = parser.parse_args()

pi_client = pigpio.pi()
mirror_client = mirror.MirrorClient(constants.OBSERVER_COORDINATE)
servo_client = servo.ServoClient(pi_client, constants.SERVO_PARAMETERS)
target_client = target.TargetClient(pi_client, constants.TARGET_PARAMETERS, args.target)
target = target_client.GetTarget()

mirror_command_callback = functools.partial(
    MirrorCommandCallback, 
    mirror_client=mirror_client, 
    servo_client=servo_client)

button_status_thread = ButtonStatusThread(target_client, mirror_command_callback)
try:
  button_status_thread.start()
  print('Started button status thread.')
  time.sleep(1)  # Letting thread to start.

  while True:
    sleeptime = mirror_command_callback(target_coordinate=target.coordinate)
    time.sleep(sleeptime)
except KeyboardInterrupt:
  button_status_thread.stop()
  button_status_thread.join()