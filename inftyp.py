from time import sleep

import ARLO.robot


arlo = robot.Robot()


def TurnRight():
    print(arlo.go_diff(64, 32, 1, 1))


while True:
