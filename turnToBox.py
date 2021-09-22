#!/usr/bin/env python3

import cv2
import numpy as np
from time import sleep
import math
import ARLO.robot

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

    rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs)
    return tvec


# få sider
def getAng():
    tvec = picPos()
    a = tvec[0][0][0]
    c = tvec[0][0][2]
    print("a = ", a, "c = ", c)
    return  math.degrees(math.asin(a/c))

# turn
def turn(deg):
    global rightSpeed
    global LeftSpeed
    global degSec
    isLeft = deg < 0
    if (isLeft):
        deg = deg * (-1)
    print(deg)
    print("Turning to box")
    print(arlo.go_diff(leftSpeed, rightSpeed, isLeft, not isLeft))
    sleep(deg * degSec)
    print(arlo.stop())

print(getAng())
turn(getAng())
