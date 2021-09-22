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
emergencyStop = False

# static
secMeter      = 2.55
leftSpeed     = math.floor(64 * 0.97)
rightSpeed    = 64
sensInterval  = 0.01

safeDist      = 300
safeDistSide  = 150

stopDist      = 500
stopDistSide  = 200


def goSafe(time):
    global sensFront
    global sensLeft
    global sensRight
    global safeDist
    global safeDistSide
    print("goSafe for sec: ", time)
    while (time > 0.01):
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
        sleep(0.01)
        time = time - 0.01
        sensFront = arlo.read_front_ping_sensor()
        sensLeft  = arlo.read_left_ping_sensor()
        sensRight = arlo.read_right_ping_sensor()
        if (sensFront < safeDist or
            sensLeft  < safeDistSide or
            sensRight < safeDistSide):
            print("EMERGENCY STOP")
            return 1
    print(arlo.stop())
    return 0


def forward():
    global sensFront
    global sensLeft
    global sensRight
    global emergencyStop
    global safeDist
    global safeDistSide

    print("forward")

    sensFront = arlo.read_front_ping_sensor()
    sensLeft = arlo.read_left_ping_sensor()
    sensRight = arlo.read_right_ping_sensor()

    goDist = (((sensFront - stopDist)/1000)*0.66)*secMeter
    while (sensFront > stopDist
           and sensLeft > stopDistSide
           and sensRight > stopDistSide
           and goDist > 0.01):
        if goSafe(goDist):
            break
        goDist = (((sensFront - stopDist)/1000)*0.66)*secMeter
    print("forward done")
    return


def angleTjek():
    sensLeft  = arlo.read_left_ping_sensor()
    sensRight = arlo.read_right_ping_sensor()
    angOK     = (sensLeft > stopDistSide and sensRight > stopDistSide)
    while (not angOK):
        DangerSide = 0 # 1 = left
        if (sensLeft < sensRight):
            DangerSide = 1
        print("Angle check drive", arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
        sleep(0.1)
        arlo.stop()
        # remeasuring
        sensLeftNew  = arlo.read_left_ping_sensor()
        sensRightNew = arlo.read_right_ping_sensor()
        if DangerSide:
            angOK = (sensLeft < sensLeftNew and sensRightNew > stopDistSide)
            if not angOK:

                print("")
        else:
            angOK = (sensRight < sensRightNew and sensLeftNew > stopDistSide)
            if not angOK:
                # drive a little right
                print("")
    return



while True:
    forward()
    # turn
    # angleTjek()
