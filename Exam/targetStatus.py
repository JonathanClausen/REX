from time import sleep
import numpy as np
import math

def checkTargetStatus(target, cam):
    sleep(0.5)
    frame = cam.get_next_frame()
    sleep(0.5)
    ids, dists, angles = cam.detect_aruco_objects(frame)
    print("Checktarget: boxes in picture = " ,str(ids))
    
    targetAngle = angles[np.where(ids == target)]
    targetDist = dists[np.where(ids == target)]
    boxAngles   = angles[np.where(ids != target)]
    boxDists    = dists[np.where(ids != target)]
    spaces = []
    for i in range(len(boxAngles)): 
        space_between_box_target = math.sin(boxAngles[i])*boxDists[i]
        spaces.append(space_between_box_target)
    
    if isinstance(ids, type(None)): 
        return 2 #Nothing is seen at all    

    elif target in ids:
        if len(ids) == 1:     
            return 0 #Target is the only thing seen
        else: 
            if np.min(space_between_box_target) < 35: #not enough space
                return 1
                print("Not enough space to get to target")
            else: 
                return 0 # Routeplan 
                print("enough space")

    else:
        return 1 #Do routeplan
  