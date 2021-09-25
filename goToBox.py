#!/usr/bin/env python3

import cv2
import numpy as np
from time import sleep
import math
import ARLO.robot
from time import perf_counter
# from goDist import go

arlo = ARLO.robot.Robot()

leftSpeed     = math.floor(64 * 0.97)
rightSpeed    = 64
degSec = 0.005

def picPos():
    markerLength = 0.145
    cameraMatrix =np.array([[506.94,0,640/2],
                            [0,506.94,480/2],
                            [0,0,1],])
    distCoeffs = 0

#distCoeffs[, rvecs[, tvecs[, _objPoints]]]

    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop)
    ret,frame = cap.read() # return a single frame in variable `frame`

#Grabbing dictionary
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    arucoParams = cv2.aruco.DetectorParameters_create()
    corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    tvec = []
    if (ids is not None):
        rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs)
    return tvec


# få sider
def getAng():
    tvec = picPos()
    if (tvec == []):
        return 45
    a = tvec[0][0][0]
    b = tvec[0][0][2]
    dist = math.sqrt(a**2+b**2)
    print("a = ", a, "b = ", b, "dist = ", dist)
    return (math.degrees(math.asin(a/dist)), dist)

# turn
def turn(deg):
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

stopDist      = 500
stopDistSide  = 200


def go():
    sensFront = arlo.read_front_ping_sensor()
    picDist = getAng()[1]*1000
    sensLeft = arlo.read_left_ping_sensor()
    sensRight = arlo.read_right_ping_sensor()
    distTime = (((min(sensFront, picDist) - stopDist)/1000)*0.66)*secMeter
    while (distTime > 0.1):
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
                break
            t = perf_counter()
        arlo.stop()
        sensFront = arlo.read_front_ping_sensor()
        picDist = getAng()[1]*1000
        sensLeft = arlo.read_left_ping_sensor()
        sensRight = arlo.read_right_ping_sensor()
        distTime = (((min(sensFront, picDist) - stopDist)/1000)*(2/3))*secMeter
    return

# def go():
#     sensFront = arlo.read_front_ping_sensor()
#     sensLeft = arlo.read_left_ping_sensor()
#     sensRight = arlo.read_right_ping_sensor()
#     distTime = (((sensFront - stopDist)/1000)*0.66)*secMeter
#     while (distTime > 0.1):
#         arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
#         sleep(distTime)
#         arlo.stop()
#         sensFront = arlo.read_front_ping_sensor()
#         sensLeft = arlo.read_left_ping_sensor()
#         sensRight = arlo.read_right_ping_sensor()
#         distTime = (((sensFront - stopDist)/1000)*(2/3))*secMeter
#         turn(getAng())
#     return



print(getAng()[0])
while (picPos() == []):
    turn(getAng()[0])
go()
