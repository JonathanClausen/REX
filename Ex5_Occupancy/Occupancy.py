import numpy as np
import sys
import math
from numpy.lib.arraysetops import unique

#Import arlo robot
sys.path.append("../")
sys.path.append("../Ex4")
import Ex4.particle as particle

grid_size = 30
sensor_max = 250
sensor_angle = math.radians(15 * 2)


## Log function
prob_free = 0.9
l_0 = prob_free
l_occ = np.log((1-prob_free/prob_free))
l_free = np.log(prob_free/(1-prob_free))


def inverse_range_sensor_model(cell, robot, sensor):
    r = math.sqrt((((cell[0]*grid_size) - robot.getX())**2) + (((cell[1]*grid_size) - robot.getY())**2) )
    # print("r for [%f][%f] = %f" % (cell[0], cell[1], r))
    angle = math.atan2( cell[1] - robot.getY(), cell[0] - robot.getX() ) - robot.getTheta()
    if (r > (max(sensor_max, sensor + (grid_size**2 / 2)))):
        return l_0
    if (sensor < sensor_max) and (abs(r - sensor) < grid_size/2):
        return l_occ
    if (r < sensor):
        return l_free
    return l_0

def occupancy_grid_mapping(grid, mean_particle, sensor):
    update_m = perceptualField(grid,mean_particle,sensor)
    for m in update_m:
        x = m[0]
        y = m[1]
        grid[x][y] = grid[x][y] + inverse_range_sensor_model([x, y, grid[x][y]], mean_particle, sensor) - l_0
        print("value for [%2i][%2i] = %f" % (x, y, grid[x][y]))
    return grid


def perceptualField(map, p, dist):
    retArr = []
    angle = math.radians(15)
    X = p.getX()
    Y = p.getY()
    roboOri = p.getTheta()
    measurePoints = math.ceil(dist/grid_size)*5

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
        x2_left   = X+math.cos(leftOri)*(dist/i)
        y2_left   = X+math.sin(leftOri)*(dist/i)
        x2_right  = X+math.cos(rightOri)*(dist/i)
        y2_right  = X+math.sin(rightOri)*(dist/i)
        x2_center = X+math.sin(centerOri)*(dist/i)
        y2_center = X+math.cos(centerOri)*(dist/i)
        retArr.append([x2_left, y2_left])
        retArr.append([x2_right, y2_right])
        retArr.append([x2_center, y2_center])
    retArr = np.array(retArr)
    print("np", retArr)

    retArr = retArr[~np.any(retArr < 0, axis = 1)]
    print("no zero", retArr)

    # conform to grid size
    retArr = np.ceil(retArr/grid_size)
    print("to grid ", retArr)

    # remove values outside map
    retArr = retArr[~np.any(retArr > len(map), axis = 1)]
    print("no large values", retArr)

    # remove duplicate boxes
    retArr = np.unique(retArr, axis=0)
    print("no dup", retArr)

    # np.flip(retArr, 1)
    # print("flip ", retArr)
    # vi bliver Nød til at flippe arrayet til sidst inden vi bruger det vi kkan ikke flippe det her.

    return retArr.astype(int)


def printMap(list):
    y, x= np.shape(list)
    startLine = "+" + ("---+"*x)
    print(startLine)
    for i in range(y):
        print("|", end="")
        for j in range(x):
            print('{:>3}|'.format(round(list[i,j])), end="")
        print()
        print(startLine)
    print()


map = occupancy_grid_mapping(np.zeros((15, 15), dtype=float), particle.Particle(50, 50, 0.785, 0), 149)
map[math.floor(50/grid_size)][math.floor(50/grid_size)] = 666
map = np.flip(map,0)
printMap(map)

print(l_occ)
print(l_free)