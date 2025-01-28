""" IMPORTS """

import numpy as np
import cv2


""" FUNCTIONS """

#function to draw contours around detected colors as well as print some text
def draw_contours(mask, color):

    # find contours in the masked image.
    cnts, _ = cv2.findContours(mask.copy(),
                                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # look for any contours 
    if len(cnts) > 0:
        # Sort the contours using area and find the largest one
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        color_bgr = color["bgr"]
        cv2.circle(frame, (int(x), int(y)), int(radius), color_bgr, 2)
        # Get the moments to calculate the center of the contour
        M = cv2.moments(cnt)
        center_point = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        center_str = str(center_point)
        cv2.putText(frame, center_str, center_point, cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2, cv2.LINE_AA)

        # write a text to frame
        color_name = str(color["name"])
        cv2.putText(frame, color_name, (int(x+50), int(y+50)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, color_bgr, 2, cv2.LINE_AA)


""" MAIN """

if __name__ == "__main__":
    
    # setup webcam feed 
    cap = cv2.VideoCapture(0)
    
    width  = cap.get(3)   # float `width`
    height = cap.get(4)

    # define a kernel for morphological operations
    kernel = np.ones((5, 5), np.uint8)

    # BGR definitions for some colors
    blue = {"name": 'blue', "bgr": [255, 0, 0]}
    red = {"name": 'red', "bgr": [0, 0, 255]}
    green = {"name": 'green', "bgr": [0, 255, 0]}
    yellow = {"name": 'yellow', "bgr": [0, 255, 255]}
    black = {"name": 'black', "bgr": [0, 0, 0]}
    
    # loop to continuously acquire frames from the webcam
    while True:
        
        # Get frame of camera ([camera resolution] x [Blue-green-red])
        _, frame = cap.read()
        
        # BGR to Hue Saturation Value
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        
        # Blue color
        low_blue = np.array([94, 80, 2])
        high_blue = np.array([126, 255, 255])
        blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
        blue_mask = cv2.erode(blue_mask, kernel, iterations=2)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
        blue_mask = cv2.dilate(blue_mask, kernel, iterations=1)
        draw_contours(blue_mask, blue)
        # blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    
    
        # Green color
        low_green = np.array([40, 52, 72])
        high_green = np.array([102, 255, 255])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        green_mask = cv2.erode(green_mask, kernel, iterations=2)
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
        green_mask = cv2.dilate(green_mask, kernel, iterations=1)
        draw_contours(green_mask, green)
        # green = cv2.bitwise_and(frame, frame, mask=green_mask)
    
    
        # Red color
        # detecting Red color requires a bit of a work around. The red color is represented by 0-30 as well as 150-180 values in openCV.
        # We use the range 0-10 and 170-180 to avoid detection of skin as red. 
        # High range of 120-255 for saturation is used because our cloth should be of highly saturated red color. 
        # The lower range of value is 70 so that we can detect red color in the wrinkles of the cloth as well.
        # combine the two mask to obtaine a final redmask (mask1 = mask1 + mask2)
    
        # low_red = np.array([161, 155, 84])
        # high_red = np.array([179, 255, 255])
        # Range for lower red
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv_frame, lower_red, upper_red)
        # Range for upper range
        lower_red = np.array([170, 120, 70])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv_frame, lower_red, upper_red)
        # Generating the final mask to detect red color
        red_mask = mask1 + mask2
        red_mask = cv2.erode(red_mask, kernel, iterations=2)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        red_mask = cv2.dilate(red_mask, kernel, iterations=1)
        draw_contours(red_mask,red)
        # red = cv2.bitwise_and(frame, frame, mask=red_mask)
        
        
        # Yellow color
        low_yellow = np.array([20, 100, 100])
        high_yellow = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
        yellow_mask = cv2.erode(yellow_mask, kernel, iterations=2)
        yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)
        yellow_mask = cv2.dilate(yellow_mask, kernel, iterations=1)
        draw_contours(yellow_mask, yellow)
        
        
        # Black color
        low_black = np.array([0, 0, 0])
        high_black = np.array([100, 100, 100])
        black_mask = cv2.inRange(hsv_frame, low_black, high_black)
        black_mask = cv2.erode(black_mask, kernel, iterations=2)
        black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, kernel)
        black_mask = cv2.dilate(black_mask, kernel, iterations=1)
        draw_contours(black_mask, black)
        
        
        # Show frame
        cv2.imshow("Frame", frame)
    
        # to quit
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
