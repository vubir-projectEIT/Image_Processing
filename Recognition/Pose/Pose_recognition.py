import cv2
import mediapipe as mp
import time

from mediapipe.framework.formats import landmark_pb2

DRAW = mp.solutions.drawing_utils
POSE_CONNECTIONS = mp.solutions.pose.POSE_CONNECTIONS
STYLE = mp.solutions.drawing_styles.get_default_pose_landmarks_style()

from CameraStream import CameraStream  # get this module from Utilities/Efficiency/CameraStream.py


# Pose Landmarker

def create_landmarker(model="pose_landmarker_lite.task"):

    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseOptions = mp.tasks.vision.PoseLandmarkerOptions
    RunningMode = mp.tasks.vision.RunningMode

    latest = {"result": None}

    def callback(result, image, timestamp):
        latest["result"] = result

    options = PoseOptions(
        base_options=BaseOptions(model_asset_path=model),
        running_mode=RunningMode.LIVE_STREAM,
        result_callback=callback
    )

    landmarker = PoseLandmarker.create_from_options(options)

    return landmarker, latest


# Draw function

def draw_landmarks(frame, result, connections=False):

    if not result or not result.pose_landmarks:
        return frame

    for pose_landmarks in result.pose_landmarks:

        proto = landmark_pb2.NormalizedLandmarkList()
        proto.landmark.extend(
            landmark_pb2.NormalizedLandmark(x=l.x, y=l.y, z=l.z)
            for l in pose_landmarks
        )
        if connections:
            DRAW.draw_landmarks(
                frame,
                proto,
                POSE_CONNECTIONS,
                STYLE
            )
        else:
            DRAW.draw_landmarks(frame, proto)

    return frame


if __name__ == "__main__":

    # Create the camera stream and the pose landmarker
    cam = CameraStream(0)
    landmarker, latest = create_landmarker()

    # Initialize variables for efficient frame processing
    reduction = 2   
    frame_counter = 0
    inference_interval = 2

    while True:

        frame = cam.read()
        if frame is None:
            continue

        # Run inference every N frames
        if frame_counter % inference_interval == 0:
            # Reduce the frame size for faster inference
            reduced = cv2.resize(frame, None, fx=1 / reduction, fy=1 / reduction)
            # Convert BGR to RGB for Mediapipe
            rgb = cv2.cvtColor(reduced, cv2.COLOR_BGR2RGB)
            # Create a Mediapipe Image object from the RGB frame
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            # Run the pose landmarker asynchronously on the reduced RGB frame
            landmarker.detect_async(mp_image, int(time.perf_counter()*1000))

        # Get the latest result and draw the landmarks on the original frame
        result = latest["result"]
        frame = draw_landmarks(frame, result)

        cv2.imshow("Pose", frame)

        frame_counter += 1
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.stop()
    cv2.destroyAllWindows()