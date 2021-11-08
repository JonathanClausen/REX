#!/usr/bin/env python3

import camera
import math
import numpy as np


def go_to_xy(a,b):
    a = a/2
    c = math.sqrt(a**2+b**2)
    #print("in go_to_xy", "a =", a, "b=" ,b )
    A = math.atan(a/b)
    return (A,c) #B = degrees, c = lenght


# funktionen her antager at robotten peger i den retning robotten ønker At køre.
# den vil så returnere (vinkel, lengde)
# robotten skal dreje og køre for at komme op på siden af kassen
def findWay(cam, targetID):
    # tag billede
    frame = cam.get_next_frame()
    # identificer alle kasser
    objectIDs, dists, angles = cam.detect_aruco_objects(frame)
    if (objectIDs is None):
        print("error in route planning, no objects found")
        return (0,0)
    bLeft = []
    distLeft = []
    bRight = []
    distRight = []
    roboToBoxLeft = []
    roboToBoxRight = []

    # find the center box, the box that is in the way
    goAroundIndex = np.argmin(np.abs(angles)) #min(enumerate(angles), key=lambda x: abs(x[1]))
    goAroundDist = dists[goAroundIndex]
    goAroundAng = angles[goAroundIndex]
    goAroundID = objectIDs[goAroundIndex]
    print("avoid object : ", goAroundID)

    # is the object to pass a landmark that is not the goal, then fail
    if ((goAroundID in [1, 2, 3, 4]) and (goAroundID != targetID)):
        print("Error in route planning (attempting to avoid landmark), not trusting current theta")
        return (0,0)

    # is the robot pointing to a box? else fail
    if (math.degrees(np.abs(goAroundAng) and goAroundDist > 15000) > 15):
        print("Error in route planning (not pointing directly to a box), not trusting current theta")
        return (0,0)

    # removing the center box from the lists
    for i in np.where(objectIDs == goAroundID): 
        objectIDs = np.delete(objectIDs, i) 
        dists = np.delete(dists, i)
        angles = np.delete(angles, i)

    # sort the objects to what is left and right of the center box
    for i in range(len(objectIDs)):
        #print("Object ID = ", objectIDs[i], ", Distance = ", dists[i], ", angle = ", angles[i])

        # devide into two lists on +- angle
        # insert the distance between center box and the other obstacle (i) -> space
        space = math.sqrt(goAroundDist**2 + dists[i]**2 - 2*goAroundDist*dists[i] * (math.cos(angles[i] - goAroundAng)))

        #print("dist between boxes", space)
        #print("angle Center = ", goAroundAng, " ob i = ", angles[i],
        #" angle between in deg= ", math.degrees((angles[i] - goAroundAng)))
        if ((space > 20000) and (np.abs(angles[i]) > math.radians(20)) and (dists[i] > 15000)):
            print("ignoring due to distance over 2 m and angle larger than 20 deg")
        elif angles[i] > 0:
            bLeft.append(objectIDs[i])
            distLeft.append(space)
            roboToBoxLeft.append(dists[i])
            
        else:
            bRight.append(objectIDs[i])
            distRight.append(space)   # find de to nærmeste kasser til højre og venstre
            roboToBoxRight.append(dists[i])
    print(roboToBoxRight ," to my right")
    print(roboToBoxLeft ," to my right")

    minLeft  = min(distLeft , default=9999999) # default hvis listen er tom
    minRight = min(distRight, default=9999999)   # hvis der er frit til en af siderne vælger den denne
    # og køre en meter ved siden af forhindringen
    distEmpty = 200
    # chossing the side with the most space
    if (minLeft >= minRight):
        if ((minLeft == 9999999) and (targetID != goAroundID)):
            # left is free finding direction next to obstacle
            print("left is clear")
            turn, dist = go_to_xy(distEmpty, goAroundDist)
            return (turn+goAroundAng, dist)
        index = distLeft.index(minLeft)
        leftBoxID = bLeft[index]

        #Go for centerbox
        if ((goAroundDist < min(roboToBoxLeft)) and (targetID != goAroundID)):
            turn, dist = go_to_xy(minLeft,goAroundDist)
            print("going left of box ", goAroundID, " and before ", leftBoxID)
            return (turn+goAroundAng, dist)
        #Go for nearest leftbox
        else:
            # find vinkelen til kassen du skal Køre op på siden af
            avioldBoxAng = angles[np.where(objectIDs == leftBoxID)[0]]
            turn, dist = go_to_xy(minLeft, dists[np.where(objectIDs == leftBoxID)[0]])
            print("avoiding ",leftBoxID, " to get closer to ", goAroundID)
            if (avioldBoxAng < turn):
                return (turn-avioldBoxAng, dist)
            else:
                return (0-(avioldBoxAng-turn), dist)

    else:
        if ((minRight == 9999999) and (targetID != goAroundID)):
            # left is free finding direction next to obstacle
            print("right is clear")
            turn, dist = go_to_xy(distEmpty,goAroundDist)
            return (0-(turn-goAroundAng), dist)
        index = distRight.index(minRight)
        rightBoxID = bRight[index]
        
        #Go for centerbox
        if ((goAroundDist < min(roboToBoxRight)) and (targetID != goAroundID)):
            turn, dist = go_to_xy(minRight,goAroundDist)
            print("going right of box ", goAroundID, " and before ", rightBoxID)
            return (0-(turn-goAroundAng), dist)
        #Go for nearest rightbox 
        else:
            avioldBoxAng = angles[np.where(objectIDs == rightBoxID)[0]]
            turn, dist = go_to_xy(minRight, dists[np.where(objectIDs == rightBoxID)[0]])
            print("avoiding ", rightBoxID, " to get closer to ", goAroundID)
            if (avioldBoxAng < turn):
                return (turn+avioldBoxAng, dist)
            else:
                return (avioldBoxAng-turn, dist)



# for testing
# try:
#     cam = camera.Camera(0, 'arlo', useCaptureThread=True)
#     turnXDRadians, goDistMM =  findWay(cam, 1)
#     turnXDegrees = math.degrees(turnXDRadians)
#     goDistM = goDistMM/1000
#     print("turnXDegrees ", turnXDegrees)
#     print("Go Dist in M ", goDistMM)
# finally:
#     cam.terminateCaptureThread()






# den gamle version!


# def findWay(cam, targetID):
#     # tag billede
#     frame = cam.get_next_frame()
#     # identificer alle kasser
#     objectIDs, dists, angles = cam.detect_aruco_objects(frame)
#     if (objectIDs is None):
#         print("error in route planning, no objects found")
#         return (0,0)
#     bLeft = []
#     distLeft = []
#     bRight = []
#     distRight = []
#     roboToBoxLeft = []
#     roboToBoxRight = []

#     # find the center box, the box that is in the way
#     goAroundIndex = np.argmin(np.abs(angles)) #min(enumerate(angles), key=lambda x: abs(x[1]))
#     goAroundDist = dists[goAroundIndex]
#     goAroundAng = angles[goAroundIndex]
#     goAroundID = objectIDs[goAroundIndex]
#     print("avoid object : ", goAroundID)

#     if ((goAroundID in [1, 2, 3, 4]) and (goAroundID != targetID)):
#         print("Error in route planning, not trusting current theta")
#         return (0,0)

#     # removing the center box from the lists
#     for i in np.where(objectIDs == goAroundID):
#         objectIDs = np.delete(objectIDs, i)
#         dists = np.delete(dists, i)
#         angles = np.delete(angles, i)

#     # sort the objects to what is left and right of the center box
#     for i in range(len(objectIDs)):
#         #print("Object ID = ", objectIDs[i], ", Distance = ", dists[i], ", angle = ", angles[i])

#         # devide into two lists on +- angle
#         # insert the distance between center box and the other obstacle (i) -> space
#         space = math.sqrt(goAroundDist**2 + dists[i]**2 - 2*goAroundDist*dists[i] * (math.cos(angles[i] - goAroundAng)))

#         #print("dist between boxes", space)
#         #print("angle Center = ", goAroundAng, " ob i = ", angles[i],
#         #" angle between in deg= ", math.degrees((angles[i] - goAroundAng)))
#         if space > 25000:
#             print("ignoring due to distance over 2.5 m")
#         elif angles[i] > 0:
#             print(objectIDs[i] ," to my left")
#             bLeft.append(objectIDs[i])
#             distLeft.append(space)
#             roboToBoxLeft.append(dists[i])
#         else:
#             print(objectIDs[i] ," to my right")
#             bRight.append(objectIDs[i])
#             distRight.append(space)   # find de to nærmeste kasser til højre og venstre
#             roboToBoxRight.append(dists[i])


#     minLeft  = min(distLeft , default=9999999) # default hvis listen er tom
#     minRight = min(distRight, default=9999999)   # hvis der er frit til en af siderne vælger den denne
#     # og køre en meter ved siden af forhindringen
#     distEmpty = 100   # chossing the side with the most space
#     if (minLeft >= minRight):
#         if ((minLeft == 9999999) and (targetID != goAroundID)):
#             # left is free finding direction next to obstacle
#             print("left is clear")
#             turn, dist = go_to_xy(distEmpty, goAroundDist)
#             return (turn-goAroundAng, dist)
#         index = distLeft.index(minLeft)
#         leftBoxID = bLeft[index]

#         #Go for centerbox
#         if ((goAroundDist < min(roboToBoxLeft)) and (targetID != goAroundID)):
#             turn, dist = go_to_xy(minLeft,goAroundDist)
#             print("going between box ", goAroundID, " and ", leftBoxID)
#             return (turn-goAroundAng, dist)
#         #Go for nearest leftbox
#         else:
#             turn, dist = go_to_xy(minLeft,  distEmpty) # dists[np.where(objectIDs == leftBoxID)[0]])
#             print("avoiding ",leftBoxID, " to get closer to ", goAroundID)
#             return (-turn-goAroundAng, dist)

#     else:
#         if ((minRight == 9999999) and (targetID != goAroundID)):
#             # left is free finding direction next to obstacle
#             print("right is clear")
#             turn, dist = go_to_xy(distEmpty,goAroundDist)
#             return (-turn-goAroundAng, dist)
#         index = distRight.index(minRight)
#         rightBoxID = bRight[index]

#         #Go for centerbox
#         if ((goAroundDist < min(roboToBoxRight)) and (targetID != goAroundID)):
#             turn, dist = go_to_xy(minRight,goAroundDist)
#             print("going between box ", goAroundID, " and ", rightBoxID)
#             return (-turn-goAroundAng, dist)
#         #Go for nearest rightbox
#         else:
#             turn, dist = go_to_xy(minRight, distEmpty) # dists[np.where(objectIDs == rightBoxID)[0]])
#             print("avoiding ", rightBoxID, " to get closer to ", goAroundID)
#             return (turn-goAroundAng, dist)
