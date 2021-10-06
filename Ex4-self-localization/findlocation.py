import sys
import math
from time import sleep
import particle
import numpy as np
import localize



# Get ARLO.Robot
sys.path.append("../")
import ARLO.robot

arlo = ARLO.robot.Robot()


def localization_turn(particles):
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
        ## sample
        sleep(1)

        ## Update samples to turn 20 degrees.
        
def estimate_target(targetX, targetY, p):
    vecX = targetX - p.getX()
    vecY = targetY - p.getY()
    roboOri = p.getTheta()

    vecLength = math.sqrt((vecX**2) + (vecY**2))
    targetOri = math.atan2(vecY, vecX)

    deltaOri = targetOri - roboOri   

    if (deltaOri > (math.pi)):
        deltaOri = (-2*(math.pi)+deltaOri)
    elif (deltaOri < (-1*(math.pi))):
        deltaOri = (2*(math.pi)+deltaOri)

    return (vecLength, deltaOri)


