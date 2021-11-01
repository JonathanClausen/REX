from time import sleep

def checkTargetStatus(target, cam):
    sleep(0.5)
    frame = cam.get_next_frame()
    sleep(0.5)
    ids, dists, angles = cam.detect_aruco_objects(frame)
    print("Checktarget: boxex in picture = " ,str(ids))
    if isinstance(ids, type(None)): 
        return 2    
    elif target in ids: 
        return 0
    else:
        return 1
  