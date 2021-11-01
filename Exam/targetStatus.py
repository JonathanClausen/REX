

def checkTargetStatus(target, cam):
    frame = cam.get_next_frame()
    ids, dists, angles = cam.detect_aruco_objects(frame)
    if not(bool(ids)): 
        return 2    
    elif target in ids: 
        return 0
    else:
        return 1
  