from time import sleep
import math

import ARLO.robot

# Create a robot object and initialize
arlo = ARLO.robot.Robot()

print("Running ...")

# send a go_diff command to drive forward
leftSpeed = math.floor(64 * 0.97)
rightSpeed = 64

# Distance before it start to inch closer
awareDist = 300

# Loop here
frontDist = arlo.read_front_ping_sensor()
rightDist = arlo.read_right_ping_sensor()
leftDist = arlo.read_left_ping_sensor()

frontClear = False
left45Clear = False
right45Clear = False

safeFrontDist = 500
safeSideDist = 200

#Updating distance variables 
def update_dists():
    global frontDist
    global rightDist
    global leftDist

    frontDist = arlo.read_front_ping_sensor()
    rightDist = arlo.read_right_ping_sensor()
    leftDist= arlo.read_left_ping_sensor()

# Checking we are to close - Thus we have to change direction
def dists_safe():
    global left45Clear
    global right45Clear
    global frontClear
    
    frontClear = False
    left45Clear = False
    right45Clear = False

    if frontDist > safeFrontDist:
        frontClear = True
    if leftDist > safeSideDist:
        left45Clear = True
    if rightDist > safeSideDist:
        right45Clear = True

# if r = 1 turn left, else turn right
# r can only be 1 or 0
def turn_x_degree(x, r):
    rightDir = r
    leftDir = 1 - rightDir
    sleeptime = 0.005555 * x
    print(arlo.go_diff(leftSpeed, rightSpeed, leftDir, rightDir))
    sleep(sleeptime)

def obstacle():
    update_dists()
    dists_safe()
    while(not(frontClear)):
        if (right45Clear or left45Clear):
            if (right45Clear):
                turn_x_degree(10, 0)
            else: 
                turn_x_degree(10, 1)
        else:
            turn_x_degree(90,0)
        update_dists()
        dists_safe()
    arlo.stop()
                       
while(True):
    arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
    sleep(0.1)
    if arlo.read_front_ping_sensor() < 500 or arlo.read_right_ping_sensor() < 200 or arlo.read_left_ping_sensor() < 200:
        obstacle()
