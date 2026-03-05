import cv2
from PIL import Image
import numpy as np

from transformers import pipeline       # pip install -q -U transformers
from accelerate import Accelerator      # pip install accelerate

device = Accelerator().device
checkpoint = "depth-anything/Depth-Anything-V2-base-hf"
pipe = pipeline("depth-estimation", model=checkpoint, device=device)

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)

    while cap.isOpened():

        ret, frame = cap.read()

        if ret:
            downsampled_frame = cv2.resize(frame, (frame.shape[1]//10, frame.shape[0]//10), interpolation=cv2.INTER_CUBIC)
            downsampled_frame = cv2.cvtColor(downsampled_frame, cv2.COLOR_BGR2RGB)
            downsampled_frame = Image.fromarray(downsampled_frame)
            depth_prediction = pipe(downsampled_frame)
            depth_prediction = np.asarray(depth_prediction["depth"])
            upsampled_depth = cv2.resize(depth_prediction, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_CUBIC)
            mask = upsampled_depth/255 > 0.4
            masked_frame = (frame.astype(np.float32) * mask[..., None]).astype(np.uint8)
            cv2.imshow('Depth', masked_frame)

        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
