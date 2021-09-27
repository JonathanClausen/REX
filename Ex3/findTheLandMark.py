import cv2
import numpy as np

#cv.aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs[, rvecs[, tvecs[, _objPoints]]] ) ->  rvecs, tvecs, _objPoints
#rvec = Output vector (e.g. cv::Mat) corresponding to the rotation vector of the board
#Output vector (e.g. cv::Mat) corresponding to the translation vector of the board
#tvec = [x,y,z]: x =  horizontal drejning, y= vertical, z= vineklret afstand 
markerLength = 0.145
cameraMatrix =np.array([[506.94,0,640/2],
               [0,506.94,480/2],
               [0,0,1],])
distCoeffs = 0

#distCoeffs[, rvecs[, tvecs[, _objPoints]]]

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
ret,frame = cap.read() # return a single frame in variable `frame`

#Grabbing dictionary 
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict,
	parameters=arucoParams)
print("corners")
print(corners)
print("ids")
print(ids)

rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs)
print("rvec")
print(rvec)
print("tvec")
print(tvec)
print("markerpoints")
print(markerPoints)
while(True):
    cv2.imshow('img1',frame) #display the captured image
    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        cv2.imwrite('images/c1.png',frame)
        cv2.destroyAllWindows()
        break

cap.release()

