from time import sleep
import math

import ARLO.robot

# Create a robot object and initialize
arlo = ARLO.robot.Robot()

print("Running ...")

# send a go_diff command to drive forward
leftSpeed = math.floor(64 * 0.97)
rightSpeed = 64

for x in range(4):

# Go straight
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    sleep(2)


# turn
    print(arlo.stop())
    sleep(0.5)

    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
#    sleep(0.396) with speed 100
#    sleep(0.755) with continout turning
    sleep(0.727)
    print(arlo.stop())
    sleep(0.5)



print(arlo.stop())

