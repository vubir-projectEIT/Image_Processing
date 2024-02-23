import numpy as np
import cv2 as cv2

class ROIFilter:

    def __init__(self):

        # Kalman filter
        self.n = 0
        states = 6          # [x, y, vx, vy, w, h]
        observables = 4     # [x, y, w, h]
        self.filter = cv2.KalmanFilter(states, observables)
        self.reset()

    def step(self, *args):

        if self.n > 0:
            # Update kf
            p = np.asarray([[args[0]], [args[1]], [args[2]], [args[3]]], np.float32)
            self.filter.correct(p)
            p = self.filter.predict()
        else:
            # Init kf
            p = np.asarray([[args[0]], [args[1]], [0], [0], [args[2]], [args[3]]], np.float32)
            self.filter.statePre = p
            self.filter.statePost = p

        self.n += 1
        return tuple([x for x in p[:, 0]])

    def predict(self):

        # Need a sample to predict
        if self.n > 0:
            p = self.filter.predict()
        else:
            p = np.array([[-1], [-1], [-1], [-1], [-1]], np.float32)

        return tuple([round(x) for x in p[:, 0]])


    def correct(self, *args):

        if self.n > 0:
            # Update kf
            p = np.asarray([[args[0]], [args[1]], [args[2]], [args[3]]], np.float32)
            self.filter.correct(p)
        else:
            # Init kf
            p = np.asarray([[args[0]], [args[1]], [0], [0], [args[2]], [args[3]]], np.float32)
            self.filter.statePre = p
            self.filter.statePost = p

        self.n += 1


    def reset(self):

        self.n = 0

        self.filter.measurementMatrix = np.array([[1, 0, 0, 0, 0, 0],
                                                  [0, 1, 0, 0, 0, 0],
                                                  [0, 0, 0, 0, 1, 0],
                                                  [0, 0, 0, 0, 0, 1]], np.float32)

        self.filter.transitionMatrix = np.array([[1, 0, 1, 0, 0, 0],
                                                 [0, 1, 0, 1, 0, 0],
                                                 [0, 0, 1, 0, 0, 0],
                                                 [0, 0, 0, 1, 0, 0],
                                                 [0, 0, 0, 0, 1, 0],
                                                 [0, 0, 0, 0, 0, 1]], np.float32)

        pn = 0.03  # 0.17 [any]
        self.filter.processNoiseCov = np.array([[pn, 0, 0, 0, 0, 0],
                                                [0, pn, 0, 0, 0, 0],
                                                [0, 0, pn, 0, 0, 0],
                                                [0, 0, 0, pn, 0, 0],
                                                [0, 0, 0, 0, pn, 0],
                                                [0, 0, 0, 0, 0, pn]], np.float32)

        nx, ny = 2, 2    # 1.4 [px]
        nw, nh = 25, 25  # 5 [mm]
        self.filter.measurementNoiseCov = np.array([[nx, 0, 0, 0],
                                                    [0, ny, 0, 0],
                                                    [0, 0, nw, 0],
                                                    [0, 0, 0, nh]], np.float32)
