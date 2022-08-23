from win32gui import GetWindowRect
from ctypes import windll
import numpy as np
import keyboard
import cv2 as cv
from time import sleep

from Screen import Screen
from Opencv import Opencv


def empty(_):
    ...


def main():
    opencv: Opencv = Opencv()

    no_fishing: bool = True
    waiting: bool = False
    hooking: bool = False

    while True:
        hwnd: int = windll.user32.FindWindowW(0, "New World")
        rect: tuple = GetWindowRect(hwnd)
        RECT_X: int = rect[0]
        RECT_Y: int = rect[1]
        RECT_W: int = rect[2]
        RECT_H: int = rect[3]

        screen: Screen = Screen()
        img: np.array = screen.grab(x=RECT_X, y=RECT_Y, w=RECT_W, h=RECT_H)

        if no_fishing:
            if opencv.detect(canvas=img, THRESHOLD=.6, PATH=r'images/drop_samples/drop.png'):
                keyboard.press_and_release('space')
                no_fishing: bool = False
                waiting: bool = True
                print('drop')
            else:
                ...

        if waiting:
            if opencv.detect(canvas=img, THRESHOLD=.8, PATH=r'images/hook_samples/hook.png'):
                keyboard.press_and_release("space")
                waiting: bool = False
                hooking: bool = True
                print('clicked')

        if hooking:
            max_val, max_loc = opencv.detect_pull(canvas=img, THRESHOLD=.9, PATH=r'images/circle_samples/circle.png')

            img_sample: np.array = cv.imread(r'images/circle_samples/circle.png')
    
            X: int = max_loc[0]+5
            Y: int = max_loc[1]+15
            W: int = img_sample.shape[0]//2
            H: int = img_sample.shape[1]//2-2

            start: tuple = (X, Y)
            end: tuple = (X+W, Y+H)

            image = cv.rectangle(img.copy(), start, end, (255, 0, 0), 2)
            image = cv.circle(image, (X+W//2, Y+H//2), 1, (0, 255, 0), 3)

            try:
                color = img[X+W//2, Y+H//2]
                print(color)
                if color[0] <= 100:
                    ...
                    #keyboard.press('space')

                elif color[0] > 100:
                    ...
                    #keyboard.release('space')
            except IndexError:
                ...

            cv.imshow('test', image)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    main()
