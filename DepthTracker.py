# First import the library
import pyrealsense2 as rs
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Create the pipeline which handles all connected realsense devices
pipeline = rs.pipeline()

# Create a configuration object
config = rs.config()

# Enable some sensors
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)          # Depth map uint16
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)         # Color map uint8 (x3 channels)

# Start the pipeline
profile = pipeline.start(config)

# Get the scale of the depth camera
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

# Load the cascade
cascade_dir = r"/Users/loris/anaconda3/envs/EIT_project/lib/python3.11/site-packages/cv2/data"
face_cascade = cv2.CascadeClassifier(cascade_dir + r"/haarcascade_frontalface_default.xml")

# List of post processing filters
filters = [rs.disparity_transform(),
           rs.spatial_filter(),
           rs.temporal_filter(),
           rs.disparity_transform(False)]

# Define some cv2 windows so that we can control how we present images
cv2.namedWindow("Color Image", cv2.WINDOW_NORMAL)
cv2.namedWindow("Depth ColorMap", cv2.WINDOW_NORMAL)
cv2.namedWindow("Depth ROI", cv2.WINDOW_NORMAL)


def ProcessData(color, depth, depth_color, color_intrinsic, depth_intrinsic):

    # Convert to grayscale
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

    # Calculate keypoints from face detector
    keypoints = face_cascade.detectMultiScale(gray, minNeighbors=8)

    # Return if there are no keypoints
    if len(keypoints) == 0:
        return

    # Use first keypoint.
    # Indexes x (column) and y (row) are top left corner of bounding box, w (width) and h (height) are its size
    x, y, w, h = keypoints[0]

    # Get the dimensions of the image
    height, width = depth.shape

    # Draw a bounding box around the face on the color image
    # Calculate limits to ensure the box is always inside the image... Not necessary for this box because bounding
    # from the face detector is always in the image, but the practice is useful for other cases
    x1 = max(x, 0)
    y1 = max(y, 0)
    x2 = min(x + w, width)
    y2 = min(y + h, height)
    cv2.rectangle(color, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Center of the face in image [u,v] from bounding box
    # Other centroid methods exist, eg. image moments, gaussian fitting, circle fitting to name a few
    u = x + 0.5 * w
    v = y + 0.5 * h

    # Draw a small circle on the color image indicating [u,v]
    cv2.circle(color, (int(u), int(v)), 5, (0, 0, 255))

    # Define a region of interest from the middle 50% of the bounding box
    ratio = 0.50
    x1 = max(int(u - ratio * 0.5 * w), 0)
    y1 = max(int(v - ratio * 0.5 * h), 0)
    x2 = min(int(u + ratio * 0.5 * w), width)
    y2 = min(int(v + ratio * 0.5 * h), height)
    cv2.rectangle(color, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.rectangle(depth_color, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Use the central bounding box to extract region of interest from depth image
    roi_depth = depth[y1:y2, x1:x2]

    # Return if the ROI is empty
    if roi_depth.size == 0:
        return

    # Create a depth roi_depth colormap for visual debugging
    roi_colorMap = cv2.applyColorMap(cv2.convertScaleAbs(roi_depth, alpha=0.03), cv2.COLORMAP_JET)
    cv2.imshow("Depth ROI", roi_colorMap)

    # Distance is mean of roi_depth
    distance = roi_depth.mean()

    # Return if distance to the face is not a finite number.
    if not np.isfinite(distance):
        return

    # Ensure the distance is meters, then scale to millimeters.
    # Some RealSense cameras report distance values in odd units (1/32 meter)
    # The D435 series of cameras already report in millimeters, but the practice is good.
    distance *= depth_scale * 1000

    # 2D pixel to 3D point using sensor intrinsics pixel position and distance
    point = rs.rs2_deproject_pixel_to_point(depth_intrinsic, [u, v], distance)

    # Project the 3D point back to 2D pixel to verify everything worked
    px = rs.rs2_project_point_to_pixel(color_intrinsic, point)

    # Return if the projected 3D point it not finite
    if not all([np.isfinite(p) for p in px]):
        return

    # Draw the projected point as a cross. This should align with the earlier [u,v] circle
    cv2.drawMarker(color, (int(px[0]), int(px[1])), (0,0,255), cv2.MARKER_CROSS, 20, 1)

    # Log results to the console
    pos_string = f"[{int(point[0])}, {int(point[1])}, {int(point[2])}]mm"
    dist_string = f"{int(distance)}mm"
    print(f"Face found at: {pos_string}, at a distance of {dist_string}")

    # Print the data to the source image
    row, col = color.shape[0] - 30, 5
    for string in [f"Distance: {dist_string}", f"Position: {pos_string}"]:
        cv2.putText(img=color,
                    text=string,
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    org=(col, row),
                    fontScale=1.1,
                    color=(255, 255, 255),
                    lineType=cv2.LINE_8)
        row += 20

    # Note: For any serious application, filtering should be done. A Kalman filter or alpha-beta filter
    # would drastically improve quality of the tracked face position over time, though at the cost of latency.

    # Pressing 'q' will pause processing and plot any image using matplotlib for inspection
    if cv2.waitKey(1) & 0xFF == ord('q'):
        plt.imshow(roi_colorMap)
        plt.show()


try:
    while True:
        # Get frames and align
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        # Get aligned frames
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Postprocessing filters
        for f in filters:
            depth_frame = f.process(depth_frame)

        # Grab new intrinsics (may be changed by decimation)
        depth_intrinsics = rs.video_stream_profile(depth_frame.profile).get_intrinsics()
        color_intrinsics = rs.video_stream_profile(color_frame.profile).get_intrinsics()

        # Create a numpy array images using this protocol with no data marshalling overhead:
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap to depth data (optional)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Perform data processing here
        ProcessData(color_image, depth_image, depth_colormap, depth_intrinsics, color_intrinsics)

        # Show the source images always, even if no faces were found
        cv2.imshow("Color Image", color_image)
        cv2.imshow("Depth ColorMap", depth_colormap)
        cv2.waitKey(1)


finally:
    pipeline.stop()


