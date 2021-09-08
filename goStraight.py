from time import sleep

import ARLO.robot

# Create a robot object and initialize
arlo = ARLO.robot.Robot()

print("Running ...")

# send a go_diff command to drive forward
leftSpeed = 100
rightSpeed = 100


# Go straight
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
sleep(3)

print(arlo.stop())

