from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 64
rightSpeed = 64

# Go straight
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

# Wait a bit while robot moves forward
sleep(3)

# Turn right
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))

# Wait a bit while robot moves forward
sleep(6)

# send a stop command
print(arlo.stop())


print("Finished")
