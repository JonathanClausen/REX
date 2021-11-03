from time import sleep
import math
import move
from time import perf_counter


# send a go_diff command to drive forward
leftSpeed = math.floor(64 * 0.97)
rightSpeed = 64

secMeter = 2.55
degSec = 0.005

frontDist = 0
rightDist = 0
leftDist = 0

frontClear = False
left45Clear = False
right45Clear = False

safeFrontDist = 500
safeSideDist = 300


#Updating distance variables 
def update_dists(arlo):
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
def turn_x_degree(x, r, arlo):
    rightDir = r
    leftDir = 1 - rightDir
    # 0.2 in time is good for small changes
    sleeptime = 0.005555 * x
    arlo.go_diff(leftSpeed, rightSpeed, leftDir, rightDir)
    sleep(round(sleeptime, 5))
    arlo.stop()


def obstacle(arlo):
    update_dists(arlo)
    dists_safe()
    go = False
    turn = 0
    # 0 = turn right
    while (not go):
        sleep(0.2)
        totalTurn = 0
        update_dists(arlo)
        dists_safe()
        if (not frontClear):
            if turn:
                totalTurn -= 10
            else:
                totalTurn += 10
            turn_x_degree(10,turn, arlo)
        elif (not left45Clear):
            turn = 0
            totalTurn += 10
            turn_x_degree(10,turn, arlo)
        elif (not right45Clear):
            turn = 1
            totalTurn -= 10
            turn_x_degree(10,turn, arlo)
        else:
            go = True
    return totalTurn


def obstacleAvoidance(particles, arlo):
    sleep(0.5)
    sum = 0
    distTime = secMeter
    while sum < distTime:
        update_dists(arlo)
        dists_safe()
        if (frontClear and left45Clear and right45Clear):
            while (sum < distTime):
                start = perf_counter()
                arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
                update_dists(arlo)
                dists_safe()    
                if (not frontClear or not left45Clear or not right45Clear):
                    print("obstacle")
                    break
                t = perf_counter()
                sum += t-start
            arlo.stop()
            move.moveAllParticles(sum/secMeter*100, particles)
        else:
            turn = obstacle(arlo)
            move.turnAllParticles(math.radians(abs(turn)), particles)
    sleep(0.5)
    return particles
