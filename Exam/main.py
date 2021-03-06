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

#Import arlo robot
sys.path.append("../")
import ARLO.robot

try:
    arlo = ARLO.robot.Robot()
    cam = camera.Camera(0, 'arlo', useCaptureThread = True)

    
    # Initialize particles
    num_particles = 1000

    perimiterToTargets = 20
    # Landmarks.
    # The robot knows the position of 2 landmarks. Their coordinates are in the unit centimeters [cm].
    landmarkIDs = [1,2,3,4]
    landmarks = {
        1: (0.0, 0.0),  # Coordinates for landmark 1
        2: (0.0, 300.0),
        3: (400.0, 0.0),
        4: (400.0, 300.0)
    }

    nextLandmarkIndex = -1
    
    particles = localize.initialize_particles(num_particles)
    distToTarget = 100
    # Initializing target
    target = landmarks[landmarkIDs[nextLandmarkIndex]]
    hasReachedTarget = True

    while (nextLandmarkIndex < 4):
        
        # Update target to next target in landmarks if current target reached.
        if (hasReachedTarget):
            nextLandmarkIndex += 1
            if (nextLandmarkIndex >= len(landmarks)):
                nextLandmarkIndex = 0
            print("Next target is: ", landmarkIDs[nextLandmarkIndex])
            target = landmarks[landmarkIDs[nextLandmarkIndex]]

        particles = copy.deepcopy(findlocation.localization_turn(particles, arlo, landmarks, cam)) 
        
        # check location. Keep spinning
        print("meanParticle = ")
        meanParticle = particle.estimate_pose(particles)
        print(meanParticle.getX(), ", ", meanParticle.getY(), ", ", meanParticle.getTheta())

        # Adjusting target so we don't run into the box
        targetPerimiter = findlocation.adjusted_target(meanParticle, target, perimiterToTargets)

        vecLength, targetOri = findlocation.estimate_target(targetPerimiter[0], targetPerimiter[1], meanParticle)

        distToTarget = math.sqrt(( targetPerimiter[0] - meanParticle.getX() )**2 + ( targetPerimiter[1] - meanParticle.getY() )**2)
        print("Distance to target: ", distToTarget)

        move.turnAll(targetOri, particles, arlo)  # Turning towards current box
        sleep(1)
        # If box is visible then go to box
        colour = cam.get_next_frame()
        objectIDs, dists, angles = cam.detect_aruco_objects(colour)
        sleep(0.5)
        if not isinstance(objectIDs, type(None)):
            if (landmarkIDs[nextLandmarkIndex] in objectIDs):
                print("Going to box: ",landmarkIDs[nextLandmarkIndex])
                turn, distTraveled, particles  = gotobox.run_goToBox(landmarkIDs[nextLandmarkIndex], arlo, particles, landmarks, cam)
                print("Travelled dist = ",distTraveled)
                move.turnAllParticles(math.radians(abs(turn)), particles)
                move.moveAllParticles(distTraveled, particles)
        else:
            move.moveAll(distToTarget, particles, arlo)
        

finally:
    cam.terminateCaptureThread()
    


    