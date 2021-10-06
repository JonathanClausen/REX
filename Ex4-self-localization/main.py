import findlocation
import numpy as np
import particle
import math
import move
import localize
import sys

#Import arlo robot
sys.path.append("../")
import ARLO.robot

arlo = ARLO.robot.Robot()

target = np.array([150,0])
# Initialize particles
num_particles = 1000
particles = localize.initialize_particles(num_particles)

# Turn 360 until we find boxes (findlocation.py)

findlocation.localization_turn(particles, arlo)


# check location. Keep spinning
print("meanParticle = ")
meanParticle = localize.localize(10, particles, 0)
print(meanParticle.getX(), ", ", meanParticle.getY(), ", ", meanParticle.getTheta())

print("estimatetarget = ")
vecLength, targetOri = findlocation.estimate_target(0,150, meanParticle)
print(vecLength)

print("disttotarget = ")
distToTarget = math.sqrt(( target[0] - meanParticle.getX() )**2 + ( target[1] - meanParticle.getY() )**2)
print(distToTarget)


move.turnAll(targetOri, particles, arlo) 
print("moveall")
move.moveAll(distToTarget, particles, arlo)
if (distToTarget < 10):
    finished = True
    


    