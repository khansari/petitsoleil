import collections
import coordinate
import json
import lirc
import numpy as np
import os
import pigpio
import time

_TARGET_PARAMETERS_CONFIG_FILENAME = 'configs/target_parameters.json'


class TargetClient(object):
  def __init__(self, user_target_name, config_filename=_TARGET_PARAMETERS_CONFIG_FILENAME):
    if user_target_name is None:
      self._current_target_name = 'idle'
    else:
      self._current_target_name = user_target_name
    lirc.init('petitsoleil', blocking=False)
    self._rate = 5
    self._config_filename = config_filename
    self._target_parameters = self.LoadConfig(self._config_filename)
    self._long_press_time = None

  def GetTarget(self):
    return self._target_parameters[self._current_target_name]

  def GetIdleTarget(self):
    return self._target_parameters['idle']
  
  def MayUpdateTarget(self):  
    button = lirc.nextcode()
    if not button:
      return
    button = str(button[0])

    if button != 'load' and button != 'save':
      self._long_press_time = None

    for target_name, target_parameter in self._target_parameters.iteritems():
      if target_name == button:
        self._current_target_name = button
        print 'Selected target %s.' % button
        return self._target_parameters[self._current_target_name]
 
    # If the target is set to sun, we do not need to check the rest of the method.
    if self._current_target_name == 'sun':
      return

    if button == 'up':
      self._target_parameters[self._current_target_name].pitch += np.deg2rad(self._rate) 
      return self.GetTarget() 
    elif button == 'down':
      self._target_parameters[self._current_target_name].pitch -= np.deg2rad(self._rate) 
      return self.GetTarget()
    elif button == 'right':
      self._target_parameters[self._current_target_name].yaw -= np.deg2rad(self._rate) 
      return self.GetTarget()
    elif button == 'left':
      self._target_parameters[self._current_target_name].yaw += np.deg2rad(self._rate) 
      return self.GetTarget()
    elif button == 'slow':
      self._rate = 1 
    elif button == 'medium':
      self._rate = 5 
    elif button == 'fast':
      self._rate = 10
    elif button == 'save' or button == 'load':
      if self._long_press_time is None:
        self._long_press_time = time.time()
      if time.time() - self._long_press_time > 3:  # seconds
        if button == 'save':
          self.SaveConfig(self._config_filename)
        else:
          self._target_parameters = self.LoadConfig(self._config_filename)
        self._long_press_time = None

  def LoadConfig(self, config_filename):
    with open(config_filename, 'r') as f:
      json_data = json.loads(f.read())  
    target_parameters = {}
    for data in json_data:
      if data['name'] == 'sun':
        target_parameters[data['name']] = coordinate.Coordinate(
            pitch=None, yaw=None, degree=True, name=data['name'])
      else:
        target_parameters[data['name']] = coordinate.Coordinate(
            pitch=data['pitch'], yaw=data['yaw'], degree=True, name=data['name'])
    print 'Config file %s was loaded successfully.' % config_filename
    return target_parameters

  def SaveConfig(self, config_filename):
    with open(config_filename, 'w') as f:
      data = []
      np.deg2rad(10)
      np.rad2deg(1)
      for target_name, target_parameter in self._target_parameters.iteritems():
        target_parameter_data = collections.OrderedDict()
        target_parameter_data['name'] = target_name
        if target_name != 'sun':
          target_parameter_data['pitch'] = np.rad2deg(target_parameter.pitch)
          target_parameter_data['yaw'] = np.rad2deg(target_parameter.yaw)
        data.append(target_parameter_data)
      json.encoder.FLOAT_REPR = lambda o: format(o, '.1f')
      f.write(json.dumps(data, indent=2, separators=(',', ': ')))
      print 'Config file %s was saved successfully.' % config_filename
