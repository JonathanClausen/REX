from time import sleep
import math

import ARLO.robot

# Create a robot object and initialize
arlo = ARLO.robot.Robot()

print("Running ...")

# send a go_diff command to drive forward
leftSpeed = math.floor(64 * 0.97)
rightSpeed = 64

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

# if r = 1 turn left, 0 = right.   (0 = R, 
# r can only be 1 or 0
def turn_x_degree(x, r):
    rightDir = r
    leftDir = 1 - rightDir
    # 0.2 in time is good for small changes
    sleeptime = 0.005555 * x
    print(arlo.go_diff(leftSpeed, rightSpeed, leftDir, rightDir))
    sleep(0.2)
    arlo.stop()
    sleep(0.2)

def obstacle():
    update_dists()
    dists_safe()
    go = False
    turn = 0

    # 0 = turn right
    while (not go):
        update_dists()
        dists_safe()
        if (not frontClear):
            turn_x_degree(10,turn)
        elif (not left45Clear):
            turn = 0
            turn_x_degree(10,turn)
        elif (not right45Clear):
            turn = 1
            turn_x_degree(10,turn)
        else:
            go = True


    # while (not go):
    #     #All blocked = Turn right 
    #     if (not frontClear and not right45Clear and not left45Clear):
    #         turn_x_degree(10,0)
    #     #Left blocked = turn right 
    #     while (not frontClear and not left45Clear):
    #         update_dists()
    #         dists_safe()
    #         turn_x_degree(10, 1)
        
    #     while (not frontClear and not left45Clear):
    #         turn_x_degree(10, 1)
    #     if (not frontClear and not )
    #     else:
    #         go = True 
    
    '''
    while((not frontClear and not right45Clear) or (not frontClear and not left45Clear)):       
        if (right45Clear or left45Clear):
            if (right45Clear):
                turn_x_degree(10, 1)
            else: 
                turn_x_degree(10, 0)
        else:
            turn_x_degree(10,1)
        update_dists()
        dists_safe()
    arlo.stop()
    '''
                       
while(True):
    arlo.go_diff(leftSpeed, rightSpeed, 1, 1)
    dists_safe()
    update_dists()
    print("Left_clear:",left45Clear, "     Front_clear:", frontClear, "     Right_clear", right45Clear)
    print("\n\n")
    sleep(0.1)
    print("L:", arlo.read_left_ping_sensor(), "    F:", arlo.read_front_ping_sensor(), "    C:", arlo.read_right_ping_sensor())
    if arlo.read_front_ping_sensor() < 600 or arlo.read_right_ping_sensor() < 500 or arlo.read_left_ping_sensor() < 500:
        print("to close")
        arlo.stop()
        obstacle()
