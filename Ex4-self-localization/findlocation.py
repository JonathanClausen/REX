import sys
import math
from time import sleep



# Get ARLO.Robot
sys.path.append("../")
import ARLO.robot

arlo = ARLO.robot.Robot()

def localization_turn():
    leftSpeed = math.floor(64 * 0.97)
    rightSpeed = 64
    degSec = 0.005
    deg = 45
    timesToTurn = 16

    for i in range(timesToTurn):
        print(arlo.go_diff(leftSpeed, rightSpeed, 0, 1))
        sleep(10)
        print(arlo.stop())

        ## Check surroundings for box
        ## Update samples to turn 20 degrees.

localization_turn()
