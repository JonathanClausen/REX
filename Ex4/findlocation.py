import math
from time import sleep
import numpy as np
from numpy.core.fromnumeric import put
import sys
sys.path.append("../")
from ARLO.robot import Robot
from Ex5_Occupancy.Occupancy import occupancy_grid_mapping
import localize
import move
import camera
import copy
import particle 




# # Get ARLO.Robot
# sys.path.append("../")
# import ARLO.robot
# arlo = ARLO.robot.Robot()


def localization_turn(particles, arlo, cam):
    deg = 15
    counter = 0
    max_turn = 24
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

        if not isinstance(objectIDs, type(None)):
            particles = copy.deepcopy(localize.localize(1, particles, 0, cam))
            for i in range(len(objectIDs)):
                if (objectIDs[i] not in landmarks):
                    landmarks.append(objectIDs[i])
                    
                    print("Found landmark: ", objectIDs[i])
        if ((3 in landmarks) and (1 in landmarks)):
            seenBoth = True

        counter += 1

        ## Update samples to turn 20 degrees.
    return particles



def printMap(list, arlo, grid_size):
    y, x= np.shape(list)
    startLine = "+" + ("------+"*x)

    print("r Y " , arlo.getX())
    print("r Y " , arlo.getY())

    print(startLine)
    for i in range(y):
        print("|", end="")
        for j in range(x):
            if (math.floor(arlo.getX()/grid_size) == i and math.floor(arlo.getY()/grid_size) == j):
                print('{:^6}|'.format("R"), end="")
            elif not (list[i,j] == 0):
                print('{:^6}|'.format(round(list[i,j], 1)), end="")
            else:
                print('{:^6}|'.format(""), end="")
        print()
        print(startLine)
    print()

def localization_turn2(particles, arlo, cam, map):
    deg = 15
    counter = 0
    max_turn = 24
    landmarks = []
    seenBoth = False

    #Variables for OccupancyMap

    while((not seenBoth) and (counter <= max_turn)):
        
        #Turn particles and update particles 
        move.turnAll(math.radians(deg), particles, arlo)
        #meanParticle = localize.localize(2, particles, 0, cam)
        sleep(0.5)
        # Check if both boxes have been spotted.
        colour = cam.get_next_frame()
        sleep(0.5)
        objectIDs, dists, angles = cam.detect_aruco_objects(colour)

        if not isinstance(objectIDs, type(None)):
            particles = copy.deepcopy(localize.localize(1, particles, 0, cam))
            for i in range(len(objectIDs)):
                if (objectIDs[i] not in landmarks):
                    landmarks.append(objectIDs[i])
                    
                    print("Found landmark: ", objectIDs[i])
        if ((7 in landmarks) and (1 in landmarks)):
            seenBoth = True

        ######TASK 5 Creating occupancy map ##########
        distToObject = round(arlo.read_front_ping_sensor()/10)
        newMap = occupancy_grid_mapping(map, particle.estimate_pose(particles), distToObject)
        map = copy.deepcopy(newMap)
        printMap(map, particle.estimate_pose(particles), 30)
        ############################################
        counter += 1

        ## Update samples to turn 20 degrees.
    return particles, map


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


