#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:11:04 2024

@author: loris

derived from mediapipe implementation of hand tracking and gesture recognition of Google
 (https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer)

"""


"""
Go through the code carefully before running it
Read the annotations and ask questions (to the internet, chatGPT, or the assistents)

"""


""" IMPORTS """

# pip install opencv-contrib-python==4.9.0.80
# pip install mediapipe==0.10.9

import cv2
from HandRecognizer import HandRecognizer   # mediapipe dependency


""" MAIN """

if __name__ == '__main__':

    # TODO: Initialize video capture
    cap = "YOUR CODE HERE"

    # Path to gesture recognizer model
    model_path = 'Absolute/path/to/model'

    # Initialize hand recognizer
    hand_recognizer = HandRecognizer(model_path)

    # Loop
    while True:

        # TODO: Get a new frame
        frame = "YOUR CODE HERE"
        
        # TODO: Translate BGR frame to RGB frame for Mediapipe
        rgb_frame = "YOUR CODE HERE"

        # Detect the hand by applying the hand recognizer on your new RGB frame
        hand_landmarks, gestures = hand_recognizer.detect(rgb_frame)
        # NOTE: Note that the hand_landmarks variable and gestures variable are defined here but remain unused. You can use them further for more advanced tasks. More information on those variables can be found at https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python#handle_and_display_results
        
        # Process hands on the orginal frame
        recognition_frame = hand_recognizer.show_hands(frame)
        
        # TODO: Display resulting recognition frame
        ## YOUR CODE HERE ##

        # Stop the program if the ESC key is pressed
        if cv2.waitKey(1) == 27:
            break


    # Close
    hand_recognizer.close()
    cap.release()
    cv2.destroyAllWindows()
