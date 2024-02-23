import cv2 as cv2
import numpy as np


class SimpleROISelector:

    def __init__(self, named_window: str, on_roi_updated=None, **kwargs):

        if not isinstance(named_window, str):
            raise TypeError(f"Argument 'named_window' <{type(named_window).__name__}> is not of type <str>")

        if on_roi_updated is not None and not callable(on_roi_updated):
            raise TypeError(f"Argument 'on_roi_updated' <{type(on_roi_updated).__name__}> is not callable")

        self.__roi = (0, 0, 0, 0)                  # Latest region of interest of tracked thing
        self.__selecting_roi = False               # Flag for user roi selection
        self.__verbose = False                     # Verbose flag
        self.__named_window = named_window         # Name of cv window
        self.__roi_updated = False                 # Flag for new roi
        self.__on_roi_updated = on_roi_updated     # Callback for new roi

        # Set mouse callback
        cv2.setMouseCallback(named_window, self.__on_mouse)

    @property
    def is_selecting_roi(self):
        return self.__selecting_roi

    @property
    def is_new_roi(self):
        return self.__roi_updated

    @property
    def roi(self):
        self.__roi_updated = False
        return self.__roi

    def update_ux(self, image):

        # Draw user roi selection
        if self.__selecting_roi and image is not None:
            p1 = (self.__roi[0], self.__roi[1])
            p2 = (self.__roi[0] + self.__roi[2], self.__roi[1] + self.__roi[3])
            cv2.rectangle(image, p1, p2, (255, 255, 255), 2, 1)

    def set_verbose(self, value):
        if isinstance(value, bool):
            self.__verbose = value

    # Function which handles mouse events
    def __on_mouse(self, event, x, y, flag, param):

        # Start user defined ROI BB
        if event == cv2.EVENT_LBUTTONDOWN and not self.__selecting_roi:
            if self.__verbose:
                print(f"Mouse Down at {x},{y}")
            self.__selecting_roi = True
            self.__roi = (x, y, 0, 0)

        # Update user defined ROI BB based on mouse
        elif event == cv2.EVENT_MOUSEMOVE and self.__selecting_roi:
            x0, y0 = self.__roi[:2]
            self.__roi = (x0, y0, x - x0, y - y0)

        # End user defined ROI BB and create tracker
        elif event == cv2.EVENT_LBUTTONUP and self.__selecting_roi:
            if self.__verbose:
                print(f"Mouse up at {x},{y}")

            # Update roi
            x, y, w, h = self.__roi
            self.__roi = (x if w >= 0 else x + w,
                               y if h >= 0 else y + h,
                               abs(w),
                               abs(h))

            if self.__verbose:
                print(f"ROI {self.__roi}")

            # Update flags
            self.__roi_updated = True
            self.__selecting_roi = False

            # Callback
            if callable(self.__on_roi_updated):
                self.__on_roi_updated(self.__roi)

        # Draw user roi selection
        if self.__selecting_roi and param is not None:
            p1 = (self.__roi[0], self.__roi[1])
            p2 = (self.__roi[0] + self.__roi[2], self.__roi[1] + self.__roi[3])
            cv2.rectangle(param, p1, p2, (255, 255, 255), 2, 1)


if __name__ == "__main__":

    # Create an video capture object
    cap = cv2.VideoCapture(0)

    # Create an image window named "Webcam"
    cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)

    # Create the simple roi selector object which is active on the window "Webcam"
    selector = SimpleROISelector("Webcam")
    roi = None

    while cap.isOpened():

        # Get latest webcam image
        ret, frame = cap.read()

        # Check if the roi selector has a new roi
        if selector.is_new_roi:
            roi = selector.roi

        # Draw the latest roi to the current image
        if roi is not None:
            x, y, w, h = roi
            cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=1, lineType=cv2.LINE_AA)

        # Always update the roi selector ux after any image processing
        # This draws the white box on the webcam image which could interfere with image processing stages
        selector.update_ux(frame)

        # Display image to window
        cv2.imshow("Webcam", frame)
        cv2.waitKey(1)




