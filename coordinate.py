import numpy as np


class Coordinate(object):
  def __init__(self, pitch, yaw, degree=False, name='unknown'):
    self.pitch = pitch
    self.yaw = yaw
    if degree:
      self.pitch = np.deg2rad(self.pitch)
      self.yaw = np.deg2rad(self.yaw)
    self.name = name

  def __add__(self, other):
    return Coordinate(pitch=(self.pitch + other.pitch), 
                      yaw=(self.yaw + other.yaw))

  def __sub__(self, other):
    return Coordinate(pitch=(self.pitch - other.pitch), 
                      yaw=(self.yaw - other.yaw))

  def __div__(self, divisor):
    assert isinstance(divisor, float) or isinstance(divisor, int)
    assert divisor > 0
    return Coordinate(pitch=(self.pitch / divisor), yaw=(self.yaw / divisor))

  def __mul__(self, multiplier):
    assert isinstance(multiplier, float) or isinstance(multiplier, int)
    return Coordinate(pitch=(self.pitch * multiplier), yaw=(self.yaw * multiplier))

  def GetRay(self, reverse=False):
    dir = -1 if reverse else 1
    return dir * np.array([ np.cos(self.yaw) * np.cos(self.pitch), 
                            np.sin(self.yaw) * np.cos(self.pitch), 
                           -np.sin(self.pitch)])

  def Print(self, degree=True):
    if degree:
      print('%s coordinate: (%0.2f, %0.2f)' % (np.rad2deg(self.pitch), 
                                               np.rad2deg(self.yaw)))
    else:
      print('%s coordinate: (%0.2f, %0.2f)' % (self.pitch, self.yaw))
    