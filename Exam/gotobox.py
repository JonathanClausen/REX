#!/usr/bin/env python3

import cv2
import numpy as np
from time import sleep
import math
from time import perf_counter
from localize import localize
import copy
# from goDist import go

leftSpeed     = math.floor(64 * 0.97)
rightSpeed    = 64
degSec = 0.005

def getAng(targetBoxID, cam):
    markerLength = 0.145
    cameraMatrix =np.array([[506.94,0,640/2],
                            [0,506.94,480/2],
                            [0,0,1],])
    distCoeffs = 0

#distCoeffs[, rvecs[, tvecs[, _objPoints]]]

    sleep(0.5)
    frame = cam.get_next_frame()
    sleep(0.5)

#Grabbing dictionary
    objectIDs, dists, angles = cam.detect_aruco_objects(frame)

    if ((objectIDs is not None) and (targetBoxID in objectIDs)):
        # Get only target angle and target dist
        angles = angles[np.where(objectIDs == targetBoxID)]
        dists = dists[np.where(objectIDs == targetBoxID)]
        print("Filtered Object IDs, dists",objectIDs[objectIDs == targetBoxID], dists)
        # Choose shortest path to box if we can see two aruco codes with same id.
        if (len(dists) > 1):
            if (dists[0] < dists[1]):
                index = 0
            else:
                index = 1
        else: 
            index = 0
        
        dist = dists[index]
        radiantAngle = angles[index]
            
        degrees = math.degrees(radiantAngle)

        if (radiantAngle < math.pi):
            degrees = -1 * math.degrees(radiantAngle)

        
        #print("min dist, min angle ", dist, radiantAngle)
        return [ round(degrees,5), round(dist,5) ] 
    else:
        return [0.0,0.0]

# få sider


# turn
def turn(deg, arlo):
    global rightSpeed
    global LeftSpeed
    global degSec
    isRight = deg > 0
    #print("isRight", isRight, "Degrees to turn ", deg)
    #print("Turning to box")
    if (not isRight):
        #print("Adjusting to left deg")
        deg = deg * (-1)
        arlo.go_diff(leftSpeed, rightSpeed, 0, 1)
    else:
        arlo.go_diff(leftSpeed, rightSpeed, 1, 0)
    sleep(round(deg * degSec, 5))
    arlo.stop()
    #print("amount of degrees to go", deg * degSec)



safeDist      = 300
safeDistSide  = 150

secMeter      = 2.55

#stopDist      = 1000 # millimeter
stopDistSide  = 200

# stopdist is millimeter
def go(targetBoxID, arlo, particles, landmarks, cam, stopDist):
    print("Stopdist = ", stopDist)
    sum = 0
    emStop = False
    sensFront = arlo.read_front_ping_sensor()
    boxAt = getAng(targetBoxID, cam)
    picDist = boxAt[1]*10
    print("picDist ", picDist)
    firstTurn = boxAt[0]
    sensLeft = arlo.read_left_ping_sensor()
    sensRight = arlo.read_right_ping_sensor()
    distTime = round((((min(sensFront, picDist) - stopDist)/1000)*0.66)*secMeter,5)
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
        sum += t-start
        arlo.stop()
        particles = copy.deepcopy(localize(1,particles, 0, landmarks, cam))

        if not emStop:
            turn(getAng(targetBoxID, cam)[0], arlo)
        sensFront = arlo.read_front_ping_sensor()
        picDist = getAng(targetBoxID, cam)[1]*1000
        sensLeft = arlo.read_left_ping_sensor()
        sensRight = arlo.read_right_ping_sensor()
        distTime = (((min(sensFront, picDist) - stopDist)/1000)*(2/3))*secMeter
    return [firstTurn, round((sum / secMeter) * 100, 5), particles, emStop]



def run_goToBox(targetBoxID, arlo, particles, landmarks, cam, stop):
    
    #print("Now i must be looking at "+str(targetBoxID)+". Calling go()")
    turn(getAng(targetBoxID, cam)[0], arlo)
    return go(targetBoxID, arlo, particles, landmarks, cam, stop)
