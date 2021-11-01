from time import sleep

from numpy.core.fromnumeric import mean
import verification
import findlocation
import numpy as np
import particle
import math
import move
import localize
import sys
import camera
import copy
import gotobox
import obstacleAvoid
import routePlan
import targetStatus


#Import arlo robot
sys.path.append("../")
import ARLO.robot

try:
    arlo = ARLO.robot.Robot()
    cam = camera.Camera(0, 'arlo', useCaptureThread = True)

    perimiterToTargets = 20

    landmarkIDs = [1,2,3,4,1]
    landmarks = {
            1: (0.0, 0.0),  # Coordinates for landmark 1
            2: (0.0, 300.0),
            3: (400.0, 0.0),
            4: (400.0, 300.0)
        }
        
    num_particles = 1000
    particles = localize.initialize_particles(num_particles)

    isLocalized = False
    hasEmergencyStopped = False
    #RUNNING UNTIL ALL ARE FOUND
    for nextLandmark in landmarkIDs:
        reachedCurrentTarget = False 
        #Checking if we can localize ourself. If not, Random via obstacle() 
        while not isLocalized:
            particles, isLocalized = copy.deepcopy(findlocation.localization_turn(particles, arlo, landmarks, cam)) 
            if isLocalized:
                break
            obstacleAvoid.obstacleAvoidance(particles, arlo)

        #Localized Succedes -> Time to move, until target is reached. 
        while not reachedCurrentTarget:
            print("_________________________________________________________\n")
            print("Attempting to find target: ", nextLandmark)
            target = landmarks[nextLandmark]

            meanParticle = particle.estimate_pose(particles)
            targetPerimiter = findlocation.adjusted_target(meanParticle, target, perimiterToTargets)
            vecLength, targetOri = findlocation.estimate_target(targetPerimiter[0], targetPerimiter[1], meanParticle)
            distToTarget = math.sqrt(( targetPerimiter[0] - meanParticle.getX() )**2 + ( targetPerimiter[1] - meanParticle.getY() )**2)
            move.turnAll(targetOri, particles, arlo)
            #ts ret -> 0,1,2
            #0 -> See goals and clear
            #1 -> See other box in path
            #2 -> See nothing
            ts = targetStatus.checkTargetStatus(nextLandmark, cam) #Check comment above
           
            if (ts == 0):
                print("TARGET IN SIGHT", nextLandmark)
                turn, distTraveled, particles, hasEmergencyStopped = gotobox.run_goToBox(
                                                                                nextLandmark, 
                                                                                arlo, 
                                                                                particles, 
                                                                                landmarks, 
                                                                                cam)
                move.turnAllParticles(math.radians(abs(turn)), particles)
                move.moveAllParticles(distTraveled, particles)
                meanCheck = verification.checkMean(meanParticle, target)
                closestPing = min(arlo.read_front_ping_sensor(),
                    arlo.read_left_ping_sensor(),
                    arlo.read_right_ping_sensor())
                boxCheck = verification.checkGoToBox(distToTarget, distTraveled)
                print("VERIFICATION:")
                print("parameters for verify: ")
                print("meanCheck = ", meanCheck)
                print("closestPing = ", closestPing)
                print("boxCheck = ", boxCheck)
                print("emergencyStop = ", hasEmergencyStopped) 

                reachedCurrentTarget = verification.verify(
                    meanCheck,
                    closestPing,
                    boxCheck,
                    hasEmergencyStopped)

            elif ts == 1:
                print("ROUTEPLANNING")
                turnRadians, dist = routePlan.findWay(cam)
                move.turnAll(turnRadians, particles, arlo)
                hasEmergencyStopped = move.moveAll(dist, particles, arlo)
                move.turnAll(0-(turnRadians*2),particles, arlo)

            elif ts == 2:
                print("OBSTACLE AVOIDANCE")
                # move.turnAll(targetOri, particles, arlo)
                obstacleAvoid.obstacleAvoidance(particles, arlo)
                particles, isLocalized = copy.deepcopy(findlocation.localization_turn(particles, arlo, landmarks, cam)) 
                hasEmergencyStopped = False


            
            #Ret -> True/false
            if (not reachedCurrentTarget and hasEmergencyStopped):
                print("EMERGENCYSTOP!")
                obstacleAvoid.obstacleAvoidance(particles, arlo)
            
            print("MEANPARTICLE X, Y:", meanParticle.getX(), meanParticle.getY() )
            

finally:
    cam.terminateCaptureThread()
