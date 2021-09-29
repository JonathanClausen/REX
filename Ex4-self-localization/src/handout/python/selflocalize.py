import cv2
import particle
import camera
import numpy as np
import time
import math
import random
from timeit import default_timer as timer
import sys
import copy



# Flags
showGUI = True  # Whether or not to open GUI windows
onRobot = False # Whether or not we are running on the Arlo robot


def isRunningOnArlo():
    """Return True if we are running on Arlo, otherwise False.
      You can use this flag to switch the code from running on you laptop to Arlo - you need to do the programming here!
    """
    return onRobot

# a is a uniform number between 0 and 1
def chooseSample(particles, a):
    for i in range(len(particles)):
        a -= particles[i].getWeight()
        if (a <= 0.0):
            return i
    return len(particles)-1

#Simple Randomizer    
def randomizer(particles, p):
    n = len(particles)
    nRandom = math.floor((len(particles)/100*p))
    for p in range(nRandom):
        particles[p] = particle.Particle(600.0*np.random.ranf() - 100.0, 600.0*np.random.ranf() - 250.0,
                                             np.mod(2.0*np.pi*np.random.ranf(), 2.0*np.pi), 0.1/n)

if isRunningOnArlo():
    # XXX: You need to change this path to point to where your robot.py file is located
    # Check!
    sys.path.append("../../../../ARLO/")


try:
    import robot
    onRobot = True
except ImportError:
    print("selflocalize.py: robot module not present - forcing not running on Arlo!")
    onRobot = False


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
landmarkIDs = [1, 4]
landmarks = {

    1: (0.0, 0.0),  # Coordinates for landmark 1
    4: (300.0, 0.0)  # Coordinates for landmark 2
}
landmark_colors = [CRED, CGREEN] # Colors used when drawing the landmarks





def jet(x):
    """Colour map for drawing particles. This function determines the colour of 
    a particle from its weight."""
    r = (x >= 3.0/8.0 and x < 5.0/8.0) * (4.0 * x - 3.0/2.0) + (x >= 5.0/8.0 and x < 7.0/8.0) + (x >= 7.0/8.0) * (-4.0 * x + 9.0/2.0)
    g = (x >= 1.0/8.0 and x < 3.0/8.0) * (4.0 * x - 1.0/2.0) + (x >= 3.0/8.0 and x < 5.0/8.0) + (x >= 5.0/8.0 and x < 7.0/8.0) * (-4.0 * x + 7.0/2.0)
    b = (x < 1.0/8.0) * (4.0 * x + 1.0/2.0) + (x >= 1.0/8.0 and x < 3.0/8.0) + (x >= 3.0/8.0 and x < 5.0/8.0) * (-4.0 * x + 5.0/2.0)

    return (255.0*r, 255.0*g, 255.0*b)

def draw_world(est_pose, particles, world):
    """Visualization.
    This functions draws robots position in the world coordinate system."""

    # Fix the origin of the coordinate system
    offsetX = 100
    offsetY = 250

    # Constant needed for transforming from world coordinates to screen coordinates (flip the y-axis)
    ymax = world.shape[0]

    world[:] = CWHITE # Clear background to white

    # Find largest weight
    max_weight = 0
    for particle in particles:
        max_weight = max(max_weight, particle.getWeight())

    # Draw particles
    for particle in particles:
        x = int(particle.getX() + offsetX)
        y = ymax - (int(particle.getY() + offsetY))
        colour = jet(particle.getWeight() / max_weight)
        cv2.circle(world, (x,y), 2, colour, 2)
        b = (int(particle.getX() + 15.0*np.cos(particle.getTheta()))+offsetX, 
                                     ymax - (int(particle.getY() + 15.0*np.sin(particle.getTheta()))+offsetY))
        cv2.line(world, (x,y), b, colour, 2)

    # Draw landmarks
    for i in range(len(landmarkIDs)):
        ID = landmarkIDs[i]
        lm = (int(landmarks[ID][0] + offsetX), int(ymax - (landmarks[ID][1] + offsetY)))
        cv2.circle(world, lm, 5, landmark_colors[i], 2)

    # Draw estimated robot pose
    a = (int(est_pose.getX())+offsetX, ymax-(int(est_pose.getY())+offsetY))
    b = (int(est_pose.getX() + 15.0*np.cos(est_pose.getTheta()))+offsetX, 
                                 ymax-(int(est_pose.getY() + 15.0*np.sin(est_pose.getTheta()))+offsetY))
    cv2.circle(world, a, 5, CMAGENTA, 2)
    cv2.line(world, a, b, CMAGENTA, 2)



def initialize_particles(num_particles):
    particles = []
    for i in range(num_particles):
        # Random starting points. 
        p = particle.Particle(600.0*np.random.ranf() - 100.0, 600.0*np.random.ranf() - 250.0, np.mod(2.0*np.pi*np.random.ranf(), 2.0*np.pi), 1.0/num_particles)
        particles.append(p)

    return particles


# Main program #
try:
    if showGUI:
        # Open windows
        WIN_RF1 = "Robot view"
        cv2.namedWindow(WIN_RF1)
        cv2.moveWindow(WIN_RF1, 50, 50)

        WIN_World = "World view"
        cv2.namedWindow(WIN_World)
        cv2.moveWindow(WIN_World, 500, 50)


    # Initialize particles
    num_particles = 1000
    particles = initialize_particles(num_particles)

    est_pose = particle.estimate_pose(particles) # The estimate of the robots current pose

    # Driving parameters
    velocity = 0.0 # cm/sec
    angular_velocity = 0.0 # radians/sec

    # Initialize the robot (XXX: You do this)

    # Allocate space for world map
    world = np.zeros((500,500,3), dtype=np.uint8)

    # Draw map
    draw_world(est_pose, particles, world)

    print("Opening and initializing camera")
    if camera.isRunningOnArlo():
        cam = camera.Camera(0, 'arlo', useCaptureThread = True)
    else:
        cam = camera.Camera(0, 'macbookpro', useCaptureThread = True)

    while True:

        # Move the robot according to user input (only for testing)
        action = cv2.waitKey(10)
        if action == ord('q'): # Quit
            break
    
        if not isRunningOnArlo():
            if action == ord('w'): # Forward
                velocity += 4.0
            elif action == ord('x'): # Backwards
                velocity -= 4.0
            elif action == ord('s'): # Stop
                velocity = 0.0
                angular_velocity = 0.0
            elif action == ord('a'): # Left
                angular_velocity += 0.2
            elif action == ord('d'): # Right
                angular_velocity -= 0.2



        
        # Use motor controls to update particles
        # XXX: Make the robot drive
        # XXX: You do this


        # Fetch next frame
        colour = cam.get_next_frame()
        
        # Detect objects
        objectIDs, dists, angles = cam.detect_aruco_objects(colour)

        varNorm = 30
        varTheta = 0.1
        varPos = 3
        varOri = 0.1
        if not isinstance(objectIDs, type(None)):
            # List detected objects
            for i in range(len(objectIDs)):
                #print("Object ID = ", objectIDs[i], ", Distance = ", dists[i], ", angle = ", angles[i])
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
                #normWeight = np.zeros(num_particles)
                for p in range(len(particles)):
                    newParticles[p].setWeight((particles[p].getWeight()/sumWeight))

                #Resampling
                for p in range(len(particles)):
                    a = random.uniform(0.0, 1.0)
                    i = chooseSample(newParticles, a)
                    newParticles[p] = copy.copy(particles[i])
                particle.add_uncertainty(newParticles, varPos, varOri)
                particles = copy.deepcopy(newParticles)
                #randomizer(particles,0.5)

                

            # Resampling ^^Look above 
            # XXX: You do this
            
            



            # Draw detected objects
            cam.draw_aruco_objects(colour)
        else:
            # No observation - reset weights to uniform distribution
            for p in particles:
                p.setWeight(1.0/num_particles)
                
        est_pose = particle.estimate_pose(particles) # The estimate of the robots current pose

        if showGUI:
            # Draw map
            draw_world(est_pose, particles, world)
    
            # Show frame
            cv2.imshow(WIN_RF1, colour)

            # Show world
            cv2.imshow(WIN_World, world)
    
  
finally: 
    # Make sure to clean up even if an exception occurred
    
    # Close all windows
    cv2.destroyAllWindows()

    # Clean-up capture thread
    cam.terminateCaptureThread()

