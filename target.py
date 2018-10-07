import pigpio


class TargetParameters(object):
  def __init__(self, coordinate=None, pin=None):
    self.coordinate = coordinate
    self.pin = pin
  
  @property
  def name(self):
    if self.coordinate is None:
      return 'None'
    return self.coordinate.name


class TargetClient(object):
  def __init__(self, pi_client, target_parameters, user_target_name):
    self._user_target_name = user_target_name
    self._pi_client = pi_client
    self._target_parameters = target_parameters
    for target_parameter in self._target_parameters.values():
      if target_parameter.pin is None:  # Skipping the no button cases.
        continue
      self._pi_client.set_mode(target_parameter.pin, pigpio.INPUT)
      self._pi_client.set_pull_up_down(target_parameter.pin, pigpio.PUD_UP)

  def GetTarget(self):
    # The default value.
    if self._user_target_name is None:
      selected_target_parameter = self._target_parameters['idle']
    else:
      selected_target_parameter = self._target_parameters[self._user_target_name]

    for target_parameter in self._target_parameters.values():
      if target_parameter.pin is None:  # Skipping the no button cases.
        continue
      if not self._pi_client.read(target_parameter.pin):
        selected_target_parameter = target_parameter
        # print(target_parameter.pin)
        break
    return selected_target_parameter
