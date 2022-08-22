import cv2 as cv
import numpy as np


class Opencv2(object):
    def __init__(self):
        ...

    def __match_template(self, canvas, sample):
        match = cv.matchTemplate(canvas, sample, cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(match)
        return max_val, max_loc

    def detect_drop(self, threshold: float, canvas) -> bool:
        # filters for drop detection

        max_val, max_loc = self.__match_template(
            canvas=canvas,
            sample=cv.imread(r'images/drop_samples/drop_1.png', cv.IMREAD_UNCHANGED)
        )

        if max_val > threshold:
            return True
        return False

    def detect_hook(self, threshold: float, canvas) -> bool:
        # filters for drop detection

        max_val, max_loc = self.__match_template(
            canvas=canvas,
            sample=cv.imread(r'images/hook_samples/hook.png', cv.IMREAD_UNCHANGED)
        )

        if max_val > threshold:
            return True
        return False

    def detect_pull(self, threshold: float, canvas) -> bool:
        hsv_canvas = cv.cvtColor(canvas, cv.COLOR_BGR2HSV)
        lower = np.array([70, 170, 60])
        upper = np.array([90, 255, 255])
        mask = cv.inRange(hsv_canvas, lower, upper)

        max_val, max_loc = self.__match_template(
            canvas=canvas,
            sample=cv.imread(r'images/pull_samples/pull.png', cv.IMREAD_UNCHANGED)
        )

        if max_val > threshold:
            return True
        return False

    def detect_release(self, threshold: float, canvas) -> bool:
        # filters for drop detection

        max_val, max_loc = self.__match_template(
            canvas=canvas,
            sample=cv.imread(r'images/release_samples/release.png', cv.IMREAD_UNCHANGED)
        )

        if max_val > threshold:
            return True
        return False


