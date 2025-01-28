""" IMPORTS """

import cv2 as cv2
import numpy as np


""" FUNCTIONS """

def gammaCorrection(src, gamma):
    invGamma = 1 / (gamma+0.001)

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(src, table)
    
    
""" MAIN """

if __name__ == '__main__':

    # Create 2 windows to display image
    src_window_name = "Source Image"
    dst_window_name = "Pipeline"
    cv2.namedWindow(src_window_name, cv2.WINDOW_NORMAL)
    cv2.namedWindow(dst_window_name, cv2.WINDOW_NORMAL)

    # Add controls to the webcam image to control blurring and HSV bandwidth
    cv2.createTrackbar('Kernel', src_window_name, 23, 50, lambda x: None)
    cv2.createTrackbar('Sigma', src_window_name, 30, 37, lambda x: None)
    cv2.createTrackbar('Gamma', src_window_name, 16, 30, lambda x: None)

    cv2.createTrackbar('hMin', src_window_name, 10, 255, lambda x: None)
    cv2.createTrackbar('sMin', src_window_name, 60, 255, lambda x: None)
    cv2.createTrackbar('vMin', src_window_name, 150, 255, lambda x: None)
    cv2.createTrackbar('hMax', src_window_name, 255, 255, lambda x: None)
    cv2.createTrackbar('sMax', src_window_name, 255, 255, lambda x: None)
    cv2.createTrackbar('vMax', src_window_name, 255, 255, lambda x: None)

    # define a video capture object
    cam = cv2.VideoCapture(0)

    while True:

        # Get an image fro the camera
        ret, frame = cam.read()
        if frame is None:
            continue

        # Get values from slider controls
        k = int(cv2.getTrackbarPos('Kernel', src_window_name))
        s = int(cv2.getTrackbarPos('Sigma', src_window_name))

        g = int(cv2.getTrackbarPos('Gamma', src_window_name))

        h_min = int(cv2.getTrackbarPos('hMin', src_window_name))
        s_min = int(cv2.getTrackbarPos('sMin', src_window_name))
        v_min = int(cv2.getTrackbarPos('vMin', src_window_name))

        h_max = int(cv2.getTrackbarPos('hMax', src_window_name))
        s_max = int(cv2.getTrackbarPos('sMax', src_window_name))
        v_max = int(cv2.getTrackbarPos('vMax', src_window_name))

        # Gamma adjustment
        g *= 0.1
        gamma = gammaCorrection(frame, g)

        # Blur
        k += (k + 1) % 2  # Ensure the kernel size is odd
        blur = cv2.GaussianBlur(gamma, (k, k), s)

        # Convert color image to HSV image
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # Apply mask thresholding to HSV image
        hsv_min = np.array([h_min, s_min, v_min], np.uint8)
        hsv_max = np.array([h_max, s_max, v_max], np.uint8)
        mask = cv2.inRange(hsv, hsv_min, hsv_max)

        # Remove noise with erosion + dilation
        morph = np.ones((5, 5), np.uint8)
        erode = cv2.erode(mask, morph, iterations=2)
        dilate = cv2.dilate(erode, morph, iterations=2)
        bgr_mask = cv2.cvtColor(dilate, cv2.COLOR_GRAY2BGR)

        # Detect Edges for fun
        edges = cv2.Canny(dilate, threshold1=64, threshold2=128)
        contours = cv2.findNonZero(edges)

        # Update image windows
        cv2.imshow(src_window_name, np.hstack((frame, gamma, hsv, bgr_mask)))
        cv2.imshow(dst_window_name, np.hstack((mask, erode, dilate, edges)))
        cv2.waitKey(1)
