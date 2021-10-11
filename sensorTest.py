#!/usr/bin/env python3

from time import sleep
import ARLO.robot as robot
arlo = robot.Robot()
# from threading import Thread, Lock


sensFront     = 0

sensInterval = 1

while True:
    sensFront = arlo.read_front_ping_sensor()
    print("Measurement: ", round(sensFront / 10 , 5) )
    sleep(sensInterval)
