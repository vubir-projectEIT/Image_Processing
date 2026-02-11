""" IMPORTS """

import cv2 as cv2
import numpy as np
from KalmanROI import ROIFilter


""" FUNCTIONS """

def property_set(f):
    """ Decorator for set only property """
    return property(None, f)


""" CLASS """

class ROITracker:
    """ Object tracker using RGB-D data and an initial region of interest.
        Must call 'init' method passing a valid roi """

    def __init__(self, *args, **kwargs):

        self.__tracker = cv2.TrackerKCF()       # The roi tracker
        self.__roi = None                       # Measured roi from roi tracker
        self.__predicted_roi = None             # Predicted roi from kalman filter
        self.__pos_3d = np.array([0, 0, 0])     # The latest 3D
        self.__camera_matrix = None             # Color sensor's camera matrix
        self.__distortion_coeff = None          # Color sensor's distortion coefficients
        self.__depth_scale = 1                  # Scale factor of depth data to mm
        self.__tracked = False                  # Latest state of tracking
        self.__initialized = False              # Flag for tracker initialized
        self.__verbose = False                  # Flag for verbose mode
        self.__filter = ROIFilter()             # A filter object to manage roi tracking

        # Define custom kcf tracker parameters
        self.__tracker_params = cv2.TrackerKCF_Params()

    def init_roi(self, roi):
        """ Initialise tracking with a given roi """
        self.__roi = roi
        self.__filter.reset()
        self.__initialized = False

    def update_ux(self, color_map):
        """ Draws latest tracking information onto the color map """

        if self.__initialized and self.__predicted_roi:
            # Draw the predicted bounding box
            p1 = (self.__predicted_roi[0], self.__predicted_roi[1])
            p2 = (self.__predicted_roi[0] + self.__predicted_roi[2], self.__predicted_roi[1] + self.__predicted_roi[3])
            cv2.rectangle(color_map, p1, p2, (255, 0, 255), 2, 1)

        if self.__tracked and self.__roi:
            # Draw the measured bounding box
            p1 = (self.__roi[0], self.__roi[1])
            p2 = (self.__roi[0] + self.__roi[2], self.__roi[1] + self.__roi[3])
            cv2.rectangle(color_map, p1, p2, (255, 255, 255), 2, 1)

        if not self.__initialized:
            # Notify initialization
            cv2.putText(color_map, "Indicate an ROI to track", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        elif not self.__tracked:
            # Notify initialization
            cv2.putText(color_map, "Tracking lost", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    def update_tracker(self, color_map, depth_map):
        """ Updated the tracking pipeline """

        self.__tracking_pipeline(color_map, depth_map)
        return self.__tracked

    def __tracking_pipeline(self, color_map, depth_map):
        """ Updates the tracker and returns the result """

        # An initial roi must be defined and tracker initialized
        if self.__roi is None:
            return
        elif not self.__initialized:
            self.__tracker: cv2.TrackerKCF = cv2.TrackerKCF_create()
            self.__tracker.init(color_map, self.__roi)
            self.__initialized = True

        # Predict roi [x,y,vx,vy,w,h]
        predicted_roi = self.__filter.predict() if self.__filter.n > 0 else None
        predicted_roi = tuple([predicted_roi[i] for i in [0, 1, 4, 5]]) if predicted_roi else None

        # Update tracking pipeline
        tracked, new_roi = self.__tracker.update(color_map)

        # Update filter
        if tracked:
            self.__filter.correct(*new_roi)
            roi = new_roi
        else:
            roi = predicted_roi

        # Get the distance to roi from depth map and project to 3D
        if d := self.__distance_to_roi(roi, depth_map):
            x = roi[0] + 0.5 * roi[2]
            y = roi[1] + 0.5 * roi[3]
            self.__pos_3d = self.__pixel_to_point((x, y), d)

        # Update state
        self.__predicted_roi = predicted_roi
        self.__tracked = tracked
        self.__roi = new_roi

    def __distance_to_roi(self, roi, depth_image):
        """ Returns the median distance to the roi """

        # Ensure a depth image
        if depth_image is None:
            return 0

        # Round roi to pixels
        x = round(roi[0])
        y = round(roi[1])
        w = round(roi[2])
        h = round(roi[3])
        r = round((w + h) * 0.335)  # Radius is 2/3 the mean roi size

        # Create circular mask
        depth_roi = depth_image[y:y+h, x:x+w]
        mask = np.ones(depth_roi.shape)
        cv2.circle(mask, (int(w / 2), int(h / 2)), r, 0, -1)
        masked = np.ma.masked_array(depth_roi, mask=mask)

        # Median of masked depth image
        d = np.ma.median(masked)
        d *= self.__depth_scale

        return d

    def __pixel_to_point(self, uv, d):
        """ Unproject an image uv coords to sensor 3D coords """

        # Undistort and scale (openCV)
        # pt = np.asarray(uv)
        # ux, uy = cv2.undistortPoints(pt, self.__camera_matrix, self.__distortion_coeff).squeeze()
        # x = ux * d
        # y = uy * d
        # z = d

        # Ensure camera parameters are set
        if self.__camera_matrix is None or self.__distortion_coeff is None:
            return np.array([-1, -1, -1])

        # Camera model
        cx = self.__camera_matrix[0, 2]
        cy = self.__camera_matrix[1, 2]
        fx = self.__camera_matrix[0, 0]
        fy = self.__camera_matrix[1, 1]
        c0, c1, c2, c3, c4 = self.__distortion_coeff

        # Undistort using inverse Brown Conrady model
        x = (uv[0] - cx) / fx
        y = (uv[1] - cy) / fy
        r2 = x * x + y * y
        f = 1 + c0 * r2 + c1 * r2 * r2 + c4 * r2 * r2 * r2
        ux = x * f + 2 * c2 * x * y + c3 * (r2 + 2 * x * x)
        uy = y * f + 2 * c3 * x * y + c2 * (r2 + 2 * y * y)

        # Scale by distance
        x = d * ux
        y = d * uy
        z = d
        pt = np.array([x, y, z])

        return pt

    @property
    def position_3d(self):
        return self.__pos_3d

    @property
    def tracked(self):
        return self.__tracked

    @property
    def initialized(self):
        return self.__initialized

    @property_set
    def intrinsics(self, args):

        if len(args) != 2:
            raise AssertionError(f"expected 2 arguments, got {len(args)}")
        elif any([not isinstance(x, np.ndarray) for x in args]):
            raise TypeError(f"expected {tuple([type(np.ndarray) for _ in args])}, got {tuple([type(x) for x in args])}")

        self.__camera_matrix = args[0]
        self.__distortion_coeff = args[1]

    @property_set
    def depth_scale(self, value):

        if not isinstance(value, (float, int)):
            raise TypeError(f"expected [{float}, {int}], got {type(value)}")

        self.__depth_scale = value

    @property_set
    def verbose(self, value):
        if isinstance(value, bool):
            self.__verbose = value
        else:
            raise TypeError(f"expected {bool}, got {type(value)}")

    @property
    def predicted_roi(self):
        return self.__predicted_roi

    @property
    def measured_roi(self):
        return self.__roi
