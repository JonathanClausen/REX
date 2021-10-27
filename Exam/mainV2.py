import findlocation
import numpy as np
import particle
import math
import move
import localize
import sys
import camera
from time import sleep
import copy
import gotobox
import obstacleAvoid
import routePlan

#Import arlo robot
sys.path.append("../")
import ARLO.robot

try:
    arlo = ARLO.robot.Robot()
    cam = camera.Camera(0, 'arlo', useCaptureThread = True)

    landmarkIDs = [1,2,3,4]
    landmarks = {
            1: (0.0, 0.0),  # Coordinates for landmark 1
            2: (0.0, 300.0),
            3: (400.0, 0.0),
            4: (400.0, 300.0)
        }

    particles = localize.initialize_particles(num_particles)
    reachedCurrentTarget = False 
    targetList = [1,2,3,4,1]
    localized = localize()

    #RUNNING UNTIL ALL ARE FOUND
    for nextLandmark in targetList:
        #Checking if we can localize ourself. If not, Random via obstacle() 
        while not localized:
            obstacleAvoid.obstacleAvoidance()
            localized = localize() #True if found

        #Localized Succedes -> Time to move, until target is reached. 
        while not reachedCurrentTarget:
            #Returns -> 0,1,2
            #0 -> See goals and clear 
            #1 -> See other box in path
            #2 -> See nothing
            print("Attempting to find target: ", nextLandmark)		
            goalVisible = turnToGoal()
            if goalVisible == 0:
                print("Goal Visible Moving")
                turn, distTraveled, hasReachedTarget = gotobox.run_goToBox(landmarkIDs[nextLandmarkIndex], arlo, cam)

            
            elif goalVisible == 1:
                print("Obstacle in way, routeplanning")
                turnRadians, dist = routePlan.routeplan()
                move.turnAll(turnRadians)
                move.moveAll(dist)
                move.turnAll(0-(turnRadians*2))

            elif goalVisible == 2:
                print("Can't See Anything, doing obstacleAvoidance")
                obstacleAvoidance()


            reachedCurrentTarget = reachedTarget() #Ret -> True/false
            if not reachedCurrentTarget and emergencyStop:
                obstacleAvoidance()


finally:
    cam.terminateCaptureThread()
    


    



            