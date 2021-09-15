#!/usr/bin/env python3

from time import sleep
import ARLO.robot as robot
arlo = robot.Robot()
# from threading import Thread, Lock
import math

secMeter = 2.55
sensFront     = 0
emergencyStop = False

sensInterval = 0.001

leftSpeed = math.floor(64 * 0.97)
rightSpeed = 64

goalDist = 500

sensFront = arlo.read_front_ping_sensor()
while (sensFront > goalDist+5):
    sensFront = arlo.read_front_ping_sensor()
    print(sensFront)
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    goDist = (((sensFront - goalDist)/1000)*0.66)*secMeter
    sleep(goDist)
    arlo.stop()
    sleep(0.5)

arlo.stop()
