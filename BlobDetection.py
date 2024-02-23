# First import the library
import pyrealsense2 as rs
import numpy as np
import cv2

webcam = True

# open webcam video stream
if webcam:
    cap = cv2.VideoCapture(0)
    
else:
    # Create the pipeline which handles all connected realsense devices
    pipeline = rs.pipeline()
    
    # Create a configuration object
    config = rs.config()
    
    # Enable some sensors
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)          # Depth map uint16
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)         # Color map uint8 (x3 channels)
    
    # Start the pipeline
    profile = pipeline.start(config)

def create_blob_detector():
    # Parameters object for simple blob detector, and assign parameters
    params = cv2.SimpleBlobDetector_Params()

    # Filter by color
    params.filterByColor = True
    params.blobColor = 0  # Black

    # Threshold (Binary pixel thresholding)
    params.minThreshold = 0
    params.thresholdStep = 10
    params.maxThreshold = 255

    # Filter by Area (number of pixels)
    params.filterByArea = True
    params.minArea = 10*10    # 10x10 pixels
    params.maxArea = 500*500  # 500x500 pixels

    # Filter by Circularity (How circular the blob)
    params.filterByCircularity = True
    params.minCircularity = 0.7  # 0 is not a circle, 1 is a perfect circle

    # Filter by Convexity (Has depressions inside blob, like a non-full moon)
    params.filterByConvexity = False
    params.minConvexity = 0.8

    # Filter by Inertia (Has an axis)
    params.filterByInertia = False
    params.minInertiaRatio = 0.6

    # Create a detector with the parameters
    return cv2.SimpleBlobDetector_create(params)

def detect_blobs(src):

    # Convert color image to grayscale for detector
    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    
    # Detect blobs as keypoints
    kpts = blob_detector.detect(gray)

    # Return blob keypoints
    return kpts

def check_thresholds(src, thresholdStep=20):

    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    
    for th in range(0, 255-thresholdStep, thresholdStep):
        mask = cv2.inRange(gray, th, th+thresholdStep)
        cv2.imshow(str(th) + "-" + str(th+thresholdStep), mask)
    

def draw_blobs(img, kpts):
    return cv2.drawKeypoints(img, kpts, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


# The blob detector object
blob_detector = create_blob_detector()


try:
    while True:
        if webcam:
            # Capture frame-by-frame for computer webcam
            ret, color_image = cap.read()
        
        else:
            # Capture temporal synchronized device data
            frames = pipeline.wait_for_frames()
    
            # Get the needed frames form the frames pipeline
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
    
            # Create a numpy array images
            # A numpy array can be constructed using this protocol with no data marshalling overhead:
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            
        # Detect blobs as keypoints
        kps = detect_blobs(color_image)

        # Draw blobs on image
        color_image = draw_blobs(color_image, kps)

        # Show both images in windows
        cv2.imshow("Color Image", color_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    if webcam:
        # When everything done, release the capture
        cap.release()
    else:
        pipeline.stop()
    # finally, close the window
    cv2.destroyAllWindows()
