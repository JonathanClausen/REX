

def checkTargetStatus(target, cam):
    frame = cam.get_next_frame()
    ids, dists, angles = cam.detect_aruco_objects(frame)
    print("Checktarget: boxex in picture = " ,str(ids))
    if isinstance(ids, type(None)): 
        return 2    
    elif target in ids: 
        return 0
    else:
        return 1
  