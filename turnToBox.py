#!/usr/bin/env python3

import cv2
import numpy as np
from time import sleep
import math
import ARLO.robot

arlo = ARLO.robot.Robot()

leftSpeed     = math.floor(64 * 0.97)
rightSpeed    = 64
degSec = 0.002

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
    isRight = deg > 0
    print("isRight", isRight, "Degrees to turn ", deg)
    print("Turning to box")
    if (not isRight):
        print("Advusting to left deg")
        deg = deg * (-1)
        print(arlo.go_diff(leftSpeed, rightSpeed, 0, 1))
    else:
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
    sleep(math.round(deg * degSec, 5))
    print(arlo.stop())
    print("amount of degrees to go", deg * degSec)

print(getAng())
turn(getAng())
