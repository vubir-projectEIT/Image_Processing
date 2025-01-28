#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 20:07:53 2024

@author: loris
"""

"""
Go through the code carefully before running it
Read the annotations and ask questions (to the internet, chatGPT, or the assistents)
"""


""" IMPORTS """

import os
import cv2          # copy the following in your console: pip install opencv-contrib-python
import numpy as np  # copy the following in your console: conda install numpy


""" FUNCTIONS """

# Function to collect single face from a frame
def collect_face(frame):
    
    # gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # get all faces in image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    # check if there is only one face, else do nothing with this frame
    if not len(faces) == 1:
        return _, None
    
    # extract roi of face
    x, y, w, h = faces[0]
    face = gray[y:y+h, x:x+w]
    # draw bounding box
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # return frame and face roi
    return frame, face

# Function to collect images for each person
def collect_person():
    
    person = []
    while len(person) < n_training_images_per_person:
        # collect one image
        _, frame = cap.read()
        frame, face = collect_face(frame)
        if face is None:
            continue
        
        # store image
        person.append(face)
        # add info and show
        cv2.putText(frame, f"Collected images: {str(len(person))}", (100,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        cv2.imshow('Move your face around to collect different angles', frame)
        
        k = cv2.waitKey(1000) & 0xff
        if k==27:
            break
        
    return person

# Function to recognize faces
def recognize_faces(frame, display_labels):
    
    # gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect all faces in image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # for each face
    for (x, y, w, h) in faces:
        # get roi of face
        roi_gray = gray[y:y+h, x:x+w]
        # recognize person
        label, confidence = recognizer.predict(roi_gray)
        
        # draw a rectangle around recognized face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # display name and confidence level
        cv2.putText(frame, str(display_labels[label]), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (36,255,12), 2)

    return frame
    
    
""" MAIN """

if __name__ == '__main__':
    
    # SETUP
    
    # Recognition parameters
    n_training_images_per_person = 10
    named_labels = False # true: manually input labels, false: labels assigned automatically

    # Video capture
    cap = cv2.VideoCapture(0)

    # Get face detection filter
    cascade_dir = os.environ['CONDA_PREFIX'] + r"/lib/python3.12/site-packages/cv2/data"
    face_cascade = cv2.CascadeClassifier(cascade_dir + r"/haarcascade_frontalface_default.xml")

    # Store images, labels and display labels
    number_person = 0
    images = []
    labels = []
    display_labels = []

    # Create empty/untrained face recognizder
    recognizer = cv2.face.LBPHFaceRecognizer_create()


    # DATA COLLECTION LOOP

    while True:
        
        # Show image
        _, frame = cap.read()
        cv2.imshow('Video', frame)
        
        k = cv2.waitKey(50) & 0xff
        # Spacebar: Collect person
        if k == 32:
            # set label as number of perosn
            person_label = "person" + str(number_person)
            # if manual label
            if named_labels:
                # get manual label from terminal
                person_label = input(f"Label for person {number_person}: ")
            person_label = person_label.lower()
            # collect images for that person
            person = collect_person()
            # store images, labels and display labels
            images.extend(person)
            labels.extend(len(person)*[number_person])
            display_labels.append(person_label)
            number_person += 1
            cv2.destroyAllWindows()
        
        # Enter/Escape: Stop collection
        elif k == 13 or k == 27:
            break


    # TRAINING OF FACE RECOGNITION

    if images:

        # Train the LBPH face recognizer
        recognizer.train(images, np.array(labels))
        # Allow main loop to start if recognizer trained
        go = True
        
    else:
        
        # Recognizer not trained => main loop not starting
        go = False


    # MAIN LOOP

    while go:
        
        # Get a new frame
        _, frame = cap.read()
        
        # Detect and recognize faces
        frame = recognize_faces(frame, display_labels)

        # Display resulting frame
        cv2.imshow('Video', frame)

        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) & 0xFF == 27:
            break


    """ CLOSE VIDEO STREAM """

    cap.release()
    cv2.destroyAllWindows()
