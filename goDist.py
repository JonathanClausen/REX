#!/usr/bin/env python3

from time import sleep
import ARLO.robot as robot
arlo = robot.Robot()
from threading import Thread, Lock
import math

# changable
sensFront     = 0
sensLeft      = 0
sensRight     = 0
# emergencyStop = False

# static
secMeter      = 2.6
leftSpeed     = math.floor(64 * 0.97)
rightSpeed    = 64
sensInterval  = 0.1

safeDist      = 300
safeDistSide  = 150

stopDist      = 500
stopDistSide  = 200


def goDist():
    sensFront = arlo.read_front_ping_sensor()
    sensLeft = arlo.read_left_ping_sensor()
    sensRight = arlo.read_right_ping_sensor()
    distTime = (((sensFront - stopDist)/1000)*0.66)*secMeter
    while (distTime > 0.1):
        arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
        sleep(distTime)
        arlo.stop()
        sensFront = arlo.read_front_ping_sensor()
        sensLeft = arlo.read_left_ping_sensor()
        sensRight = arlo.read_right_ping_sensor()
        distTime = (((sensFront - stopDist)/1000)*0.66)*secMeter
    return

goDist()
