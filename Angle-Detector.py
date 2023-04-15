"""
program which calculates the angle between 2 pathces of color
inspired from botforge
"""

import cv2
import numpy as np
import math


def distance(x1, y1, x2, y2):
    """
    Calculate distance between two points
    """
    dist = math.sqrt(math.fabs(x2 - x1) ** 2 + math.fabs(y2 - y1) ** 2)
    return dist


def find_color1(frame):
    """
    Filter "frame" for HSV bounds for color1 (inplace, modifies frame) & return coordinates of the object with that color
    """
    """
    red color
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # converts color from RGB to HSV
    hsv_lowerbound = np.array([0, 120, 170])  # replace THIS LINE w/ your hsv lowerb
    hsv_upperbound = np.array([40, 255, 255])  # replace THIS LINE w/ your hsv upperb
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # return approx contours
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)
        # Helps us find center of the contour
        m = cv2.moments(maxcontour)
        if m['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
            center_x = int(m['m10'] / m['m00'])
            center_y = int(m['m01'] / m['m00'])
            return (center_x, center_y), True
        else:
            return (1700, 1700), False  # faraway point
    else:
        # return False
        return (1700, 1700), False  # faraway point


def find_color2(frame):
    """
    Filter "frame" for HSV bounds for color1 (inplace, modifies frame) & return coordinates of the object with that color
    """

    """
    blue color
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([90, 120, 120])  # replace THIS LINE w/ your hsv lowerb
    hsv_upperbound = np.array([125, 255, 255])  # replace THIS LINE w/ your hsv upperb
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)

        # Helps us find center of the contour
        m = cv2.moments(maxcontour)
        if m['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
            center_x = int(m['m10'] / m['m00'])
            center_y = int(m['m01'] / m['m00'])
            return (center_x, center_y), True
        else:
            return (1700, 1700), False  # faraway point
    else:
        # return False
        return (1700, 1700), False  # faraway point


cap = cv2.VideoCapture(0)


def perform():
    _, orig_frame = cap.read()
    # we'll be inplace modifying frames, so save a copy
    copy_frame = orig_frame.copy()
    (color1_x, color1_y), found_color1 = find_color1(copy_frame)
    (color2_x, color2_y), found_color2 = find_color2(copy_frame)
    #
    # draw circles in the place of the objects
    
    cv2.circle(copy_frame, (color1_x, color1_y), 20, (255, 0, 0), -1)
    cv2.circle(copy_frame, (color2_x, color2_y), 20, (0, 128, 255), -1)

    if found_color2 and found_color1:
        # trig stuff to get the line
        hypotenuse = distance(color1_x, color1_x, color2_x, color2_y)
        horizontal = distance(color1_x, color1_y, color2_x, color1_y)
        vertical = distance(color2_x, color2_y, color2_x, color1_y)
        if hypotenuse != 0:
            if -1 < vertical/hypotenuse < 1:
                angle = np.arcsin(vertical / hypotenuse) * 180.0 / math.pi

                # draw all 3 lines
                cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color2_y), (0, 0, 255), 2)
                cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color1_y), (0, 0, 255), 2)
                cv2.line(copy_frame, (color2_x, color2_y), (color2_x, color1_y), (0, 0, 255), 2)

                # put angle text (allow for calculations up to 180 degrees)
                angle_text = ""
                angle_final = 0

                if isinstance(angle, float) and angle < 360:
                    if color2_y < color1_y and color2_x > color1_x:
                        angle_final = int(angle)
                        angle_text = str(int(angle))
                    elif color2_y < color1_y and color2_x < color1_x:
                        angle_final = int(180 - angle)
                        angle_text = str(int(180 - angle))
                    elif color2_y > color1_y and color2_x < color1_x:
                        angle_final = int(180 + angle)
                        angle_text = str(int(180 + angle))
                    elif color2_y > color1_y and color2_x > color1_x:
                        angle_final = int(360 - angle)
                        angle_text = str(int(360 - angle))

                if 45 < angle_final < 135:
                    print("up")
                elif 135 < angle_final < 225:
                    print("right")
                elif 225 < angle_final < 315:
                    print("down")
                else:
                    print("left")

                # CHANGE FONT HERE
                cv2.putText(copy_frame, angle_text, (color1_x - 30, color1_y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 128, 229), 2)

    cv2.imshow('mat', copy_frame)
    cv2.waitKey(1)

while (1):
    perform()

