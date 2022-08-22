import mss
import numpy as np
import keyboard
from time import sleep


class Screen(object):
    def __init__(self):
        ...

    def grab(self, x, y, w, h) -> np.array:
        with mss.mss() as sct:
            monitor: dict = {"top": y, "left": x, "width": w, "height": h}
            img_array: np.array = np.array(sct.grab(monitor))
            return img_array

    def make_screenshot(self, secs_between_screenshots: int = 10) -> None:
        while True:
            keyboard.press_and_release('F12')
            sleep(secs_between_screenshots)
