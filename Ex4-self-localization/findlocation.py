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


def localization_turn(particles, arlo):
    deg = 20
    counter = 0
    max_turn = 18
    cam = camera.Camera(0)
    landmarks = []
    seenBoth = False

    while(not seenBoth or counter >= max_turn):
        #Turn particles and update particles 
        move.turnAll(deg, particles, arlo)
        meanParticle = localize.localize(2, particles, 0)

        # Check if both boxes have been spotted.
        colour = cam.get_next_frame()
        objectIDs, dists, angles = cam.detect_aruco_objects(colour)
        for i in range(len(objectIDs)):
            if (not isinstance(objectIDs[i], type(None)) and (objectIDs[i] not in landmarks)):
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


