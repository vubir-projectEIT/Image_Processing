#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:11:04 2024

@author: loris

derived from mediapipe implementation of hand tracking and gesture recognition of Google
 (https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer)

"""

import os
import time
import cv2
import mediapipe as mp

def initialize_hand_recognizer(model_path, num_hands, min_hand_detection_confidence, min_hand_presence_confidence, min_tracking_confidence):

    """
    Get an initialized hand recognizer and corresponding recognition results list
        INPUTS
        - model_path: path to file called gesture_recognizer.task
        - num_hands: int = maximale amount of hands to be detected in the frame
        - min_hand_detection_confidence: float = confidence of detected hands
        - min_hand_presence_confidence: float = confidence of presence of hands in frame
        - min_tracking_confidence: float = confidence of tracking of hands in frames
        
        OUTPUTS
        - recognizer = object that can detect hands in a frame
        - recognition_result_list = list in which we will save the recognition results
    """
    
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    
    recognition_result_list = []
    
    def save_result(result: vision.GestureRecognizerResult, unused_output_image: mp.Image, timestamp_ms: int):
        recognition_result_list.append(result)
    
    # Initialize the gesture recognizer model
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.GestureRecognizerOptions(base_options=base_options,
                                      running_mode=vision.RunningMode.LIVE_STREAM,
                                      num_hands=num_hands,
                                      min_hand_detection_confidence=0.7,
                                      min_hand_presence_confidence=0.7,
                                      min_tracking_confidence=0.5,
                                      result_callback=save_result)
    recognizer = vision.GestureRecognizer.create_from_options(options)
    
    return recognizer, recognition_result_list


from mediapipe.framework.formats import landmark_pb2

def show_hands(current_frame, recognition_result_list, show_gesture=True):

    """
    Return the current frame with the detected hands shown onto it
        INPUTS
        - current_frame: np.array(H,W,3) = current frame from OpenCV
        - recognition_result_list: list = list containing the last results of the hand detection (https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python#run_the_task)
        - show_gesture: [True]/False = showing the detected gesture or not
        
        OUTPUTS
        - np.array(H,W,3) = current frame from OpenCV with hands (and gesture)
    """

    if recognition_result_list:
        # Get a list of all the detected landmarks of the hands
        hand_landmark_list = recognition_result_list[0].hand_landmarks
        # Get a list of all the detected gestures of the hands
        gestures = recognition_result_list[0].gestures
        # Print the landmarks and connections between landmarks for each hand
        for hand_index, hand_landmarks in enumerate(hand_landmark_list):
            normalized_hand_landmarks = landmark_pb2.NormalizedLandmarkList()
            normalized_hand_landmarks.landmark.extend([landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
            mp.solutions.drawing_utils.draw_landmarks(
              current_frame,
              normalized_hand_landmarks,
              mp.solutions.hands.HAND_CONNECTIONS,
              # Uncomment the following to show all fingers in different colors
              #mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
              #mp.solutions.drawing_styles.get_default_hand_connections_style()
              )
            
            # Show detected gesture
            if show_gesture:
                
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
                text_y = y_min_px - 10

                # Make sure the text is within the frame boundaries
                if text_y < 0:
                    text_y = y_max_px + text_height

                # Draw the text
                cv2.putText(current_frame, category_name, (text_x, text_y),
                          cv2.FONT_HERSHEY_DUPLEX, 1,
                          (255,255,255), 1, cv2.LINE_AA)
            
        recognition_result_list.clear()
        
    return current_frame

    
## INITIALIZATE OBJECTS

# Initialinze hand recognizer

# path to gesture recognizer model
model_path = os.path.dirname(__file__) + '/gesture_recognizer.task'
# maximal number of hands to track in frame
num_hands = 2
# confidence of detected hands
min_hand_detection_confidence = 0.7
# confidence of presence of hands in frame
min_hand_presence_confidence = 0.7
# confidence of tracking of hands in frames
min_tracking_confidence = 0.5

hand_recognizer, recognition_result_list = initialize_hand_recognizer(model_path, num_hands, min_hand_detection_confidence, min_hand_presence_confidence, min_tracking_confidence)

# True: show the detected gesture
show_gesture = True
    
# Initialize video capture
cap = cv2.VideoCapture(0)


## MAIN LOOP

while True:
    # Get a new frame
    _, frame = cap.read()
    
    # Translate OpenCV frame to Mediapipe frame
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Run gesture recognizer on new frame
    
    hand_recognizer.recognize_async(mp_frame, time.time_ns()//1000000)
    
    # Process hands on original frame
    recognition_frame = show_hands(frame, recognition_result_list, show_gesture)
    
    # Show resulting frame (with hands)
    cv2.imshow('Hands', recognition_frame)

    # Stop the program if the ESC key is pressed.
    if cv2.waitKey(1) == 27:
        break


## CLOSE INIALIZED OBJECTS

# Close hand recognizer
hand_recognizer.close()

# Close video capture
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
