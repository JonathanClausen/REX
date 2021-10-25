#!/usr/bin/env python3

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


def findWay(meanPart, goalLandmark, cam):
    # tag billede
    frame = cam.get_next_frame()

    # identificer alle kasser
    objectIDs, dists, angles = cam.detect_aruco_objects(frame)
    bLeft = []
    distLeft = []
    bRight = []
    distRight = []

    # find the center box
    goAroundIndex = min(enumerate(angles), key=lambda x: abs(x[1]))
    goAroundDist = dists[goAroundIndex]
    goAroundAng = angles[goAroundIndex]

    # removing the center box from the lists
    angles.pop(goAroundIndex)
    dists.pop(goAroundIndex)
    objectIDs.pop(goAroundIndex)

    for i in range(len(objectIDs)):
        print("Object ID = ", objectIDs[i], ", Distance = ", dists[i], ", angle = ", angles[i])
        # devide into two lists on +- angle
        space = goAroundDist**2 + dists[i]**2 - 2*goAroundDist*dists[i] * cos(goAroundAng)
        if space > 300:
            print("ignoring due to distance over 3 m")
        elif angles[i] > 0:
            print("to my left")
            bLeft.append(objectsIDs[i])
            # calculate the distance between the boxes
            distLeft.append(space)
        else:
            print("to my right")
            bRight.append(objectsIDs[i])
            distRight.append(space)

    # find de to nærmeste kasser i hver trekant
    minLeft = min(bLeft)
    minRight = min(bRight)
    if minLeft < minRight:


    # giv data til emil

    return (x, y)














































































j
