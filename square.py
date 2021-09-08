from time import sleep

import ARLO.robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 64
rightSpeed = 64
turnTime = 2

# Go straight
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
sleep(3)

# Turn right
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
sleep(turnTime)

# Go straight
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
sleep(3)

# Turn right
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
sleep(turnTime)

# Go straight
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
sleep(3)

# Turn right
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
sleep(turnTime)

# Go straight
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
sleep(3)

# Turn right
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
sleep(turnTime)

# send a stop command
print(arlo.stop())

print("Finished")
