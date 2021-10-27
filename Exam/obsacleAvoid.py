from time import sleep
import math

import ARLO.robot

# Create a robot object and initialize

# send a go_diff command to drive forward
leftSpeed = math.floor(64 * 0.97)
rightSpeed = 64

frontDist = arlo.read_front_ping_sensor()
rightDist = arlo.read_right_ping_sensor()
leftDist = arlo.read_left_ping_sensor()

frontClear = False
left45Clear = False
right45Clear = False

safeFrontDist = 500
safeSideDist = 300

#Updating distance variables 
def update_dists():
    global frontDist
    global rightDist
    global leftDist

    frontDist = arlo.read_front_ping_sensor()
    rightDist = arlo.read_right_ping_sensor()
    leftDist= arlo.read_left_ping_sensor()

# Checking we are to close - Thus we have to change direction
def dists_safe():
    global left45Clear
    global right45Clear
    global frontClear
    
    frontClear = False
    left45Clear = False
    right45Clear = False

    if frontDist > safeFrontDist:
        frontClear = True
    if leftDist > safeSideDist:
        left45Clear = True
    if rightDist > safeSideDist:
        right45Clear = True

# if r = 1 turn left, 0 = right.   (0 = R, 
# r can only be 1 or 0
def turn_x_degree(x, r):
    rightDir = r
    leftDir = 1 - rightDir
    # 0.2 in time is good for small changes
    sleeptime = 0.005555 * x
    print(arlo.go_diff(leftSpeed, rightSpeed, leftDir, rightDir))
    sleep(round(sleeptime, 5))
    arlo.stop()

def obstacle():
    update_dists()
    dists_safe()
    go = False
    turn = 0
    # 0 = turn right
    while (not go):
        totalTurn = 0
        update_dists()
        dists_safe()
        if (not frontClear):
            if turn:
                totalTurn -= 10
            else:
                totalTurn += 10
            turn_x_degree(10,turn)
        elif (not left45Clear):
            turn = 0
            totalTurn += 10
            turn_x_degree(10,turn)
        elif (not right45Clear):
            turn = 1
            totalTurn -= 10
            turn_x_degree(10,turn)
        else:
            go = True
    return totalTurn

def obstacleAvoidance(particles):
    sum = 0
    while sum < secMeter:
        update_dists()
        dists_safe()
        if (frontClear and left45Clear and right45Clear):
            start = perf_counter()
            t = start
            arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
            while ((t - start) < distTime):
                update_dists()
                dists_safe()
                if (frontClear or left45Clear or right45Clear):
                    print("obstacle")
                    break
                t = perf_counter()
            sum += t-start
            arlo.stop()
            move.moveAllParticles((t-start)*secMeter/100, particles)
        else:
            turn = obstacle()
            move.turnAllParticles(math.radians(abs(turn)), particles)
    return particles