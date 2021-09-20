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

emLock        = Lock()
roboLock      = Lock()


# thread for Emergency logic
def measure(roboLock, emLock):
    measure = True
    while measure:
        global sensFront
        global sensLeft
        global sensRight
        global emergencyStop
        global safeDist
        global safeDistSide
        # kontinuerte målinger her
        roboLock.acquire()
        sensFront = arlo.read_front_ping_sensor()
        sensLeft = arlo.read_left_ping_sensor()
        sensRight = arlo.read_right_ping_sensor()
        roboLock.release()
        if (sensFront < safeDist or
            sensLeft < safeDistSide or
            sensRight < safeDistSide):
            emLock.acquire()
            emergencyStop = True
            emLock.release()
            print("EMERGENCY STOP")
            print("front: ", sensFront)
            print("Left", sensLeft)
            print("Right", sensRight)
            measure = False
        sleep(sensInterval)
    return



def forward():
    measureThread.start()
    roboLock.acquire()
    goDist = (((sensFront - stopDist)/1000)*0.66)*secMeter
    while (not emergencyStop
           and sensFront > stopDist
           and sensLeft > stopDistSide
           and sensRight > stopDistSide
           and goDist > 0.1):
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
        roboLock.release()
        sleep(0.1)

    roboLock.acquire()k
    print(arlo.stop())
    roboLock.release()
    measureThread.join()
    return

def angleTjek():
    sensLeft  = arlo.read_left_ping_sensor()
    sensRight = arlo.read_right_ping_sensor()
    angOK     = (sensLeft > StopDistSide and sensRight > StopDistSide)
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
            angOK = sensLeft < sensLeftNew and sensRightNew > stopDistSide
            if not angOK:
                # drive a little left
        else:
            angOK = sensright < sensRightNew and sensLeftNew > stopDistSide
            if not angOK:
                # drive a little right
    return



measureThread = Thread(target=measure, args=(roboLock, emLock,))

while True:
    forward()
    # turn
    # angleTjek()
