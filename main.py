from win32gui import GetWindowRect
from ctypes import windll
import numpy as np
import cv2 as cv
import keyboard
import pyautogui
from time import sleep

from Screen import Screen
from Opencv import Opencv2


def empty(a):
    ...


def main():
    opencv = Opencv2()
    cv.namedWindow("trackBars")
    cv.resizeWindow("trackBars", 640, 240)
    cv.createTrackbar("h min", 'trackBars', 0, 179, empty)
    cv.createTrackbar("h max", 'trackBars', 179, 179, empty)
    cv.createTrackbar("s min", 'trackBars', 0, 255, empty)
    cv.createTrackbar("s max", 'trackBars', 255, 255, empty)
    cv.createTrackbar("v min", 'trackBars', 0, 255, empty)
    cv.createTrackbar("v max", 'trackBars', 255, 255, empty)

    while True:
        hwnd: int = windll.user32.FindWindowW(0, "New World")
        rect: tuple = GetWindowRect(hwnd)
        x: int = rect[0]
        y: int = rect[1]
        w: int = rect[2]
        h: int = rect[3]

        screen: Screen = Screen()
        img: np.array = screen.grab(x=x, y=y, w=w, h=h)

        #img = cv.imread('images/20220822181135_1.jpg')

        hsv_canvas = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        h_min = cv.getTrackbarPos("h min", 'trackBars')
        h_max = cv.getTrackbarPos("h max", 'trackBars')
        s_min = cv.getTrackbarPos("s min", 'trackBars')
        s_max = cv.getTrackbarPos("s max", 'trackBars')
        v_min = cv.getTrackbarPos("v min", 'trackBars')
        v_max = cv.getTrackbarPos("v max", 'trackBars')
        hsv_canvas = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower = np.array([70, 170, 60])
        upper = np.array([90, 255, 255])
        mask = cv.inRange(hsv_canvas, lower, upper)

        if opencv.detect_hook(.9, canvas=img):
            keyboard.press_and_release("space")
            print('clicked')

        while opencv.detect_pull(.8, canvas=img):
            print('press_space_button')

        '''


        opencv.set_canvas(canvas=img)
        


        if opencv.detect_release(.8):
            print('release_mouse_button')
        '''
        cv.imshow("test", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break



if __name__ == '__main__':
    main()
