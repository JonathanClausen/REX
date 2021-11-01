

def checkTargetStatus(target, cam):
    frame = cam.get_next_frame()
    ids, dists, angles = cam.detect_aruco_objects(frame)
    print(ids)
    if ids is None: 
        return 2    
    elif target in ids: 
        return 0
    else:
        return 1
  