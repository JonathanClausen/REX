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
    # this makes a full circle
    deg = 30
    timesToTurn = 19 

    for i in range(timesToTurn):
        print(arlo.go_diff(leftSpeed, rightSpeed, 0, 1))
        sleep(round(deg * degSec, 5) )
        print(arlo.stop())
        sleep(1)

        ## Check surroundings for box
        ## Update samples to turn 20 degrees.

localization_turn()
