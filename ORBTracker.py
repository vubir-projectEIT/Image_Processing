import cv2 as cv2
import numpy as np

from SimpleROISelector import SimpleROISelector


class ORBTracker:

    def __init__(self, ref_img):

        self.ref = np.copy(ref_img)
        MAX_FEATURES = 500
        self.detector = cv2.ORB_create(nfeatures=MAX_FEATURES)
        kpts, desc = self.detector.detectAndCompute(ref_img, None)
        self.desc = desc.astype(np.float32)
        self.kpts = kpts

    def update(self, image):

        # Detect orb features
        kpts, desc = self.detector.detectAndCompute(image, None)
        if desc is None:
            return

        # Cast as float32 for compatibility
        desc = desc.astype(np.float32)

        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary

        # FLANN match of kpts
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(self.desc, desc, k=2)

        # Filter matches based on distance metric
        good_matches = [(m, n) for m, n in matches if m.distance < 0.75 * n.distance]
        
        for match, _ in good_matches:
            img_idx = match.trainIdx
        
            # Get the keypoint coordinates
            x, y = kpts[img_idx].pt
            cv2.circle(image, (int(x), int(y)), 10, (0, 255, 0), 2)

        # Draw matches to an image
        r = cv2.drawMatchesKnn(self.ref, self.kpts, image, kpts, good_matches, None)
        cv2.imshow("R", r)
        return

# Callback method for new roi to initialise the roi tracker
def on_new_roi(roi):
    global tracker, image

    # Top left corner [x0, y0] width and height [x1, y1]
    x0, y0, x1, y1 = roi

    # Slice roi from camera image and init orb tracker
    ref = image[y0: y0 + y1, x0: x0 + x1]
    tracker = ORBTracker(ref_img=ref)
    

if __name__ == "__main__":

    # Create an output window for webcam
    cv2.namedWindow("Webcam")

    # Init null orb tracker
    tracker: ORBTracker = None

    # Init roi selector
    selector = SimpleROISelector("Webcam", on_roi_updated=on_new_roi)

    # Start camera
    cap = cv2.VideoCapture(0)

    # Main processing loop
    while True:

        # Latest webcam image
        ret, image = cap.read()

        # Ensure tracker is initialized before we can track
        if tracker is not None:
            tracker.update(image)

        # Update ux and output result
        selector.update_ux(image)
        cv2.imshow("Webcam", image)

        k = cv2.waitKey(1) &0xFF
        if k == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()



