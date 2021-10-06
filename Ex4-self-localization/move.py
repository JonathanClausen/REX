import sys
import math
from time import sleep
import particle
from time import perf_counter
import numpy as np

sys.path.append("../")
import ARLO.robot
arlo = ARLO.robot.Robot()

leftSpeed = math.floor(64 * 0.97)
rightSpeed = 64

safeDist      = 300
safeDistSide  = 150

secMeter      = 2.55
stopDist      = 400
stopDistSide  = 200

def go_straight(length):
    emStop = False
    sensFront = arlo.read_front_ping_sensor()
    ensLeft = arlo.read_left_ping_sensor()
    sensRight = arlo.read_right_ping_sensor()
    distTime = round(length/100*secMeter,5)
    while (distTime > 0.1 and (not emStop)):
        print("time to go", distTime)
        start = perf_counter()
        t = start
        arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
        while ((t - start) < distTime):
            sensFront = arlo.read_front_ping_sensor()
            sensLeft = arlo.read_left_ping_sensor()
            sensRight = arlo.read_right_ping_sensor()
            if (sensFront < safeDist or
                sensRight < safeDistSide or
                sensLeft  < safeDistSide):
                print("Emercency stop!!! sensors :\nR ", sensRight,
                      ",\n L ", sensLeft,
                      ",\n F ", sensFront,
                      "\n time traveled = ", t)
                emStop = True
                break
            t = perf_counter()
        arlo.stop()
    return

def goTurn(deg):
    degSec = 0.005
    # this makes a full circle

    if (np.sign(deg) == 1):
        # Turn right
        print(arlo.go_diff(leftSpeed, rightSpeed, 0, 1))
    else:
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
    sleep(round(deg * degSec, 5) )
    print(arlo.stop())
    ## sample

def moveAll(length, particles):
    go_straight(length)
    for p in particles: 
        x = math.cos(p.getTheta())*length
        y = math.sin(p.getTheta())*length
        particle.move_particle(p,x,y,0)


def turnAll(delta_theta, particles):
    goTurn(delta_theta)
    for p in particles: 
        p.setTheta(particle.getTheta()+delta_theta)


