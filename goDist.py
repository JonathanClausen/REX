#!/usr/bin/env python3

from time import sleep
from time import process_time
import ARLO.robot as robot
arlo = robot.Robot()
from threading import Thread, Lock
import math
from turnToBox import getAng, turn

# changable
sensFront     = 0
sensLeft      = 0
sensRight     = 0
# emergencyStop = False

# static
secMeter      = 2.55
leftSpeed     = math.floor(64 * 0.97)
rightSpeed    = 64
sensInterval  = 0.1

safeDist      = 300
safeDistSide  = 150

stopDist      = 500
stopDistSide  = 200


def go():
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
        distTime = (((sensFront - stopDist)/1000)*(2/3))*secMeter
        turn(getAng())
    return


# def goDist():
#     sensFront = arlo.read_front_ping_sensor()
#     sensLeft = arlo.read_left_ping_sensor()
#     sensRight = arlo.read_right_ping_sensor()
#     distTime = (((sensFront - stopDist)/1000)*0.66)*secMeter
#     while (distTime > 0.1):
#         start = process_time()
#         t = start
#         print("time to go", distTime)
#         arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
#         while ((t - start) < distTime):
#             sensFront = arlo.read_front_ping_sensor()
#             sensLeft = arlo.read_left_ping_sensor()
#             sensRight = arlo.read_right_ping_sensor()
#             if (sensFront < safeDist or
#                 sensRight < safeDistSide or
#                 sensLeft  < safeDistSide):
#                 print("Emercency stop!!! sensors :\nR ", sensRight,
#                       ",\n L ", sensLeft,
#                       ",\n F ", sensFront,
#                       "\n time traveled = ", t)
#                 break
#             t = process_time()
#         arlo.stop()
#         sensFront = arlo.read_front_ping_sensor()
#         sensLeft = arlo.read_left_ping_sensor()
#         sensRight = arlo.read_right_ping_sensor()
#         distTime = (((sensFront - stopDist)/1000)*(2/3))*secMeter
#     return
