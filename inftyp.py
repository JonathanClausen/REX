from time import sleep
import math
import ARLO.robot


arlo = ARLO.robot.Robot()


def Circle(r,outerSpeed, dir):
    inner = 2 * (r - 19.4) * math.pi
    outer = 2 * (r + 19.4) * math.pi

    outerTime = outer / (0.622 * outerSpeed)

    innerSpeed = inner / (0.622 * outerTime)
    if (dir == 0):
        print(arlo.go_diff(math.floor(outerSpeed * 0.97), math.floor(innerSpeed), 1, 1))
        sleep(10.9)
    else:
        print(arlo.go_diff(math.floor(innerSpeed * 0.97), math.floor(outerSpeed), 1, 1))
        sleep(11.5)



i = 3

while(i > 0):
	Circle(50,64,0)
#	print(arlo.stop())
#	sleep(0.5)
	Circle(50,64,1)
	print(arlo.stop())
	i = i-1
