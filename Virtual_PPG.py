"""
Adapted from https://github.com/ibush/231A_Project/blob/master/src/hrFaceDetection.py
"""

import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from sklearn.decomposition import FastICA
import warnings
import random


""" PARAMETERS TO SET """

# Set path to face cascade
CASCADE_PATH = r"/Users/loris/anaconda3/envs/EIT_project/lib/python3.11/site-packages/cv2/data"
CASCADE_PATH = CASCADE_PATH + r"/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(CASCADE_PATH)

# Initialize videocapture
video = cv2.VideoCapture(0)

# Toggle these for different ROIs
REMOVE_EYES = False
FOREHEAD_ONLY = True
USE_SEGMENTATION = False

# Toggle to see signals and spectrum
DEBUG_MODE = False


""" FIXED PARAMETERS """

FPS = video.get(cv2.CAP_PROP_FPS)

MIN_FACE_SIZE = 100
WIDTH_FRACTION = 0.6 # Fraction of bounding box width to include in ROI
HEIGHT_FRACTION = 1

WINDOW_TIME_SEC = 30
WINDOW_SIZE = int(np.ceil(WINDOW_TIME_SEC * FPS))
MIN_HR_BPM = 45.0
MAX_HR_BMP = 240.0
MAX_HR_CHANGE = 12.0
SEC_PER_MIN = 60

SEGMENTATION_HEIGHT_FRACTION = 1.2
SEGMENTATION_WIDTH_FRACTION = 0.8
GRABCUT_ITERATIONS = 5
MY_GRABCUT_ITERATIONS = 2

EYE_LOWER_FRAC = 0.25
EYE_UPPER_FRAC = 0.5

BOX_ERROR_MAX = 0.5
ADD_BOX_ERROR = False


""" FUNCTIONS """

def segment(image, faceBox):
    mask = np.zeros(image.shape[:2],np.uint8)
    bgModel = np.zeros((1,65),np.float64)
    fgModel = np.zeros((1,65),np.float64)
    cv2.grabCut(image, mask, faceBox, bgModel, fgModel, GRABCUT_ITERATIONS, cv2.GC_INIT_WITH_RECT)
    backgrndMask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD),True,False).astype('uint8')
    
    backgrndMask = np.broadcast_to(backgrndMask[:,:,np.newaxis], np.shape(image))
    return backgrndMask

def getROI(image, faceBox): 
    if USE_SEGMENTATION:
        widthFrac = SEGMENTATION_WIDTH_FRACTION
        heigtFrac = SEGMENTATION_HEIGHT_FRACTION
    else:
        widthFrac = WIDTH_FRACTION
        heigtFrac = HEIGHT_FRACTION

    # Adjust bounding box
    (x, y, w, h) = faceBox
    widthOffset = int((1 - widthFrac) * w / 2)
    heightOffset = int((1 - heigtFrac) * h / 2)
    faceBoxAdjusted = (x + widthOffset, y + heightOffset,
        int(widthFrac * w), int(heigtFrac * h))

    # Segment
    if USE_SEGMENTATION:
        backgrndMask = segment(image, faceBoxAdjusted)

    else:
        (x, y, w, h) = faceBoxAdjusted
        backgrndMask = np.full(image.shape, True, dtype=bool)
        backgrndMask[y:y+h, x:x+w, :] = False
    
    (x, y, w, h) = faceBox
    if REMOVE_EYES:
        backgrndMask[y + int(h * EYE_LOWER_FRAC) : y + int(h * EYE_UPPER_FRAC), :] = True
    if FOREHEAD_ONLY:
        backgrndMask[y + int(h * EYE_LOWER_FRAC) :, :] = True

    roi = np.ma.array(image, mask=backgrndMask) # Masked array
    return roi

# Sum of square differences between x1, x2, y1, y2 points for each ROI
def distance(roi1, roi2):
    return sum((roi1[i] - roi2[i])**2 for i in range(len(roi1)))

def getBestROI(frame, faceCascade, previousFaceBox):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(MIN_FACE_SIZE, MIN_FACE_SIZE), flags=cv2.CASCADE_SCALE_IMAGE)
    roi = None
    faceBox = None

    # If no face detected, use ROI from previous frame
    if len(faces) == 0:
        faceBox = previousFaceBox

    # if many faces detected, use one closest to that from previous frame
    elif len(faces) > 1:
        if previousFaceBox is not None:
            # Find closest
            minDist = float("inf")
            for face in faces:
                if distance(previousFaceBox, face) < minDist:
                    faceBox = face
        else:
            # Chooses largest box by area (most likely to be true face)
            maxArea = 0
            for face in faces:
                if (face[2] * face[3]) > maxArea:
                    faceBox = face

    # If only one face dectected, use it!
    else:
        faceBox = faces[0]

    if faceBox is not None:
        if ADD_BOX_ERROR:
            noise = []
            for i in range(4):
                noise.append(random.uniform(-BOX_ERROR_MAX, BOX_ERROR_MAX))
            (x, y, w, h) = faceBox
            x1 = x + int(noise[0] * w)
            y1 = y + int(noise[1] * h)
            x2 = x + w + int(noise[2] * w)
            y2 = y + h + int(noise[3] * h)
            faceBox = (x1, y1, x2-x1, y2-y1)

        # Show rectangle
        #(x, y, w, h) = faceBox
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)

        roi = getROI(frame, faceBox)

    return faceBox, roi

def debugPlot(signals, sources, spectrum):
    fig, [ax0, ax1, ax2] = plt.subplots(3,1)
    colors = ["r", "g", "b"]
    fig.patch.set_facecolor('white')
    
    seconds = np.arange(0, WINDOW_TIME_SEC, 1.0 / FPS)
    freqs = np.fft.fftfreq(WINDOW_SIZE, 1.0 / FPS)
    idx = np.argsort(freqs)
    
    for i in range(3):
        ax0.plot(seconds, signals[:,i], colors[i])
        ax0.set_ylabel('Signals', fontsize=17)
        ax1.plot(seconds, sources[:,i], 'black')
        ax1.set_ylabel('Sources', fontsize=17)
        ax0.set_xlabel('Time (sec)', fontsize=17)
        ax1.sharex(ax0)
        
        ax2.plot(freqs[idx], spectrum[idx,i])
        ax2.set_xlabel("Frequency (Hz)", fontsize=17)
        ax2.set_ylabel("Power", fontsize=17)
        ax2.set_xlim([0.75, 4])
        
    plt.show()

def getHeartRate(window, lastHR):
    # Normalize across the window to have zero-mean and unit variance
    mean = np.mean(window, axis=0)
    std = np.std(window, axis=0)
    normalized = (window - mean) / std

    # Separate into three source signals using ICA
    ica = FastICA(whiten='unit-variance')
    srcSig = ica.fit_transform(normalized)

    # Find power spectrum
    powerSpec = np.abs(np.fft.fft(srcSig, axis=0))**2
    freqs = np.fft.fftfreq(WINDOW_SIZE, 1.0 / FPS)

    # Find heart rate
    maxPwrSrc = np.max(powerSpec, axis=1)
    validIdx = np.where((freqs >= MIN_HR_BPM / SEC_PER_MIN) & (freqs <= MAX_HR_BMP / SEC_PER_MIN))
    validPwr = maxPwrSrc[validIdx]
    validFreqs = freqs[validIdx]
    maxPwrIdx = np.argmax(validPwr)
    hr = validFreqs[maxPwrIdx]
    
    if DEBUG_MODE:
        print(f"BPM: {SEC_PER_MIN*hr}")
        debugPlot(normalized, srcSig, powerSpec)
        
    return hr


""" MAIN """

colorSig = [] # Will store the average RGB color values in each frame's ROI
heartRates = [] # Will store the heart rate calculated every 1 second
previousFaceBox = None

while True:
    # Capture frame-by-frame
    _, frame = video.read()

    previousFaceBox, roi = getBestROI(frame, faceCascade, previousFaceBox)
    
    # If ROI found, extract average colors
    if (roi is not None) and (np.size(roi) > 0):
        colorChannels = roi.reshape(-1, roi.shape[-1])
        avgColor = colorChannels.mean(axis=0)
        colorSig.append(avgColor)

    # Calculate heart rate every one second (once have 30-second of data)
    heartRate = None
    if (len(colorSig) >= WINDOW_SIZE) and (len(colorSig) % np.ceil(FPS) == 0):
        windowStart = len(colorSig) - WINDOW_SIZE
        window = colorSig[windowStart : windowStart + WINDOW_SIZE]
        lastHR = heartRates[-1] if len(heartRates) > 0 else None
        heartRate = getHeartRate(window, lastHR)
        heartRates.append(heartRate)
    
    # Show ROI
    if np.ma.is_masked(roi):
        roi = np.where(roi.mask == True, 0, roi)
    
    if heartRates:
        BPM = SEC_PER_MIN*heartRates[-1]
        cv2.putText(roi, f"BPM : {int(BPM)}", (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
        
    cv2.imshow('ROI', roi)
    
    k = cv2.waitKey(1)
    if k == 27:
        break

video.release()
cv2.destroyAllWindows()
