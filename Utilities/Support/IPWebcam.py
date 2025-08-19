""" IMPORTS """

import cv2


""" LOCAL SERVER """

ip_address = "10.240.20.239"
port = "8080"


""" MAIN """

if __name__ == '__main__':

    url = f"https://{ip_address}:{port}/video"

    cap = cv2.VideoCapture(url)

    while cap.isOpened():

        ret, frame = cap.read()

        if ret:
            cv2.imshow('IP Webcam', frame)

        k = cv2.waitKey(1)
        if k == 27:
            break

    print(f"Using this setup, I can get {int(cap.get(cv2.CAP_PROP_FPS))} frames per seconds",
          f"at a resolution of {int(cap.get(3))}x{int(cap.get(4))}")

    cap.release()
    cv2.destroyAllWindows()
