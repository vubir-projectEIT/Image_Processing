#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:11:04 2024

@author: loris

derived from mediapipe implementation of hand tracking and gesture recognition of Google
 (https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer)

"""


""" IMPORTS """

# pip install opencv-contrib-python==4.9.0.80
# pip install mediapipe==0.10.9

import os
import time

import cv2

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2


""" CLASS """

class HandRecognizer():
    
    # Only for students with advanced understanding of python
    # Method to initialize hand recognizer based on hand recognition parameters
    def __init__(self, model_path: str = '', num_hands: int = 2, min_hand_detection_confidence: float = 0.7, min_hand_presence_confidence: float = 0.7, min_tracking_confidence: float = 0.5):

        """
        Get an initialized hand recognizer and corresponding recognition results list
            INPUTS
            - model_path: str = path to file called gesture_recognizer.task
            - num_hands: int = maximale amount of hands to be detected in the frame
            - min_hand_detection_confidence: float = confidence of detected hands
            - min_hand_presence_confidence: float = confidence of presence of hands in frame
            - min_tracking_confidence: float = confidence of tracking of hands in frames

        """
        
        # initialize the list of detected hands
        self.recognition_result_list = []
        # initialize the list of hand landmarks
        self.hand_landmark_list = None
        # initialie the list of gestures
        self.gestures = None
        
        # define a function to save hands that were detected to the list of detected hands
        def save_result(result: vision.GestureRecognizerResult, unused_output_image: mp.Image, timestamp_ms: int):
            self.recognition_result_list.append(result)
        
        # initialize the hand recognizer model options
        if not os.path.exists(model_path):
            try_default_model_path = os.path.join(os.path.dirname(__file__), '/gesture_recognizer.task')
            if os.path.exists(try_default_model_path):
                model_path = try_default_model_path
                print(f"WARNING: The model path that you gave does not exist and was replaced by the default path: {model_path}")
            else:
                raise Exception(f"Model path '{model_path}' does not exist.")
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(base_options=base_options,
                                          running_mode=vision.RunningMode.LIVE_STREAM,
                                          num_hands=num_hands,
                                          min_hand_detection_confidence=0.7,
                                          min_hand_presence_confidence=0.7,
                                          min_tracking_confidence=0.5,
                                          result_callback=save_result)
        
        # initialize the hand recognizer model
        self.hand_recognizer = vision.GestureRecognizer.create_from_options(options)

    # Only for students with advanced understanding of python
    # Method for detection of a hand on a frame
    def detect(self, rgb_frame):
    
        """
        Detect hands on an RGB frame, results can be returned and used further in your code
            INPUTS 
            - rgb_frame: np.ndarray = the frame on which to detect hands
            
            OUTPUTS
            - hand_landmark_list: list = list of hands. Each hand is an object containing all the landmarks of that hand in world coordinates with associated confidence scores
            - gestures: list = list of hands. Each hand is an object containing the gestures with associated confidence scores
        """
        
        # transform RGB image defined in OpenCV to RGB image defined in Mediapipe
        mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # detect hands on the frame
        self.hand_recognizer.recognize_async(mp_frame, time.time_ns()//1000000)
        
        # if hands are detected
        if self.recognition_result_list:
            # extract the hand landmarks
            self.hand_landmark_list = self.recognition_result_list[0].hand_landmarks
            # extract the gestures
            self.gestures = self.recognition_result_list[0].gestures
            # clear the list of detected hands
            self.recognition_result_list.clear()
            
        # return the hand landmarks and the gestures
        return self.hand_landmark_list, self.gestures
        
    # Only for students with advanced understanding of python
    # Method to show the detected hand on a frame
    def show_hands(self, current_frame, show_gesture: bool = True):

        """
        Return the current frame with the detected hands shown onto it
            INPUTS
            - current_frame: np.array(H,W,3) = current frame from OpenCV
            - show_gesture: [True]/False = showing the detected gesture or not
            
            OUTPUTS
            - np.ndarray(H,W,3) = current frame from OpenCV with hands (and gesture)
        """
        
        # check if hand landmarks and gestures have been detected
        if self.hand_landmark_list and self.gestures:
            # loop over all the detected hands
            for hand_index, hand_landmarks in enumerate(self.hand_landmark_list):
                # get the normalized hand landmarks
                normalized_hand_landmarks = landmark_pb2.NormalizedLandmarkList()
                normalized_hand_landmarks.landmark.extend([landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
                # print the landmarks and connections between landmarks for each hand
                mp.solutions.drawing_utils.draw_landmarks(
                  current_frame,
                  normalized_hand_landmarks,
                  mp.solutions.hands.HAND_CONNECTIONS,
                  # Uncomment the following to show all fingers in different colors
                  #mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                  #mp.solutions.drawing_styles.get_default_hand_connections_style()
                  )
                
                # show detected gesture
                if show_gesture:
                    
                    # find the part of the hand closest to the left border
                    x_min = min([landmark.x for landmark in hand_landmarks])
                    # find the extent of the hand along the veritcal direction
                    y_min = min([landmark.y for landmark in hand_landmarks])
                    y_max = max([landmark.y for landmark in hand_landmarks])
                    # translate position of the hand to pixel positions on the frame
                    frame_height, frame_width = current_frame.shape[:2]
                    x_min_px = int(x_min * frame_width)
                    y_min_px = int(y_min * frame_height)
                    y_max_px = int(y_max * frame_height)
                    
                    # get the gesture of this hand
                    gesture = self.gestures[hand_index]
                    # get the gesture category
                    category_name = str(gesture[0].category_name)

                    # compute text size
                    text_width, text_height = cv2.getTextSize(category_name, cv2.FONT_HERSHEY_DUPLEX, 1, 1)[0]

                    # calculate text position (above the hand)
                    text_x = x_min_px
                    text_y = y_min_px - 10

                    # make sure the text is within the frame boundaries
                    if text_y < 0:
                        text_y = y_max_px + text_height

                    # draw the text
                    cv2.putText(current_frame, category_name, (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            
        return current_frame
        
    # Only for students with advanced understanding of python
    # Method to close the hand recognizer model
    def close(self):
        self.hand_recognizer.close()
