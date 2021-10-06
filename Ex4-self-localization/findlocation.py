import math
from time import sleep
import numpy as np
import localize
import move
import camera



# # Get ARLO.Robot
# sys.path.append("../")
# import ARLO.robot
# arlo = ARLO.robot.Robot()


def localization_turn(particles, arlo, cam):
    deg = 15
    counter = 0
    max_turn = 18
    landmarks = []
    seenBoth = False

    while((not seenBoth) and (counter <= max_turn)):
        
        #Turn particles and update particles 
        move.turnAll(math.radians(deg), particles, arlo)
        #meanParticle = localize.localize(2, particles, 0, cam)
        sleep(0.5)
        # Check if both boxes have been spotted.
        colour = cam.get_next_frame()
        sleep(0.5)
        objectIDs, dists, angles = cam.detect_aruco_objects(colour)
        print("Object IDs: ", objectIDs)
        if not isinstance(objectIDs, type(None)):
            meanParticle = localize.localize(1, particles, 1, cam)
            for i in range(len(objectIDs)):
                if (objectIDs[i] not in landmarks):
                    landmarks.append(objectIDs[i])
                    
                    print("Found landmark: ", objectIDs[i])
        if ((3 in landmarks) and (1 in landmarks)):
            seenBoth = True

        counter += 1

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


