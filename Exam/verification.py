import particle
import math

mean_tolerance = 60                 #in centimeter
sens_front_tolerance = 600          #in millimeter
go_to_box_tolerance = 20            #in centimeter

def verify(mean, front, goBox, emergency):
    if emergency:
        if ((goBox and mean) or goBox):
            return True
        else:
            return False
    elif (mean and goBox and (front < sens_front_tolerance)):
        return True
    elif (mean and goBox):
        if (front > 3000):
            return True
        else:
            return False
    elif (goBox and (front < sens_front_tolerance)):
        return True

def checkMean(mean, target):
    pX = mean.getX()
    pY = mean.getY()

    dist = math.sqrt((pX - target[0])**2 + (pY- target[1])**2)
    print("CheckMean Distance: ", dist)

    return (dist < mean_tolerance)

def checkGoToBox(total, traveled):
    delta = total - traveled
    return ((delta < go_to_box_tolerance) and (delta > -go_to_box_tolerance))