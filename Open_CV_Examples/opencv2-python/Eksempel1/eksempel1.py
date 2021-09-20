# This script shows how to open a camera in OpenCV and grab frames and show these.
# Kim S. Pedersen, 2015

import cv2 # Import the OpenCV library


# Open a camera device for capturing
cam = cv2.VideoCapture(0);

if not cam.isOpened(): # Error
    print("Could not open camera");
    exit(-1);
    
    
# Open a window
WIN_RF = "Eksempel 1";
cv2.namedWindow(WIN_RF);
cv2.moveWindow(WIN_RF, 100       , 0);


while cv2.waitKey(4) == -1: # Wait for a key pressed event
    retval, frameReference = cam.read() # Read frame
    
    if not retval: # Error
        print(" < < <  Game over!  > > > ");
        exit(-1);
    
    # Show frames
    cv2.imshow(WIN_RF, frameReference);
    

# Finished successfully
