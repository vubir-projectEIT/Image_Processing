""" IMPORTS """

import cv2
import time


""" LOCAL SERVER """

username = "camera"
password = "eit123"
ip_adress = "10.240.78.159"
port = "1812"


""" MAIN """

if __name__ == '__main__':

    url = f"https://{username}:{password}@{ip_adress}:{port}/video"

    cap = cv2.VideoCapture(url)

    fps = 0

    while cap.isOpened():

        t = time.time()

        ret, frame = cap.read()

        if ret:
            cv2.imshow('IP Webcam', frame)

        k = cv2.waitKey(1)
        if k == 27:
            break

        fps = (fps + 1 / (time.time() - t)) / 2

    print(f"Using this setup, I can get {int(fps)} frames per seconds",
          f"at a resolution of {int(cap.get(3))}x{int(cap.get(4))}")

    cap.release()
    cv2.destroyAllWindows()