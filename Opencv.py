import cv2 as cv
import numpy as np


class Opencv(object):
    def __init__(self):
        ...

    @staticmethod
    def __match_template(canvas: np.array, PATH: str):
        match = cv.matchTemplate(
            canvas,
            cv.imread(PATH, cv.IMREAD_UNCHANGED),
            cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(match)
        return max_val, max_loc

    def detect(self, canvas: np.array, PATH: str, THRESHOLD: float = .7) -> bool:
        max_val, _ = self.__match_template(
            canvas=canvas,
            PATH=PATH
        )
        if max_val > THRESHOLD:
            return True
        return False

    def detect_pull(self, canvas: np.array, PATH: str, THRESHOLD: float) -> tuple:
        max_val, max_loc = self.__match_template(
            canvas=canvas,
            PATH=PATH
        )
        return max_val, max_loc
