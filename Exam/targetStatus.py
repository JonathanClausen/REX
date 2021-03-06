from time import sleep
import numpy as np
import math

def checkTargetStatus(target, cam):
    sleep(0.5)
    frame = cam.get_next_frame()
    sleep(0.5)
    ids, dists, angles = cam.detect_aruco_objects(frame)
    print("Checktarget: boxes in picture = " ,str(ids))
    
    
    
    if isinstance(ids, type(None)): 
        return 2 #Nothing is seen at all    

    elif target in ids:
        if len(ids) == 1:
            print("targetStatus: Only seen target")     
            return 0 #Target is the only thing seen
        else:   
            print("targetStatus: Seen target + others")
            targetAngle = np.abs(angles[np.where(ids == target)])
            boxAngles   = (angles[np.where(ids != target)])
            #boxAngles = [n + targetAngle for n in boxAngles]
            boxDists    = dists[np.where(ids != target)]
            #print("!!!!!boxAngle, boxDists = !!!!!!", boxAngles, boxDists)
            spaces = []
            for i in range(len(boxAngles)): 
                space_between_box_target = math.sin(np.abs(boxAngles[i]))*boxDists[i]
                spaces.append(space_between_box_target)
                #print("minSpaces = ", np.min(spaces))
            if ((len(spaces) > 0) and (np.min(spaces) < 35)): #not enough space
                print("Not enough space - Routeplan")
                return 1
            else: 
                print("Enough space - Goto target")
                return 0 # go to target  

    else:
        return 1 #Do routeplan
