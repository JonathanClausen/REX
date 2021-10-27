#!/usr/bin/env python3

import cv2
import numpy as np
from time import sleep
import math
from time import perf_counter
# from goDist import go

leftSpeed     = math.floor(64 * 0.97)
rightSpeed    = 64
degSec = 0.005

def picPos(targetBoxID, cam):
    markerLength = 0.145
    cameraMatrix =np.array([[506.94,0,640/2],
                            [0,506.94,480/2],
                            [0,0,1],])
    distCoeffs = 0

#distCoeffs[, rvecs[, tvecs[, _objPoints]]]

    frame = cam.get_next_frame()


#Grabbing dictionary
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    arucoParams = cv2.aruco.DetectorParameters_create()
    corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    tvec = []
    print("corners: ", corners)
    if ((ids is not None) and (targetBoxID in ids)):
        print("target: ", targetBoxID)
        corners = corners[ids.index(targetBoxID)]
        rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs)
    return tvec


# få sider
def getAng(targetBoxID, cam):
    tvec = picPos(targetBoxID, cam)
    if (tvec == []):
        return (45, 10000)
    a = tvec[0][0][0]
    b = tvec[0][0][2]
    dist = math.sqrt(a**2+b**2)
    print("a = ", a, "b = ", b, "dist = ", dist)
    print("ang  with minus = ", math.degrees(math.asin(a/dist)), "ang -a = ", math.degrees(math.asin(-a/dist)))
    return (round(math.degrees(math.asin(a/dist)), 5), dist)

# turn
def turn(deg, arlo):
    global rightSpeed
    global LeftSpeed
    global degSec
    isRight = deg > 0
    print("isRight", isRight, "Degrees to turn ", deg)
    print("Turning to box")
    if (not isRight):
        print("Advusting to left deg")
        deg = deg * (-1)
        print(arlo.go_diff(leftSpeed, rightSpeed, 0, 1))
    else:
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
    sleep(round(deg * degSec, 5))
    print(arlo.stop())
    print("amount of degrees to go", deg * degSec)



safeDist      = 300
safeDistSide  = 150

secMeter      = 2.55

stopDist      = 400
stopDistSide  = 200


def go(targetBoxID, arlo, cam):
    sum = 0
    emStop = False
    sensFront = arlo.read_front_ping_sensor()
    boxAt = getAng(targetBoxID, cam)
    picDist = boxAt[1]*1000
    firstTurn = boxAt[0]
    sensLeft = arlo.read_left_ping_sensor()
    sensRight = arlo.read_right_ping_sensor()
    distTime = (((min(sensFront, picDist) - stopDist)/1000)*0.66)*secMeter
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

        if not emStop:
            turn(getAng(targetBoxID, cam)[0], arlo)
        sensFront = arlo.read_front_ping_sensor()
        picDist = getAng(targetBoxID, cam)[1]*1000
        sensLeft = arlo.read_left_ping_sensor()
        sensRight = arlo.read_right_ping_sensor()
        distTime = (((min(sensFront, picDist) - stopDist)/1000)*(2/3))*secMeter
    return [firstTurn, sum * secMeter]



def run_goToBox(targetBoxID, arlo, cam):
    while (picPos(targetBoxID, cam) == []):
        turn(getAng(targetBoxID, cam)[0], arlo)
    turn(getAng(targetBoxID, cam)[0], arlo)
    go(targetBoxID, arlo, cam)
