from Exam.routePlan import findWay, go_to_xy
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

#Import arlo robot
sys.path.append("../")
import ARLO.robot

try:
    arlo = ARLO.robot.Robot()
    cam = camera.Camera(0, 'arlo', useCaptureThread = True)

    
    boxOne = np.array([300,0])
    # Initialize particles
    num_particles = 1000

    perimiterToTargets = 40
    # Landmarks.
    # The robot knows the position of 2 landmarks. Their coordinates are in the unit centimeters [cm].
    landmarkIDs = [1,9,3,4]
    landmarks = {
        1: (0.0, 0.0),  # Coordinates for landmark 1
        9: (0.0, 300.0),
        3: (400.0, 0.0),
        4: (400.0, 300.0)
    }

    nextLandmark = 0
    
    particles = localize.initialize_particles(num_particles)
    distToTarget = 100
    # Initializing target
    target = [landmarks[landmarkIDs[nextLandmark]][0], landmarks[landmarkIDs[nextLandmark]][1]]

    while (nextLandmark < 4):
        
        particles = copy.deepcopy(findlocation.localization_turn(particles, arlo, landmarks, cam)) 
        
        # check location. Keep spinning
        print("meanParticle = ")
        meanParticle = particle.estimate_pose(particles)
        print(meanParticle.getX(), ", ", meanParticle.getY(), ", ", meanParticle.getTheta())

        # Update target to next target in landmarks if current target reached.
        if (distToTarget < 30):
            nextLandmark += 1
            print("Next target is: ", landmarkIDs[nextLandmark])
            target = [landmarks[landmarkIDs[nextLandmark]][0], landmarks[landmarkIDs[nextLandmark]][1]]
        x,y = findWay(meanParticle, landmarkIDs[1], cam)
        target, dist = go_to_xy(x,y)
        move.turnAll(var2, particles, arlo) 
        sleep(1)
        move.moveAll(round(distToTarget * 1.10, 5), particles, arlo)
        

finally:
    cam.terminateCaptureThread()