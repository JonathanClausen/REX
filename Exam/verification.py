import particle
import math

def verify(mean, front, goBox, emergency):
    if emergency:
        if (goBox and mean) or ((front < 400) and goBox):
            return True
        else:
            return False
    elif (mean and goBox and (front < 400)):
        return True
    elif (mean and goBox):
        if (front > 3000):
            return True
        else:
            return False
    elif (goBox and (front < 400)):
        return True

def checkMean(particle, target):
    pX = particle.getX()
    pY = particle.getY()

    dist = math.sqrt((pX - target[0])**2 + (pY- target[1])**2)

    return (dist < 40)

def checkGoToBox(total, traveled):
    delta = total - traveled
    return ((delta < 40) and (delta > -10))