from time import sleep
import math

import ARLO.robot

# Create a robot object and initialize
arlo = ARLO.robot.Robot()

print("Running ...")

# send a go_diff command to drive forward
leftSpeed = math.floor(100 * 0.97)
rightSpeed = 100


# Go straight
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
sleep(0.803)

print(arlo.stop())

