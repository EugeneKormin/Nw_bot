@staticmethod
def __empty(_):
    ...

cv2.namedWindow("trackBars")
cv2.resizeWindow("trackBars", 640, 240)
cv2.createTrackbar("h min", 'trackBars', 0, 255, empty)
cv2.createTrackbar("h max", 'trackBars', 255, 255, empty)
cv2.createTrackbar("s min", 'trackBars', 0, 255, empty)
cv2.createTrackbar("s max", 'trackBars', 255, 255, empty)
cv2.createTrackbar("v min", 'trackBars', 0, 255, empty)
cv2.createTrackbar("v max", 'trackBars', 255, 255, empty)

h_min = cv2.getTrackbarPos("h min", 'trackBars')
h_max = cv2.getTrackbarPos("h max", 'trackBars')
s_min = cv2.getTrackbarPos("s min", 'trackBars')
s_max = cv2.getTrackbarPos("s max", 'trackBars')
v_min = cv2.getTrackbarPos("v min", 'trackBars')
v_max = cv2.getTrackbarPos("v max", 'trackBars')
hsv_canvas = cv2.cv2tColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([h_min, s_min, v_min])
upper = np.array([h_max, s_max, v_max])
mask = cv2.inRange(hsv_canvas, lower, upper)
