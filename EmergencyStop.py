#!/usr/bin/env python3

from time import sleep
import ARLO.robot as robot
arlo = robot.Robot()
from threading import Thread, Lock
import math



# kør ligeud hvis der ikke er nogen forhindringer
# hvis forhindring kontroler om der er plads til højre og venstre
# 45 grader drejning til ledig retning
# 90 grader drej for at se om man kan komme tilbage på kurs
#   hvis ja kør frem til den linje du var på
#   hvis nej drej 45 grader tilbage for at fortsætte i ny akse
# hvis der ikke er ledigt hverken hæjre eller venstre så drejning 90 grader og kontrol af fri bane

# changable
sensFront     = 0
sensLeft      = 0
sensRight     = 0
emergencyStop = False

sensInterval = 0.001
leftSpeed = math.floor(64 * 0.97)
rightSpeed = 64
emLock = Lock()
roboLock = Lock()

def measure(roboLock, emLock):
    measure = True
    while measure:
        global sensFront
        global sensLeft
        global sensRight
        global emergencyStop
        safeDist = 300
        safeDistSide = 150
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
            measure = False
            print("front: ", sensFront)
            print("Left", sensLeft)
            print("Right", sensRight)
        sleep(sensInterval)
    return


measureThread = Thread(target=measure, args=(roboLock, emLock,))
measureThread.start()


go = True
roboLock.acquire()
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
roboLock.release()
while go:
    emLock.acquire()
    go = not emergencyStop
    emLock.release()

roboLock.acquire()
print(arlo.stop())
roboLock.release()

measureThread.join()
