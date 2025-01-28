#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:38:01 2025

@author: loris

Adapted from https://github.com/ibush/231A_Project/blob/master/src/hrFaceDetection.py
"""

""" IMPORTS """

import cv2
import numpy as np

import matplotlib.pyplot as plt


""" HELPER FUNCTIONS """

# Extract face from a frame
def _get_face_bbox(frame, face_classifier, previous_face_bbox, min_face_size=100):
    """
    Extract all faces in a frame using the face_classifier.
    
    inputs:
        - frame: the frame in which to extract the faces (np.ndarray)
        - face_classifier: the classifier to be used (cv2.CascadeClassifier)
        - previous_face_bbox: previously detected face bounding box (list)
        - [min_face_size]: minimal size that a face has to be to be detected (int) -> default = 100
        
    outputs:
        - face_bbox: the bounding box corresponding to the face (list)
    """

    # Detect faces in frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1,
        minNeighbors=5, minSize=(min_face_size, min_face_size), flags=cv2.CASCADE_SCALE_IMAGE)
    
    # Initalize face bounding box
    face_bbox = None

    # If no face detected, use ROI from previous frame
    if len(faces) == 0:
        face_bbox = previous_face_bbox

    # If many faces detected, use one closest to that from previous frame
    elif len(faces) > 1:
        # If there is a previous face_bbox, find closest box
        if previous_face_bbox is not None:
            min_dist = float("inf")
            for face in faces:
                distance = sum((previous_face_bbox[i] - face[i])**2 for i in range(len(face)))
                if distance < min_dist:
                    face_bbox = face
        # If there is no previous face_bbox, chooses largest box (most likely to be true face)
        else:
            max_area = 0
            for face in faces:
                if (face[2] * face[3]) > max_area:
                    face_bbox = face

    # If only one face dectected, use that one
    else:
        face_bbox = faces[0]
        
    return face_bbox

# Mask ROI on frame
def _extract_roi(frame, face_bbox, remove_eyes=True, forehead_only=False, width_fraction=0.6, heigt_fraction=1, eye_lower_frac=0.25, eye_upper_frac=0.5):
    """
    Mask the region of interest corresponding to the most interesting part of the face in the frame.
    
    inputs:
        - frame: the frame in which to extract the faces (np.ndarray)
        - face_bbox: the bounding box around the face (list)
        - [remove_eyes]: whether to remove the eyes in the ROI (bool) -> default = True
        - [forehead_only]: whether to only keep the forehead in the ROI (bool) -> default = False
        - [width_fraction]: fraction of the width of the bounding box to consider for the ROI (float) -> default = 0.6
        - [heigt_fraction]: fraction of the hieght of the bounding box to consider for the ROI (float) -> default = 1
        - [eye_lower_frac]: lower fraction of the height of the bounding box in which to find the eyes (float) -> default = 0.25
        - [eye_upper_frac]: upper fraction of the height of the bounding box in which to find the eyes (float) -> default = 0.5
        
    outputs:
        - roi: masked version of the frame corresponding to the ROI (np.ma.array)
    """

    roi = None
    
    if face_bbox is not None:
        # Adjust bounding box
        (x, y, w, h) = face_bbox
        width_offset = int((1 - width_fraction) * w / 2)
        height_offset = int((1 - heigt_fraction) * h / 2)
        adjusted_face_bbox = (x + width_offset, y + height_offset, int(width_fraction * w), int(heigt_fraction * h))
        
        # Create mask for face
        (x, y, w, h) = adjusted_face_bbox
        backgroundnd_mask = np.full(frame.shape, True, dtype=bool)
        backgroundnd_mask[y:y+h, x:x+w, :] = False
        
        # Adjust mask according to eyes and forehead
        (x, y, w, h) = face_bbox
        if remove_eyes:
            backgroundnd_mask[y + int(h * eye_lower_frac) : y + int(h * eye_upper_frac), :] = True
        if forehead_only:
            backgroundnd_mask[y + int(h * eye_lower_frac) :, :] = True

        roi = np.ma.array(frame, mask=backgroundnd_mask) # Masked array
        
    return roi
    
# Get the best ROI from a frame
def get_roi(frame, face_classifier, previous_face_bbox, remove_eyes=True, forehead_only=False):
    """
    Get the region of interest in the image.
    
    inputs:
        - frame: the frame in which to extract the faces (np.ndarray)
        - face_classifier: the classifier to be used (cv2.CascadeClassifier)
        - previous_face_bbox: previously detected face bounding box (list)
        - [remove_eyes]: whether to remove the eyes in the ROI (bool) -> default = True
        - [forehead_only]: whether to only keep the forehead in the ROI (bool) -> default = False
        
    outputs:
        - roi: ROI in the image (np.ndarray)
    """
    
    # Get a bounding box around the face
    face_bbox = _get_face_bbox(frame, face_classifier, previous_face_bbox)
    
    # Adjust the bounding box to the region of interest
    roi = _extract_roi(frame, face_bbox, remove_eyes, forehead_only)
    
    if np.ma.is_masked(roi):
        roi = np.where(roi.mask == True, 0, roi)

    return face_bbox, roi

# Utility function for debugging
def debug_plot(sources, spectrum, fps, window_size):
    """
    Plot some debugging graphs: time signal and power spectrum
    
    inputs:
        - sources: the signal corresponding to the sources or the raw color signal (np.array)
        - spectrum: the power spectrum (np.array)
        - fps: frame per second of the camera (int)
        - window_size: size of the window to consider in units of list indices (int)
        
    """
    
    fig, [ax1, ax2] = plt.subplots(1,2, figsize=(20,7))
    colors = ["r", "g", "b"]
    fig.patch.set_facecolor('white')
    
    seconds = np.arange(0, window_size/fps, 1.0/fps)
    freqs = np.fft.fftfreq(window_size, 1.0/fps)
    idx = np.argsort(freqs)
    
    for i in range(3):
        ax1.plot(seconds, sources[:,i], colors[i])
        ax1.set_ylabel('Sources', fontsize=17)
        ax1.set_xlabel('Time (sec)', fontsize=17)
        
        ax2.plot(freqs[idx], spectrum[idx,i])
        ax2.set_xlabel("Frequency (Hz)", fontsize=17)
        ax2.set_ylabel("Power", fontsize=17)
        ax2.set_xlim([0.75, 4])
    plt.tight_layout()
    plt.show()
