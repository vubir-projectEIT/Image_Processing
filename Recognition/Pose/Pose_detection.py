""" IMPORTS """

import time
import cv2              # copy the following in your console: pip install opencv-contrib-python
import numpy as np      # copy the following in your console: conda install numpy

import mediapipe as mp  # copy the following in your console: pip install mediapipe
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


""" FUNCTIONS """

def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks

  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks])
    solutions.drawing_utils.draw_landmarks(rgb_image, pose_landmarks_proto, solutions.pose.POSE_CONNECTIONS, solutions.drawing_styles.get_default_pose_landmarks_style())

  return rgb_image

def create_pose_landmarker(model_path = 'pose_landmarker_lite.task'):

    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    result_list = []

    def save_result(result: vision.GestureRecognizerResult, unused_output_image: mp.Image, timestamp_ms: int):
        result_list.append(result)

    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=save_result)

    pose_landmarker = PoseLandmarker.create_from_options(options)

    return result_list, pose_landmarker


""" MAIN """

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    result_list, pose_landmarker = create_pose_landmarker()

    while cap.isOpened():

        _, frame = cap.read()
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        pose_landmarker.detect_async(mp_image, time.time_ns()//1000000)
        if result_list:
            results = result_list[0]
            result_list.clear()
            frame = draw_landmarks_on_image(frame, results)

        cv2.imshow("Pose", frame)

        k = cv2.waitKey(int(1000/24)) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()