from time import sleep
import math
import ARLO.robot


arlo = ARLO.robot.Robot()


def Circle(r,outerSpeed):
    inner = 2 * (r - 19.4) * math.PI
    outer = 2 * (r + 19.4) * math.PI

    outerTime = outer / (0.622 * outerSpeed)

    innerSpeed = inner / (0.622 * outerTime)

    print(arlo.go_diff(math.floor(outerSpeed * 0.97), innerSpeed, 1, 1))


Circle(50,100)
