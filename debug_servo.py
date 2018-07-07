import constants
import coordinate
import pigpio
import servo


pi_client = pigpio.pi()
servo_client = servo.ServoClient(pi_client, constants.SERVO_PARAMETERS)

while True:
  input = raw_input('Enter pitch yaw: ')
  input_list = input.split(' ')
  pitch = int(input_list[0])
  yaw = int(input_list[1])
  target = coordinate.Coordinate(pitch=pitch, yaw=yaw, degree=True, name='target')
  target.Print()
  servo_client.MoveTo(target)
  