import cv2
import threading

class CameraStream:

    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.running = True

        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            self.ret, self.frame = self.cap.read()

    def read(self):
        if self.ret:
            return self.frame

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()


if __name__ == "__main__":
    
    cam = CameraStream(0)

    while True:
        frame = cam.read()
        if frame is not None:
            cv2.imshow("Camera Stream", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.stop()
    cv2.destroyAllWindows()