import math
import numpy as np
from time import sleep
import ARLO.robot

arlo = ARLO.robot.Robot()

leftSpeed     = math.floor(64 * 0.97)
rightSpeed    = 64
degSec90 = 0.005
degSec10 = 0.005


print(arlo.go_diff(leftSpeed, rightSpeed, 0, not 0))
sleep(10 * degSec10)
print(arlo.stop())