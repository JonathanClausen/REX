import numpy as np
import sys

import math

#Import arlo robot
sys.path.append("../")

sys.path.append("../Ex4-self-localization")
import ARLO.robot
import particle

def occupancy_grid_mapping(grid, ):
    update_m = perceptualField(m,xt,zt)
    for m in update_m:
        x = m[0] 
        y = m[1]
        grid[x][y] = grid[x][y] + inverse_range_sensor_model([x, y], mean_particle, sensation)
            

def inverse_range_sensor_model(cell,robot,sensor):
    r = math.sqrt(((cell[0] - robot.getX())**2) + ((cell[1] - robot.getY())**2) )
    angle = math.atan2( cell[1] - robot.getY, cell[0] - robot.getX() ) - robot.getTheta()


def perceptualField(m, robot):
    
    
    

     
