import coordinate
import mirror

sun = coordinate.Coordinate(pitch=60, yaw=270, degree=True, name='sun')
sun.Print()
target = coordinate.Coordinate(pitch=10, yaw=135, degree=True, name='target')
target.Print()

mirror.GetMirrorCoordinate(sun, target, max_iter=50)
