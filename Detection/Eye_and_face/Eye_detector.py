""" IMPORTS """

import os
import cv2


""" MAIN """

if __name__ == '__main__':

    # Path to cv2/data. If this gives an error:
    #   - option 1: Find the 'haarcascade_eye.xml' file on your computer and modify the path hereunder to the path of the folder containing 'haarcascade_eye.xml'.
    #   - option 2: You can also download haarcascade_eye.xml from the internet, place it in your project folder, and modify the path hereunder.
    cascade_dir = os.environ['CONDA_PREFIX'] + r"/lib/python3.12/site-packages/cv2/data"
    
    # Load the cascade
    eye_cascade = cv2.CascadeClassifier(cascade_dir + r"/haarcascade_eye.xml")
    face_cascade = cv2.CascadeClassifier(cascade_dir + r"/haarcascade_frontalface_default.xml")


    # To capture video from webcam.
    cap = cv2.VideoCapture(0)
    # To use a video file as input
    # cap = cv2.VideoCapture('filename.mp4')

    cat_filename = __file__.split('.')[0] + "_Cat.png"
    cat_img = cv2.imread(cat_filename, cv2.IMREAD_COLOR)
      
    cat_img = cv2.resize(cat_img, (200,200))

    while True:
        # Read the frame
        _, img = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for (x, y, w, h) in face_cascade.detectMultiScale(gray, 1.1, 4):
            img[y:y + h, x:x + w] = cv2.resize(cat_img, (h, w))

        # Draw the rectangle around each face
        # for (x, y, w, h) in eye_cascade.detectMultiScale(gray, 1.1, 4):
            # img[y:y+h, x:x+w] = cv2.resize(cat_img, (h,w))

        # Display
        cv2.namedWindow("img", cv2.WINDOW_FREERATIO)
        cv2.imshow('img', img)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
        
    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()
