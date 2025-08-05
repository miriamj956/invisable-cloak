"""
Algorithm:
1. Capture and store the background frame [ This will be done for some seconds ]
2. Detect the red colored cloth using color detection and segmentation algorithm.
3. Segment out the red colored cloth by generating a mask. [ used in code ]
4. Generate the final augmented output to create a magical effect. [ video.mp4 ]
"""
import cv2
import numpy as np
import time

# 0 if the camera is inbuilt, 1 if its an external camera
raw_video = cv2.VideoCapture(1)

time.sleep(1)
#how many frame is getting captured
count = 0
#capturing background
background = 0 

for i in range(60):
    return_val,background = raw_video.read()
    if return_val == False:
        continue

background = np.flip(background, axis=1)

while(raw_video.isOpened()):
    return_val, img = raw_video.read()
    if not return_val:
        break
    count = count + 1 
    img = np.flip(img, axis = 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #mask1
    lighest_red = np.array([100, 40, 40])
    darkest_red = np.array([100, 255, 255])
    mask1 = cv2.inRange(hsv, lighest_red, darkest_red)

    #mask2
    lighest_red = np.array([155, 40, 40])
    darkest_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lighest_red, darkest_red)

    mask1 = mask1 + mask2 

    #to expand the image and make it not blurry 
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3,3), np.uint8), iterations=1)

    #this basically means that all the red is being saved in the mask 1 variable and so mask 2 will carry all the leftover(everything thats not red)
    mask2 = cv2.bitwise_not(mask1)

    #masking process 
    #bitwise is used to change one value to another(basically if all the values of the computer (binary code) are 0 it will make it into 1 which is the opposite.)
    #it is being used this code to change the value of red(idk what numebr that is)but to change it from red into nothing
    res1 = cv2.bitwise_and(background, background, mask = mask1)
    res2 = cv2.bitwise_and(img, img, mask = mask2)

    #0 - brightness of image
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imshow("Invisable Man", final_output)

    k = cv2.waitKey(10)
    #27 = ESC
    if k == 27:
        break 
    










cv2.destroyAllWindows()
