import numpy as np
import sys

import math

from numpy.lib.arraysetops import unique

#Import arlo robot
sys.path.append("../")
sys.path.append("../Ex4")
import Ex4.particle as particle

grid_size = 10
sensor_max = 250
sensor_angle = math.radians(15 * 2)


## Log function
prob_free = 0.9
l_0 = prob_free
l_occ = np.log((1-prob_free) / prob_free)
l_free = np.log(prob_free / (1 - prob_free))

def occupancy_grid_mapping(grid, mean_particle, sensors):
    update_m = perceptualField(grid,mean_particle,sensors)
    for m in update_m:
        x = m[0] 
        y = m[1]
        grid[x][y] = grid[x][y] + inverse_range_sensor_model([x, y, grid[x][y]], mean_particle, sensors) - l_0
    return grid
    
            

def inverse_range_sensor_model(cell,robot,sensor):
    r = math.sqrt(((cell[0] - robot.getX())**2) + ((cell[1] - robot.getY())**2) )
    angle = math.atan2( cell[1] - robot.getY, cell[0] - robot.getX() ) - robot.getTheta()
    if (r > (max(sensor_max, sensor + (grid_size**2 / 2))) or  abs(angle) > sensor_angle  ):
        return cell[2]
    if (sensor < sensor_max) and (abs(r - sensor) < grid_size/2):
        return l_occ
    if (r < sensor):
        return l_free
        
def perceptualField(map, p, dist):
    retArr = []
    angle = 0.12
    X = p.getX()
    Y = p.getY()
    roboOri = p.getTheta()
    measurePoints = math.ceil(dist/grid_size)

    leftOri = roboOri + angle
    rightOri = roboOri - angle
    centerOri = roboOri

    if (leftOri > (math.pi)):
        leftOri = (-2*(math.pi)+leftOri)
    elif (leftOri < (-1*(math.pi))):
        leftOri = (2*(math.pi)+leftOri)

    if (rightOri > (math.pi)):
        rightOri = (-2*(math.pi)+rightOri)
    elif (rightOri < (-1*(math.pi))):
        rightOri = (2*(math.pi)+rightOri)
    for i in range(1,measurePoints): 
            
            x2_left = math.floor(X+math.cos(leftOri))*(dist/i)
            y2_left = math.floor(X+math.sin(leftOri))*(dist/i)    
            x2_right = math.floor(X+math.cos(rightOri))*(dist/i)
            y2_right = math.floor(X+math.sin(rightOri))*(dist/i)    
            x2_center = math.floor(X+math.sin(centerOri))*(dist/i)    
            y2_center =math.floor(X+math.cos(centerOri))*(dist/i)     
            retArr.append([x2_left,y2_left])
            retArr.append([x2_right,y2_right])
            retArr.append([x2_center,y2_center])
    retArr = np.array(retArr)
    print(retArr)
    retArr = retArr[~np.all(retArr < 0, axis = 1)]
    retArr = retArr[~np.all(retArr > len(map), axis = 1)]
    return(np.unique(retArr))

def printMap(list):
    y, x= np.shape(list)
    startLine = "+" + ("---+"*x)
    print(startLine)
    for i in range(y):
        print("|", end="")
        for j in range(x):
            print('{:>3}|'.format(list[i,j]), end="")
        print()
    print(startLine)
    print()


    

     
map = occupancy_grid_mapping(np.zeros((100,100)), particle.Particle(5, 5, 0, 0), 50)
printMap(map)
