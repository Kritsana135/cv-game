from src.HitBallGame import HitBallGame
from threading import Thread
from queue import Queue
import cv2
import imutils
import math


def load_vdo(path_vdo):
    return cv2.VideoCapture(path_vdo)


def bgr2hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def mask_set(hsv, red_Lower, red_Upper):
    mask = cv2.inRange(hsv, red_Lower, red_Upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    return mask


def contours_img(mask):
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    return contours


class screenSize:
    h = 0
    w = 0
    hr = 0
    wr = 0
    halfL = 0
    halfR = 0
    r = 0

    def __init__(self, h, w, r, half):
        self.h = h
        self.w = w
        self.r = r
        self.hr = int(h/r)
        self.wr = int(w/r)
        self.halfL = int(self.wr*half)
        self.halfR = int(self.wr*(half+1))

    def printData(self):
        print("Width X : ", self.w)
        print("Height Y : ", self.h)
        print("1 / ", self.r, " Width  : ", self.wr)
        print("1 / ", self.r, " Height : ", self.hr)
        print("Half Left : ", self.halfL)
        print("Half Right : ", self.halfR)


class position:
    x = 0
    y = 0

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y


video = './videos/2ball3.mp4'
# video = 'vdo/ballonthewall2.mp4'

cap = load_vdo(video)

# color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
#               'white': [[180, 18, 255], [0, 0, 231]],
#               'red1': [[180, 255, 255], [159, 50, 70]],
#               'red2': [[9, 255, 255], [0, 50, 70]],
#               'green': [[89, 255, 255], [36, 50, 70]],
#               'blue': [[128, 255, 255], [90, 50, 70]],
#               'yellow': [[35, 255, 255], [25, 50, 70]],
#               'purple': [[158, 255, 255], [129, 50, 70]],
#               'orange': [[24, 255, 255], [10, 50, 70]],
#               'gray': [[180, 18, 230], [0, 0, 40]]}

yellow_Lower = (25, 50, 70)
yellow_Upper = (35, 255, 255)
# 'yellow': [[35, 255, 255], [25, 50, 70]],

red_Lower = (0, 50, 70)
red_Upper = (9, 255, 255)
# red2': [[9, 255, 255], [0, 50, 70]],

purple_Lower = (129, 50, 70)
purple_Upper = (158, 255, 255)
# 'purple': [[158, 255, 255], [129, 50, 70]],

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

ret, first_frame = cap.read()

screen = screenSize(int(cap.get(4)), int(cap.get(3)), 9, 4)

# Create Game class
game = HitBallGame(maxPoint=5, between=screen.halfR-screen.halfL,
                   screenHeight=screen.h-(screen.hr*2), screenWidth=screen.w-(screen.wr*2))

screen.printData()

left_pos = position()
right_pos = position()

font = cv2.FONT_HERSHEY_PLAIN


def loop_cv(out_q):
    while(cap.isOpened()):
        ret, frame = cap.read()
        # out_q.put((1, 1, "CENTER"))

        if ret == True:

            # Press Q on keyboard to  exit
            key = cv2.waitKey(60)
            if key == ord('q'):
                break

            frame_L = frame[screen.hr:screen.h -
                            screen.hr, screen.wr:screen.halfL]
            frame_R = frame[screen.hr:screen.h - screen.hr,
                            screen.halfR:screen.w - screen.wr]

            ######################################################################
            # L

            blurred = cv2.GaussianBlur(frame_L, (11, 11), 0)
            hsv = bgr2hsv(blurred)

            mask = mask_set(hsv, purple_Lower, purple_Upper)
            # find contours in the mask and initialize the current
            contours = contours_img(mask)

            # (x, y) center of the ball
            center = None
            x = 0
            y = 0
            distance = 0

            if len(contours) > 0:

                c = max(contours, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.putText(frame_L, "x: " + str(x) + " y: " + str(y),
                            (10, 60), font, 1.5, (0, 0, 255), 2)

                if radius > 10:
                    cv2.circle(frame_L, (int(x), int(y)),
                               int(radius), (0, 255, 255), 2)
                    cv2.circle(frame_L, center, 5, (128, 0, 128), -1)

                ##############
                if left_pos.x != 0.0 and left_pos.y != 0.0:
                    distance = math.sqrt(
                        ((left_pos.x-x)**2)+((left_pos.y-y)**2))
                    cv2.putText(frame_L, "distance: " + str(distance),
                                (10, 90), font, 1.5, (0, 0, 255), 2)

                    if distance < 20:
                        out_q.put((int(x), int(y), "LEFT"))
                        cv2.putText(frame, "HIT LEFT!!", (screen.wr, 50),
                                    font, 2.5, (0, 0, 255), 3)
                        # cv2.putText(frame_L, "x: " + str(x) + " y: " + str(y) , (10,60), font, 1.5, (0,0,255), 2)

            left_pos.setX(x)
            left_pos.setY(y)

            #######
            ######################################################################
            # R

            blurred = cv2.GaussianBlur(frame_R, (11, 11), 0)
            hsv = bgr2hsv(blurred)

            mask = mask_set(hsv, yellow_Lower, yellow_Upper)
            # find contours in the mask and initialize the current
            contours = contours_img(mask)

            center = None
            x = 0
            y = 0
            distance = 0

            if len(contours) > 0:

                c = max(contours, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.putText(frame_R, "x: " + str(x) + " y: " + str(y),
                            (10, 60), font, 1.5, (0, 0, 255), 2)

                if radius > 10:
                    cv2.circle(frame_R, (int(x), int(y)),
                               int(radius), (128, 0, 128), 2)
                    cv2.circle(frame_R, center, 5, (0, 255, 255), -1)

                ##############
                if right_pos.x != 0.0 and right_pos.y != 0.0:
                    distance = math.sqrt(
                        ((right_pos.x-x)**2)+((right_pos.y-y)**2))
                    cv2.putText(frame_R, "distance: " + str(distance),
                                (10, 90), font, 1.5, (0, 0, 255), 2)

                    if distance < 20:
                        cv2.putText(frame, "HIT Right!!",
                                    (screen.halfR, 50), font, 2.5, (0, 0, 255), 3)
                        out_q.put((int(x), int(y), "RIGHT"))

                        # cv2.putText(frame_R, "x: " + str(x) + " y: " + str(y) , (10,60), font, 1.5, (0,0,255), 2)

            right_pos.setX(x)
            right_pos.setY(y)

            ######################################################################
            thickness = 2

            cv2.rectangle(frame, (screen.wr, screen.hr), (screen.halfL,
                                                          screen.h - screen.hr), (0, 0, 255), thickness)

            cv2.rectangle(frame, (screen.halfR, screen.hr), (screen.w -
                                                             screen.wr, screen.h - screen.hr), (0, 255, 255), thickness)

            cv2.imshow('L', frame_L)
            cv2.imshow('R', frame_R)
            cv2.imshow("image", frame)
            # game.start()

        else:
            break


cv2.destroyAllWindows()


if __name__ == '__main__':
    q = Queue()
    Thread(target=game.start).start()
    Thread(target=game.event, args=(q, )).start()
    Thread(target=loop_cv, args=(q, )).start()
