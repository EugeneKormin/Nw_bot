from win32gui import GetWindowRect
from ctypes import windll
import numpy as np
import cv2 as cv
import keyboard
from time import sleep

from Screen import Screen
from Opencv import Opencv


def empty(a):
    ...


def main():
    opencv = Opencv()
    while True:
        hwnd: int = windll.user32.FindWindowW(0, "New World")
        rect: tuple = GetWindowRect(hwnd)
        x: int = rect[0]
        y: int = rect[1]
        w: int = rect[2]
        h: int = rect[3]

        screen: Screen = Screen()
        img: np.array = screen.grab(x=x, y=y, w=w, h=h)

        """
        circles = cv.HoughCircles(img_gray, cv.HOUGH_GRADIENT, 1, img_gray.shape[0] / 8,
                                   param1=100, param2=60,
                                   minRadius=30, maxRadius=300)

        res = np.zeros(img.shape)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv.circle(res, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv.circle(res, center, radius, (255, 0, 255), 3)
        """

        if opencv.detect_hook(canvas=img, THRESHOLD=.9, PATH=r'images/hook_samples/hook.png'):
            keyboard.press_and_release("space")
            print('clicked')

        max_val, max_loc = opencv.detect_pull(canvas=img, THRESHOLD=.7, PATH=r'images/circle_samples/circle.png')
        '''
        sleep(1)
        if not keyboard.is_pressed('space'):
            keyboard.press('space')
        '''

        if opencv.detect_release(canvas=img):
            sleep(1)
            keyboard.release('space')

        if opencv.detect_drop(canvas=img, THRESHOLD=.8, PATH=r'images/drop_samples/drop_1.png') & \
                opencv.is_hotspot_in_front(canvas=img):
            keyboard.press_and_release('space')

        x = max_loc[0]+5
        y = max_loc[1]+15

        img_sample = cv.imread(r'images/circle_samples/circle.png')
        w = img_sample.shape[0]//2
        h = img_sample.shape[1]//2-2

        start = (x, y)
        end = (x+w, y+h)

        blurred_image = cv.GaussianBlur(img, (13, 13), 0)

        image = cv.rectangle(blurred_image, start, end, (255, 0, 0), 2)

        cv.circle(image, (x+w//2, y+h//2), 1, (0, 255, 0), 3)

        hsv_canvas = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower = np.array([76, 127, 20])
        upper = np.array([179, 255, 255])
        mask = cv.inRange(hsv_canvas, lower, upper)

        res = cv.bitwise_not(img, mask)

        color = blurred_image[x+w//2, y+h//2]
        print(color)

        cv.imshow("test", res)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
