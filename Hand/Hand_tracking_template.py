#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:11:04 2024

@author: loris
"""

import os
import time
import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

# Return the current frame with the detected hands shown onto it
    # current_frame: np.array(H,W,3) = current frame from OpenCV
    # recognition_result_list: list = list containing the last results of the hand detection (https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python#run_the_task)
    # show_gesture: [True]/False = showing the detected gesture or not
    
    # return: np.array(H,W,3) = current frame from OpenCV with hands (and gesture)
    
def show_hands(current_frame, recognition_result_list, show_gesture=True):

    if recognition_result_list:
        hand_landmark_list = recognition_result_list[0].hand_landmarks
        for hand_index, hand_landmarks in enumerate(hand_landmark_list):
            normalized_hand_landmarks = landmark_pb2.NormalizedLandmarkList()
            normalized_hand_landmarks.landmark.extend([landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
            mp.solutions.drawing_utils.draw_landmarks(
              current_frame,
              normalized_hand_landmarks,
              mp.solutions.hands.HAND_CONNECTIONS,
              #mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
              #mp.solutions.drawing_styles.get_default_hand_connections_style()
              )
        
            if show_gesture:
            
                gestures = recognition_result_list[0].gestures
                
                x_min = min([landmark.x for landmark in hand_landmarks])
                y_min = min([landmark.y for landmark in hand_landmarks])
                y_max = max([landmark.y for landmark in hand_landmarks])
                frame_height, frame_width = current_frame.shape[:2]
                x_min_px = int(x_min * frame_width)
                y_min_px = int(y_min * frame_height)
                y_max_px = int(y_max * frame_height)
                
                gesture = gestures[hand_index]
                category_name = str(gesture[0].category_name)

                # Compute text size
                text_width, text_height = cv2.getTextSize(category_name, cv2.FONT_HERSHEY_DUPLEX, 1, 1)[0]

                # Calculate text position (above the hand)
                text_x = x_min_px
                text_y = y_min_px - 10  # Adjust this value as needed

                # Make sure the text is within the frame boundaries
                if text_y < 0:
                    text_y = y_max_px + text_height

                # Draw the text
                cv2.putText(current_frame, category_name, (text_x, text_y),
                          cv2.FONT_HERSHEY_DUPLEX, 1,
                          (255,255,255), 1, cv2.LINE_AA)
            
        recognition_result_list.clear()
        
    return current_frame


# Please code your own hand recognizer in a separate file, this can serve as a template (Tip: use imports)

if __name__ == '__main__':

    # TODO: Initialize hand recognizer and result list (https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python#create_the_task)
    
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        # Get frame
        _, frame = cap.read()
        
        # TODO: Recognize hands in frame (https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python#prepare_data and further)
        
        recognition_frame = show_hands(frame, recognition_result_list, show_gesture=True)

        cv2.imshow('Hands', recognition_frame)

        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
