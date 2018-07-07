
import math
import numpy as np


def GetRay(yaw, pitch, reverse=False):
  dir = -1 if reverse else 1
  return dir * np.array([ np.cos(yaw) * np.cos(pitch), 
                          np.sin(yaw) * np.cos(pitch), 
                         -np.sin(pitch)])

def GetReflectionAngles(sun_pitch, sun_yaw, mirror_pitch, mirror_yaw):
  world_ray_sun = GetRay(sun_yaw, sun_pitch, reverse=True)
  world_normal_mirror = GetRay(mirror_yaw, mirror_pitch, reverse=False)
  dot_product = world_ray_sun.transpose().dot(world_normal_mirror)
  world_ray_reflection = world_ray_sun - 2 * dot_product * world_normal_mirror

  reflection_yaw = np.arctan2(world_ray_reflection[1], world_ray_reflection[0])
  reflection_pitch = np.arcsin(-world_ray_reflection[2])
  print('reflection_yaw: %0.2f' % np.rad2deg(reflection_yaw))
  print('reflection_pitch: %0.2f' % np.rad2deg(reflection_pitch))
  return reflection_pitch, reflection_yaw

def GetMirrorPitchYaw(sun_pitch, sun_yaw, target_pitch, target_yaw, 
                      convergence_precision=np.deg2rad(0.1),
                      max_iter=10):
  mirror_pitch = (sun_pitch + target_pitch) / 2.0
  mirror_yaw = (sun_yaw + target_yaw) / 2.0

  for i in xrange(max_iter):
    print('*********************************************')
    print('Iter %d' % i)
    print('Using mirror (pitch, yaw): (%0.2f, %.2f)' % 
          (np.rad2deg(mirror_pitch), np.rad2deg(mirror_yaw)))
    reflection_pitch, reflection_yaw = GetReflectionAngles(
        sun_pitch, sun_yaw, mirror_pitch, mirror_yaw)
    error_yaw = target_yaw - reflection_yaw
    mirror_yaw += error_yaw / 2.0
    error_pitch = target_pitch - reflection_pitch
    mirror_pitch += error_pitch / 2.0
    if (abs(error_yaw) < convergence_precision and
        abs(error_pitch) < convergence_precision):
      break

  print('*********************************************')
  print('mirror_yaw: %0.2f' % np.rad2deg(mirror_yaw))
  print('mirror_pitch: %0.2f' % np.rad2deg(mirror_pitch))
  GetReflectionAngles(
        sun_yaw, sun_pitch, mirror_yaw, mirror_pitch)
