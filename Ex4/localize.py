#!/usr/bin/env python3

from numpy.linalg.linalg import norm
import cv2
import particle
import camera
import numpy as np
import math
import random
import sys
import copy



#sys.path.append("../ARLO/")


# a is a uniform number between 0 and 1
def chooseSample(Weights, a):
    i = 0
    j = len(Weights)-1

    while (True):
        b = math.ceil(((j - i) / 2) + i)
        if (a == Weights[b]):
            return b
        elif (a > Weights[b]):
            i = b
        else:
            if j == b:
                return b
            else:
                j = b


#Simple Randomizer
def randomizer(particles, p):
    n = len(particles)
    nRandom = math.floor((len(particles)/100*p))
    for p in range(nRandom):
        particles[p] = particle.Particle(600.0*np.random.ranf() - 100.0, 600.0*np.random.ranf() - 250.0,
                                             np.mod(2.0*np.pi*np.random.ranf(), 2.0*np.pi), 0.01/n)


# Some color constants in BGR format
CRED = (0, 0, 255)
CGREEN = (0, 255, 0)
CBLUE = (255, 0, 0)
CCYAN = (255, 255, 0)
CYELLOW = (0, 255, 255)
CMAGENTA = (255, 0, 255)
CWHITE = (255, 255, 255)
CBLACK = (0, 0, 0)

# Landmarks.
# The robot knows the position of 2 landmarks. Their coordinates are in the unit centimeters [cm].
landmarkIDs = [7, 1 ]
landmarks = {

    1: (0.0, 0.0),  # Coordinates for landmark 1
    7: (300.0, 0.0)   # Coordinates for landmark 3
    #4: (300.0, 0.0)  # Coordinates for landmark 4
}


def localize(numResample, particles, debug, cam):
    est_pose = particle.estimate_pose(particles) # The estimate of the robots current pose
    num_particles = len(particles)

    varNorm = 30
    varTheta = 0.1
    varPos = 3
    varOri = 0.1
    for run in range(numResample):
        if debug:
            print("Runnig sampling ", run)

        # Fetch next frame
        colour = cam.get_next_frame()
        # Detect objects
        objectIDs, dists, angles = cam.detect_aruco_objects(colour)
        if not isinstance(objectIDs, type(None)):
            # List detected objects
            for i in range(len(objectIDs)):
                print("Object ID = ", objectIDs[i], ", Distance = ", dists[i], ", angle = ", angles[i])
                    # XXX: Do something for each detected object - remember, the same ID may appear several times
                lx = (landmarks[objectIDs[i]])[0]
                ly = (landmarks[objectIDs[i]])[1]
                sumWeight = 0
                for p in particles:
                    # Calculating coordinate weights
                    pDist = math.sqrt( ( lx - p.getX() )**2 + ( ly - p.getY() )**2 )
                    pPosWeight =  1/math.sqrt(2*math.pi * varNorm**2) * math.exp(- ((dists[i] - pDist )**2) / (2 * varNorm**2))

                    # Calculating orientation weight

                    e0 = np.array([ [ math.cos(p.getTheta()) ],[ math.sin(p.getTheta())]])
                    el = (np.array([ [ lx - p.getX() ],[ ly - p.getY() ] ])) / pDist
                    eHat = np.array([[ - math.sin( p.getTheta() )], [ math.cos( p.getTheta() )]])

                    pPhi = (np.sign(el.T @ eHat)) * (np.arccos(el.T @ e0))

                    pOrientWeight = 1/math.sqrt(2*math.pi * varTheta**2) * math.exp(- ((angles[i] - pPhi )**2) / (2 * varTheta**2))

                    pWeight = pPosWeight * pOrientWeight

                    sumWeight += pWeight
                    p.setWeight(pWeight)


                # Normalize weights
                newParticles = copy.deepcopy(particles)
                cumNormWeights = np.zeros(len(particles))

                #normWeight = np.zeros(num_particles)
                for p in range(len(particles)):
                    normWeight = (particles[p].getWeight()/sumWeight)
                    newParticles[p].setWeight(normWeight)
                    if p == 0:
                        cumNormWeights[p] = normWeight
                    else:
                        cumNormWeights[p] = normWeight + cumNormWeights[p-1]


                #Resampling
                for p in range(len(particles)):
                    a = random.uniform(0.0, 1.0)
                    i = chooseSample(cumNormWeights, a)
                    newParticles[p] = copy.deepcopy(particles[i])
                particle.add_uncertainty(newParticles, varPos, varOri)
                particles = copy.deepcopy(newParticles)
                #randomizer(particles,0.5)

            #est_pose = particle.estimate_pose(particles) # The estimate of the robots current pose

            if debug:
                print("est_pose X = ", est_pose.getX(), " Y = ", est_pose.getY(), " theta = ", est_pose.getTheta())
    return particles




def initialize_particles(num_particles):
    particles = []
    for i in range(num_particles):
        # Random starting points.
        p = particle.Particle(600.0*np.random.ranf() - 100.0, 600.0*np.random.ranf() - 250.0, np.mod(2.0*np.pi*np.random.ranf(), 2.0*np.pi), 1.0/num_particles)
        particles.append(p)
    return particles


#particles = initialize_particles(1000)
#pos = localize(10, particles, 0)
#print("X = ", pos.getX(), " - Y = ", pos.getY(), " - Theta = ", pos.getTheta())
