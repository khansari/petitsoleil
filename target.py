import pigpio


class TargetParameters(object):
  def __init__(self, name, coordinate):
    self.name = name
    self.coordinate = coordinate


class TargetClient(object):
  def __init__(self, pi_client, target_parameters):
    self._pi_client = pi_client
    self._target_parameters = target_parameters
    for pin in self._target_parameters.keys():
      if pin < 0:
        continue
      self._pi_client.set_mode(pin, pigpio.INPUT)
      self._pi_client.set_pull_up_down(pin, pigpio.PUD_UP)

  def GetTargetCoordinateFromButtons(self):
    for target_pin, target_parameter in self._target_parameters.iteritems():
      if target_pin < 0:  # Skipping the idle pin.
        continue
      if not self._pi_client.read(target_pin):
        return target_parameter.coordinate
    # If button is in the idle pose, returning the idle coordinate.
    return self._target_parameters[-1].coordinate

  def GetTargetCoordinateFromName(self, target_name):
    for target_parameter in self._target_parameters.values():
      if target_name == target_parameter.name:
        return target_parameter.coordinate
    # If no match is found, we return the idle coordinate.
    return self._target_parameters[-1].coordinate
