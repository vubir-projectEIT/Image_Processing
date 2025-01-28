#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:38:01 2025

@author: loris

Adapted from https://github.com/ibush/231A_Project/blob/master/src/hrFaceDetection.py
"""

"""
Important message for the developer:

This is a template for making a virtual heart rate sensor, also refered to as a virtual PPG (why would that be? 🤔).
We already give you some helper functions to detect faces in images. 
If you are interested, you can check the implementation in the corresponinding file (see imports).
Now it is up to you, follow the guide and extract the heart rate from a video of your face.
Good luck!
"""


""" IMPORTS """

import cv2
import numpy as np

# Check out the implementation of these helper functions in the Virtual_PPG_helpers.py file
from Virtual_PPG_helpers import get_roi, debug_plot


""" FUNCTIONS """

def get_heart_rate(window, fps, window_size, min_heart_rate=45, max_heart_rate=240, debug_mode=False):

    # Normalize across the window to have zero-mean and unit variance
    normalized_window = "YOUR CODE HERE"
    
    # Separate into three source signals using ICA (check sklearn FastICA)
    source_signal = "YOUR CODE HERE"
    
    # Calculate the Fourier transform
    power_spectrum = "YOUR CODE HERE"
    frequencies = "YOUR CODE HERE"
    
    # Find heart rate
    # find maximal power spectrum
    max_power_spectrum = "YOUR CODE HERE"
    # find the valid indices in the Fourier spectrum (i.e. where min_heart_rate <= valid <= max_heart_rate)
    valid_indices = "YOUR CODE HERE"
    # select the valid power spectrum and frequencies
    valid_power_spectrum = "YOUR CODE HERE"
    valid_frequencies = "YOUR CODE HERE"
    # find the frequency corresponding to the maximal power in the valid Fourier spectrum
    heart_rate = "YOUR CODE HERE"
    
    if debug_mode:
        debug_plot(source_signal, power_spectrum, fps, window_size)
        
    return heart_rate


""" PARAMETERS TO SET """

# Haar cascade face classifier path
CASCADE_PATH = r"/Users/loris/anaconda3/envs/EIT/lib/python3.12/site-packages/cv2/data"
CASCADE_PATH = CASCADE_PATH + r"/haarcascade_frontalface_default.xml"

# Set window time in seconds
WINDOW_TIME_SEC = 20

# Toggle these for different ROIs
REMOVE_EYES = True
FOREHEAD_ONLY = False


""" MAIN """

# Initialize videocapture
video = "YOUR CODE HERE"

# Initialize Haar cascade face classifier
face_cascade = "YOUR CODE HERE"

# Window size
fps = "YOUR CODE HERE"
window_size = int(np.ceil(WINDOW_TIME_SEC * fps))

# Main loop parameters
color_signal = [] # Will store the average RGB color values in each frame's ROI
heart_rates = [] # Will store the heart rate calculated every 1 second
previous_face_bbox = None

while True:

    # Capture frame
    _, frame = "YOUR CODE HERE"
    
    # Get ROI
    previous_face_bbox, roi = get_roi(frame, face_cascade, previous_face_bbox, REMOVE_EYES, FOREHEAD_ONLY)
        
    # If ROI found, extract average colors
    if roi is not None:
        # get color channels
        color_channels = roi.reshape(-1, roi.shape[-1])
        # average the color channels
        average_colors = "YOUR CODE HERE"
        # add latest sample to the color signal
        "YOUR CODE HERE"
        
    # Calculate heart rate every one second (once have 30-second of data)
    if (len(color_signal) >= window_size) and (len(color_signal) % np.ceil(fps) == 0):
        # get last N samples with N = window_size
        window = "YOUR CODE HERE"
        # calculate heart rate
        heart_rate = get_heart_rate(window, fps, window_size)
        # add heart rate to list of heart rates
        "YOUR CODE HERE"
    
    # Display heart rate
    if heart_rates:
        # calculate BPM
        BPM = "YOUR CODE HERE"
        # display BPM
        cv2.putText(roi, f"BPM : {int(BPM)}", (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
    else:
        # display 'initializing...'
        cv2.putText(roi, f"Initializing... [{int(100*len(colorSig)/window_size)}%]", (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
    
    # Show the image
    if roi is None:
        roi = frame
    "YOUR CODE HERE"
    
    # Escape
    k = cv2.waitKey(1)
    if k == 27:
        break

# Close video capture and destroy windows
video.release()
cv2.destroyAllWindows()
