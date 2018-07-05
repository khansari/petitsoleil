import datetime
import ephem
import math

date = datetime.datetime.utcnow()

obs=ephem.Observer()
obs.lat='37.49000'
obs.long='-122.25910'
obs.date = date
print obs

sun = ephem.Sun(obs)
sun.compute(obs)
sun_alt = float(sun.alt) * 180 / math.pi
sun_az = float(sun.az) * 180 / math.pi
print 'Sun location: (%f, %f)' % (sun_alt, sun_az)


