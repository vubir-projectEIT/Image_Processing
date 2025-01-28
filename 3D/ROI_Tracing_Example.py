""" IMPORTS """

import numpy as np
import cv2 as cv2
from RealSenseCamera import RealSenseCamera
from ROITracker import ROITracker
from SimpleROISelector import SimpleROISelector


""" MAIN """

if __name__ == '__main__':

    # Create cv2 windows
    window_name = "ROI Tracker Example"
    cv2.namedWindow(window_name)

    # Create all objects
    camera = RealSenseCamera()                 # Instantiate camera device
    tracker = ROITracker()                     # Instantiate roi tracker
    selector = SimpleROISelector(window_name)  # Instantiate roi selector

    # Control flags
    intrinsics_set = False

    # Start the camera
    camera.start_async()

    # Main loop
    while camera.is_alive:

        # Get the latest image frame (this is blocking!)
        frame = camera.get_latest_frame()
        color_image = frame.color_map
        depth_image = frame.depth_map

        # Ensure the camera intrinsics passed to the tracker (this is required for 3D deprojeciton)
        if not intrinsics_set:
            tracker.intrinsics = camera.color_intrinsics
            tracker.depth_scale = camera.depth_scale
            intrinsics_set = True

        # Check if there is a new roi to track
        if selector.is_new_roi:
            tracker.init_roi(selector.roi)

        # Update tracker and get latest point (pt == [0,0,0] if not initialize with an roi)
        tracker.update_tracker(color_image, depth_image)
        pt = tracker.position_3d

        # We only care about the pt if the tracker is actually initialized with an roi
        if tracker.initialized:

            # The point returned is either the measured or predicted position
            if tracker.tracked:
                print(f"Tracked POS= [{pt[0]:.2f}, {pt[1]:.2f}, {pt[2]:.2f}] at ROI={tracker.predicted_roi}")
            else:
                print(f"Predicted POS= [{pt[0]:.2f}, {pt[1]:.2f}, {pt[2]:.2f}] at ROI={tracker.predicted_roi}")

        # Update ux after image processing tasks
        tracker.update_ux(color_image)
        selector.update_ux(color_image)

        # Apply colormap to depth data (optional) and update image windows
        depth_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        cv2.imshow(window_name, np.hstack((color_image, depth_image)))
        cv2.waitKey(1)
