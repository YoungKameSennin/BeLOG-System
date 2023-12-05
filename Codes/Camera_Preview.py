# Camera Preview
# version 1.0
# Data: Nov 12, 2023

import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

pipeline.start(config)

print("Starting preview.\nClose this window to stop.")

cv2.namedWindow('Preview')
cv2.moveWindow('Preview', 620, 0)

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap to depth image
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Stack both images vertically
        images = np.vstack((color_image, depth_colormap))

        # Resize the image to fit 1280x720 window
        resized_image = cv2.resize(images, (640, 720))

        # Display the combined and resized image
        cv2.imshow('Preview', resized_image)

        key = cv2.waitKey(1)
finally:
    pipeline.stop()
    cv2.destroyAllWindows()
