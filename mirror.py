import coordinate
import datetime
import ephem
import numpy as np


def GetReflectionAngles(sun_coordinate, mirror_coordinate):
  world_ray_sun = sun_coordinate.GetRay(reverse=True)
  world_normal_mirror = mirror_coordinate.GetRay(reverse=False)
  dot_product = world_ray_sun.transpose().dot(world_normal_mirror)
  world_ray_reflection = world_ray_sun - 2 * dot_product * world_normal_mirror

  reflection_yaw = np.arctan2(world_ray_reflection[1], world_ray_reflection[0])
  reflection_pitch = np.arcsin(-world_ray_reflection[2])
  if reflection_yaw < 0:
    reflection_yaw += 2 * np.pi
  return coordinate.Coordinate(
      pitch=reflection_pitch, yaw=reflection_yaw, name='Reflection', degree=False)


def GetMirrorCoordinate(sun_coordinate,
                        target_coordinate, 
                        convergence_precision=np.deg2rad(0.1),
                        max_iter=10,
                        verbose=False):
  mirror_coordinate = (sun_coordinate + target_coordinate) / 2.0
  mirror_coordinate.name = 'mirror'

  for i in xrange(max_iter):
    if verbose:
      print('*********************************************')
      print('Iter %d' % i)
      mirror_coordinate.Print()
    reflection_coordinate = GetReflectionAngles(sun_coordinate, mirror_coordinate)
    error_coordinate = target_coordinate - reflection_coordinate
    error_coordinate.name = 'error'
    if verbose:
      error_coordinate.Print()
    mirror_coordinate += error_coordinate / 10.0
    mirror_coordinate.name = 'mirror'
    if (abs(error_coordinate.yaw) < convergence_precision and
        abs(error_coordinate.pitch) < convergence_precision):
      break

  reflection_coordinate = GetReflectionAngles(sun_coordinate, mirror_coordinate)

  if verbose:
    print('*********************************************')
    reflection_coordinate.Print()
    mirror_coordinate.Print()
  return mirror_coordinate


class MirrorClient(object):

  def __init__(self, observer_coordinate):
    self._observer = ephem.Observer()
    self._observer.lat = observer_coordinate[0]
    self._observer.long = observer_coordinate[1]

  def GetSunCoordinate(self):
    self._observer.date = datetime.datetime.utcnow()
    sun = ephem.Sun(self._observer)
    return coordinate.Coordinate(pitch=float(sun.alt), yaw=float(sun.az), name='Sun', degree=False)

  def GetMirrorCoordinate(self,
                          target_coordinate, 
                          convergence_precision=np.deg2rad(0.1),
                          max_iter=50):
    sun_coordinate = self.GetSunCoordinate()
    return GetMirrorCoordinate(sun_coordinate,
                               target_coordinate, 
                               convergence_precision,
                               max_iter)
