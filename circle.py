from time import sleep
import math
import ARLO.robot


arlo = ARLO.robot.Robot()


def Circle(r,outerSpeed):
    inner = 2 * (r - 20) * math.pi
    outer = 2 * (r + 20) * math.pi

    outerTime = outer / (0.622 * outerSpeed)
    print(outerTime)

    innerSpeed = inner / (0.622 * outerTime)
    print(innerSpeed)
    print(arlo.go_diff(math.floor(outerSpeed * 0.97), math.floor(innerSpeed), 1, 1))

    sleep(outerTime)
    print(arlo.stop())


Circle(50,100)
