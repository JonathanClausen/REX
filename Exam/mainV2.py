from time import sleep
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

    reachedCurrentTarget = False 
    isLocalized = False
    #RUNNING UNTIL ALL ARE FOUND
    for nextLandmark in landmarkIDs:
        #Checking if we can localize ourself. If not, Random via obstacle() 
        while not isLocalized:
            particles, isLocalized = copy.deepcopy(findlocation.localization_turn(particles, arlo, landmarks, cam)) 
            if isLocalized:
                break
            obstacleAvoid.obstacleAvoidance(particles, arlo)

        #Localized Succedes -> Time to move, until target is reached. 
        while not reachedCurrentTarget:
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
            print("Calculating targetstatus")
            ts = targetStatus.checkTargetStatus(nextLandmark, cam) #Check comment above
           
            if (ts == 0):
                print("Target Visible -> Moving to", nextLandmark)
                turn, distTraveled, particles, hasEmergencyStopped = gotobox.run_goToBox(
                                                                                nextLandmark, 
                                                                                arlo, 
                                                                                particles, 
                                                                                landmarks, 
                                                                                cam)
                move.turnAllParticles(math.radians(abs(turn)), particles)
                move.moveAllParticles(distTraveled, particles)

            elif ts == 1:
                print("Obstacle in way, routeplanning")
                move.turnAll(targetOri, particles, arlo)
                turnRadians, dist = routePlan.routeplan()
                move.turnAll(turnRadians)
                move.moveAll(dist)
                move.turnAll(0-(turnRadians*2))

            elif ts == 2:
                print("Can't See target or other boxes, turning to target -> obstacleAvoidance")
                # move.turnAll(targetOri, particles, arlo)
                obstacleAvoid.obstacleAvoidance(particles, arlo)


            reachedCurrentTarget = targetStatus.verify(
                targetStatus.checkMean(meanParticle, target), 
                min(arlo.read_front_ping_sensor(),
                    arlo.read_left_ping_sensor(),
                    arlo.read_right_ping_sensor()),
                targetStatus.checkGoToBox(distToTarget, distTraveled),
                hasEmergencyStopped
            ) #Ret -> True/false
            if (not reachedCurrentTarget and hasEmergencyStopped):
                obstacleAvoid.obstacleAvoidance()


finally:
    cam.terminateCaptureThread()
