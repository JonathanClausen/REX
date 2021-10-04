import findlocation
import numpy as np
import particle
import selflocalize
import math
import move
import localize

target = np.array([150,0])
# Initialize particles
num_particles = 1000
particles = selflocalize.initialize_particles(num_particles)

# Turn 360 until we find boxes (findlocation.py)
#initial_location = findlocation.localization_turn(particles)

# Main loop


# Drive towards middle of boxes


# check location.
meanParticle = localize.localize(10, particles, 0)
vecLength, targetOri = findlocation.estimate_target(0,300, meanParticle)
distToTarget = math.sqrt(( target[0] - meanParticle.getX() )**2 + ( target[1] - meanParticle.getY() )**2)

#Moving
#move.turnAll(targetOri, particles) 
move.moveAll(vecLength, particles)
if (distToTarget < 10):
    finished = True
    


    