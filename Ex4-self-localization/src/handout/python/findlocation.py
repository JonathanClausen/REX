import sys
import math
from time import sleep


# Get ARLO.Robot
sys.path.append("../../../../ARLO/")
import robot as arlo

def localization_turn():
    leftSpeed = math.floor(64 * 0.97)
    rightSpeed = 64
    degSec10 = 0.005
    timesToTurn = 16

    for i in range(timesToTurn):
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
        sleep(2 * degSec10)
        print(arlo.stop())

        ## Check surroundings for box
        ## Update samples to turn 20 degrees.

