#!/usr/bin/env python3


import camera
import math
import numpy as np
# localize
# drej mod mål
# kan jeg se mål?
#   nej
#       tag afstand til object i målretning




#       if left free
#           turn left_45
#           go x_lenght
#       elif right_free
#           turn right_45
#           go x_lenght
#       else
#           check dist between boxes
#           filter large dists away fx over 3 m
#           select shortest distance from left and right triangle
#
#           go_toSide largest min dist's side, 1/2 dist from obst
#           if sist left < dist right
#               go dist/2 to the left side of obst



def go_to_xy(a,b):
    a = a/2
    c = math.sqrt(a**2+b**2)
    A = math.atan(a/b)
    return (A,c) #B = degrees, c = lenght

# funktionen her antager at robotten peger i den retning robotten ønker At køre.
# den vil så returnere (vinkel, lengde)
# robotten skal dreje og køre for at komme op på siden af kassen
#
def findWay(cam):
    # tag billede
    frame = cam.get_next_frame()
    # identificer alle kasser
    objectIDs, dists, angles = cam.detect_aruco_objects(frame)
    if (objectIDs is None):
        print("error no objects found")
        return (0,0)
    bLeft = []
    distLeft = []
    bRight = []
    distRight = []   # find the center box, the box that is in the way
    goAroundIndex = np.argmin(np.abs(angles)) #min(enumerate(angles), key=lambda x: abs(x[1]))
    goAroundDist = dists[goAroundIndex]
    goAroundAng = angles[goAroundIndex]
    print("avoid object : ", objectIDs[goAroundIndex])   # removing the center box from the lists
    angles = np.delete(angles, goAroundIndex)
    dists = np.delete(dists, goAroundIndex)
    objectIDs = np.delete(objectIDs, goAroundIndex)   # sort the objects to what is left and right of the center box
    for i in range(len(objectIDs)):
        print("Object ID = ", objectIDs[i], ", Distance = ", dists[i], ", angle = ", angles[i])
        # devide into two lists on +- angle
        # insert the distance between center box and the other obstacle (i) -> space
        space = goAroundDist**2 + dists[i]**2 - 2*goAroundDist*dists[i] * math.cos(angles[i] - goAroundAng)
        print("dist between boxes", space)
        print("angle Center = ", goAroundAng, " ob i = ", angles[i], " angle between = ", math.cos(angles[i] - goAroundAng))
        if space > 25000:
            print("ignoring due to distance over 2.5 m")
        elif angles[i] > 0:
            print("to my left")
            bLeft.append(objectIDs[i])
            distLeft.append(space)
        else:
            print("to my right")
            bRight.append(objectIDs[i])
            distRight.append(space)   # find de to nærmeste kasser til højre og venstre
    minLeft = min(bLeft, default=999) # default hvis listen er tom
    minRight = min(bRight, default=999)   # hvis der er frit til en af siderne vælger den denne
    # og køre en meter ved siden af forhindringen
    distEmpty = 100   # chossing the side with the most space
    if (minLeft >= minRight):
        if minLeft == 999:
            # left is free finding direction next to obstacle
            print("left is clear")
            return go_to_xy(goAroundDist, distEmpty)
        index = distLeft.index(minLeft)
        leftBoxID = bLeft[index]
        # the total angle between the two boxes we want to go between
        # angBetweenBoxes = abs(angles[objectIDs.index(leftBoxID)]) + abs(goAroundAng)
        print("going between box ", objects[goAroundIndex], " and ", leftBoxID)
        return go_to_xy(goAroundDist, minLeft)
    else:
        if minRight == 999:
            # left is free finding direction next to obstacle
            print("right is clear")
            turn, dist = go_to_xy(goAroundDist, minRight)
            return go_to_xy(goAroundDist, distEmpty)
        index = distRight.index(minRight)
        rightBoxID = bLeft[index]
        # the total angle between the two boxes we want to go between
        #        angBetweenBoxes = abs(angles[objectIDs.index(rightBoxID)]) + abs(goAroundAng)
        print("going between box ", objects[goAroundIndex], " and ", rightBoxID)
        turn, dist = go_to_xy(goAroundDist, minRight)
        return (-turn, dist)


try:
    cam = camera.Camera(0, 'arlo', useCaptureThread=True)
    print("result ", findWay(cam))
finally:
    cam.terminateCaptureThread()
