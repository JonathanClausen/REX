from time import sleep
import math

import ARLO.robot

# Create a robot object and initialize
arlo = ARLO.robot.Robot()

print("Running ...")

# send a go_diff command to drive forward
leftSpeed = math.floor(100 * 0.97)
rightSpeed = 100

for x in range(4):

# Go straight
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    sleep(0.803)

# turn
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
    sleep(0.5836)



print(arlo.stop())

