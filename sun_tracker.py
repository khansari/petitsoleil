import datetime
import ephem
import math

OBSERVER_COORDINATE = ['37.49000', '-122.25910']  # [lat, long]

class SunTracker(object):

  def __init__(self, observer_coordinate):
    self._observer = ephem.Observer()
    self._observer.lat = observer_coordinate[0]
    self._observer.long = observer_coordinate[1]

  def GetSunLocation(self):
    self._observer.date = datetime.datetime.utcnow()
    sun = ephem.Sun(self._observer)
    sun_elevation = float(sun.alt) * 180 / math.pi
    sun_azimuth = float(sun.az) * 180 / math.pi
    print 'Sun location: (%f, %f)' % (sun_elevation, sun_azimuth)
    return (sun_elevation, sun_azimuth)
