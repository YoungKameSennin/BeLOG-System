# Camera Preview
# version 1.0
# Data: Nov 12, 2023

import numpy as np
import cv2

# Initialize the video capture object with the default camera (usually the first camera)
cap = cv2.VideoCapture(0)

# Set the desired resolution (optional, depends on camera support)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Starting preview.\nPress 'q' to stop.")

cv2.namedWindow('Preview')
cv2.moveWindow('Preview', 620, 0)

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Display the resulting frameq
        cv2.imshow('Preview', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # When everything done, release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

